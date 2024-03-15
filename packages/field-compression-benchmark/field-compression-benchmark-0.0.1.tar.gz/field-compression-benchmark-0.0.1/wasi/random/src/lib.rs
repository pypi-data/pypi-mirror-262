#![cfg_attr(not(test), no_main)]

use std::sync::{Mutex, MutexGuard, OnceLock};

use rand_core::RngCore;
use rand_pcg::Pcg64;

use crate::bindings::{
    exports::wasi::random::{
        insecure::Guest as WasiRandomInsecure, insecure_seed::Guest as WasiRandomInsecureSeed,
    },
    // wasi::random::insecure_seed::insecure_seed as insecure_seed_host,
};

mod bindings {
    wit_bindgen::generate!({
        path: "../wit",
        world: "virtual-wasi-random",
    });
}

pub enum VirtRandom {}
crate::bindings::export!(VirtRandom with_types_in bindings);

fn rng() -> MutexGuard<'static, Pcg64> {
    static RNG: OnceLock<Mutex<Pcg64>> = OnceLock::new();

    #[cold]
    #[inline(never)]
    fn init_rng() -> &'static Mutex<Pcg64> {
        RNG.get_or_init(|| {
            const PCG64_DEFAULT_STREAM: u128 = 0xa02bdbf7bb3c0a7ac28fa16a64abf96;

            // let (state_lo, state_hi) = insecure_seed_host();
            // let state = u128::from(state_lo) | (u128::from(state_hi) << 64);
            let state = 0xcafef00dd15ea5e5;

            Mutex::new(Pcg64::new(state, PCG64_DEFAULT_STREAM))
        })
    }

    RNG.get().unwrap_or_else(|| init_rng()).lock().unwrap()
}

impl WasiRandomInsecureSeed for VirtRandom {
    fn insecure_seed() -> (u64, u64) {
        let mut rng = rng();
        (rng.next_u64(), rng.next_u64())
    }
}

impl WasiRandomInsecure for VirtRandom {
    fn get_insecure_random_bytes(len: u64) -> Vec<u8> {
        let mut buffer = vec![0; usize::try_from(len).unwrap()];
        rng().fill_bytes(&mut buffer);
        buffer
    }

    fn get_insecure_random_u64() -> u64 {
        rng().next_u64()
    }
}
