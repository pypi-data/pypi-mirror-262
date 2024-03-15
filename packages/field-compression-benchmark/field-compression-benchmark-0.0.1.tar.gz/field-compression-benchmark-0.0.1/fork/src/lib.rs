#![deny(clippy::pedantic)]
#![deny(clippy::unwrap_used)]
#![deny(clippy::expect_used)]
#![deny(clippy::indexing_slicing)]
#![deny(clippy::panic)]
#![deny(clippy::todo)]
#![deny(clippy::unimplemented)]
#![deny(clippy::unreachable)]
#![allow(clippy::module_name_repetitions)]

mod fork;
mod reaper;
mod work;

pub use self::{
    fork::{ChildWaitError, Fork, ForkChild, ForkParent},
    reaper::{Reaper, REAPER_TOKEN},
    work::{distribute_work, DistributedWorkError},
};
