# Výstupný kontrakt vstupných adaptérov

28. 10. 2026 · @RadoMuntag · **návrh na odsúhlasenie** (roly 1, 3, 4, 5)

Tento dokument vysvetľuje, aké dáta odovzdáva rola 2 (vstupné adaptéry) ostatným rolám: aké objekty existujú, čo znamená každé pole a kto ho na čo používa. Podrobný technický popis je v [Input_Adapters_Role_Guide.md](Input_Adapters_Role_Guide.md) §4. Ak sa tieto dokumenty líšia, platí SPEC, potom guide.

Príklady používajú vymyslené API **Acme Payments**, rovnako ako FAQ.

## 1. Čo je kontrakt a prečo ho treba dohodnúť teraz

Kontrakt je **dohodnutý tvar dát**, ktoré adaptéry odovzdávajú zvyšku systému. Hovorí, aké objekty existujú, aké majú polia a čo jednotlivé polia znamenajú.

Všetky roly začínajú programovať naraz. Keď sa tvar dohodne na začiatku, každý môže písať kód proti nemu, aj keď adaptéry ešte nie sú hotové. Keď sa nedohodne, každý si tvar tipne inak a pri spájaní sa veci rozbijú. Guide (§14) to uvádza ako najväčšie riziko roadmapy.

**Stav:** kontrakt ešte nie je v kóde. Bude v `core/src/notinspec/model.py` ako Pydantic v2 modely. Najprv ho potrebujeme odsúhlasiť (pozri §7), potom príde malý PR iba s `model.py`.

Pravidlá pre všetky objekty:

- sú **frozen**: po vytvorení sa nedajú zmeniť;
- ukladajú sa ako **kanonický JSON** (zoradené kľúče, pevné oddeľovače), aby sa dali hashovať a porovnávať;
- rovnaký vstup dá vždy rovnaký výstup, bajt po bajte;
- každá zmena kontraktu ide cez vedúceho.

## 2. Kontrakt vs. interné dáta adaptérov

Adaptéry už majú hotové načítanie a normalizáciu špecifikácie (vetva `core/openapi-loader`). Tie vyrábajú **interné „karty“** endpointov (`NormalizedSpec`, `NormalizedOperation`, `NormalizedField`). Tie nie sú súčasťou kontraktu a nemáte na ne stavať.

| | Interné karty (hotové) | Kontrakt (na odsúhlasenie) |
|---|---|---|
| Kde | `adapters/openapi/normalize.py` | `model.py` |
| Typy | `NormalizedSpec`, `NormalizedOperation`, `NormalizedField` | `SpecVersion`, `Operation`, `Claim`, `Snippet` |
| Kto ich používa | iba rola 2 | všetky roly |
| Môžu sa meniť bez dohody? | áno | nie, iba cez vedúceho |

Z kariet sa vyrábajú objekty kontraktu. Viac o kartách je v [Code_Walkthrough.md](Code_Walkthrough.md).

## 3. Štyri objekty

### 3.1 `SpecVersion`: jedna verzia špecifikácie z histórie

```python
class SpecVersion(BaseModel):
    target: str  # "acme"
    version: str  # "2025-03": mesiac, alebo release tag
    commit: str  # git commit SHA, z ktorého verzia pochádza
    committed_at: datetime
    files: list[str]  # cesty k súborom špecifikácie v danom commite
    content_hash: str  # sha256 normalizovaného obsahu
```

- **Na čo:** rola 5 ho ukladá do databázy. Každý výsledok testu sa naň odvoláva („model odpovedal proti verzii 2025-03“).
- **Ako vzniká:** adaptéry z git histórie vyberú jednu verziu za mesiac (alebo podľa release tagov), od pevného prvého mesiaca.
- **`content_hash`:** keď niekto špecifikáciu iba preformátuje, hash normalizovaného obsahu sa nezmení a nová verzia nevznikne.

### 3.2 `Operation`: ktorý endpoint

```python
class Operation(BaseModel):
    method: str  # "POST"
    path: str  # "/v1/charges"
    operation_id: str | None
    tags: list[str]
    deprecated: bool
```

Iba identifikácia endpointu vo vnútri tvrdenia. Ostatné roly nepotrebujú všetky parametre endpointu, len vedieť, o ktorý ide.

### 3.3 `Claim` (tvrdenie): jeden overiteľný fakt

Toto je **jadro kontraktu**. Jedno tvrdenie = jeden fakt zo špecifikácie, ktorý môže model pomýliť. Z každého vybraného tvrdenia generátor (rola 1) vyrobí jednu testovaciu úlohu.

```python
class Claim(BaseModel):
    id: str  # stabilné, pozri §4
    target: str
    layer: Literal["hard"]
    type: Literal[
        "endpoint-exists",
        "param-name",
        "required-field",
        "enum-value",
        "auth-scheme",
        "removed",
        "renamed",
    ]
    verify: Literal["execute-against-mock"]
    operation: Operation | None  # None iba pri auth-scheme
    location: Literal["path", "query", "header", "body"] | None
    name: str | None  # názov poľa / parametra; pri auth-scheme názov schémy
    old_name: str | None  # iba pri renamed
    value_type: str | None  # "integer", "string", ...
    enum_values: list[str | int | float | bool] | None
    example: Any | None  # príkladová hodnota zo špecifikácie
    slice_key: str | None  # tag slice, v ktorom je endpoint
    since_version: str | None  # pri removed / renamed: verzia zmeny
    fact: str  # čitateľná veta pre reporty
    source: str  # JSON pointer do špecifikácie
    spec_version: str
```

#### Typy tvrdení (SPEC §2.2)

| Typ | Fakt | Model musí… |
|---|---|---|
| `endpoint-exists` | endpoint existuje | použiť správnu metódu + cestu |
| `param-name` | parameter / pole má tento názov a umiestnenie | použiť správny názov na správnom mieste |
| `required-field` | pole tela je povinné | povinné pole poslať |
| `enum-value` | pole má len určité povolené hodnoty | použiť platnú hodnotu |
| `auth-scheme` | spôsob prihlásenia | autentifikovať sa správne |
| `removed` | niečo bolo odstránené | to **nepoužiť** |
| `renamed` | niečo bolo premenované | použiť nový názov, nie starý |

Prvých päť typov vzniká z aktuálnej špecifikácie. `removed` a `renamed` vznikajú porovnaním po sebe idúcich verzií nástrojom oasdiff.

#### Polia po skupinách

**Identita**

- `id`: stabilný kľúč, pozri §4.
- `target`: ktoré API.
- `layer`: vždy `"hard"`. MVP používa iba tvrdú vrstvu a vrstvy sa nikdy nepriemerujú.
- `type`: jeden zo 7 typov vyššie.

**Ako sa overuje**

- `verify`: vždy `"execute-against-mock"`: požiadavka modelu sa pošle na Prism, ktorý beží nad špecifikáciou. Zadanie projektu vyžaduje, aby každé tvrdenie nieslo svoj spôsob overenia.

**O čom fakt hovorí**

- `operation`: ktorý endpoint. Pri `auth-scheme` je `None`, lebo prihlásenie platí pre celé API. Inak by jedna schéma vytvorila tisíce rovnakých tvrdení.
- `location`: `path` / `query` / `header` / `body`.
- `name`: názov parametra alebo poľa. Vnorené polia tela majú názov s bodkou (`shipping.address`), najviac 2 úrovne.
- `old_name`: iba pri `renamed`, starý názov.
- `value_type`: typ hodnoty. Ak pole povoľuje viac typov, sú spojené a zoradené: `"integer|string"`.
- `enum_values`: povolené hodnoty. Môžu byť aj čísla a booleany, nielen reťazce.
- `example`: príkladová hodnota zo špecifikácie, ak existuje. Generátor ju môže použiť v zadaní úlohy („vytvor platbu na 1000 centov“).

**Pre režimy s kontextom**

- `slice_key`: v ktorom tag slice je endpoint. V režime `full-sliced` model dostane práve tento slice. Pri `auth-scheme` je `None`.

**História**

- `since_version`: pri `removed` / `renamed` verzia, v ktorej zmena nastala. Report potom vie povedať „`customer_id` neplatí od 2025-03“.

**Pre ľudí a dohľadanie**

- `fact`: čitateľná veta do reportov, vždy generovaná z pevnej šablóny, nikdy nie ručne písaná.
- `source`: JSON pointer na miesto, kde je fakt v špecifikácii definovaný, napr. `#/components/schemas/ChargeCreate/properties/amount`.
- `spec_version`: verzia, z ktorej fakt pochádza.

#### Príklady

`required-field`: „`POST /v1/charges` vyžaduje `amount`“:

```json
{
  "id": "acme/hard/required-field/POST-/v1/charges/body/amount",
  "target": "acme",
  "layer": "hard",
  "type": "required-field",
  "verify": "execute-against-mock",
  "operation": {
    "method": "POST",
    "path": "/v1/charges",
    "operation_id": "createCharge",
    "tags": ["Charges"],
    "deprecated": false
  },
  "location": "body",
  "name": "amount",
  "old_name": null,
  "value_type": "integer",
  "enum_values": null,
  "example": 1000,
  "slice_key": "Charges",
  "since_version": null,
  "fact": "POST /v1/charges requires the body field `amount` (integer)",
  "source": "#/components/schemas/ChargeCreate/properties/amount",
  "spec_version": "2025-03"
}
```

`renamed`: „`customer_id` sa v 2025-03 premenoval na `customer`“ (iba polia, ktoré sa líšia):

```json
{
  "id": "acme/hard/renamed/POST-/v1/charges/body/customer",
  "type": "renamed",
  "location": "body",
  "name": "customer",
  "old_name": "customer_id",
  "since_version": "2025-03",
  "fact": "POST /v1/charges: body field `customer_id` was renamed to `customer` in 2025-03"
}
```

`auth-scheme`: „API používa bearer token“:

```json
{
  "id": "acme/hard/auth-scheme/bearerAuth",
  "type": "auth-scheme",
  "operation": null,
  "location": null,
  "name": "bearerAuth",
  "slice_key": null,
  "fact": "The API authenticates with a bearer token (scheme `bearerAuth`)"
}
```

Presné znenie viet `fact` je zatiaľ ilustračné. Šablóny viet budú v kóde.

### 3.4 `Snippet`: kus dokumentácie pre model

```python
class Snippet(BaseModel):
    id: str
    target: str
    kind: Literal["operation", "tag"]
    key: str  # "POST /v1/charges" alebo názov tagu "Charges"
    text: str  # vyrenderovaný, deterministický
    size_bytes: int
```

- `kind="operation"`: jeden endpoint ako kompaktný text (metóda, cesta, popis, parametre, polia tela, autentifikácia). V nich hľadá BM25 v režime `snippet` (rola 4).
- `kind="tag"`: slice, teda všetky endpointy jedného tagu, pre režim `full-sliced`. Endpoint bez tagu patrí do slice podľa prvého segmentu cesty (`/v1/charges/...` → `charges`).
- `size_bytes`: aby reporty vedeli ukázať, koľko textu model dostal.
- Rovnaká špecifikácia dá vždy bajtovo rovnaké snippety.

Príklad textu snippetu:

```
POST /v1/charges  (tag: Charges)
Create a charge.
Auth: bearer token
Header: Idempotency-Key (string, optional)
Body:
  amount    integer, required — amount in the smallest currency unit
  currency  string,  required
  customer  string
  capture   string, one of: automatic, manual
```

Formát `Snippet.id` ešte nie je definovaný (pozri §7).

## 4. ID tvrdení

ID musí byť **rovnaké každý týždeň**, kým sa fakt nezmení. Na ID stojí výber ~100 tvrdení (sampler), porovnanie behov aj celá história výsledkov. Keby sa ID zmenilo, tvrdenie by vyzeralo ako nové a stratila by sa jeho história.

Tvar podľa typu:

```
{target}/hard/{type}/{METHOD}-{path}                     endpoint-exists, removed (endpoint)
{target}/hard/{type}/{METHOD}-{path}/{location}/{name}   param-name, required-field, enum-value,
                                                         removed (pole), renamed (nový názov)
{target}/hard/auth-scheme/{scheme}                       auth-scheme
```

Príklady:

```
acme/hard/endpoint-exists/POST-/v1/charges
acme/hard/required-field/POST-/v1/charges/body/amount
acme/hard/renamed/POST-/v1/charges/body/customer
acme/hard/removed/DELETE-/v1/charges/{}
acme/hard/auth-scheme/bearerAuth
```

Pravidlá:

- **Žiadna verzia v ID.** Ten istý fakt vo verziách 2024-11 až 2025-10 má jedno ID.
- **Umiestnenie je v ID.** `limit` ako query parameter a `limit` v tele sú dva rôzne fakty.
- **Názvy zástupných parametrov v ceste sa vymažú** (`/v1/charges/{id}` → `/v1/charges/{}`). Keď špecifikácia premenuje `{id}` na `{charge}`, API sa nezmenilo, takže ani ID sa nesmie zmeniť.
- **ID sa nerozkladá na časti.** Cesta obsahuje `/`, takže ID sa nedá spoľahlivo rozdeliť späť. Kto potrebuje názov poľa alebo cestu, číta polia `name` a `operation`.
- **Opakovaná zmena:** ak sa pole odstráni, znova pridá a znova odstráni, ostane jedno tvrdenie `removed` s najnovšou `since_version`.

Pozor: príklad ID vo FAQ §2 je starší a nemá umiestnenie (`.../POST-/v1/charges/amount`). Platí tvar z tohto dokumentu; FAQ treba upraviť.

## 5. Čo ďalšie adaptéry odovzdávajú

Okrem štyroch objektov:

| Výstup | Pre koho | Na čo |
|---|---|---|
| **Súbory špecifikácie každej verzie**, bez úprav | rola 3 | spustiť Prism nad staršou verziou a zistiť, či bola odpoveď kedysi správna (`stale-knowledge`) |
| **Index názvov**: pre každý endpoint, umiestnenie a názov zoznam verzií, v ktorých existoval | rola 3 | rozlíšiť `stale-knowledge` (názov kedysi existoval) od `hallucinated` (nikdy neexistoval) |
| **Počty tvrdení podľa typu** pre každý cieľ a verziu | rola 4 | stratifikovaný výber a pokrytie |

Príklad indexu názvov:

```json
{
  "POST /v1/charges": {
    "body": {
      "customer_id": ["2023-11", "...", "2025-02"],
      "customer": ["2025-03", "...", "2025-10"]
    }
  }
}
```

## 6. Kto čo používa

| Rola | Čo berie | Na čo |
|---|---|---|
| 1 Vedúci / generátor | `Claim` (type, operation, location, name, example, …) | vyplní šablónu úlohy a očakávané podmienky |
| 3 Spúšťanie a overovanie | `Claim`, súbory verzií, index názvov | overí požiadavku cez Prism, určí príčinu zlyhania |
| 4 Vyhodnotenie | `Claim.type`, počty, `Snippet`, `slice_key` | výber tvrdení, BM25, slice-y |
| 5 Backend a dáta | všetky štyri objekty | uloží ich do Postgresu |

Celý tok na jednom tvrdení:

```
špecifikácia ─► adaptéry ─► Claim required-field / amount
  ─► rola 1: „Using the Acme Payments API, call POST /v1/charges …“
  ─► model odpovie HTTP požiadavkou bez `amount`
  ─► rola 3: Prism vráti 422 → fail, príčina missing-required
  ─► rola 5: uloží výsledok s claim id a spec_version
```

## 7. Čo potrebujeme odsúhlasiť

Toto sú zmeny oproti pôvodnému návrhu alebo otvorené body. Prosím o potvrdenie alebo pripomienky od uvedených rolí:

| # | Bod | Návrh | Kto potvrdí |
|---|---|---|---|
| 1 | Pole `verify` | vždy `"execute-against-mock"` | 1, 3 |
| 2 | `operation` pri `auth-scheme` | `None`, jedno tvrdenie na schému | 1, 4 |
| 3 | Typ `enum_values` | aj čísla a booleany | 1, 3, 5 |
| 4 | Pole `example` | príkladová hodnota zo špecifikácie, môže chýbať | 1 |
| 5 | Pole `slice_key` | tag slice endpointu | 4 |
| 6 | Tvar ID | podľa §4, s umiestnením a vymazanými zástupnými názvami | všetci |
| 7 | Formát `Snippet.id` | zatiaľ nedefinovaný | 4, 5 |
| 8 | „Celý dokument“ pre režim `full` | všetky snippety operácií spojené, nie surový súbor | 4 |
| 9 | Kontext pre tvrdenia `removed` | ukazuje aktuálne API; `slice_key` = slice, kde endpoint je teraz, alebo bol predtým | 1, 4 |
| 10 | Zastarané (deprecated) endpointy | tvrdenia vznikajú, sú označené; sampler rozhodne | 4 |
| 11 | `required-field` pre query / path parametre | iba polia tela (SPEC §2.2) | 1 |
| 12 | Twilio: viac súborov | jeden Prism na súbor, alebo zlúčenie | 3 |

Po odsúhlasení: PR s `model.py`. Ďalší krok adaptérov je výroba tvrdení a snippetov z už hotových kariet.
