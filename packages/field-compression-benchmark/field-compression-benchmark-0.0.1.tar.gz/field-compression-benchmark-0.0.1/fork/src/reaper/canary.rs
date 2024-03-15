use std::cmp::Ordering;

use signal_hook::iterator::Signals;
use thiserror::Error;

use core_error::LocationError;

use super::{exit_with_report, handler::reaper_handler_setup};
use crate::{Fork, Reaper};

pub fn reaper_canary_setup<F: FnOnce(&Reaper) -> Q, Q>(
    inner: F,
) -> Result<Q, LocationError<CanarySetupError>> {
    let canary_pid = unsafe { libc::getpid() };

    match Reaper::new().fork() {
        Err(err) => Err(CanarySetupError::CanaryForkError(err).into()),
        Ok(Fork::Child(_)) => match reaper_handler_setup(canary_pid, inner) {
            Ok(result) => Ok(result),
            Err(err) => exit_with_report(err),
        },
        Ok(Fork::Parent(parent)) => match reaper_canary(canary_pid, parent.child_pid()) {
            Ok(status) => std::process::exit(status),
            Err(err) => exit_with_report(err),
        },
    }
}

fn reaper_canary(canary_pid: i32, handler_pid: i32) -> Result<i32, LocationError<CanaryError>> {
    let mut signals =
        Signals::new((1..32).filter(|signal| !signal_hook::consts::FORBIDDEN.contains(signal)))
            .map_err(CanaryError::SignalInstallation)?;

    let status = loop {
        let mut status = 0;

        match unsafe { libc::waitpid(handler_pid, &mut status, libc::WNOHANG) }.cmp(&0) {
            Ordering::Less => {
                return Err(CanaryError::HandlerWait(std::io::Error::last_os_error()).into());
            },
            Ordering::Equal => (),
            Ordering::Greater => break libc::WEXITSTATUS(status),
        };

        for signal in signals.wait() {
            log::debug!(
                "The CANARY {} has received the signal {}.",
                canary_pid,
                signal
            );

            if signal != libc::SIGCHLD {
                log::debug!(
                    "The CANARY {} will send the signal {} to the HANDLER {}.",
                    handler_pid,
                    signal,
                    handler_pid
                );

                // Error is ignored as the handler may have already terminated
                unsafe { libc::kill(handler_pid, signal) };
            }
        }
    };

    log::debug!(
        "The CANARY {} will exit with status {}.",
        canary_pid,
        status
    );

    Ok(status)
}

#[derive(Debug, Error)]
pub enum CanarySetupError {
    #[error("failed to fork the main process into a canary and a handler")]
    CanaryForkError(#[source] LocationError<std::io::Error>),
}

#[derive(Debug, Error)]
enum CanaryError {
    #[error("failed to install the signal handler in the canary")]
    SignalInstallation(#[source] std::io::Error),
    #[error("failed to wait for the handler to terminate")]
    HandlerWait(#[source] std::io::Error),
}
