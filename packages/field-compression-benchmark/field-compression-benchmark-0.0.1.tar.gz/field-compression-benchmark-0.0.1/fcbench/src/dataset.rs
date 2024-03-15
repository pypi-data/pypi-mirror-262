use std::{
    collections::{HashMap, HashSet},
    path::{Path, PathBuf},
};

use pyo3::{
    exceptions::{PyKeyError, PyRuntimeError},
    prelude::*,
    types::{PyDict, PyList},
};
use vecmap::VecSet;

use crate::dataclass::{Dataclass, DataclassOut, DataclassOutFrozen};

pub fn create_module(py: Python) -> Result<&PyModule, PyErr> {
    let module = PyModule::new(py, "dataset")?;

    module.add_class::<Dataset>()?;
    module.add_function(wrap_pyfunction!(settings, module)?)?;

    Ok(module)
}

#[pyclass(module = "fcbench.dataset", frozen)]
pub struct Dataset {
    pub(crate) dataset: core_dataset::dataset::Dataset,
}

#[pymethods]
impl Dataset {
    #[allow(clippy::needless_pass_by_value)]
    #[staticmethod]
    #[pyo3(signature = (unit_registry, settings, **kwargs))]
    pub fn from_config_kwargs(
        py: Python,
        unit_registry: &core_dataset::units::UnitRegistry,
        settings: Dataclass<core_dataset::dataset::DatasetSettings>,
        kwargs: Option<&PyDict>,
    ) -> Result<Self, PyErr> {
        let mut depythonizer =
            pythonize::Depythonizer::from_object(kwargs.unwrap_or(PyDict::new(py)));

        match core_dataset::dataset::Dataset::from_deserialised_config(
            py,
            &mut depythonizer,
            unit_registry,
            &settings,
        ) {
            Ok(dataset) => Ok(Self { dataset }),
            Err(err) => Err(PyErr::from(err)),
        }
    }

    #[allow(clippy::needless_pass_by_value)]
    #[staticmethod]
    pub fn from_config_str(
        py: Python,
        config: &str,
        unit_registry: &core_dataset::units::UnitRegistry,
        settings: Dataclass<core_dataset::dataset::DatasetSettings>,
    ) -> Result<Self, PyErr> {
        match core_dataset::dataset::Dataset::from_config_str(py, config, unit_registry, &settings)
        {
            Ok(dataset) => Ok(Self { dataset }),
            Err(err) => Err(PyRuntimeError::new_err(format!("{err:#}"))),
        }
    }

    #[allow(clippy::needless_pass_by_value)]
    #[staticmethod]
    pub fn from_config_file(
        py: Python,
        config_file: PathBuf,
        unit_registry: &core_dataset::units::UnitRegistry,
        settings: Dataclass<core_dataset::dataset::DatasetSettings>,
    ) -> Result<Self, PyErr> {
        match core_dataset::dataset::Dataset::from_config_file(
            py,
            &config_file,
            unit_registry,
            &settings,
        ) {
            Ok(dataset) => Ok(Self { dataset }),
            Err(err) => Err(PyRuntimeError::new_err(format!("{err:#}"))),
        }
    }

    #[allow(clippy::needless_pass_by_value)]
    #[staticmethod]
    pub fn from_config_files(
        py: Python,
        config_files: HashSet<PathBuf>,
        unit_registry: &core_dataset::units::UnitRegistry,
        settings: Dataclass<core_dataset::dataset::DatasetSettings>,
    ) -> Result<HashMap<PathBuf, Self>, PyErr> {
        match core_dataset::dataset::Dataset::from_config_files(
            py,
            &VecSet::from_iter(config_files),
            unit_registry,
            &settings,
        ) {
            Ok(datasets) => Ok(datasets
                .into_iter()
                .map(|(path, dataset)| (path, Self { dataset }))
                .collect()),
            Err(err) => Err(PyRuntimeError::new_err(format!("{err:#}"))),
        }
    }

    #[allow(clippy::needless_pass_by_value)]
    #[staticmethod]
    pub fn from_config_directory(
        py: Python,
        config_directory: PathBuf,
        unit_registry: &core_dataset::units::UnitRegistry,
        settings: Dataclass<core_dataset::dataset::DatasetSettings>,
    ) -> Result<HashMap<PathBuf, Self>, PyErr> {
        match core_dataset::dataset::Dataset::from_config_directory(
            py,
            &config_directory,
            unit_registry,
            &settings,
        ) {
            Ok(datasets) => Ok(datasets
                .into_iter()
                .map(|(path, dataset)| (path, Self { dataset }))
                .collect()),
            Err(err) => Err(PyRuntimeError::new_err(format!("{err:#}"))),
        }
    }

    #[must_use]
    #[getter]
    pub fn config_path(&self) -> Option<&Path> {
        self.dataset.config_path()
    }

    #[must_use]
    #[getter]
    pub fn path(&self) -> &Path {
        self.dataset.path()
    }

    #[must_use]
    #[getter]
    pub fn format(&self) -> String {
        format!("{}", self.dataset.format())
    }

    pub fn minimise(&self, variables: bool, dimensions: bool, derivatives: bool) -> Self {
        // copy on write since Self is a frozen PyO3 class
        let mut this = Self {
            dataset: self.dataset.clone(),
        };
        this.dataset.minimise(variables, dimensions, derivatives);
        this
    }

    pub fn filter(&self, keep_variable: &PyAny) -> Result<Self, PyErr> {
        // copy on write since Self is a frozen PyO3 class
        let mut this = Self {
            dataset: self.dataset.clone(),
        };

        let mut result = Ok(());

        let keep_variable = |variable: &str| {
            // if an error occurs, we don't filter out any more items to
            //  keep the dataset the same, as if we had returned early
            if result.is_err() {
                return true;
            }

            match keep_variable.call1((variable,)).and_then(PyAny::extract) {
                Ok(keep) => keep,
                Err(err) => {
                    result = Err(err);
                    true
                },
            }
        };

        this.dataset.filter(keep_variable);

        result.map(|()| this)
    }

    pub fn open_xarray<'py>(&self, py: Python<'py>) -> Result<&'py PyAny, PyErr> {
        self.dataset
            .open_xarray(py)
            .map_err(core_error::LocationError::into_error)
    }

    pub fn open_xarray_sliced_variable<'py>(
        &self,
        py: Python<'py>,
        variable: &DataVariable,
    ) -> Result<&'py PyAny, PyErr> {
        self.dataset
            .open_xarray_sliced_variable(py, &variable.variable)
            .map_err(core_error::LocationError::into_error)
    }

    #[must_use]
    #[getter]
    pub fn variables(this: PyRef<Self>) -> DataVariableIterator {
        let iter = this.dataset.variables();
        let iter: Box<dyn ExactSizeIterator<Item = &core_dataset::variable::DataVariable> + Send> =
            Box::new(iter);
        // Safety:
        // - we borrow the dataset that's inside PyRef<Self> and Py<Self>
        // - the iterator and its items all carry around clones of Py<Self>
        // - so the dataset lives long enough
        // - Self is a frozen class, so no mutation can occur
        #[allow(unsafe_code)]
        let iter: Box<
            dyn ExactSizeIterator<Item = &'static core_dataset::variable::DataVariable>
                + Send
                + 'static,
        > = unsafe { std::mem::transmute(iter) };

        let py_dataset: Py<Self> = Py::from(this);

        DataVariableIterator {
            dataset: py_dataset,
            iter,
        }
    }

    #[must_use]
    #[getter]
    pub fn ignored_variables<'py>(&self, py: Python<'py>) -> &'py PyList {
        PyList::new(py, self.dataset.ignored_variables())
    }
}

#[pyfunction]
#[pyo3(signature = (**kwargs))]
fn settings(
    py: Python,
    kwargs: Option<&PyDict>,
) -> Result<DataclassOut<core_dataset::dataset::DatasetSettings>, PyErr> {
    DataclassOut::new(
        &*kwargs
            .unwrap_or(PyDict::new(py))
            .extract::<Dataclass<_>>()?,
        py,
    )
}

#[pyclass(module = "fcbench.dataset", frozen)]
pub struct DataVariable {
    pub(crate) variable: core_dataset::variable::DataVariable,
}

#[pymethods]
impl DataVariable {
    #[must_use]
    #[getter]
    pub fn name(&self) -> &str {
        self.variable.name()
    }

    #[must_use]
    #[getter]
    pub fn long_name(&self) -> Option<&str> {
        self.variable.long_name()
    }

    #[getter]
    pub fn units(
        &self,
        py: Python,
    ) -> Result<Option<DataclassOutFrozen<core_dataset::units::DataUnitSummary>>, PyErr> {
        self.variable
            .units()
            .map(|unit| DataclassOutFrozen::new(&unit.summary(), py))
            .transpose()
    }

    #[must_use]
    #[getter]
    pub fn dtype(&self) -> String {
        format!("{}", self.variable.dtype())
    }
}

#[pyclass(module = "fcbench.compressor", mapping)]
// not frozen as the iterator is mutated on iteration
pub struct DataVariableIterator {
    dataset: Py<Dataset>,
    // FIXME: remove boxing once impl Trait inside an associated type is stable
    iter: Box<
        dyn ExactSizeIterator<Item = &'static core_dataset::variable::DataVariable>
            + Send
            + 'static,
    >,
}

#[pymethods]
impl DataVariableIterator {
    pub fn __iter__(this: PyRef<Self>) -> PyRef<Self> {
        this
    }

    pub fn __next__(&mut self) -> Option<DataVariable> {
        self.iter.next().map(|variable| DataVariable {
            variable: variable.clone(),
        })
    }

    #[must_use]
    pub fn __len__(&self) -> usize {
        self.iter.len()
    }

    pub fn __contains__(&self, py: Python, name: &str) -> Result<bool, PyErr> {
        let dataset: PyRef<Dataset> = self.dataset.try_borrow(py)?;
        let dataset: &Dataset = &dataset;

        Ok(dataset.dataset.get_variable(name).is_some())
    }

    pub fn __getitem__(&self, py: Python, name: &str) -> Result<DataVariable, PyErr> {
        let dataset: PyRef<Dataset> = self.dataset.try_borrow(py)?;
        let dataset: &Dataset = &dataset;

        match dataset.dataset.get_variable(name) {
            Some(variable) => Ok(DataVariable {
                variable: variable.clone(),
            }),
            None => Err(PyKeyError::new_err(String::from(name))),
        }
    }
}
