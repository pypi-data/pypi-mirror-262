use pyo3::prelude::*;

use crate::dataclass::Dataclass;

pub fn create_module(py: Python) -> Result<&PyModule, PyErr> {
    let module = PyModule::new(py, "model")?;

    module.add_class::<Model>()?;
    module.add_class::<TimeStep>()?;
    module.add_class::<Boundary>()?;

    Ok(module)
}

type DynModel = dyn Send
    + core_model::model::Model<
        Dtype = f64,
        Dimension = ndarray::Ix1,
        State = ndarray::Array1<f64>,
        Ext = (),
    >;
type DynTimeStep = dyn Send + core_model::timestep::TimeStep<DynModel>;
type DynBoundaryCondition = dyn Send + core_model::boundary::BoundaryCondition<DynModel>;

#[pyclass(module = "fcbench.model")]
pub struct Model {
    #[allow(clippy::struct_field_names)]
    model: Box<DynModel>,
    timestep: Box<DynTimeStep>,
    boundary: Box<DynBoundaryCondition>,
    dt: f64,
}

#[pymethods]
impl Model {
    #[getter]
    pub fn state(this: &PyCell<Self>) -> Result<&numpy::PyArray1<f64>, PyErr> {
        let mut slf: PyRefMut<Self> = this.try_borrow_mut()?;
        let slf: &mut Self = &mut slf;

        let state = slf.model.state_mut();

        // SAFETY: The memory backing `state` will stay valid as long as this
        //         object is alive, as we do not modify `state` in any way
        //         which would cause it to be reallocated.
        #[allow(unsafe_code)]
        Ok(unsafe { numpy::PyArray1::borrow_from_array(&state, this) })
    }

    pub fn step(&mut self, dt: Option<f64>) {
        self.timestep
            .step(&mut *self.model, &mut (), dt.unwrap_or(self.dt));
        self.boundary.apply(&mut *self.model);
    }

    pub fn __iter__(this: PyRef<Self>) -> PyRef<Self> {
        this
    }

    #[allow(clippy::unnecessary_wraps)]
    pub fn __next__(this: &PyCell<Self>) -> Result<Option<&numpy::PyArray1<f64>>, PyErr> {
        {
            let mut slf: PyRefMut<Self> = this.try_borrow_mut()?;
            let slf: &mut Self = &mut slf;

            slf.step(None);
        }

        Self::state(this).map(Some)
    }

    #[staticmethod]
    #[allow(clippy::needless_pass_by_value)]
    pub fn lorenz_63(
        params: Dataclass<core_model::model::lorenz_63::Lorenz63Parameters<f64>>,
        initial: [f64; 3],
        timestep: &TimeStep,
        dt: f64,
    ) -> Self {
        let model: Box<DynModel> = Box::new(core_model::model::lorenz_63::Lorenz63::new(
            *params, initial,
        ));
        let timestep = timestep.as_boxed(&*model);

        Self {
            model,
            timestep,
            boundary: Box::new(core_model::boundary::NoopBoundary),
            dt,
        }
    }

    #[staticmethod]
    #[allow(clippy::needless_pass_by_value)]
    pub fn lorenz_96(
        params: Dataclass<
            core_model::model::lorenz_96::Lorenz96Parameters<
                f64,
                core_model::model::lorenz_96::Const<f64>,
            >,
        >,
        initial: numpy::PyReadonlyArray1<f64>,
        timestep: &TimeStep,
        dt: f64,
    ) -> Self {
        let model: Box<
            dyn Send
                + core_model::model::Model<
                    Dtype = f64,
                    Dimension = ndarray::Ix1,
                    State = ndarray::Array1<f64>,
                    Ext = (),
                >,
        > = Box::new(core_model::model::lorenz_96::Lorenz96::new(
            *params,
            initial.as_array().into_owned(),
        ));
        let timestep = timestep.as_boxed(&*model);

        Self {
            model,
            timestep,
            boundary: Box::new(core_model::boundary::NoopBoundary),
            dt,
        }
    }

    #[staticmethod]
    #[allow(clippy::needless_pass_by_value)]
    pub fn linadv(
        params: Dataclass<core_model::model::linadv::LinadvParameters<f64>>,
        initial: numpy::PyReadonlyArray1<f64>,
        timestep: &TimeStep,
        boundary: &Boundary,
        dt: f64,
    ) -> Self {
        let model: Box<
            dyn Send
                + core_model::model::Model<
                    Dtype = f64,
                    Dimension = ndarray::Ix1,
                    State = ndarray::Array1<f64>,
                    Ext = (),
                >,
        > = Box::new(core_model::model::linadv::Linadv::new(
            *params,
            initial.as_array().into_owned(),
        ));
        let timestep = timestep.as_boxed(&*model);
        let boundary = boundary.as_boxed();

        Self {
            model,
            timestep,
            boundary,
            dt,
        }
    }
}

#[pyclass(module = "fcbench.model")]
pub enum TimeStep {
    Direct,
    EulerSmoothing,
    LeapFrog,
    RangeKutta,
}

impl TimeStep {
    fn as_boxed(
        &self,
        model: &dyn core_model::model::Model<
            Dtype = f64,
            Dimension = ndarray::Ix1,
            State = ndarray::Array1<f64>,
            Ext = (),
        >,
    ) -> Box<DynTimeStep> {
        match self {
            Self::Direct => Box::new(core_model::timestep::Direct),
            Self::EulerSmoothing => Box::new(core_model::timestep::EulerSmoothing),
            Self::LeapFrog => Box::new(core_model::timestep::LeapFrog::new(
                model.state().into_owned(),
            )),
            Self::RangeKutta => Box::new(core_model::timestep::RungeKutta),
        }
    }
}

#[pyclass(module = "fcbench.model")]
pub enum Boundary {
    Zero,
    Periodic,
}

impl Boundary {
    fn as_boxed(&self) -> Box<DynBoundaryCondition> {
        match self {
            Self::Zero => Box::new(core_model::boundary::ZeroBoundary::<1>),
            Self::Periodic => Box::new(core_model::boundary::PeriodicBoundary::<1>),
        }
    }
}
