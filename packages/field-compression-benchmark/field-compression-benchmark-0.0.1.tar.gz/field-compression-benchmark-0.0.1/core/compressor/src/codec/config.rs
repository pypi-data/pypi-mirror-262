use std::fmt;

use pyo3::{
    exceptions::PyTypeError,
    intern,
    prelude::*,
    types::{IntoPyDict, PyType},
};
use vecmap::{VecMap, VecSet};

use crate::parameter::Parameter;

use super::Codec;

pub struct CodecSeed<'py> {
    py: Python<'py>,
}

impl<'py> CodecSeed<'py> {
    pub fn new(py: Python<'py>) -> Self {
        Self { py }
    }
}

impl<'py, 'de> serde::de::DeserializeSeed<'de> for CodecSeed<'py> {
    type Value = Codec;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_struct(deserializer, "Codec", FIELDS, self)
    }
}

const FIELDS: &[&str] = &["import", "kind", "parameters"];

#[derive(Clone, Copy)]
enum Field {
    Import,
    Kind,
    Parameters,
    Excessive,
}

impl<'de> serde::de::DeserializeSeed<'de> for Field {
    type Value = ();

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_identifier(deserializer, self)
    }
}

impl<'de> serde::de::Visitor<'de> for Field {
    type Value = ();

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a codec config field identifier")
    }

    fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
        match (self, value) {
            (Self::Import, "import") | (Self::Kind, "kind") | (Self::Parameters, "parameters") => {
                Ok(())
            },
            _ => Err(serde::de::Error::unknown_field(
                value,
                match self {
                    Self::Import => &["import"],
                    Self::Kind => &["kind"],
                    Self::Parameters => &["parameters"],
                    Self::Excessive => &[],
                },
            )),
        }
    }

    fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
        match (self, value) {
            (Self::Import, b"import")
            | (Self::Kind, b"kind")
            | (Self::Parameters, b"parameters") => Ok(()),
            _ => {
                let value = String::from_utf8_lossy(value);
                Err(serde::de::Error::unknown_field(
                    &value,
                    match self {
                        Self::Import => &["import"],
                        Self::Kind => &["kind"],
                        Self::Parameters => &["parameters"],
                        Self::Excessive => &[],
                    },
                ))
            },
        }
    }
}

struct CodecImportSeed<'py> {
    py: Python<'py>,
}

impl<'py, 'de> serde::de::DeserializeSeed<'de> for CodecImportSeed<'py> {
    type Value = (String, VecSet<String>);

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_str(self)
    }
}

impl<'py, 'de> serde::de::Visitor<'de> for CodecImportSeed<'py> {
    type Value = (String, VecSet<String>);

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a codec import string")
    }

    fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> {
        fn visit_str_inner(py: Python, import: &str) -> Result<VecSet<String>, PyErr> {
            let mut locals = Vec::new();
            for (pos, c) in import.char_indices() {
                if c == '.' {
                    if let Some(module) = import.get(..pos) {
                        locals.push((module, py.import(module)?));
                    }
                }
            }
            let locals = locals.into_py_dict(py);

            let ty: &PyType = py.eval(import, None, Some(locals))?.extract()?;

            if !ty.is_subclass(
                py.import(intern!(py, "numcodecs.abc"))?
                    .getattr(intern!(py, "Codec"))?,
            )? {
                return Err(PyTypeError::new_err(
                    "not an instance of `numcodecs.abc.Codec`",
                ));
            }

            // TODO: Could we look into the parameter annotations and check the type?
            let parameters = py
                .import(intern!(py, "inspect"))?
                .getattr(intern!(py, "signature"))?
                .call1((ty.getattr(intern!(py, "__init__"))?,))?
                .getattr(intern!(py, "parameters"))?
                .call_method0(intern!(py, "keys"))?
                .iter()?
                .map(|name| name.and_then(PyAny::extract))
                .collect::<Result<VecSet<_>, _>>()?;

            Ok(parameters)
        }

        match visit_str_inner(self.py, v) {
            Ok(parameters) => Ok((String::from(v), parameters)),
            Err(err) => Err(serde::de::Error::custom(err)),
        }
    }
}

struct CodecParameterNameSeed<'a> {
    import: &'a str,
    parameters: &'a VecSet<String>,
    parameters_seen: &'a mut VecSet<String>,
}

impl<'a, 'de> serde::de::DeserializeSeed<'de> for CodecParameterNameSeed<'a> {
    type Value = String;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_str(self)
    }
}

impl<'a, 'de> serde::de::Visitor<'de> for CodecParameterNameSeed<'a> {
    type Value = String;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a parameter name")
    }

    fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> {
        if !self.parameters.contains(v) {
            return Err(serde::de::Error::custom(format!(
                "codec {} does not have a parameter named {v:?}",
                self.import
            )));
        }

        if !self.parameters_seen.insert(String::from(v)) {
            return Err(serde::de::Error::custom(format!(
                "duplicate parameter name {v:?}"
            )));
        }

        Ok(String::from(v))
    }
}

struct CodecParametersSeed<'a> {
    import: &'a str,
    parameters: VecSet<String>,
    parameters_seen: VecSet<String>,
}

impl<'a, 'de> serde::de::DeserializeSeed<'de> for CodecParametersSeed<'a> {
    type Value = VecMap<String, Parameter>;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        deserializer.deserialize_map(self)
    }
}

impl<'a, 'de> serde::de::Visitor<'de> for CodecParametersSeed<'a> {
    type Value = VecMap<String, Parameter>;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a map of parameters")
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(
        mut self,
        mut map: A,
    ) -> Result<Self::Value, A::Error> {
        let mut parameters = VecMap::with_capacity(map.size_hint().unwrap_or(0));

        while let Some(name) = map.next_key_seed(CodecParameterNameSeed {
            import: self.import,
            parameters: &self.parameters,
            parameters_seen: &mut self.parameters_seen,
        })? {
            parameters.insert(name, map.next_value()?);
        }

        Ok(parameters)
    }
}

impl<'py, 'de> serde::de::Visitor<'de> for CodecSeed<'py> {
    type Value = Codec;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a codec config")
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let Some(()) = map.next_key_seed(Field::Import)? else {
            return Err(serde::de::Error::custom(
                "a codec must start with an `import` field",
            ));
        };

        let (import, parameters) = map.next_value_seed(CodecImportSeed { py: self.py })?;

        let Some(()) = map.next_key_seed(Field::Kind)? else {
            return Err(serde::de::Error::missing_field("kind"));
        };

        let kind = map.next_value()?;

        let Some(()) = map.next_key_seed(Field::Parameters)? else {
            return Err(serde::de::Error::missing_field("parameters"));
        };

        let parameters = map.next_value_seed(CodecParametersSeed {
            import: &import,
            parameters_seen: VecSet::with_capacity(parameters.len()),
            parameters,
        })?;

        map.next_key_seed(Field::Excessive)?;

        Ok(Codec {
            import,
            kind,
            parameters,
        })
    }
}
