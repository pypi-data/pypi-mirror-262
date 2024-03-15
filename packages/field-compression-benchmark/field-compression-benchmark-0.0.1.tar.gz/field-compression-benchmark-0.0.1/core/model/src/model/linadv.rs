use ndarray::{Array, Array1, ArrayView, ArrayViewMut, Ix1, NdFloat};

use crate::{model::Model, num::two};

pub struct Linadv<F: NdFloat> {
    parameters: LinadvParameters<F>,
    h_m: Array1<F>,
}

impl<F: NdFloat> Linadv<F> {
    #[must_use]
    pub const fn new(parameters: LinadvParameters<F>, h_m: Array1<F>) -> Self {
        Self { parameters, h_m }
    }

    #[must_use]
    pub const fn parameters(&self) -> &LinadvParameters<F> {
        &self.parameters
    }
}

impl<F: NdFloat> Model for Linadv<F> {
    type Dimension = Ix1;
    type Dtype = F;
    type Ext = ();
    type State = Array<F, Ix1>;

    fn state(&self) -> ArrayView<Self::Dtype, Self::Dimension> {
        self.h_m.view()
    }

    fn state_mut(&mut self) -> ArrayViewMut<Self::Dtype, Self::Dimension> {
        self.h_m.view_mut()
    }

    fn tendencies_for_state(
        &self,
        state: ArrayView<Self::Dtype, Self::Dimension>,
        _ext: &mut Self::Ext,
    ) -> Array<Self::Dtype, Self::Dimension> {
        let h_m = state;

        let LinadvParameters { dx_m, U_const_m_s } = self.parameters;

        let mut h_tend_m_s = Array1::<F>::zeros([h_m.len()]);

        for ((h_tend_m_s_i, h_m_ip1), h_m_im1) in h_tend_m_s
            .iter_mut()
            .skip(1)
            .zip(h_m.iter().skip(2).copied())
            .zip(h_m.iter().copied())
        {
            *h_tend_m_s_i = -U_const_m_s * (h_m_ip1 - h_m_im1) / (dx_m * two());
        }

        h_tend_m_s
    }

    fn with_state(&self, h_m: Array<Self::Dtype, Self::Dimension>) -> Self {
        Self::new(self.parameters, h_m)
    }
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
#[allow(non_snake_case)]
pub struct LinadvParameters<F: NdFloat> {
    pub dx_m: F,
    pub U_const_m_s: F,
}
