use std::{
    borrow::Cow,
    fmt,
    hash::{Hash, Hasher},
    ops::ControlFlow,
};

use nonempty::NonEmpty;

mod config;

#[derive(Debug, Clone)]
pub enum Parameter {
    IntValue { value: i64 },
    IntRange { min: i64, max: i64 },
    IntSet { values: NonEmpty<i64> },
    FloatValue { value: f64 },
    FloatSet { values: NonEmpty<f64> },
    StrValue { value: String },
    StrSet { values: NonEmpty<String> },
}

impl Parameter {
    #[must_use]
    pub fn cyclic_iter(&self) -> ParameterIterator {
        match self {
            Self::IntValue { value } => ParameterIterator::IntValue { value: *value },
            Self::IntRange { min, max } => ParameterIterator::IntRange {
                min: *min,
                max: *max,
                value: *min,
            },
            Self::IntSet { values } => ParameterIterator::IntSet { values, index: 0 },
            Self::FloatValue { value } => ParameterIterator::FloatValue { value: *value },
            Self::FloatSet { values } => ParameterIterator::FloatSet { values, index: 0 },
            Self::StrValue { value } => ParameterIterator::StrValue { value },
            Self::StrSet { values } => ParameterIterator::StrSet { values, index: 0 },
        }
    }

    pub fn minimise(&mut self) {
        match self {
            Self::IntValue { .. } | Self::FloatValue { .. } | Self::StrValue { .. } => (),
            Self::IntRange { min, .. } => *self = Self::IntValue { value: *min },
            Self::IntSet { values } => *self = Self::IntValue { value: values.head },
            Self::FloatSet { values } => *self = Self::FloatValue { value: values.head },
            Self::StrSet { values } => {
                *self = Self::StrValue {
                    value: values.head.clone(),
                }
            },
        }
    }
}

impl fmt::Display for Parameter {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::IntValue { value } => value.fmt(fmt),
            Self::IntRange { min, max } => fmt.write_fmt(format_args!("{min}..={max}")),
            Self::IntSet { values } => fmt.debug_set().entries(values.iter()).finish(),
            Self::FloatValue { value } => value.fmt(fmt),
            Self::FloatSet { values } => fmt.debug_set().entries(values.iter()).finish(),
            Self::StrValue { value } => fmt.write_fmt(format_args!("{value:?}")),
            Self::StrSet { values } => fmt.debug_set().entries(values.iter()).finish(),
        }
    }
}

pub enum ParameterIterator<'a> {
    IntValue {
        value: i64,
    },
    IntRange {
        min: i64,
        max: i64,
        value: i64,
    },
    IntSet {
        values: &'a NonEmpty<i64>,
        index: usize,
    },
    FloatValue {
        value: f64,
    },
    FloatSet {
        values: &'a NonEmpty<f64>,
        index: usize,
    },
    StrValue {
        value: &'a String,
    },
    StrSet {
        values: &'a NonEmpty<String>,
        index: usize,
    },
}

impl<'a> ParameterIterator<'a> {
    pub fn next(&mut self) -> ControlFlow<ConcreteParameter<'a>, ConcreteParameter<'a>> {
        match self {
            Self::IntValue { ref value } => {
                ControlFlow::Break(ConcreteParameter::Int { value: *value })
            },
            Self::IntRange {
                ref min,
                ref max,
                value,
            } => {
                let old_value = *value;
                if old_value < *max {
                    *value += 1;
                    ControlFlow::Continue(ConcreteParameter::Int { value: old_value })
                } else {
                    *value = *min;
                    ControlFlow::Break(ConcreteParameter::Int { value: old_value })
                }
            },
            Self::IntSet { values, index } => {
                let old_value = values.get(*index).copied().unwrap_or(values.head);
                if *index + 1 < values.len() {
                    *index += 1;
                    ControlFlow::Continue(ConcreteParameter::Int { value: old_value })
                } else {
                    *index = 0;
                    ControlFlow::Break(ConcreteParameter::Int { value: old_value })
                }
            },
            Self::FloatValue { ref value } => {
                ControlFlow::Break(ConcreteParameter::Float { value: *value })
            },
            Self::FloatSet { values, index } => {
                let old_value = values.get(*index).copied().unwrap_or(values.head);
                if *index + 1 < values.len() {
                    *index += 1;
                    ControlFlow::Continue(ConcreteParameter::Float { value: old_value })
                } else {
                    *index = 0;
                    ControlFlow::Break(ConcreteParameter::Float { value: old_value })
                }
            },
            Self::StrValue { value } => ControlFlow::Break(ConcreteParameter::Str { value }),
            Self::StrSet { values, index } => {
                let old_value = values.get(*index).unwrap_or(&values.head);
                if *index + 1 < values.len() {
                    *index += 1;
                    ControlFlow::Continue(ConcreteParameter::Str { value: old_value })
                } else {
                    *index = 0;
                    ControlFlow::Break(ConcreteParameter::Str { value: old_value })
                }
            },
        }
    }

    pub fn get(&self) -> ConcreteParameter<'a> {
        match self {
            Self::IntValue { value } | Self::IntRange { value, .. } => {
                ConcreteParameter::Int { value: *value }
            },
            Self::IntSet { values, index } => {
                let value = values.get(*index).copied().unwrap_or(values.head);
                ConcreteParameter::Int { value }
            },
            Self::FloatValue { value } => ConcreteParameter::Float { value: *value },
            Self::FloatSet { values, index } => {
                let value = values.get(*index).copied().unwrap_or(values.head);
                ConcreteParameter::Float { value }
            },
            Self::StrValue { value } => ConcreteParameter::Str { value },
            Self::StrSet { values, index } => {
                let value = values.get(*index).unwrap_or(&values.head);
                ConcreteParameter::Str { value }
            },
        }
    }
}

#[derive(Debug, Clone)]
pub enum ConcreteParameter<'a> {
    Int { value: i64 },
    Float { value: f64 },
    Str { value: &'a str },
}

impl<'a> ConcreteParameter<'a> {
    pub fn summary(&self) -> ConcreteParameterSummary<'a> {
        let inner = match self {
            Self::Int { value } => ConcreteParameterSummaryInner::Int {
                r#type: IntType::Int,
                value: *value,
            },
            Self::Float { value } => ConcreteParameterSummaryInner::Float {
                r#type: FloatType::Float,
                value: *value,
            },
            Self::Str { value } => ConcreteParameterSummaryInner::Str {
                r#type: StrType::Str,
                value: Cow::Borrowed(*value),
            },
        };

        ConcreteParameterSummary { inner }
    }
}

impl<'a> Hash for ConcreteParameter<'a> {
    fn hash<H: Hasher>(&self, state: &mut H) {
        std::mem::discriminant(self).hash(state);

        match self {
            Self::Int { value } => value.hash(state),
            Self::Float { value } => {
                if value.is_nan() {
                    if value.is_sign_negative() {
                        f64::NAN.to_bits().hash(state);
                    } else {
                        (-f64::NAN).to_bits().hash(state);
                    }
                } else {
                    value.to_bits().hash(state);
                }
            },
            Self::Str { value } => value.hash(state),
        }
    }
}

impl<'a> fmt::Display for ConcreteParameter<'a> {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::Int { value } => value.fmt(fmt),
            Self::Float { value } => value.fmt(fmt),
            Self::Str { value } => fmt.write_fmt(format_args!("{value:?}")),
        }
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "Parameter")]
#[serde(transparent)]
pub struct ConcreteParameterSummary<'a> {
    #[serde(borrow)]
    inner: ConcreteParameterSummaryInner<'a>,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "Parameter")]
#[serde(untagged)]
enum ConcreteParameterSummaryInner<'a> {
    Int {
        r#type: IntType,
        value: i64,
    },
    Float {
        r#type: FloatType,
        value: f64,
    },
    Str {
        r#type: StrType,
        #[serde(borrow)]
        value: Cow<'a, str>,
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
#[serde(rename = "Type")]
#[serde(rename_all = "lowercase")]
enum StrType {
    Str,
}
