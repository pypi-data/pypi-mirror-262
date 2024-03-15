use std::{num::NonZeroUsize, ops::ControlFlow};

use pyo3::{
    intern,
    prelude::*,
    types::{IntoPyDict, PySlice},
};

use core_error::LocationError;

mod config;

use config::slice::{Type, Values};
pub(super) use config::{DataDimensionsSeed, PerVariableDataDimension};

#[derive(Debug, Clone)]
pub struct DataDimension {
    pub(in super::super) size: NonZeroUsize,
    pub(in super::super) slice: DataSlice,
}

impl DataDimension {
    #[must_use]
    pub fn with_size(size: NonZeroUsize) -> Self {
        Self {
            size,
            slice: DataSlice::All { reduce: false },
        }
    }

    #[must_use]
    pub fn size(&self) -> NonZeroUsize {
        self.size
    }

    #[must_use]
    pub fn slice(&self) -> &DataSlice {
        &self.slice
    }

    #[must_use]
    pub fn num_reductions(&self) -> usize {
        match self.slice {
            DataSlice::IntValue { .. }
            | DataSlice::FloatValue { .. }
            | DataSlice::Index { .. }
            | DataSlice::All { reduce: false } => 1,
            DataSlice::All { reduce: true } => self.size.get(),
        }
    }

    #[must_use]
    pub fn iter_reductions(&self) -> Option<DataDimensionReductionIterator> {
        match self.slice {
            // single-value dimensions are dropped in the slicing
            DataSlice::IntValue { .. } | DataSlice::FloatValue { .. } | DataSlice::Index { .. } => {
                None
            },
            DataSlice::All { reduce: false } => Some(DataDimensionReductionIterator::All),
            DataSlice::All { reduce: true } => Some(DataDimensionReductionIterator::Reduction {
                size: self.size,
                value: 0,
            }),
        }
    }

    pub fn minimise(&mut self) {
        match self.slice {
            DataSlice::IntValue { .. }
            | DataSlice::FloatValue { .. }
            | DataSlice::Index { .. }
            | DataSlice::All { reduce: false } => (),
            DataSlice::All { reduce: true } => self.slice = DataSlice::Index { index: 0 },
        }
    }

    #[must_use]
    pub fn summary(&self) -> DataDimensionSummary {
        DataDimensionSummary {
            size: self.size,
            slice: self.slice.summary(),
        }
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DataDimensionSummary {
    size: NonZeroUsize,
    slice: DataSliceSummary,
}

#[derive(Debug, Clone)]
pub enum DataSlice {
    IntValue { value: i64 },
    FloatValue { value: f64 },
    Index { index: isize },
    All { reduce: bool },
}

impl DataSlice {
    pub fn sel<'py>(
        &self,
        py: Python<'py>,
        da: &'py PyAny,
        dim_name: &str,
    ) -> Result<&'py PyAny, LocationError<PyErr>> {
        let (selector, is_index) = match self {
            Self::IntValue { value } => (value.into_py(py), false),
            Self::FloatValue { value } => (value.into_py(py), false),
            Self::Index { index } => (index.into_py(py), true),
            Self::All { .. } => return Ok(da),
        };

        da.call_method(
            if is_index {
                intern!(py, "isel")
            } else {
                intern!(py, "sel")
            },
            ([(dim_name, selector)].into_py_dict(py),),
            // https://github.com/pydata/xarray/issues/4073#issuecomment-1163292454
            Some([(intern!(py, "drop"), true)].into_py_dict(py)),
        )
        .map_err(LocationError::new)
    }

    #[must_use]
    pub fn summary(&self) -> DataSliceSummary {
        let inner = match self {
            Self::IntValue { value } => DataSliceSummaryInner::IntValue {
                r#type: IntType::Int,
                value: *value,
            },
            Self::FloatValue { value } => DataSliceSummaryInner::FloatValue {
                r#type: FloatType::Float,
                value: *value,
            },
            Self::Index { index } => DataSliceSummaryInner::Index { index: *index },
            Self::All { reduce } => DataSliceSummaryInner::All {
                values: AllValues::All,
                reduce: *reduce,
            },
        };

        DataSliceSummary { inner }
    }
}

impl serde::Serialize for DataSlice {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        use serde::ser::SerializeStruct;

        let mut r#struct = serializer.serialize_struct(
            "DataSlice",
            match self {
                Self::IntValue { .. } | Self::FloatValue { .. } | Self::All { .. } => 2,
                Self::Index { .. } => 1,
            },
        )?;
        match self {
            Self::IntValue { value } => {
                r#struct.serialize_field("type", &Type::Int)?;
                r#struct.serialize_field("value", value)
            },
            Self::FloatValue { value } => {
                r#struct.serialize_field("type", &Type::Float)?;
                r#struct.serialize_field("value", value)
            },
            Self::Index { index } => r#struct.serialize_field("index", index),
            Self::All { reduce } => {
                r#struct.serialize_field("values", &Values::All)?;
                r#struct.serialize_field("reduce", reduce)
            },
        }?;
        r#struct.end()
    }
}

pub enum DataDimensionReductionIterator {
    All,
    Reduction { size: NonZeroUsize, value: usize },
}

impl DataDimensionReductionIterator {
    pub fn next(&mut self, py: Python) -> ControlFlow<Py<PyAny>, Py<PyAny>> {
        match self {
            Self::All => ControlFlow::Break(Py::from(PySlice::full(py))),
            Self::Reduction { ref size, value } => {
                let old_value = *value;
                if (old_value + 1) < size.get() {
                    *value += 1;
                    ControlFlow::Continue(old_value.into_py(py))
                } else {
                    *value = 0;
                    ControlFlow::Break(old_value.into_py(py))
                }
            },
        }
    }

    #[must_use]
    pub fn get(&self, py: Python) -> Py<PyAny> {
        match self {
            Self::All => Py::from(PySlice::full(py)),
            Self::Reduction { value, .. } => value.into_py(py),
        }
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "DataSlice")]
#[serde(transparent)]
pub struct DataSliceSummary {
    inner: DataSliceSummaryInner,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "DataSlice")]
#[serde(untagged)]
enum DataSliceSummaryInner {
    IntValue {
        r#type: IntType,
        value: i64,
    },
    FloatValue {
        r#type: FloatType,
        value: f64,
    },
    Index {
        index: isize,
    },
    All {
        values: AllValues,
        #[serde(default)]
        reduce: bool,
    },
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "Type")]
#[serde(rename_all = "lowercase")]
enum IntType {
    Int,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "Type")]
#[serde(rename_all = "lowercase")]
enum FloatType {
    Float,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "lowercase")]
enum AllValues {
    All,
}
