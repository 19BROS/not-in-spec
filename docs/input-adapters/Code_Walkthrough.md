# Input adapters: code walkthrough

What [load.py](../../core/src/notinspec/adapters/openapi/load.py), [refs.py](../../core/src/notinspec/adapters/openapi/refs.py) and [normalize.py](../../core/src/notinspec/adapters/openapi/normalize.py) do, in detail. Companion to [Input_Adapters_Role_Guide.md](Input_Adapters_Role_Guide.md) §6.

The three files form a small pipeline. Each one does one job and hands its result to the next:

```
spec file (bytes) ──► load.py ──► dict ──► normalize.py ──► NormalizedSpec (flat "cards")
                                              │
                                              └── uses refs.py to follow every $ref
```

- **load.py** turns a file into a Python dict and checks that it is valid OpenAPI.
- **refs.py** follows `$ref` cross-references inside that dict.
- **normalize.py** walks the dict and writes each endpoint as one flat, complete card.

All three are pure functions: no network, no database, no clock. The same file always gives the same result.

---

## 1. load.py: read and check the file

**Input:** a file path, or raw bytes (later, `git show` will give bytes for old versions).
**Output:** a `LoadedSpec`:

```python
LoadedSpec(
    document={...},  # the whole spec as a dict
    openapi_version="3.1.0",
    problems=("#/paths/~1v1~1charges~1{id}/get/parameters/0: 'required' is a required property",),
    problem_count=1,
)
```

### Step by step

**1. Pick a parser (`parse_spec`)**

- `.json` files go to `orjson` (very fast).
- `.yaml` / `.yml` files go to PyYAML with its C library (`libyaml`), which is about 10× faster than pure Python. That matters for GitHub's multi-MB file.
- A file with no known suffix is treated as JSON if it starts with `{`, otherwise as YAML.

**2. Fix YAML's surprises (the `_Loader` class)**

PyYAML follows the old YAML 1.1 rules, which silently change values:

| In the file | Plain PyYAML gives | Our loader gives |
|---|---|---|
| `example: 2024-01-01` | a `date` object | `"2024-01-01"` |
| `enum: [on, off]` | `[True, False]` | `["on", "off"]` |
| `yes` / `no` | `True` / `False` | `"yes"` / `"no"` |
| `true` / `false` | booleans | booleans (unchanged) |

Without this, an enum value `"on"` would turn into `True`, and a claim would say the API accepts `True`. That would be a wrong fact.

**3. Make every key a string (`_stringify_keys`)**

In YAML, `200:` under `responses` is read as the number `200`. JSON and OpenAPI only have string keys, so it becomes `"200"`. After this, a YAML spec and the same spec in JSON give identical dicts (a test checks this).

**4. Reject files that can't be used (`SpecLoadError`)**

The loader stops with an error only when the file is unusable:

- it doesn't parse;
- the top level isn't a mapping;
- it's Swagger 2.0;
- the `openapi` version isn't 3.0, 3.1 or 3.2.

**5. Validate, but never fail (`validate_spec`)**

- `openapi-spec-validator` checks the dict against the official OpenAPI schema.
- Every problem becomes one line, `pointer: message`, and the list is sorted.
- Problems don't stop anything. Real specs often break small rules (the Acme fixture has a path parameter without `required: true`, which is very common).
- The validator itself sometimes **crashes** on broken input (e.g. `KeyError: 'in'` on a parameter without `in`). The crash is caught and recorded as a problem too.
- Only the first 100 problem lines are kept, but `problem_count` counts all of them.
- `validate=False` skips this step, because validating GitHub's huge file is slow.

---

## 2. refs.py: follow cross-references

OpenAPI files avoid repetition with `$ref`:

```yaml
schema: { $ref: '#/components/schemas/ChargeCreate' }
```

This means "the real content is over there". The part after `#` is a **JSON pointer**: a path through the dict, with `/` between the steps.

### JSON pointer escaping (`escape`, `unescape`, `join`)

Keys can contain `/` themselves (every API path does), so they are escaped: `/` becomes `~1` and `~` becomes `~0`.

```python
join("#/paths", "/v1/charges", "post")  # → "#/paths/~1v1~1charges/post"
```

These pointers are what end up in a claim's `source`, so a report can link to the exact place in the spec.

### `Resolver.lookup(ref)`: find what a pointer points to

It walks the dict one token at a time. `#/components/schemas/ChargeCreate` means `doc["components"]["schemas"]["ChargeCreate"]`. It also handles list indexes (`/parameters/0`) and percent-encoding (`%7E`). It raises `RefError` when:

- the target doesn't exist;
- the ref points to another file (`other.yaml#/...`), which isn't supported because the MVP targets are single self-contained files;
- the text isn't a valid pointer.

### `Resolver.resolve(node, pointer)`: follow the whole chain

A ref can point to another ref (`A → B → real schema`). `resolve` keeps following until it reaches real content, and returns three things:

```python
Resolved(
    node={"type": "string"},  # the real content
    pointer="#/components/schemas/B",  # where it is defined → becomes `source`
    refs=("#/components/schemas/A", "#/components/schemas/B"),  # the path taken
)
```

If a chain loops back on itself (`LoopA → LoopB → LoopA`), it raises `RefError("$ref cycle: ...")` instead of looping forever.

`refs` (the path taken) is what lets normalize.py detect **recursive schemas** further up, as described below.

---

## 3. normalize.py: one flat card per endpoint

**Input:** the dict from load.py.
**Output:** a `NormalizedSpec`, built from four frozen (unchangeable) dataclasses:

```
NormalizedSpec
├── operations: NormalizedOperation[]   ← one card per endpoint
│     ├── method, path, operation_id, summary, description, tags, deprecated
│     ├── parameters: NormalizedField[]  (path / query / header / cookie)
│     ├── body_media_type, body_required
│     ├── body_fields: NormalizedField[]
│     └── security
├── security_schemes: SecurityScheme[]
└── problems: str[]
```

A `NormalizedField` is one parameter or one body field: `location`, `name`, `type`, `required`, `enum`, `deprecated`, `description`, `example`, `source`.

These are internal working types, not the shared `Claim` / `Snippet` contract. That contract still has to be agreed in `model.py`. The next step (claims and snippets) will read these cards.

Most of the work happens inside the `_Normalizer` class. Here is what it does for each endpoint.

### a) Find the endpoints (`path_items`, `run`)

- Goes through every `paths.<path>.<method>`, for the 8 HTTP methods.
- Skips vendor extensions (`x-...`).
- Records a path that doesn't start with `/` as a problem.
- Follows the path item through `refs.py` if it is itself a `$ref`.

### b) Parameters (`parameters`, `operation`)

- **Merges** the parameters defined on the path with those on the operation. When both define the same `name` + `in`, the operation's version wins. Header names are compared case-insensitively (`Idempotency-Key` = `idempotency-key`), because HTTP headers work that way.
- A parameter that is a `$ref` (like `#/components/parameters/Expand`) is followed, and its `source` is where it is defined.
- **Path parameters are always required**, even if the spec forgets to say so.
- The type comes from `schema`, or from `content` when the spec uses that instead.
- A parameter without a valid `name` / `in` is skipped and recorded as a problem.
- The result is sorted by location (path → query → header → cookie), then by name.

### c) Request body (`request_body`)

- Picks the **first media type from the configured list** that the endpoint offers. The default list is `application/json`, then `application/x-www-form-urlencoded` (Stripe).
- Ignores extras like `; charset=utf-8` when matching.
- A body only in another type (e.g. `multipart/form-data`) gives `body_media_type=None` and no fields. You can change the list with `normalize(doc, body_media_types=[...])`.

### d) Flatten the body schema into fields (`properties`, `body_fields`)

This is the hardest part. A body schema can be built from pieces, and the rules are:

| Construct | Rule |
|---|---|
| `properties` | each property becomes a field |
| `required: [...]` | marks those fields as required |
| `allOf` (all parts apply) | properties from all parts are merged; a field required in **any** part is required |
| `oneOf` / `anyOf` (one of the variants) | fields from all branches are collected; a field is required **only if it is required in every branch** |
| `readOnly: true` | skipped (it only appears in responses) |
| nested object | goes one level deeper with a dotted name (`shipping.address`), at most **2 levels** |
| array | not descended into |

From the composition fixture: `method` is a `oneOf` of `Card {number, exp}` and `Bank {number, iban}`.

- `method.number` is required, because both branches require it.
- `method.exp` and `method.iban` are not, because only one branch requires each.

**Nested required:** a nested field is only required if its parent is too. `shipping.address` is required *inside* `shipping`, but `shipping` itself is optional, so `shipping.address` is not required for the request.

**Recursive schemas:** `Node` has a `parent` field that is again a `Node`. Each step carries a `stack` of the refs already followed. When a ref appears that is already on the stack, the walk stops, so it doesn't descend forever. `parent` is listed as a field, but nothing inside it is.

### e) Type, enum, docs of one field (`schema_info`)

- **type:**
  - from `type`; in 3.1 that can be a list, and `"null"` is dropped;
  - otherwise guessed from shape (`properties` → `object`, `items` → `array`);
  - otherwise collected from `oneOf` / `anyOf` / `allOf` branches.
  - Several types are joined in sorted order: `"integer|string"`.
- **enum:**
  - from `enum`, or `const` (a single value);
  - across branches, an enum is kept only if **every** branch has one. The `mode` field is `anyOf: [enum fast/slow, any string]`, so any string is allowed and it is not an enum.
  - `True` and `1` are kept as different values (Python normally treats them as equal).
- **description:** in 3.1 a description can sit next to a `$ref`. That one describes this specific use, so it wins over the shared one.
- **example:** from `example`, or the first item of `examples`.

### f) Security (`security`, `security_schemes`)

- **Effective security:** the operation's own `security` if it has one, otherwise the global one.
- The result is a list of alternatives:
  - `(("apiKey",), ("bearerAuth",))` means api key **or** bearer;
  - `()` means no auth (`security: []`);
  - `((),)` means auth is optional.
- Security schemes are read from `components.securitySchemes`: type, HTTP scheme (`bearer`, lowercased) and, for API keys, where the key goes and its name.
- A reference to a scheme that doesn't exist is recorded as a problem.

### g) Problems and determinism

- Anything broken (missing ref, ref cycle, nameless parameter, unknown scheme, wrong structure) is **skipped and recorded** in `problems` as `pointer: message`. One bad endpoint never stops the rest of the spec.
- The output is fully sorted: operations by path then method, fields by name, problems alphabetically. Key order in the source file doesn't matter, and a test checks this by reversing the dict and comparing bytes.
- [canonical.py](../../core/src/notinspec/adapters/canonical.py) serializes the result with sorted keys. That gives byte-identical golden files and a stable `content_hash`, which `SpecVersion.content_hash` will use later.

---

## Where this leads

The next step reads these cards and produces claims. For example, the `amount` field becomes:

- `param-name`: `acme/hard/param-name/POST-/v1/charges/body/amount`
- `required-field`: `acme/hard/required-field/POST-/v1/charges/body/amount`

Both have `source = #/components/schemas/ChargeCreate/properties/amount`. Snippets will be rendered from the same cards.
