"""Download the pinned model once, and measure scoring speed where it runs (SPEC §12)."""

import sys
import time
from dataclasses import dataclass
from pathlib import Path

from notinspec.nli.local import MODEL_ID, REVISION, NliUnavailable, TransformersNli
from notinspec.nli.scores import NliModel

# What the model needs from the repo; it also holds pytorch_model.bin and ONNX exports (~3 GB).
FILES = (
    "added_tokens.json",
    "config.json",
    "model.safetensors",
    "special_tokens_map.json",
    "spm.model",
    "tokenizer.json",
    "tokenizer_config.json",
)

# Realistic pairs: urllib3 NLI premises (breadcrumb + cited block) and claims, labelled by hand in
# experiments/nli (run 007): 3 x entailment, neutral, contradiction, in that order.
SAMPLE: tuple[tuple[str, str], ...] = (
    (
        "urllib3 > Changelog > 2.8.0 (2026-09-15) > Bugfixes:\n\nFixed HTTPSConnection.connect() "
        "overriding ProxyConfig.ssl_context's certificate policy and proxy identity checks with "
        "the target connection's TLS settings when forwarding through an HTTPS proxy. "
        "HTTPSConnection no longer applies target SNI, assertions, or client credentials to "
        "forwarding proxy handshakes and continues to use its ssl_context as a fallback when an "
        "HTTPS proxy forwards an HTTP target.",
        "HTTPSConnection continues to use its ssl_context as a fallback when an HTTPS proxy "
        "forwards an HTTP target.",
    ),
    (
        "urllib3 > User Guide > Retrying Requests:\n\nTo disable redirects but keep the retrying "
        "logic, specify redirect=False:",
        "Specifying redirect=False disables redirects while keeping the retrying logic in urllib3.",
    ),
    (
        "urllib3 > User Guide > Retrying Requests > Configuring Exponential Backoff:\n\nseconds, "
        "with no delay before the second attempt (the first retry) because most transient errors "
        "resolve immediately. For example, a backoff_factor of 0.5 yields retry sleeps of 0.0s, "
        "1.0s, 2.0s, etc., up to backoff_max:",
        "urllib3's Retry applies no delay before the second attempt (the first retry).",
    ),
    (
        "urllib3 > Changelog > 2.8.0 (2026-09-15) > Security:\n\nFixed the following security "
        "issues:\n\nThe TLS configuration for HTTPS proxies could be ignored or overridden. (High "
        "severity, GHSA-8988-9cw3-xx77)",
        "Passing `ssl_context` instead of `proxy_ssl_context` for HTTPS proxies when "
        "`use_forwarding_for_https=True` in urllib3 will raise an error in v3.0.",
    ),
    (
        "urllib3 > Changelog > 2.8.0 (2026-09-15) > Security:\n\nFixed the following security "
        "issues:",
        "In urllib3 2.8.0, urllib3.contrib.pyopenssl was fixed to use cryptography APIs when "
        "reading a certificate subject and loading encrypted private keys.",
    ),
    (
        "urllib3 > User Guide > Retrying Requests:\n\nurllib3 can automatically retry idempotent "
        "requests. This same mechanism also handles redirects.",
        "Setting a non-zero backoff_factor in urllib3's Retry introduces exponential delays "
        "between retries when no server-requested delay is applied.",
    ),
    (
        "urllib3 > User Guide > Retrying Requests:\n\nYou can control the retries using the "
        "retries parameter to request(). By default, urllib3 will retry requests 3 times and "
        "follow up to 3 redirects.",
        "By default, urllib3 follows up to 10 redirects.",
    ),
    (
        "urllib3 > User Guide > Using Timeouts:\n\nTimeouts allow you to control how long (in "
        "seconds) requests are allowed to run before being aborted. In simple cases, you can "
        "specify a timeout as a float to request():",
        "Timeouts in urllib3 are specified in milliseconds.",
    ),
    (
        "urllib3 > User Guide > Retrying Requests:\n\nurllib3 can automatically retry idempotent "
        "requests. This same mechanism also handles redirects.",
        "urllib3 never retries idempotent requests automatically.",
    ),
)


def fetch(model_id: str = MODEL_ID, revision: str = REVISION) -> Path:
    """Puts the pinned weights into the Hugging Face cache (HF_HOME). Offline if already there."""
    try:
        from huggingface_hub import constants, snapshot_download
        from huggingface_hub.errors import LocalEntryNotFoundError
    except ImportError as e:
        raise NliUnavailable("NLI needs the optional dependencies: notinspec[nli]") from e
    # the same allow_patterns in both calls: without them the cached snapshot counts as
    # incomplete, because the repo also has files we never download
    want = {"repo_id": model_id, "revision": revision, "allow_patterns": list(FILES)}
    try:
        path = Path(snapshot_download(**want, local_files_only=True))
        if all((path / f).is_file() for f in FILES):
            return path
    except LocalEntryNotFoundError:
        pass
    if constants.HF_HUB_OFFLINE:
        raise NliUnavailable(f"{model_id} is not cached and HF_HUB_OFFLINE is set; unset it")
    return Path(snapshot_download(**want))


@dataclass(frozen=True)
class Bench:
    pairs: int
    load_seconds: float
    seconds: float

    @property
    def pairs_per_second(self) -> float:
        return self.pairs / self.seconds if self.seconds else 0.0


def bench(model: NliModel, pairs: int = 64) -> Bench:
    """Times loading and scoring `pairs` pairs (SAMPLE repeated). One claim = one pair."""
    start = time.perf_counter()
    if isinstance(model, TransformersNli):
        model.load()
    loaded = time.perf_counter()
    sample = [SAMPLE[i % len(SAMPLE)] for i in range(pairs)]
    model.score(sample)
    return Bench(pairs, loaded - start, time.perf_counter() - loaded)


def torch_threads() -> int | None:
    torch = sys.modules.get("torch")
    return int(torch.get_num_threads()) if torch else None
