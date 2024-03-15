use ndarray::{array, Array, ArrayView, ArrayViewMut, Ix1, NdFloat};

use crate::model::Model;

pub struct Lorenz63<F: NdFloat> {
    parameters: Lorenz63Parameters<F>,
    state: [F; 3],
}

impl<F: NdFloat> Lorenz63<F> {
    #[must_use]
    pub const fn new(parameters: Lorenz63Parameters<F>, state: [F; 3]) -> Self {
        Self { parameters, state }
    }

    #[must_use]
    pub const fn parameters(&self) -> &Lorenz63Parameters<F> {
        &self.parameters
    }
}

impl<F: NdFloat> Model for Lorenz63<F> {
    type Dimension = Ix1;
    type Dtype = F;
    type Ext = ();
    type State = Array<F, Ix1>;

    fn state(&self) -> ArrayView<Self::Dtype, Self::Dimension> {
        ArrayView::from(&self.state)
    }

    fn state_mut(&mut self) -> ArrayViewMut<Self::Dtype, Self::Dimension> {
        ArrayViewMut::from(&mut self.state)
    }

    fn tendencies_for_state(
        &self,
        state: ArrayView<Self::Dtype, Self::Dimension>,
        _ext: &mut Self::Ext,
    ) -> Array<Self::Dtype, Self::Dimension> {
        let mut new_state @ [x1, x2, x3] = [F::zero(); 3];
        ArrayViewMut::from(&mut new_state).assign(&state);

        let Lorenz63Parameters { sigma, rho, beta } = self.parameters;

        array![
            sigma * (x2 - x1),
            x1 * (rho - x3) - x2,
            (x1 * x2) - (beta * x3),
        ]
    }

    fn with_state(&self, state: Array<Self::Dtype, Self::Dimension>) -> Self {
        let mut new_state = [F::zero(); 3];
        ArrayViewMut::from(&mut new_state).assign(&state);
        Self::new(self.parameters, new_state)
    }
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct Lorenz63Parameters<F: NdFloat> {
    pub sigma: F,
    pub rho: F,
    pub beta: F,
}
