use std::{
    collections::{HashMap, HashSet},
    path::{Path, PathBuf},
};

use pyo3::{
    exceptions::PyRuntimeError,
    prelude::*,
    types::{PyDict, PyList, PyType},
};
use vecmap::VecSet;

use crate::dataclass::{Dataclass, DataclassOutFrozen};

pub fn create_module(py: Python) -> Result<&PyModule, PyErr> {
    let module = PyModule::new(py, "compressor")?;

    module.add_class::<Compressor>()?;
    module.add_function(wrap_pyfunction!(
        compute_dataarray_compress_decompress,
        module
    )?)?;

    Ok(module)
}

#[pyclass(module = "fcbench.compressor", frozen)]
pub struct Compressor {
    compressor: core_compressor::compressor::Compressor,
}

#[pymethods]
impl Compressor {
    #[staticmethod]
    #[pyo3(signature = (**kwargs))]
    pub fn from_config_kwargs(py: Python, kwargs: Option<&PyDict>) -> Result<Self, PyErr> {
        let mut depythonizer =
            pythonize::Depythonizer::from_object(kwargs.unwrap_or(PyDict::new(py)));

        match core_compressor::compressor::Compressor::from_deserialised_config(
            py,
            &mut depythonizer,
        ) {
            Ok(compressor) => Ok(Self { compressor }),
            Err(err) => Err(PyErr::from(err)),
        }
    }

    #[staticmethod]
    pub fn from_config_str(py: Python, config: &str) -> Result<Self, PyErr> {
        match core_compressor::compressor::Compressor::from_config_str(py, config) {
            Ok(compressor) => Ok(Self { compressor }),
            Err(err) => Err(PyRuntimeError::new_err(format!("{err:#}"))),
        }
    }

    #[allow(clippy::needless_pass_by_value)]
    #[staticmethod]
    pub fn from_config_file(py: Python, config_file: PathBuf) -> Result<Self, PyErr> {
        match core_compressor::compressor::Compressor::from_config_file(py, &config_file) {
            Ok(compressor) => Ok(Self { compressor }),
            Err(err) => Err(PyRuntimeError::new_err(format!("{err:#}"))),
        }
    }

    #[staticmethod]
    pub fn from_config_files(
        py: Python,
        config_files: HashSet<PathBuf>,
    ) -> Result<HashMap<String, Self>, PyErr> {
        match core_compressor::compressor::Compressor::from_config_files(
            py,
            &VecSet::from_iter(config_files),
        ) {
            Ok(compressors) => Ok(compressors
                .into_iter()
                .map(|(name, compressor)| (name, Self { compressor }))
                .collect()),
            Err(err) => Err(PyRuntimeError::new_err(format!("{err:#}"))),
        }
    }

    #[allow(clippy::needless_pass_by_value)]
    #[staticmethod]
    pub fn from_config_directory(
        py: Python,
        config_directory: PathBuf,
    ) -> Result<HashMap<String, Self>, PyErr> {
        match core_compressor::compressor::Compressor::from_config_directory(py, &config_directory)
        {
            Ok(compressors) => Ok(compressors
                .into_iter()
                .map(|(name, compressor)| (name, Self { compressor }))
                .collect()),
            Err(err) => Err(PyRuntimeError::new_err(format!("{err:#}"))),
        }
    }

    #[must_use]
    #[getter]
    pub fn name(&self) -> &str {
        self.compressor.name()
    }

    #[must_use]
    #[getter]
    pub fn config_path(&self) -> Option<&Path> {
        self.compressor.config_path()
    }

    #[must_use]
    #[getter]
    pub fn codecs(this: PyRef<Self>) -> CodecIterator {
        let iter = this.compressor.codecs();
        let iter: Box<dyn ExactSizeIterator<Item = &core_compressor::codec::Codec> + Send> =
            Box::new(iter);
        // Safety:
        // - we borrow the compressor that's inside PyRef<Self> and Py<Self>
        // - the iterator and its items all carry around clones of Py<Self>
        // - so the compressor lives long enough
        // - Self is a frozen class, so no mutation can occur
        #[allow(unsafe_code)]
        let iter: Box<
            dyn ExactSizeIterator<Item = &'static core_compressor::codec::Codec> + Send + 'static,
        > = unsafe { std::mem::transmute(iter) };

        let py_compressor: Py<Self> = Py::from(this);

        CodecIterator {
            _compressor: py_compressor,
            iter,
        }
    }

    pub fn minimise(&self) -> Self {
        // copy on write since Self is a frozen PyO3 class
        let mut this = Self {
            compressor: self.compressor.clone(),
        };
        this.compressor.minimise();
        this
    }

    pub fn __str__(&self) -> String {
        format!("{}", self.compressor)
    }

    pub fn ensure_imports(&self, py: Python) -> Result<(), PyErr> {
        self.compressor
            .ensure_py_imports(py)
            .map_err(core_error::LocationError::into_error)
    }

    #[must_use]
    #[getter]
    pub fn concrete(this: PyRef<Self>) -> ConcreteCompressorIterator {
        let iter: core_compressor::compressor::ConcreteCompressorIterator<'_> =
            this.compressor.iter_concrete();
        // Safety:
        // - we borrow the compressor that's inside PyRef<Self> and Py<Self>
        // - the iterator and its items all carry around clones of Py<Self>
        // - so the compressor lives long enough
        // - Self is a frozen class, so no mutation can occur
        #[allow(unsafe_code)]
        let iter: core_compressor::compressor::ConcreteCompressorIterator<'static> =
            unsafe { std::mem::transmute(iter) };

        let py_compressor: Py<Self> = Py::from(this);

        ConcreteCompressorIterator {
            compressor: py_compressor,
            iter,
        }
    }
}

#[pyclass(module = "fcbench.compressor", frozen)]
pub struct Codec {
    codec: core_compressor::codec::Codec,
}

#[pymethods]
impl Codec {
    #[getter]
    pub fn r#type<'py>(&self, py: Python<'py>) -> Result<&'py PyType, PyErr> {
        self.codec
            .import_py(py)
            .map_err(core_error::LocationError::into_error)
    }

    #[must_use]
    #[getter]
    pub fn import_path(&self) -> &str {
        self.codec.import()
    }

    #[must_use]
    #[getter]
    pub fn kind(&self) -> String {
        format!("{}", self.codec.kind())
    }

    pub fn __str__(&self) -> String {
        format!("{}", self.codec)
    }
}

#[pyclass(module = "fcbench.compressor")]
// not frozen as the iterator is mutated on iteration
pub struct CodecIterator {
    _compressor: Py<Compressor>,
    // FIXME: remove boxing once impl Trait inside an associated type is stable
    iter:
        Box<dyn ExactSizeIterator<Item = &'static core_compressor::codec::Codec> + Send + 'static>,
}

#[pymethods]
impl CodecIterator {
    pub fn __iter__(this: PyRef<Self>) -> PyRef<Self> {
        this
    }

    pub fn __next__(&mut self) -> Option<Codec> {
        self.iter.next().map(|codec| Codec {
            codec: codec.clone(),
        })
    }

    pub fn __len__(&self) -> usize {
        self.iter.len()
    }
}

#[pyclass(module = "fcbench.compressor", frozen)]
pub struct ConcreteCompressor {
    _compressor: Py<Compressor>,
    pub(crate) concrete: core_compressor::compressor::ConcreteCompressor<'static>,
}

#[pymethods]
impl ConcreteCompressor {
    #[must_use]
    pub fn name(&self) -> &str {
        self.concrete.name()
    }

    #[must_use]
    pub fn config_path(&self) -> Option<&Path> {
        self.concrete.config_path()
    }

    pub fn __str__(&self) -> String {
        format!("{}", self.concrete)
    }

    pub fn build<'py>(&self, py: Python<'py>) -> Result<&'py PyList, PyErr> {
        self.concrete
            .build_py(py)
            .map_err(core_error::LocationError::into_error)
    }

    #[must_use]
    #[getter]
    pub fn codecs(this: PyRef<Self>) -> ConcreteCodecIterator {
        let iter = this.concrete.codecs();
        let iter: Box<dyn ExactSizeIterator<Item = &core_compressor::codec::ConcreteCodec> + Send> =
            Box::new(iter);
        // Safety:
        // - we borrow the compressor that's inside PyRef<Self> and Py<Self>
        // - the iterator and its items all carry around clones of Py<Self>
        // - so the compressor lives long enough
        // - Self is a frozen class, so no mutation can occur
        #[allow(unsafe_code)]
        let iter: Box<
            dyn ExactSizeIterator<Item = &'static core_compressor::codec::ConcreteCodec<'static>>
                + Send
                + 'static,
        > = unsafe { std::mem::transmute(iter) };

        let py_compressor: Py<Self> = Py::from(this);

        ConcreteCodecIterator {
            compressor: py_compressor,
            iter,
        }
    }
}

#[pyclass(module = "fcbench.compressor")]
// not frozen as the iterator is mutated on iteration
pub struct ConcreteCompressorIterator {
    compressor: Py<Compressor>,
    iter: core_compressor::compressor::ConcreteCompressorIterator<'static>,
}

#[pymethods]
impl ConcreteCompressorIterator {
    pub fn __iter__(this: PyRef<Self>) -> PyRef<Self> {
        this
    }

    pub fn __next__(&mut self, py: Python) -> Option<ConcreteCompressor> {
        self.iter.next().map(|concrete| ConcreteCompressor {
            _compressor: self.compressor.clone_ref(py),
            concrete,
        })
    }
}

#[pyclass(module = "fcbench.compressor", frozen)]
pub struct ConcreteCodec {
    _compressor: Py<ConcreteCompressor>,
    concrete: core_compressor::codec::ConcreteCodec<'static>,
}

#[pymethods]
impl ConcreteCodec {
    pub fn build<'py>(
        &self,
        py: Python<'py>,
    ) -> Result<&'py core_compressor::numcodecs::Codec, PyErr> {
        match self.concrete.build_py(py) {
            Ok(concrete) => Ok(concrete),
            Err(err) => Err(err.into_error()),
        }
    }

    #[must_use]
    #[getter]
    pub fn import_path(&self) -> &str {
        self.concrete.import()
    }

    #[must_use]
    #[getter]
    pub fn kind(&self) -> String {
        format!("{}", self.concrete.kind())
    }

    pub fn __str__(&self) -> String {
        format!("{}", self.concrete)
    }
}

#[pyclass(module = "fcbench.compressor")]
// not frozen as the iterator is mutated on iteration
pub struct ConcreteCodecIterator {
    compressor: Py<ConcreteCompressor>,
    // FIXME: remove boxing once impl Trait inside an associated type is stable
    iter: Box<
        dyn ExactSizeIterator<Item = &'static core_compressor::codec::ConcreteCodec<'static>>
            + Send
            + 'static,
    >,
}

#[pymethods]
impl ConcreteCodecIterator {
    pub fn __iter__(this: PyRef<Self>) -> PyRef<Self> {
        this
    }

    pub fn __next__(&mut self, py: Python) -> Option<ConcreteCodec> {
        self.iter.next().map(|concrete| ConcreteCodec {
            _compressor: self.compressor.clone_ref(py),
            concrete: concrete.clone(),
        })
    }

    pub fn __len__(&self) -> usize {
        self.iter.len()
    }
}

#[pyfunction]
pub fn compute_dataarray_compress_decompress<'py>(
    py: Python<'py>,
    da: &'py PyAny,
    compressor: &'py PyList,
) -> Result<
    (
        &'py PyAny,
        Vec<DataclassOutFrozen<core_compressor::compress::CodecPerformanceMeasurement>>,
    ),
    PyErr,
> {
    match core_compressor::compress::DataArrayCompressor::compute_compress_decompress(
        py, da, compressor,
    ) {
        Ok((da, measurements)) => Ok((
            da,
            measurements
                .into_iter()
                .map(|measurement| Dataclass::new(measurement).output_frozen(py))
                .collect::<Result<_, _>>()?,
        )),
        Err(err) => Err(err.into_error()),
    }
}
