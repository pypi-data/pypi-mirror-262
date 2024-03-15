use std::{borrow::Cow, fmt, ops::ControlFlow};

use pyo3::{
    prelude::*,
    types::{IntoPyDict, PyDict, PyType},
};
use vecmap::VecMap;

use core_error::LocationError;

use crate::{
    numcodecs,
    parameter::{ConcreteParameter, ConcreteParameterSummary, Parameter, ParameterIterator},
};

mod config;
pub(super) use config::CodecSeed;

#[derive(Debug, Clone)]
pub struct Codec {
    import: String,
    kind: CodecKind,
    parameters: VecMap<String, Parameter>,
}

impl Codec {
    pub fn import_py<'py>(&self, py: Python<'py>) -> Result<&'py PyType, LocationError<PyErr>> {
        let mut locals = Vec::new();
        for (pos, c) in self.import.char_indices() {
            if c == '.' {
                if let Some(module) = self.import.get(..pos) {
                    locals.push((module, py.import(module)?));
                }
            }
        }
        let locals = locals.into_py_dict(py);

        py.eval(&self.import, None, Some(locals))?
            .extract()
            .map_err(LocationError::new)
    }

    #[must_use]
    pub fn cyclic_iter_concrete(&self) -> ConcreteCodecIterator {
        let parameters = self
            .parameters
            .values()
            .map(Parameter::cyclic_iter)
            .collect::<Vec<_>>();

        ConcreteCodecIterator {
            codec: self,
            parameters,
        }
    }

    pub fn minimise(&mut self) {
        self.parameters.values_mut().for_each(Parameter::minimise);
    }

    #[must_use]
    pub fn import(&self) -> &str {
        &self.import
    }

    #[must_use]
    pub fn kind(&self) -> CodecKind {
        self.kind
    }
}

impl fmt::Display for Codec {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        let name = match self.import.rsplit_once('.') {
            Some((_, name)) => name,
            None => &*self.import,
        };

        fmt.write_fmt(format_args!("{name}("))?;

        for (i, (name, value)) in self.parameters.iter().enumerate() {
            if i > 0 {
                fmt.write_str(", ")?;
            }

            fmt.write_fmt(format_args!("{name}={value}"))?;
        }

        fmt.write_str(")")
    }
}

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum CodecKind {
    BinaryLossless,
    SymbolicLossless,
    Lossy,
}

impl fmt::Display for CodecKind {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        match self {
            CodecKind::BinaryLossless => fmt.write_str("binary-lossless"),
            CodecKind::SymbolicLossless => fmt.write_str("symbolic-lossless"),
            CodecKind::Lossy => fmt.write_str("lossy"),
        }
    }
}

#[derive(Debug, Clone)]
pub struct ConcreteCodec<'a> {
    codec: &'a Codec,
    parameters: Vec<ConcreteParameter<'a>>,
}

impl<'a> ConcreteCodec<'a> {
    pub fn build_py<'py>(
        &self,
        py: Python<'py>,
    ) -> Result<&'py numcodecs::Codec, LocationError<PyErr>> {
        let py_codec = self.codec.import_py(py)?;

        let config = PyDict::new(py);

        for (name, parameter) in self.codec.parameters.keys().zip(self.parameters.iter()) {
            match parameter {
                ConcreteParameter::Int { value } => {
                    config.set_item(name, *value)?;
                },
                ConcreteParameter::Float { value } => {
                    config.set_item(name, *value)?;
                },
                ConcreteParameter::Str { value } => {
                    config.set_item(name, value)?;
                },
            }
        }

        numcodecs::Codec::from_config(py_codec, config).map_err(LocationError::new)
    }

    #[must_use]
    pub fn import(&self) -> &str {
        self.codec.import()
    }

    #[must_use]
    pub fn kind(&self) -> CodecKind {
        self.codec.kind()
    }

    pub fn parameters(&self) -> impl Iterator<Item = (&str, &ConcreteParameter<'a>)> {
        self.codec
            .parameters
            .iter()
            .zip(self.parameters.iter())
            .map(|((name, _), concrete)| (&**name, concrete))
    }

    #[must_use]
    pub fn summary(&self) -> ConcreteCodecSummary<'a> {
        ConcreteCodecSummary {
            import: Cow::Borrowed(self.codec.import.as_str()),
            kind: self.codec.kind,
            parameters: self
                .codec
                .parameters
                .keys()
                .map(|name| Cow::Borrowed(name.as_str()))
                .zip(self.parameters.iter().map(ConcreteParameter::summary))
                .collect(),
        }
    }
}

impl<'a> fmt::Display for ConcreteCodec<'a> {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        let name = match self.codec.import.rsplit_once('.') {
            Some((_, name)) => name,
            None => &*self.codec.import,
        };

        fmt.write_fmt(format_args!("{name}("))?;

        for (i, (name, value)) in self
            .codec
            .parameters
            .keys()
            .zip(self.parameters.iter())
            .enumerate()
        {
            if i > 0 {
                fmt.write_str(", ")?;
            }

            fmt.write_fmt(format_args!("{name}={value}"))?;
        }

        fmt.write_str(")")
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "Codec")]
#[serde(deny_unknown_fields)]
pub struct ConcreteCodecSummary<'a> {
    #[serde(borrow)]
    import: Cow<'a, str>,
    kind: CodecKind,
    #[serde(borrow)]
    parameters: VecMap<Cow<'a, str>, ConcreteParameterSummary<'a>>,
}

pub struct ConcreteCodecIterator<'a> {
    codec: &'a Codec,
    parameters: Vec<ParameterIterator<'a>>,
}

impl<'a> ConcreteCodecIterator<'a> {
    #[allow(clippy::should_implement_trait)] // FIXME
    pub fn next(&mut self) -> ControlFlow<ConcreteCodec<'a>, ConcreteCodec<'a>> {
        let mut all_done = true;

        let parameters = self
            .parameters
            .iter_mut()
            .map(|parameter| {
                if all_done {
                    match parameter.next() {
                        ControlFlow::Break(value) => value,
                        ControlFlow::Continue(value) => {
                            all_done = false;
                            value
                        },
                    }
                } else {
                    parameter.get()
                }
            })
            .collect();

        let iter = ConcreteCodec {
            codec: self.codec,
            parameters,
        };

        if all_done {
            ControlFlow::Break(iter)
        } else {
            ControlFlow::Continue(iter)
        }
    }

    pub fn get(&self) -> ConcreteCodec<'a> {
        let parameters = self.parameters.iter().map(ParameterIterator::get).collect();

        ConcreteCodec {
            codec: self.codec,
            parameters,
        }
    }
}
