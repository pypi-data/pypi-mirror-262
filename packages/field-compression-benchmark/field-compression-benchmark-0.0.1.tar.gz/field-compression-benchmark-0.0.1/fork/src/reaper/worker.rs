use thiserror::Error;

use core_error::LocationError;

use crate::Reaper;

pub fn reaper_worker<F: FnOnce(&Reaper) -> Q, Q>(
    inner: F,
) -> Result<Q, LocationError<WorkerSetupError>> {
    let worker_pid = unsafe { libc::getpid() };

    if unsafe { libc::setsid() } == -1 {
        return Err(WorkerSetupError::ProcessGroupSetup(std::io::Error::last_os_error()).into());
    }

    log::debug!("The WORKER {} will now start to execute.", worker_pid,);

    let result = inner(&Reaper::new());

    log::debug!("The WORKER {} has finished executing.", worker_pid,);

    Ok(result)
}

#[derive(Debug, Error)]
pub enum WorkerSetupError {
    #[error("failed to create a new process group for the worker")]
    ProcessGroupSetup(#[source] std::io::Error),
}
