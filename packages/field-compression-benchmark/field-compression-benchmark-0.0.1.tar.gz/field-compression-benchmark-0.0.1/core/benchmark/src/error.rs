use std::{convert::Infallible, fmt};

use pyo3::{
    exceptions::{PyKeyboardInterrupt, PyRuntimeError},
    prelude::*,
};
use thiserror::Error;

use core_error::LocationError;
use core_measure::stats::AnalysisError;

#[derive(Debug, thiserror::Error)]
pub enum BenchmarkSingleCaseError {
    #[error("failed to execute Python code")]
    Python(#[source] LocationError<PyErr>),
    #[error("failed to analyse some measurements")]
    Analysis(#[source] LocationError<AnalysisError>),
}

impl From<PyErr> for BenchmarkSingleCaseError {
    #[track_caller]
    fn from(err: PyErr) -> Self {
        Self::Python(err.into())
    }
}

impl From<AnalysisError> for BenchmarkSingleCaseError {
    #[track_caller]
    fn from(err: AnalysisError) -> Self {
        Self::Analysis(err.into())
    }
}

impl From<Infallible> for BenchmarkSingleCaseError {
    fn from(err: Infallible) -> Self {
        match err {}
    }
}

impl From<LocationError<PyErr>> for BenchmarkSingleCaseError {
    fn from(err: LocationError<PyErr>) -> Self {
        Self::Python(err)
    }
}

impl From<LocationError<AnalysisError>> for BenchmarkSingleCaseError {
    fn from(err: LocationError<AnalysisError>) -> Self {
        Self::Analysis(err)
    }
}

impl From<LocationError<Infallible>> for BenchmarkSingleCaseError {
    fn from(err: LocationError<Infallible>) -> Self {
        err.infallible()
    }
}

impl From<BenchmarkSingleCaseError> for PyErr {
    fn from(err: BenchmarkSingleCaseError) -> Self {
        match err {
            BenchmarkSingleCaseError::Analysis(analysis) => Python::with_gil(|py| {
                let err = PyRuntimeError::new_err("failed to analyse the measurments");
                err.set_cause(py, Some(PyRuntimeError::new_err(format!("{analysis:?}"))));
                err
            }),
            BenchmarkSingleCaseError::Python(python) => Python::with_gil(|py| {
                let err = PyRuntimeError::new_err("failed to execute Python code");
                err.set_cause(py, Some(python.into_error()));
                err
            }),
        }
    }
}

#[derive(Debug, Clone, Error, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum BenchmarkCaseError {
    #[error("failed to execute Python code")]
    Python(#[source] LocationError<PyErrString>),
    #[error("failed to analyse some measurements")]
    Analysis(#[source] LocationError<StringifiedError>),
    #[error("failed to distribute a benchmark case")]
    Distributed(#[source] LocationError<StringifiedError>),
}

#[derive(Debug, Clone, Error, serde::Serialize, serde::Deserialize)]
#[serde(transparent)]
#[error("{0}")]
pub struct StringError(pub String);

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(untagged)]
pub enum StringifiedError {
    String(String),
    Error {
        message: String,
        source: StringError,
    },
}

impl StringifiedError {
    #[must_use]
    pub fn from_string(message: String) -> Self {
        Self::String(message)
    }

    #[must_use]
    pub fn from_err<E: std::error::Error>(err: E) -> Self {
        let message = format!("{err}");

        if let Some(source) = std::error::Error::source(&err) {
            Self::Error {
                message,
                source: StringError(format!("{source:#}")),
            }
        } else {
            Self::String(message)
        }
    }
}

impl fmt::Display for StringifiedError {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::String(message) | Self::Error { message, .. } => fmt.write_str(message),
        }
    }
}

impl std::error::Error for StringifiedError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::String(_) => None,
            Self::Error { source, .. } => Some(source),
        }
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "PyErr")]
#[serde(deny_unknown_fields)]
pub struct PyErrString {
    pub r#type: String,
    pub message: String,
    pub traceback: Option<StringError>,
}

impl fmt::Display for PyErrString {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        write!(fmt, "{}: {}", self.r#type, self.message)
    }
}

impl std::error::Error for PyErrString {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        self.traceback
            .as_ref()
            .map(|err| err as &dyn std::error::Error)
    }
}

impl From<BenchmarkSingleCaseError> for BenchmarkCaseError {
    fn from(err: BenchmarkSingleCaseError) -> Self {
        match err {
            BenchmarkSingleCaseError::Python(err) => Python::with_gil(|py| {
                let err = err.map(|err| {
                    let value = err.value(py);

                    let r#type = String::from(
                        value
                            .get_type()
                            .name()
                            .unwrap_or("<exception type() failed>"),
                    );
                    let message = String::from(
                        value
                            .str()
                            .map(|s| s.to_string_lossy())
                            .unwrap_or(std::borrow::Cow::Borrowed("<exception str() failed>")),
                    );
                    let traceback = if err.is_instance_of::<PyKeyboardInterrupt>(py) {
                        None
                    } else {
                        err.traceback(py).map(|t| {
                            t.format()
                                .unwrap_or_else(|_| String::from("<exception traceback() failed>"))
                        })
                    };

                    PyErrString {
                        r#type,
                        message,
                        traceback: traceback.map(StringError),
                    }
                });

                Self::Python(err)
            }),
            BenchmarkSingleCaseError::Analysis(err) => {
                Self::Analysis(err.map(StringifiedError::from_err))
            },
        }
    }
}
