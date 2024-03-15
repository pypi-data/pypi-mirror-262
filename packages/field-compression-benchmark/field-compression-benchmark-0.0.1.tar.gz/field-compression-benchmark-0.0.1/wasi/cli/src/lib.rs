#![cfg_attr(not(test), no_main)]

mod environment;
mod exit;
mod stdio;
mod terminal;

#[allow(clippy::missing_safety_doc, clippy::transmute_int_to_bool)]
mod bindings {
    wit_bindgen::generate!({
        path: "../wit",
        world: "virtual-wasi-cli",
    });
}

pub enum VirtCli {}
crate::bindings::export!(VirtCli with_types_in bindings);
