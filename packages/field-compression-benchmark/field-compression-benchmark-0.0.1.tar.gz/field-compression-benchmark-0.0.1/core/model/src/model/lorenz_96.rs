use std::marker::PhantomData;

use ndarray::{Array, Array1, ArrayView, ArrayViewMut, Ix1, NdFloat};
use rand::RngCore;
use rand_distr::Distribution;

use crate::model::Model;

pub struct Lorenz96<F: NdFloat, S: ForcingSampler<Dtype = F>> {
    parameters: Lorenz96Parameters<F, S>,
    state: Array1<F>,
}

impl<F: NdFloat, S: ForcingSampler<Dtype = F>> Lorenz96<F, S> {
    #[must_use]
    pub const fn new(parameters: Lorenz96Parameters<F, S>, state: Array1<F>) -> Self {
        // TODO: validate shape >= 4
        Self { parameters, state }
    }

    #[must_use]
    pub const fn parameters(&self) -> &Lorenz96Parameters<F, S> {
        &self.parameters
    }
}

impl<F: NdFloat, S: ForcingSampler<Dtype = F>> Model for Lorenz96<F, S> {
    type Dimension = Ix1;
    type Dtype = F;
    type Ext = S::Ext;
    type State = Array<F, Ix1>;

    fn state(&self) -> ArrayView<Self::Dtype, Self::Dimension> {
        self.state.view()
    }

    fn state_mut(&mut self) -> ArrayViewMut<Self::Dtype, Self::Dimension> {
        self.state.view_mut()
    }

    fn tendencies_for_state(
        &self,
        state: ArrayView<Self::Dtype, Self::Dimension>,
        ext: &mut Self::Ext,
    ) -> Array<Self::Dtype, Self::Dimension> {
        let Lorenz96Parameters { forcing } = &self.parameters;

        let mut tendencies = state.to_owned();

        for (((x_k, &x_kp1), &x_km1), &x_km2) in tendencies
            .iter_mut()
            .zip(state.iter().cycle().skip(1))
            .zip(
                state.iter().cycle().skip(state.len() - 1), // FIXME
            )
            .zip(
                state.iter().cycle().skip(state.len() - 2), // FIXME
            )
        {
            *x_k = -x_km2 * x_km1 + x_km1 * x_kp1 - (*x_k) + forcing.sample(ext);
        }

        tendencies
    }

    fn with_state(&self, state: Array<Self::Dtype, Self::Dimension>) -> Self {
        Self::new(self.parameters.clone(), state)
    }
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct Lorenz96Parameters<F: NdFloat, S: ForcingSampler<Dtype = F>> {
    pub forcing: S,
}

pub trait ForcingSampler: Clone {
    type Dtype: NdFloat;
    type Ext: ?Sized;

    fn sample(&self, ext: &mut Self::Ext) -> Self::Dtype;
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct Const<F: NdFloat> {
    r#const: F,
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct Distr<F: NdFloat, D: Distribution<F> + Clone> {
    distr: D,
    _marker: PhantomData<F>,
}

impl<F: NdFloat> ForcingSampler for Const<F> {
    type Dtype = F;
    type Ext = ();

    fn sample(&self, _ext: &mut Self::Ext) -> Self::Dtype {
        self.r#const
    }
}

impl<F: NdFloat, D: Distribution<F> + Clone> ForcingSampler for Distr<F, D> {
    type Dtype = F;
    type Ext = dyn RngCore;

    fn sample(&self, ext: &mut Self::Ext) -> Self::Dtype {
        self.distr.sample(ext)
    }
}
