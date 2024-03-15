use std::borrow::Cow;

use nonempty::NonEmpty;
use serde::Deserialize;
use sorted_vec::SortedSet;

mod config;

pub(super) use config::DataDerivativeFormulaSetSeed;

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Deserialize)]
#[serde(untagged)]
pub enum DataDerivative {
    Differentiate { differentiate: String },
    Integrate { integrate: String },
}

impl DataDerivative {
    #[must_use]
    pub fn summary(&self) -> DataDerivativeSummary {
        let inner = match self {
            Self::Differentiate { differentiate } => DataDerivativeSummaryInner::Differentiate {
                differentiate: Cow::Borrowed(differentiate.as_str()),
            },
            Self::Integrate { integrate } => DataDerivativeSummaryInner::Integrate {
                integrate: Cow::Borrowed(integrate.as_str()),
            },
        };

        DataDerivativeSummary { inner }
    }
}

#[derive(
    Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize,
)]
#[serde(transparent)]
pub struct DataDerivativeSummary<'a> {
    #[serde(borrow)]
    inner: DataDerivativeSummaryInner<'a>,
}

#[derive(
    Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize,
)]
#[serde(untagged)]
enum DataDerivativeSummaryInner<'a> {
    Differentiate {
        #[serde(borrow)]
        differentiate: Cow<'a, str>,
    },
    Integrate {
        #[serde(borrow)]
        integrate: Cow<'a, str>,
    },
}

pub(super) fn serialize<S: serde::Serializer>(
    derivatives: &SortedSet<NonEmpty<DataDerivativeSummary>>,
    serializer: S,
) -> Result<S::Ok, S::Error> {
    serde::Serializer::collect_seq(serializer, derivatives.iter())
}

pub(super) fn deserialize<'de, D: serde::Deserializer<'de>>(
    deserializer: D,
) -> Result<SortedSet<NonEmpty<DataDerivativeSummary<'de>>>, D::Error> {
    let vec = Vec::deserialize(deserializer)?;
    Ok(SortedSet::from_unsorted(vec))
}
