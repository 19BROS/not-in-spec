"""OpenAPI 3.x adapter: load, resolve $refs, normalize."""

from notinspec.adapters.openapi.load import LoadedSpec, SpecLoadError, load_spec, load_spec_bytes
from notinspec.adapters.openapi.normalize import (
    NormalizedField,
    NormalizedOperation,
    NormalizedSpec,
    SecurityScheme,
    normalize,
)
from notinspec.adapters.openapi.refs import RefError, Resolved, Resolver

__all__ = [
    "LoadedSpec",
    "NormalizedField",
    "NormalizedOperation",
    "NormalizedSpec",
    "RefError",
    "Resolved",
    "Resolver",
    "SecurityScheme",
    "SpecLoadError",
    "load_spec",
    "load_spec_bytes",
    "normalize",
]
