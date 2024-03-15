use std::{marker::PhantomData, ops::Deref};

use pyo3::{
    intern,
    prelude::*,
    types::{IntoPyDict, PyDict, PyList, PyMapping, PyTuple},
};
use pythonize::{PythonizeDictType, PythonizeTypes};

pub struct Dataclass<T: serde::Serialize> {
    data: T,
}

impl<T: serde::Serialize> Dataclass<T> {
    #[must_use]
    pub fn new(data: T) -> Self {
        Self { data }
    }

    #[must_use]
    pub fn into_data(self) -> T {
        self.data
    }

    pub fn output(&self, py: Python) -> Result<DataclassOut<T>, PyErr> {
        DataclassOut::new(&self.data, py)
    }

    pub fn output_frozen(&self, py: Python) -> Result<DataclassOutFrozen<T>, PyErr> {
        DataclassOutFrozen::new(&self.data, py)
    }
}

impl<T: serde::Serialize> Deref for Dataclass<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.data
    }
}

impl<'py, T: serde::Serialize + serde::Deserialize<'py>> FromPyObject<'py> for Dataclass<T> {
    fn extract(obj: &'py PyAny) -> Result<Self, PyErr> {
        Ok(Self {
            data: pythonize::depythonize(obj)?,
        })
    }
}

// TODO: unite with Dataclass once there is a fallible IntoPy
pub struct DataclassOut<T: serde::Serialize> {
    data: Py<PyAny>,
    inner: PhantomData<T>,
}

impl<T: serde::Serialize> DataclassOut<T> {
    pub fn new(data: &T, py: Python) -> Result<Self, PyErr> {
        match pythonize::pythonize_custom::<PythonizeNamespace, T>(py, data) {
            Ok(data) => Ok(Self {
                data,
                inner: PhantomData::<T>,
            }),
            Err(err) => Err(PyErr::from(err)),
        }
    }
}

impl<T: serde::Serialize> IntoPy<Py<PyAny>> for DataclassOut<T> {
    fn into_py(self, _py: Python) -> Py<PyAny> {
        self.data
    }
}

pub struct DataclassOutFrozen<T: serde::Serialize> {
    data: Py<PyAny>,
    inner: PhantomData<T>,
}

impl<T: serde::Serialize> DataclassOutFrozen<T> {
    pub fn new(data: &T, py: Python) -> Result<Self, PyErr> {
        match pythonize::pythonize_custom::<PythonizeFrozenDataclass, T>(py, data) {
            Ok(data) => Ok(Self {
                data,
                inner: PhantomData::<T>,
            }),
            Err(err) => Err(PyErr::from(err)),
        }
    }
}

impl<T: serde::Serialize> IntoPy<Py<PyAny>> for DataclassOutFrozen<T> {
    fn into_py(self, _py: Python) -> Py<PyAny> {
        self.data
    }
}

pub enum PythonizeNamespace {}

impl PythonizeTypes for PythonizeNamespace {
    type List = PyList;
    type Map = PythonizeNamespace;
}

impl PythonizeDictType for PythonizeNamespace {
    fn create_mapping(py: Python) -> Result<&PyMapping, PyErr> {
        Ok(PyDict::new(py).as_mapping())
    }

    fn create_mapping_with_items<
        K: ToPyObject,
        V: ToPyObject,
        U: ExactSizeIterator<Item = (K, V)>,
    >(
        py: Python,
        items: impl IntoIterator<Item = (K, V), IntoIter = U>,
    ) -> PyResult<&PyMapping> {
        Ok(items.into_py_dict(py).as_mapping())
    }

    fn create_mapping_with_items_name<
        'py,
        K: ToPyObject,
        V: ToPyObject,
        U: ExactSizeIterator<Item = (K, V)>,
    >(
        py: Python<'py>,
        name: &str,
        items: impl IntoIterator<Item = (K, V), IntoIter = U>,
    ) -> Result<&'py PyMapping, PyErr> {
        let items = items.into_py_dict(py);

        let bases = (
            py.import(intern!(py, "types"))?
                .getattr(intern!(py, "SimpleNamespace"))?,
            py.import(intern!(py, "collections"))?
                .getattr(intern!(py, "abc"))?
                .getattr(intern!(py, "Mapping"))?,
        );

        let namespace: &PyDict = py
            .eval(
                "dict(
            __len__ = lambda self: self.__dict__.__len__(),
            __contains__ = lambda self, key: self.__dict__.__contains__(key),
            __getitem__ = lambda self, key: self.__dict__.__getitem__(key),
            __iter__ = lambda self: self.__dict__.__iter__(),
            keys = lambda self: self.__dict__.keys(),
            values = lambda self: self.__dict__.values(),
            items = lambda self: self.__dict__.items(),
        )",
                None,
                None,
            )?
            .extract()?;

        let class = py
            .import(intern!(py, "builtins"))?
            .getattr(intern!(py, "type"))?
            .call1((name, bases, namespace))?;

        class.call((), Some(items.into_py_dict(py)))?.extract()
    }
}

pub enum PythonizeFrozenDataclass {}

impl PythonizeTypes for PythonizeFrozenDataclass {
    type List = PyTuple;
    type Map = PythonizeFrozenDataclass;
}

impl PythonizeDictType for PythonizeFrozenDataclass {
    fn create_mapping(py: Python) -> Result<&PyMapping, PyErr> {
        py.import(intern!(py, "types"))?
            .getattr(intern!(py, "MappingProxyType"))?
            .call1((PyDict::new(py),))?
            .extract()
    }

    fn create_mapping_with_items<
        K: ToPyObject,
        V: ToPyObject,
        U: ExactSizeIterator<Item = (K, V)>,
    >(
        py: Python,
        items: impl IntoIterator<Item = (K, V), IntoIter = U>,
    ) -> PyResult<&PyMapping> {
        py.import(intern!(py, "types"))?
            .getattr(intern!(py, "MappingProxyType"))?
            .call1((items.into_py_dict(py),))?
            .extract()
    }

    fn create_mapping_with_items_name<
        'py,
        K: ToPyObject,
        V: ToPyObject,
        U: ExactSizeIterator<Item = (K, V)>,
    >(
        py: Python<'py>,
        name: &str,
        items: impl IntoIterator<Item = (K, V), IntoIter = U>,
    ) -> Result<&'py PyMapping, PyErr> {
        let items = items.into_py_dict(py);

        let bases = (
            py.import(intern!(py, "collections"))?
                .getattr(intern!(py, "namedtuple"))?
                .call1((name, items.keys()))?,
            py.import(intern!(py, "collections"))?
                .getattr(intern!(py, "abc"))?
                .getattr(intern!(py, "Mapping"))?,
        );

        let namespace: &PyDict = py
            .eval(
                "dict(
            __slots__ = (),
            __contains__ = lambda self, key: self._asdict().__contains__(key),
            __getitem__ = lambda self, key: self._asdict().__getitem__(key),
            keys = lambda self: self._asdict().keys(),
            values = lambda self: self._asdict().values(),
            items = lambda self: self._asdict().items(),
        )",
                None,
                None,
            )?
            .extract()?;

        let class = py
            .import(intern!(py, "builtins"))?
            .getattr(intern!(py, "type"))?
            .call1((name, bases, namespace))?;

        class.call((), Some(items.into_py_dict(py)))?.extract()
    }
}
