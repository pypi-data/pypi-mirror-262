use std::cmp::Ordering;

use signal_hook::iterator::Signals;
use thiserror::Error;

use core_error::LocationError;

use super::{exit_with_report, worker::reaper_worker};
use crate::{Fork, Reaper};

pub fn reaper_handler_setup<F: FnOnce(&Reaper) -> Q, Q>(
    canary_pid: i32,
    inner: F,
) -> Result<Q, LocationError<HandlerSetupError>> {
    let handler_pid = unsafe { libc::getpid() };

    if unsafe { libc::prctl(libc::PR_SET_PDEATHSIG, libc::SIGCHLD) } == -1 {
        return Err(HandlerSetupError::DeathSignalSetup(std::io::Error::last_os_error()).into());
    }
    if unsafe { libc::setsid() } == -1 {
        return Err(HandlerSetupError::ProcessGroupSetup(std::io::Error::last_os_error()).into());
    }
    if unsafe { libc::prctl(libc::PR_SET_CHILD_SUBREAPER, 1) } == -1 {
        return Err(HandlerSetupError::SubReaperSetup(std::io::Error::last_os_error()).into());
    }

    // Check if the canary quit before the handler, if so abort
    if unsafe { libc::getppid() } != canary_pid {
        log::warn!(
            "The CANARY {} has been terminated before the HANDLER {} could start.",
            canary_pid,
            handler_pid
        );

        std::process::abort();
    }

    match Reaper::new().fork() {
        Err(err) => Err(HandlerSetupError::HandlerForkError(err).into()),
        Ok(Fork::Child(_)) => match reaper_worker(inner) {
            Ok(result) => Ok(result),
            Err(err) => exit_with_report(err),
        },
        Ok(Fork::Parent(parent)) => {
            match reaper_handler(canary_pid, handler_pid, parent.child_pid()) {
                Ok(status) => std::process::exit(status),
                Err(err) => exit_with_report(err),
            }
        },
    }
}

fn reaper_handler(
    canary_pid: i32,
    handler_pid: i32,
    worker_pid: i32,
) -> Result<i32, LocationError<HandlerError>> {
    let mut signals =
        Signals::new((1..32).filter(|signal| !signal_hook::consts::FORBIDDEN.contains(signal)))
            .map_err(HandlerError::SignalInstallation)?;

    let status = 'outer: loop {
        let mut status = 0;

        match unsafe { libc::waitpid(worker_pid, &mut status, libc::WNOHANG) }.cmp(&0) {
            Ordering::Less => {
                return Err(HandlerError::WorkerWait(std::io::Error::last_os_error()).into());
            },
            Ordering::Equal => (),
            Ordering::Greater => break status,
        };

        for signal in signals.wait() {
            log::debug!(
                "The HANDLER {} has received the signal {}.",
                handler_pid,
                signal
            );

            if signal != libc::SIGCHLD {
                log::debug!(
                    "The HANDLER {} will send the signal {} to the WORKER group {}.",
                    handler_pid,
                    signal,
                    worker_pid
                );

                unsafe {
                    // Error is ignored as the worker may have already terminated
                    libc::kill(-worker_pid, signal);
                }
            } else if unsafe { libc::getppid() } != canary_pid {
                log::debug!(
                    "The HANDLER {} has been informed that the CANARY {} has died.",
                    handler_pid,
                    canary_pid
                );
                log::debug!(
                    "The HANDLER {} will terminate the WORKER group {}.",
                    handler_pid,
                    worker_pid
                );

                // Error is ignored as the worker may have already terminated
                unsafe {
                    libc::kill(-worker_pid, libc::SIGKILL);
                }

                log::debug!(
                    "The HANDLER {} will wait for the WORKER leader {}.",
                    handler_pid,
                    worker_pid
                );

                let mut status = 0;
                if unsafe { libc::waitpid(worker_pid, &mut status, 0) } > 0 {
                    break 'outer status;
                }

                return Err(HandlerError::WorkerWait(std::io::Error::last_os_error()).into());
            }
        }
    };

    log::debug!(
        "The HANDLER {} will wait for the WORKER group {}.",
        handler_pid,
        worker_pid
    );

    // Error means that we haved waited for all children
    while unsafe { libc::waitpid(-1, std::ptr::null_mut(), libc::WNOHANG) } >= 0 {}

    log::debug!(
        "The HANDLER {} will exit with status {}.",
        handler_pid,
        status
    );

    Ok(status)
}

#[derive(Debug, Error)]
pub enum HandlerSetupError {
    #[error("failed to setup the death signal in the handler")]
    DeathSignalSetup(#[source] std::io::Error),
    #[error("failed to create a new process group for the handler")]
    ProcessGroupSetup(#[source] std::io::Error),
    #[error("failed to make the handler a sub-reaper for its descendants")]
    SubReaperSetup(#[source] std::io::Error),
    #[error("failed to fork the handler process into a handler and a worker")]
    HandlerForkError(#[source] LocationError<std::io::Error>),
}

#[derive(Debug, Error)]
enum HandlerError {
    #[error("failed to install the signal handler in the handler")]
    SignalInstallation(#[source] std::io::Error),
    #[error("failed to wait for the worker to terminate")]
    WorkerWait(#[source] std::io::Error),
}
