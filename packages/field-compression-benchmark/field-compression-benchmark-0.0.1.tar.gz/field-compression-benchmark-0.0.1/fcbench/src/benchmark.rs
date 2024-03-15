use std::{borrow::Cow, collections::HashSet, path::PathBuf};

use pyo3::{
    exceptions::{PyKeyError, PyTypeError, PyValueError},
    intern,
    prelude::*,
    types::PyDict,
};

use crate::{
    compressor::ConcreteCompressor,
    dataclass::{Dataclass, DataclassOut},
    dataset::Dataset,
};

pub fn create_module(py: Python) -> Result<&PyModule, PyErr> {
    let module = PyModule::new(py, "benchmark")?;

    module.add_class::<BenchmarkCase>()?;
    module.add_class::<BenchmarkCaseId>()?;
    module.add_class::<BenchmarkCaseFilter>()?;
    module.add_function(wrap_pyfunction!(report, module)?)?;
    module.add_function(wrap_pyfunction!(settings, module)?)?;

    Ok(module)
}

#[pyclass(module = "fcbench.benchmark", frozen)]
pub struct BenchmarkCase {
    dataset: Py<crate::dataset::Dataset>,
    variable: Py<crate::dataset::DataVariable>,
    compressor: Py<crate::compressor::ConcreteCompressor>,
}

#[pymethods]
impl BenchmarkCase {
    #[new]
    pub fn new(
        py: Python,
        dataset: PyRef<Dataset>,
        variable: &str,
        compressor: PyRef<ConcreteCompressor>,
    ) -> Result<Self, PyErr> {
        let Some(variable) = dataset.dataset.get_variable(variable) else {
            return Err(PyKeyError::new_err(String::from(variable)));
        };

        let variable = crate::dataset::DataVariable {
            variable: variable.clone(),
        };

        Ok(Self {
            dataset: dataset.into(),
            variable: Py::new(py, variable)?,
            compressor: compressor.into(),
        })
    }

    #[getter]
    pub fn id(&self, py: Python) -> Result<BenchmarkCaseId, PyErr> {
        self.with_case(py, |case| Ok(BenchmarkCaseId { id: case.get_id() }))
    }

    #[getter]
    pub fn uuid<'py>(&self, py: Python<'py>) -> Result<&'py PyAny, PyErr> {
        self.with_case(py, |case| {
            let uuid = case.get_uuid();

            py.import(intern!(py, "uuid"))?
                .getattr("UUID")?
                .call1((format!("{uuid}"),))
        })
    }

    #[allow(clippy::needless_pass_by_value)]
    pub fn benchmark<'py>(
        &self,
        py: Python<'py>,
        settings: Dataclass<core_benchmark::settings::BenchmarkSettings>,
    ) -> Result<&'py PyDict, PyErr> {
        let dataset: &core_dataset::dataset::Dataset = &self.dataset.try_borrow(py)?.dataset;
        let variable: &core_dataset::variable::DataVariable =
            &self.variable.try_borrow(py)?.variable;
        let compressor: &core_compressor::compressor::ConcreteCompressor =
            &self.compressor.try_borrow(py)?.concrete;

        match core_benchmark::run_benchmark_case(dataset, variable, compressor, &settings) {
            Ok(result) => {
                let result_py = pythonize::pythonize(
                    py,
                    &core_benchmark::report::BenchmarkCaseReport {
                        dataset: Cow::Borrowed(dataset.path()),
                        format: dataset.format(),
                        variable: variable.summary(),
                        compressor: compressor.summary(),
                        result: Ok(result),
                    },
                )
                .map_err(PyErr::from)?;

                result_py.into_ref(py).extract()
            },
            Err(err) => Err(PyErr::from(err)),
        }
    }
}

impl BenchmarkCase {
    fn with_case<Q>(
        &self,
        py: Python,
        inner: impl FnOnce(core_benchmark::case::BenchmarkCase) -> Result<Q, PyErr>,
    ) -> Result<Q, PyErr> {
        inner(core_benchmark::case::BenchmarkCase {
            dataset: &self.dataset.try_borrow(py)?.dataset,
            variable: &self.variable.try_borrow(py)?.variable,
            compressor: Cow::Borrowed(&self.compressor.try_borrow(py)?.concrete),
        })
    }
}

#[pyclass(module = "fcbench.benchmark", frozen)]
#[derive(PartialEq, Eq, Hash)]
pub struct BenchmarkCaseId {
    id: core_benchmark::case::BenchmarkCaseId,
}

#[pymethods]
impl BenchmarkCaseId {
    #[staticmethod]
    #[pyo3(signature = (uuid), text_signature = "(uuid: uuid.UUID)")]
    pub fn from_uuid(py: Python, uuid: &PyAny) -> Result<Self, PyErr> {
        let codec = py
            .import(intern!(py, "uuid"))?
            .getattr(intern!(py, "UUID"))?;

        if !uuid.is_instance(codec)? {
            return Err(PyErr::new::<PyTypeError, _>(
                "uuid is not an instance of uuid.UUID",
            ));
        }

        let uuid: &str = uuid.str()?.extract()?;
        let uuid = uuid
            .parse()
            .map_err(|err| PyErr::new::<PyValueError, _>(format!("{err}")))?;

        Ok(Self {
            id: core_benchmark::case::BenchmarkCaseId::from_uuid(uuid),
        })
    }

    #[getter]
    pub fn uuid<'py>(&self, py: Python<'py>) -> Result<&'py PyAny, PyErr> {
        let uuid = self.id.into_uuid();

        py.import(intern!(py, "uuid"))?
            .getattr("UUID")?
            .call1((format!("{uuid}"),))
    }
}

impl<'py> FromPyObject<'py> for BenchmarkCaseId {
    fn extract(object: &'py PyAny) -> Result<Self, PyErr> {
        if let Ok(id) = object.downcast::<PyCell<Self>>() {
            let id: PyRef<Self> = PyCell::try_borrow(id)?;
            let id: &Self = &id;
            return Ok(Self { id: id.id });
        }

        BenchmarkCaseId::from_uuid(object.py(), object)
    }
}

#[pyclass(module = "fcbench.benchmark", frozen)]
pub struct BenchmarkCaseFilter {
    filter: core_benchmark::case::BenchmarkCaseFilter,
}

#[pymethods]
impl BenchmarkCaseFilter {
    #[new]
    pub fn new(ids: HashSet<BenchmarkCaseId>) -> Self {
        Self {
            filter: core_benchmark::case::BenchmarkCaseFilter::new(
                ids.into_iter().map(|id| id.id).collect(),
            ),
        }
    }

    #[must_use]
    pub fn __len__(&self) -> usize {
        self.filter.len()
    }

    #[must_use]
    pub fn __iter__(this: PyRef<Self>) -> BenchmarkCaseFilterIterator {
        let iter = this.filter.iter();
        let iter: Box<dyn ExactSizeIterator<Item = core_benchmark::case::BenchmarkCaseId> + Send> =
            Box::new(iter);
        // Safety:
        // - we borrow the filter that's inside PyRef<Self> and Py<Self>
        // - the iterator carries around clones of Py<Self>
        // - the iterator items contain no lifetimes
        // - so the dataset lives long enough
        // - Self is a frozen class, so no mutation can occur
        #[allow(unsafe_code)]
        let iter: Box<
            dyn ExactSizeIterator<Item = core_benchmark::case::BenchmarkCaseId> + Send + 'static,
        > = unsafe { std::mem::transmute(iter) };

        let py_filter: Py<Self> = Py::from(this);

        BenchmarkCaseFilterIterator {
            filter: py_filter,
            iter,
        }
    }

    #[must_use]
    #[allow(clippy::needless_pass_by_value)]
    pub fn __contains__(&self, id: BenchmarkCaseId) -> bool {
        self.filter.contains_case_id(&id.id)
    }

    #[must_use]
    #[allow(clippy::needless_pass_by_value)]
    pub fn contains_dataset(&self, dataset: PathBuf) -> bool {
        self.filter.contains_dataset(&dataset)
    }

    #[must_use]
    pub fn contains_variable(&self, variable: &str) -> bool {
        self.filter.contains_variable(variable)
    }

    #[must_use]
    #[allow(clippy::needless_pass_by_value)]
    pub fn contains_compressor(&self, compressor: PathBuf) -> bool {
        self.filter.contains_compressor(&compressor)
    }

    #[must_use]
    pub fn contains_codec_params(
        &self,
        codec_params: &crate::compressor::ConcreteCompressor,
    ) -> bool {
        self.filter.contains_codec_params(&codec_params.concrete)
    }

    pub fn contains_case(&self, py: Python, case: &BenchmarkCase) -> Result<bool, PyErr> {
        case.with_case(py, |case| Ok(self.filter.contains_case(&case)))
    }
}

#[pyclass(module = "fcbench.benchmark")]
// not frozen as the iterator is mutated on iteration
pub struct BenchmarkCaseFilterIterator {
    filter: Py<BenchmarkCaseFilter>,
    // FIXME: remove boxing once impl Trait inside an associated type is stable
    iter: Box<dyn ExactSizeIterator<Item = core_benchmark::case::BenchmarkCaseId> + Send + 'static>,
}

#[pymethods]
impl BenchmarkCaseFilterIterator {
    pub fn __iter__(this: PyRef<Self>) -> PyRef<Self> {
        this
    }

    pub fn __next__(&mut self) -> Option<BenchmarkCaseId> {
        self.iter.next().map(|id| BenchmarkCaseId { id })
    }

    #[must_use]
    pub fn __len__(&self) -> usize {
        self.iter.len()
    }

    #[allow(clippy::needless_pass_by_value)]
    pub fn __contains__(&self, py: Python, id: BenchmarkCaseId) -> Result<bool, PyErr> {
        let filter: PyRef<BenchmarkCaseFilter> = self.filter.try_borrow(py)?;
        let filter: &BenchmarkCaseFilter = &filter;

        Ok(filter.filter.contains_case_id(&id.id))
    }
}

#[pyfunction]
#[pyo3(signature = (**kwargs))]
fn settings(
    py: Python,
    kwargs: Option<&PyDict>,
) -> Result<DataclassOut<core_benchmark::settings::BenchmarkSettings>, PyErr> {
    DataclassOut::new(
        &*kwargs
            .unwrap_or(PyDict::new(py))
            .extract::<Dataclass<_>>()?,
        py,
    )
}

#[pyfunction]
#[pyo3(signature = (**kwargs))]
fn report<'py>(
    py: Python<'py>,
    kwargs: Option<&'py PyDict>,
) -> Result<DataclassOut<core_benchmark::report::BenchmarkReport<'py>>, PyErr> {
    DataclassOut::new(
        &*kwargs
            .unwrap_or(PyDict::new(py))
            .extract::<Dataclass<_>>()?,
        py,
    )
}
