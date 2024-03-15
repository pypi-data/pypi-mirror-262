use std::cmp::Ordering;

use thiserror::Error;

use core_error::LocationError;

use crate::Reaper;

#[derive(Debug, Error)]
#[error("failed to wait for the forked child process")]
pub struct ChildWaitError;

pub enum Fork {
    Child(ForkChild),
    Parent(ForkParent),
}

pub struct ForkChild {
    _private: (),
}

pub struct ForkParent {
    child_pid: i32,
    _private: (),
}

impl ForkParent {
    /// Wait for the forked child process to terminate and return its exit code
    /// on success.
    ///
    /// # Errors
    /// Returns the [`std::io::Error`] if waiting on the child process failed.
    pub fn wait_for_child(self) -> Result<i32, LocationError<std::io::Error>> {
        loop {
            let mut status = 0;

            match unsafe { libc::waitpid(self.child_pid, &mut status, libc::WNOHANG) }.cmp(&0) {
                Ordering::Less => return Err(std::io::Error::last_os_error().into()),
                Ordering::Equal => continue,
                Ordering::Greater => return Ok(libc::WEXITSTATUS(status)),
            };
        }
    }

    /// Try to wait for the forked child process to terminate and return its
    /// exit code on success. If the child has not yet terminated, [`Self`]
    /// is returned to try again.
    ///
    /// # Errors
    /// Returns the [`std::io::Error`] if waiting on the child process failed.
    pub fn try_wait_for_child(self) -> Result<Result<i32, Self>, LocationError<std::io::Error>> {
        let mut status = 0;

        match unsafe { libc::waitpid(self.child_pid, &mut status, libc::WNOHANG) }.cmp(&0) {
            Ordering::Less => Err(std::io::Error::last_os_error().into()),
            Ordering::Equal => Ok(Err(self)),
            Ordering::Greater => Ok(Ok(libc::WEXITSTATUS(status))),
        }
    }

    pub(crate) fn child_pid(&self) -> i32 {
        self.child_pid
    }
}

impl Reaper {
    /// Forks the current process and returns on the child and the parent
    /// process. [`Fork`] indicates if the process is the child or parent
    /// on success.
    ///
    /// # Errors
    /// Returns the [`std::io::Error`] if forking child process failed.
    pub fn fork(&self) -> Result<Fork, LocationError<std::io::Error>> {
        match unsafe { libc::fork() } {
            -1 => Err(std::io::Error::last_os_error().into()),
            0 => Ok(Fork::Child(ForkChild { _private: () })),
            child_pid => Ok(Fork::Parent(ForkParent {
                child_pid,
                _private: (),
            })),
        }
    }
}
