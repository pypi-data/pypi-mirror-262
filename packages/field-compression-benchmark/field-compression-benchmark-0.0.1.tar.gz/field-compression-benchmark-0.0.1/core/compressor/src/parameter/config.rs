use std::fmt;

use nonempty::NonEmpty;
use vecmap::VecSet;

use super::Parameter;

impl<'de> serde::Deserialize<'de> for Parameter {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        serde::Deserializer::deserialize_struct(deserializer, "Parameter", FIELDS, Visitor)
    }
}

const FIELDS: &[&str] = &["type", "value", "values", "min", "max"];

struct TypeField;

impl<'de> serde::Deserialize<'de> for TypeField {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Visitor;

        impl<'de> serde::de::Visitor<'de> for Visitor {
            type Value = TypeField;

            fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
                formatter.write_str("a codec config type field identifier")
            }

            fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
                if value == "type" {
                    return Ok(TypeField);
                }
                Err(serde::de::Error::custom(format!(
                    "unexpected field `{value}`, a parameter must start with a `type` field"
                )))
            }

            fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
                if value == b"type" {
                    return Ok(TypeField);
                }
                let value = String::from_utf8_lossy(value);
                Err(serde::de::Error::custom(format!(
                    "unexpected field `{value}`, a parameter must start with a `type` field"
                )))
            }
        }

        serde::Deserializer::deserialize_identifier(deserializer, Visitor)
    }
}

#[derive(Clone, Copy)]
enum Field {
    Value,
    Values,
    Min,
    Max,
}

struct FieldSeed<const N: usize> {
    keys: &'static [&'static str; N],
    values: &'static [Field; N],
}

impl<const N: usize> FieldSeed<N> {
    fn with_deserialize_key<
        'de,
        A: serde::de::MapAccess<'de>,
        F: FnOnce(&mut A, Field) -> Result<Option<Q>, A::Error>,
        Q,
    >(
        self,
        map: &mut A,
        inner: F,
    ) -> Result<Q, A::Error> {
        let keys = self.keys.as_slice();

        let mode = if let Some(field) = map.next_key_seed(self)? {
            match inner(map, field) {
                Ok(Some(result)) => return Ok(result),
                Ok(None) => "expected",
                Err(err) => return Err(err),
            }
        } else {
            "missing"
        };

        match keys {
            [] => Err(serde::de::Error::custom(format!(
                "{mode} an impossible field"
            ))),
            [a] => Err(serde::de::Error::custom(format!("{mode} field `{a}`"))),
            [a, b] => Err(serde::de::Error::custom(format!(
                "{mode} field `{a}` or `{b}`"
            ))),
            [a @ .., b] => {
                let mut msg = String::from("expected ");
                msg.push_str(mode);
                msg.push(' ');
                for a in a {
                    msg.push('`');
                    msg.push_str(a);
                    msg.push_str("`, ");
                }
                msg.push_str("or `");
                msg.push_str(b);
                msg.push('`');
                Err(serde::de::Error::custom(msg))
            },
        }
    }
}

impl<'de, const N: usize> serde::de::DeserializeSeed<'de> for FieldSeed<N> {
    type Value = Field;

    fn deserialize<D: serde::Deserializer<'de>>(
        self,
        deserializer: D,
    ) -> Result<Self::Value, D::Error> {
        serde::Deserializer::deserialize_identifier(deserializer, self)
    }
}

impl<'de, const N: usize> serde::de::Visitor<'de> for FieldSeed<N> {
    type Value = Field;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a codec config field identifier")
    }

    fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
        if let Some(field) = self
            .keys
            .iter()
            .position(|key| value == *key)
            .and_then(|index| self.values.get(index))
        {
            return Ok(*field);
        }

        Err(serde::de::Error::unknown_field(value, self.keys))
    }

    fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
        if let Some(field) = self
            .keys
            .iter()
            .position(|key| value == key.as_bytes())
            .and_then(|index| self.values.get(index))
        {
            return Ok(*field);
        }

        let value = String::from_utf8_lossy(value);
        Err(serde::de::Error::unknown_field(&value, self.keys))
    }
}

#[derive(serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "lowercase")]
enum Type {
    Int,
    Float,
    Str,
}

struct Visitor;

impl<'de> serde::de::Visitor<'de> for Visitor {
    type Value = Parameter;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a codec parameter")
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let Some(TypeField) = map.next_key()? else {
            return Err(serde::de::Error::custom("expected field `type`"));
        };
        let r#type: Type = map.next_value()?;

        let parameter = match r#type {
            Type::Int => FieldSeed {
                keys: &["value", "values", "min"],
                values: &[Field::Value, Field::Values, Field::Min],
            }
            .with_deserialize_key(&mut map, |map, field| match field {
                Field::Value => Ok(Some(Parameter::IntValue {
                    value: map.next_value()?,
                })),
                Field::Values => {
                    let values: VecSet<i64> = map.next_value()?;
                    match NonEmpty::collect(values.into_iter()) {
                        Some(values) => Ok(Some(Parameter::IntSet { values })),
                        None => Err(serde::de::Error::custom("empty int parameter values range")),
                    }
                },
                Field::Min => {
                    let range_min: i64 = map.next_value()?;
                    FieldSeed {
                        keys: &["max"],
                        values: &[Field::Max],
                    }
                    .with_deserialize_key(map, |_, _| Ok(Some(())))?;
                    let range_max: i64 = map.next_value()?;
                    if range_max >= range_min {
                        Ok(Some(Parameter::IntRange {
                            min: range_min,
                            max: range_max,
                        }))
                    } else {
                        Err(serde::de::Error::custom(
                            "empty int parameter min..=max range",
                        ))
                    }
                },
                Field::Max => Ok(None),
            }),
            Type::Float => FieldSeed {
                keys: &["value", "values"],
                values: &[Field::Value, Field::Values],
            }
            .with_deserialize_key(&mut map, |map, field| match field {
                Field::Value => Ok(Some(Parameter::FloatValue {
                    value: map.next_value()?,
                })),
                Field::Values => {
                    let values: VecSet<F64> = map.next_value()?;
                    match NonEmpty::collect(values.into_iter().map(|f| f.0)) {
                        Some(values) => Ok(Some(Parameter::FloatSet { values })),
                        None => Err(serde::de::Error::custom(
                            "empty float parameter values range",
                        )),
                    }
                },
                _ => Ok(None),
            }),
            Type::Str => FieldSeed {
                keys: &["value", "values"],
                values: &[Field::Value, Field::Values],
            }
            .with_deserialize_key(&mut map, |map, field| match field {
                Field::Value => Ok(Some(Parameter::StrValue {
                    value: map.next_value()?,
                })),
                Field::Values => {
                    let values: VecSet<String> = map.next_value()?;
                    match NonEmpty::collect(values.into_iter()) {
                        Some(values) => Ok(Some(Parameter::StrSet { values })),
                        None => Err(serde::de::Error::custom("empty str parameter values range")),
                    }
                },
                _ => Ok(None),
            }),
        }?;

        map.next_key_seed(FieldSeed {
            keys: &[],
            values: &[],
        })?;

        Ok(parameter)
    }
}

#[derive(serde::Deserialize)]
#[repr(transparent)]
struct F64(f64);

impl PartialEq for F64 {
    fn eq(&self, other: &Self) -> bool {
        match self.0.total_cmp(&other.0) {
            std::cmp::Ordering::Equal => true,
            std::cmp::Ordering::Less | std::cmp::Ordering::Greater => false,
        }
    }
}

impl Eq for F64 {}
