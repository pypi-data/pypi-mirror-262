__all__ = ["benchmark", "codecs", "compressor", "dataset", "model", "plot"]

import sys as _sys

# fix-up submodule imports for the _fcbench extension module
from . import _fcbench

for _module in _fcbench.__all__:
    _sys.modules[f"fcbench._fcbench.{_module}"] = getattr(_fcbench, _module)

from . import benchmark, codecs, compressor, dataset, model, plot  # noqa: E402

# polyfill for fcpy imports
_sys.modules["fcpy"] = _sys.modules[__name__]
