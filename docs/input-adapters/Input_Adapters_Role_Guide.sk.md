# NOT-IN-SPEC: Rola 2, vstupné adaptéry

27. 10. 2026 · @RadoMuntag

> Slovenský preklad dokumentu [Input_Adapters_Role_Guide.md](Input_Adapters_Role_Guide.md). Ak sa verzie líšia, platí anglická.

Podrobná pracovná dokumentácia pre rolu **vstupných adaptérov**: čo táto časť systému robí, ako funguje každý krok, aké technológie používa a čo odovzdáva ostatným rolám. Vychádza zo SPEC.md a FAQ.md. Ak sa tento dokument a SPEC nezhodujú, platí SPEC a opraví sa tento dokument.

Podobne ako FAQ má väčšina sekcií tri časti:

- **Ako to funguje**: technické detaily.
- **Príklad**: konkrétny prípad na vymyslenom API **Acme Payments**.
- **Jednoducho povedané**: tá istá myšlienka pre niekoho, kto neprogramuje.

## 1. Za čo rola zodpovedá

**Ako to funguje.** Adaptéry menia surový vstup (OpenAPI súbory a ich git históriu) na štruktúrovaný materiál, z ktorého pracujú všetky ďalšie kroky. Podľa SPEC §2.1 a §11 táto rola zodpovedá za:

| Výstup | Používa ho |
| --- | --- |
| OpenAPI 3.x adaptér: špecifikácia → operácie, tvrdenia (claims), snippety | generátor (1), vyhľadávanie (4) |
| História verzií: staré verzie špecifikácie z gitu | všetci ďalší v reťazci |
| Tvrdenia o zmenách (`removed`, `renamed`) z oasdiff | generátor (1) |
| Súbory špecifikácie pre každú verziu, pripravené pre Prism | spúšťanie a overovanie (3) |
| Index názvov naprieč všetkými verziami | príčiny zlyhaní (3) |

Adaptéry nikdy nevolajú jazykový model a nikdy nerozhodujú, či je odpoveď správna. Iba opisujú, *čo hovorí špecifikácia*.

**Jednoducho povedané.** Som ten, kto si pozorne prečíta manuál, vypíše z neho každý fakt a odloží si na policu každé staré vydanie. Všetci ostatní v tíme pracujú z mojich zoznamov.

## 2. Kde sa nachádza v reťazci

```
 git repozitáre ──► fetch ──► verzie špecifikácie ──► načítanie + normalizácia ──► tvrdenia ──► generátor ──► …
 (Stripe,                          │                          │                   snippety ─► vyhľadávanie (BM25)
  GitHub,                          │                          │
  Twilio)                          └──► oasdiff ──► tvrdenia removed / renamed
                                   └──► index názvov ──► príčiny zlyhaní (runner)
                                   └──► súbory špecifikácie ──► Prism (runner)
```

Všetko žije v balíku `core` (`notinspec.adapters`). CLI, worker a GitHub Action ho iba volajú.

## 3. Vstupy: tri cieľové API

**Ako to funguje.** Všetky tri ciele zverejňujú oficiálne OpenAPI špecifikácie vo verejných git repozitároch (SPEC §4). Každý cieľ je opísaný v malom konfiguračnom súbore, takže pridať nové API znamená pridať konfiguráciu, nie kód.

```yaml
# targets/acme.yaml
id: acme
name: Acme Payments
repo: https://github.com/acme/openapi
spec_paths: [openapi/spec.yaml]     # jeden alebo viac súborov
version_rule: monthly               # ako sa vyberá história, pozri §5
history_from: 2024-11               # pevný prvý mesiac histórie, pozri §5
body_media_types: [application/json, application/x-www-form-urlencoded]
```

Čo treba vedieť o skutočných cieľoch (pred použitím overiť priamo v repozitároch):

| Cieľ | Repozitár | Poznámky |
| --- | --- | --- |
| Stripe | `stripe/openapi` | Jedna veľká špecifikácia. Telá požiadaviek sú **form-encoded**, nie JSON. Veľa `anyOf` a rekurzívnych `$ref`. |
| GitHub REST | `github/rest-api-description` | Veľmi veľký súbor (niekoľko MB). Viac variantov (github.com, verzie GHES); používa sa iba verejný github.com. |
| Twilio | `twilio/twilio-oai` | Rozdelené do **mnohých súborov, jeden na produkt**. Vyberiem pevnú podmnožinu (napr. základné REST API) a zapíšem, ktoré súbory to sú. Každý súbor je samostatná špecifikácia a Prism mockuje naraz iba jednu, takže rola 3 musí vedieť, z ktorého súboru tvrdenie pochádza (je to v `source`). Či sa súbory zlúčia, alebo pobeží jeden Prism na súbor, treba dohodnúť s rolou 3. |

**Jednoducho povedané.** Každá firma má svoj plán API vo verejnom priečinku so všetkými starými vydaniami. Zapíšem si, kde ten priečinok je a ktoré súbory z neho čítam.

## 4. Výstupný kontrakt

Tvary výstupov sú dohoda so zvyškom tímu (roadmapa, 8. týždeň). Sú v `core/src/notinspec/model.py` a dohodnuté s rolami 1, 3 a 5. Každá zmena ide cez vedúceho.

**Ako to funguje.** Modely v Pydantic v2, zmrazené (nemenné), serializované ako kanonický JSON.

```python
class SpecVersion(BaseModel):
    target: str  # "acme"
    version: str  # "2025-03" (naše označenie, pozri §5)
    commit: str  # SHA git commitu, z ktorého pochádza
    committed_at: datetime
    files: list[str]  # cesty k súborom špecifikácie v danom commite
    content_hash: str  # sha256 normalizovaného obsahu


class Operation(BaseModel):
    method: str  # "POST"
    path: str  # "/v1/charges"
    operation_id: str | None
    tags: list[str]
    deprecated: bool


class Claim(BaseModel):
    id: str  # stabilné, pozri nižšie
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
    verify: Literal["execute-against-mock"]  # každé tvrdenie nesie svoj spôsob overenia
    operation: Operation | None  # None iba pre auth-scheme (jedno tvrdenie na schému)
    location: Literal["path", "query", "header", "body"] | None
    name: str | None  # názov poľa alebo parametra; pri auth-scheme názov schémy
    old_name: str | None  # iba pre renamed
    value_type: str | None  # "integer", "string", ...
    enum_values: list[str | int | float | bool] | None  # enumy nie sú vždy reťazce
    example: Any | None  # príkladová hodnota zo špecifikácie, ak existuje (pre šablóny úloh)
    slice_key: str | None  # kľúč tag slice-u, v ktorom je operácia (režim full-sliced)
    since_version: str | None  # pre removed / renamed: verzia, v ktorej nastala zmena
    fact: str  # čitateľná veta pre reporty
    source: str  # JSON pointer do špecifikácie
    spec_version: str


class Snippet(BaseModel):
    id: str
    target: str
    kind: Literal["operation", "tag"]
    key: str  # "POST /v1/charges" alebo názov tagu "Charges"
    text: str  # vyrenderovaný, deterministický
    size_bytes: int
```

**ID tvrdení** musia byť stabilné medzi behmi, pretože sampler, porovnanie behov aj história sú na nich postavené. Rozširujú formát z FAQ §2 o umiestnenie (location), ktoré je potrebné na rozlíšenie query parametra a poľa v tele s rovnakým názvom (príklad vo FAQ sa upraví). Tvar závisí od typu:

```
{target}/hard/{type}/{METHOD}-{path}                     endpoint-exists, removed (endpoint)
{target}/hard/{type}/{METHOD}-{path}/{location}/{name}   param-name, required-field, enum-value,
                                                         removed (pole), renamed (nový názov)
{target}/hard/auth-scheme/{scheme}                       auth-scheme

acme/hard/endpoint-exists/POST-/v1/charges
acme/hard/required-field/POST-/v1/charges/body/amount
acme/hard/renamed/POST-/v1/charges/body/customer
acme/hard/auth-scheme/bearerAuth
```

Pravidlá:

- ID neobsahuje verziu špecifikácie. Tvrdenie, ktoré existuje v mnohých verziách, si drží rovnaké ID. Vďaka tomu sa dajú behy porovnávať týždeň po týždni.
- Názvy zástupných parametrov v ceste sa v ID vymažú (`/v1/charges/{id}` → `/v1/charges/{}`), rovnako ako pri porovnávaní ciest v indexe názvov (§10). Inak by premenovanie zástupného parametra v špecifikácii zmenilo ID, hoci sa API v skutočnosti nezmenilo.
- ID sú nepriehľadné kľúče. Cesty obsahujú `/`, takže ID sa nemá rozdeľovať na časti; použite polia tvrdenia.
- Ak sa to isté tvrdenie o zmene objaví v histórii dvakrát (pole odstránené, znova pridané, znova odstránené), ponechá sa jedno, s **najnovšou** `since_version`.

**Jednoducho povedané.** Tím sa raz dohodne, ako vyzerá „fakt“ na papieri, aby sa roly po mne mohli spoľahnúť, že každý fakt má rovnaké polia na rovnakých miestach.

## 5. Krok 1: sťahovanie špecifikácií a histórie

**Ako to funguje.**

1. Každý cieľový repozitár sa raz naklonuje do cache priečinka na VM (`/data/repos/<target>`); ďalšie behy robia `git fetch`.
2. Vypíšu sa commity, ktoré menili súbory špecifikácie: `git log --format='%H %cI' -- openapi/spec.yaml`
3. Verzie sa vyberajú **pevným pravidlom**, aby tá istá história vždy dala tie isté verzie. Predvolene: **posledný commit každého kalendárneho mesiaca**, ktorý menil špecifikáciu, počínajúc pevným mesiacom `history_from` z konfigurácie cieľa. Okno nikdy nie je „posledných N mesiacov“ počítaných od dnes, pretože potom by ten istý repozitár dal o mesiac iné verzie. Označenie je mesiac (`2025-03`). Ciele so skutočnými release tagmi môžu namiesto toho použiť `version_rule: tags`.
4. Súbory každej vybranej verzie sa exportujú cez `git show <sha>:<path>` do `/data/specs/<target>/<version>/`.
5. Najnovšia verzia je „aktuálna“. Všetko ostatné je história.

Systémový `git` cez `subprocess` je jednoduchý a rýchly. Plné klony týchto repozitárov sú veľké, preto sa cache drží medzi behmi a nikdy sa neklonuje znova.

**Príklad.** Špecifikácia Acme sa za posledný rok zmenila 41-krát. Mesačné pravidlo z toho spraví 12 verzií, `2024-11` … `2025-10`. Release, ktorý premenoval `customer_id`, vyšiel v marci, takže sa ukáže ako krok `2025-02 → 2025-03`.

**Známe obmedzenie mesačného pravidla.** Jeden mesačný krok môže spojiť veľa zmien. Viac premenovaní je potom nejednoznačných, takže ich párovacie pravidlo (§9) zmení na obyčajné tvrdenia `removed`, a pole, ktoré bolo pridané a odstránené v rámci jedného mesiaca, sa vôbec nezachytí. Ak má cieľ release tagy (Stripe a Twilio ich zverejňujú), `version_rule: tags` väčšinu z toho rieši.

**Jednoducho povedané.** Namiesto každého vydania, ktoré kedy vyšlo, si nechám jedno vydanie za mesiac. Stačí to na to, aby bolo vidno, čo sa zmenilo a kedy, a polica zostane rozumne veľká.

## 6. Krok 2: načítanie a normalizácia špecifikácie

**Ako to funguje.**

1. **Parsovanie.** JSON cez `orjson`, YAML cez C loader z PyYAML (`CSafeLoader`), čo je dôležité pri veľmi veľkom súbore GitHubu.
2. **Validácia.** `openapi-spec-validator` skontroluje, či je súbor platné OpenAPI 3.0/3.1. Problémy sa zalogujú a spočítajú, nie sú fatálne. Skutočné špecifikácie sú málokedy dokonalé.
3. **Rozlíšenie `$ref`.** Malý vlastný resolver s ochranou proti cyklom (Stripe a iné majú rekurzívne schémy). Pamätá si pôvodný JSON pointer každej časti, ktorý sa stane `source` tvrdenia.
4. **Sploštenie operácií.** Pre každú `paths.<path>.<method>`: zlúčia sa `parameters` na úrovni cesty a operácie (pri rovnakom `name` + `in` vyhráva úroveň operácie); zoberie sa telo požiadavky pre nakonfigurované media typy (`application/json`, alebo form-encoded pre Stripe); zoberie sa platné zabezpečenie: `security` na úrovni operácie, ak existuje, inak globálne. Prázdny zoznam (`security: []`) znamená bez autentifikácie.
5. **Sploštenie schém** na zoznam polí tela: `allOf` zlúči vlastnosti a zoznamy `required`; pri `oneOf` / `anyOf` sa zozbierajú polia zo všetkých vetiev, ale pole sa označí ako povinné **iba ak je povinné v každej vetve**; vlastnosti `readOnly` sa vynechajú (patria do odpovedí, nie požiadaviek); ide sa najviac 2 úrovne do hĺbky, vnorené polia majú názov s bodkou (`shipping.address`).

Výsledkom je zoznam normalizovaných operácií, každá so svojimi parametrami, poľami tela, enumami a zabezpečením. Všetko ďalej pracuje s týmto, nikdy so surovým YAML.

**Príklad.** Surový fragment Acme:

```yaml
/v1/charges:
  parameters:
    - { name: Idempotency-Key, in: header, schema: { type: string } }
  post:
    tags: [Charges]
    requestBody:
      content:
        application/json:
          schema: { $ref: '#/components/schemas/ChargeCreate' }
```

Po normalizácii:

```
POST /v1/charges  tags=[Charges]
  header  Idempotency-Key  string
  body    amount           integer  required
  body    currency         string   required
  body    customer         string
  body    capture          string   enum=[automatic, manual]
  auth    bearerAuth
```

**Jednoducho povedané.** Plán API je plný krížových odkazov („pozri stranu 40“). Prejdem každý odkaz a každý endpoint prepíšem na jednu plochú, úplnú kartu, aby už nikto nemusel listovať.

## 7. Krok 3: extrakcia štrukturálnych tvrdení

**Ako to funguje.** Jeden prechod cez normalizované operácie vytvorí päť štrukturálnych typov tvrdení zo SPEC §2.2:

| Typ | Jedno tvrdenie na | Príklad faktu |
| --- | --- | --- |
| `endpoint-exists` | operáciu | `POST /v1/charges` existuje |
| `param-name` | parameter alebo pole tela | `customer` je pole tela `POST /v1/charges` |
| `required-field` | povinné pole tela | `POST /v1/charges` vyžaduje `amount` |
| `enum-value` | pole alebo parameter s `enum` | `capture` ∈ {`automatic`, `manual`} |
| `auth-scheme` | použitú bezpečnostnú schému | API používa bearer autentifikáciu |

Pravidlá, vďaka ktorým je výstup predvídateľný:

- Tvrdenia sa pred opustením adaptéra zoradia podľa ID.
- Zastarané (deprecated) operácie tiež vytvárajú tvrdenia, ale sú označené; či ich sampler použije, rozhoduje rola 4.
- `auth-scheme` je na schému, nie na operáciu (inak by jedna schéma vytvorila tisíce rovnakých tvrdení). Má `operation = None` a vlastný tvar ID (§4).
- Veta `fact` sa generuje z pevnej šablóny, nikdy sa nepíše ručne.

Počty tvrdení podľa typu sa reportujú pre každý cieľ a verziu, pretože sampler (rola 4) ich potrebuje na stratifikovaný výber a pokrytie.

**Príklad.** Z normalizovaného `POST /v1/charges` vyššie:

```
acme/hard/endpoint-exists/POST-/v1/charges
acme/hard/param-name/POST-/v1/charges/header/Idempotency-Key
acme/hard/param-name/POST-/v1/charges/body/amount
acme/hard/param-name/POST-/v1/charges/body/currency
acme/hard/param-name/POST-/v1/charges/body/customer
acme/hard/param-name/POST-/v1/charges/body/capture
acme/hard/required-field/POST-/v1/charges/body/amount
acme/hard/required-field/POST-/v1/charges/body/currency
acme/hard/enum-value/POST-/v1/charges/body/capture
```

**Jednoducho povedané.** Každú kartu endpointu premením na zoznam krátkych, overiteľných výrokov, tak ako učiteľ premení kapitolu na fakty pripravené na skúšku.

## 8. Krok 4: snippety a slice-y

**Ako to funguje.** Snippety sú text, ktorý modely vidia v režimoch `snippet` a `full` (SPEC §2.4). Sú dva druhy:

- **Snippet operácie**: jeden na operáciu, vyrenderovaný z normalizovanej karty ako kompaktný čistý text: metóda, cesta, súhrn, popis, parametre, polia tela, autentifikácia. V nich vyhľadáva BM25 (rola 4).
- **Tag slice**: všetky operácie s rovnakým tagom, používa sa v režime `full-sliced`, keď sa celá špecifikácia nezmestí do kontextu modelu. Ak operácia nemá tag, použije sa prvý segment cesty (`/v1/charges/...` → `charges`).

Renderovanie je deterministické: pevné poradie polí, pevné formátovanie, žiadne časové značky. Tá istá špecifikácia vždy dá bajtovo rovnaké snippety. `size_bytes` sa ukladá, aby reporty mohli ukázať veľkosť slice-ov.

Tri ďalšie veci, ktoré režimy od tohto kroku potrebujú:

- **Celý dokument.** Režim `full` dáva modelu „celý dokument, ak sa zmestí“ (SPEC §2.4). Návrh: celý dokument sú všetky snippety operácií spojené v zoradenom poradí, nie surový súbor špecifikácie. Je oveľa menší ako surový YAML (súbor GitHubu má niekoľko MB) a používa rovnaké renderovanie ako ostatné režimy. Treba potvrdiť s rolou 4 (otvorená otázka, §17).
- **Tvrdenie → slice.** `full-sliced` používa „slice obsahujúci tvrdenie“, takže každé tvrdenie s operáciou nesie `slice_key`. Pri tvrdeniach `auth-scheme` (bez operácie) je `None`.
- **Tvrdenia o zmenách.** Tvrdenie `removed` ukazuje na niečo, čo v aktuálnej špecifikácii nie je, takže nemá aktuálny snippet. Je to zámer: kontext ukazuje aktuálne API a správna odpoveď je odstránenú vec nepoužiť. Jeho `slice_key` je slice, v ktorom operácia je teraz, alebo pri odstránenom endpointe slice, v ktorom bol predtým. Treba potvrdiť s rolami 1 a 4.

**Príklad.**

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

**Jednoducho povedané.** Okrem zoznamu faktov rozstrihám manuál aj na prehľadné stránky. Keď model smie „pozrieť sa do dokumentácie“, dostane na čítanie práve tieto stránky.

## 9. Krok 5: tvrdenia o zmenách cez oasdiff

**Ako to funguje.** Tvrdenia `removed` a `renamed` vznikajú porovnaním po sebe idúcich verzií nástrojom **oasdiff**, nie čítaním textu changelogu (SPEC §2.1, FAQ §2). SPEC ponecháva text changelogu iba ako podporný dôkaz (napr. ukázať správcovi poznámku k releasu); to je mimo rozsahu adaptérov v MVP.

1. Pre každú dvojicu po sebe idúcich verzií (`2025-02 → 2025-03`) sa spustí `oasdiff changelog old.yaml new.yaml --format json`. oasdiff beží ako zafixovaný Docker image alebo zafixovaná binárka v našom image, takže každý dostane rovnaký výstup.
2. Relevantné záznamy o zmenách sa namapujú na typy tvrdení: odstránený endpoint, odstránený parameter požiadavky a odstránená vlastnosť tela požiadavky sa stanú tvrdením `removed`; pridané parametre a vlastnosti sa odložia na párovanie premenovaní. Presné ID kontrol oasdiff vypíše `oasdiff checks`; mapovacia tabuľka je v kóde a má vlastný test.
3. **Párovanie premenovaní.** oasdiff hlási premenovanie ako „odstránené X“ + „pridané Y“. Spárujú sa iba vtedy, keď platí **všetko** naraz: rovnaká operácia, rovnaké umiestnenie (path / query / header / body), rovnaký typ, odstránené aj pridané v tom istom kroku verzie, a je to **jediný** možný pár v danej operácii a umiestnení. Ak by sa dali spárovať dve odstránené a dve pridané polia, adaptér nehádá: vytvorí obyčajné tvrdenia `removed`. Opatrnosť udržiava tvrdenia `renamed` dôveryhodné.
4. Tvrdenie o zmene zaznamenáva `since_version` (verziu, v ktorej zmena nastala) a starý názov.

**Príklad.** oasdiff na Acme `2025-02 → 2025-03`, zjednodušene:

```
POST /v1/charges   request property removed   customer_id (string)
POST /v1/charges   request property added     customer    (string)
DELETE /v1/charges/{id}   endpoint removed
```

Výsledok:

```
acme/hard/renamed/POST-/v1/charges/body/customer        old_name=customer_id  since=2025-03
acme/hard/removed/DELETE-/v1/charges/{}                 since=2025-03
```

**Jednoducho povedané.** Položím plán z minulého mesiaca vedľa toho z tohto mesiaca a označím každý riadok, ktorý zmizol. Keď riadok zmizol a na tom istom mieste sa objavil veľmi podobný, nazvem to premenovaním, ale iba ak o tom niet pochýb.

## 10. Krok 6: index názvov pre príčiny zlyhaní

**Ako to funguje.** Keď odpoveď modelu zlyhá, rola 3 určuje *prečo* (SPEC §2.6). Dve príčiny závisia od dát z tejto roly: `stale-knowledge` (požiadavka je platná voči **staršej** verzii) a `hallucinated` (používa názov, ktorý neexistuje v **žiadnej** známej verzii).

Táto rola poskytuje:

1. **Súbory špecifikácie pre každú verziu**, exportované bez zmien, aby rola 3 mohla spustiť Prism na staršej verzii a požiadavku znova overiť. Podľa FAQ §5 špecifikácie **nesprísňujem**; pôvodné obmedzenia zostávajú.
2. **Index názvov**: pre každú trojicu (operácia, umiestnenie, názov) zoznam verzií, v ktorých sa vyskytuje.

```json
{
  "POST /v1/charges": {
    "body": {
      "customer_id": ["2023-11", "...", "2025-02"],
      "customer":    ["2025-03", "...", "2025-10"],
      "amount":      ["2023-11", "...", "2025-10"]
    }
  }
}
```

Cesty sa porovnávajú bez ohľadu na názvy parametrov (`/v1/charges/{id}` a `/v1/charges/{charge}` sú tá istá cesta), pretože špecifikácie niekedy premenujú zástupné parametre bez zmeny API.

**Príklad.** Model pošle `customer_id`. Index ukáže, že existoval do `2025-02`, takže rola 3 to môže označiť ako `stale-knowledge` a povedať, odkedy. Model pošle `client_ref`, ktorý nie je v žiadnej verzii, takže ide o `hallucinated`.

**Jednoducho povedané.** Vediem register každého názvu, ktorý sa kedy v pláne objavil, a kedy. Vďaka tomu projekt vie dokázať, že nesprávna odpoveď AI bola kedysi správna.

## 11. Determinizmus a testovanie

**Ako to funguje.** Celý projekt stojí na „rovnaký vstup → rovnaký výstup“ (SPEC §2.3, §9). Pre adaptéry to znamená: vo výstupe sa nikde nepoužíva aktuálny čas, náhodné čísla ani poradie v slovníkoch; všetko sa pred zápisom zoradí podľa stabilných kľúčov; kanonický JSON (zoradené kľúče, pevné oddeľovače) pre všetko, čo sa hashuje; externé nástroje (oasdiff) zafixované na presnú verziu.

Testy (pytest):

| Test | Čo zachytí |
| --- | --- |
| **Golden súbory** pre každý krok adaptéra: testovacia špecifikácia → očakávané tvrdenia, snippety, index názvov | akúkoľvek neúmyselnú zmenu výstupu |
| Spustiť dvakrát, porovnať hashe | skrytý nedeterminizmus |
| Malé ručne písané testovacie špecifikácie so známymi `allOf`, `oneOf`, cyklami `$ref`, form telami | chyby v normalizácii |
| Dve testovacie verzie so známym premenovaním a odstránením | mapovanie oasdiff a párovacie pravidlo |
| Nejednoznačné premenovanie (2 odstránené, 2 pridané) | párovacie pravidlo zostáva opatrné |
| Smoke test na skutočných špecifikáciách Stripe, GitHub, Twilio (nie v každom CI behu, je pomalý) | pády na zvláštnostiach reálnych špecifikácií |

Keď sa výstup zmení zámerne, golden súbory sa pregenerujú v tom istom PR, takže reviewer presne vidí, čo sa zmenilo. Testovacia špecifikácia je v `deploy/fixtures/openapi.yaml` a zdieľa ju aj end-to-end test (rola 7).

**Jednoducho povedané.** Uložím si „hárok so správnymi odpoveďami“ pre testovací plán. Pri každej zmene kódu program skontroluje, že stále vytvára presne tento hárok, takže chyby sa nevkradnú nepozorovane.

## 12. Technológie

| Potreba | Voľba | Prečo |
| --- | --- | --- |
| Jazyk | Python 3.12+ | štandard projektu (SPEC §5) |
| Dátové modely | Pydantic v2 | typované, validované, jednoduchý JSON; zdieľané s backendom |
| YAML / JSON | PyYAML (`CSafeLoader`), `orjson` | dosť rýchle pre niekoľkomegabajtové špecifikácie |
| Validácia špecifikácie | `openapi-spec-validator` | overí platnosť OpenAPI 3.0 / 3.1 |
| Rozlíšenie `$ref` | vlastný malý resolver | potrebuje ošetriť cykly a zachovať zdrojové pointery |
| Rozdiely špecifikácií | **oasdiff** (zafixovaná binárka / Docker image) | povinné podľa SPEC; štruktúrovaný JSON changelog |
| História | `git` CLI cez `subprocess` | jednoduché, bez ďalšej závislosti |
| Testovanie | pytest, golden súbory | SPEC §9 |
| Kvalita | ruff, mypy (strict na `core/`) | SPEC §5 |
| Balíčkovanie | uv | SPEC §5 |

Nepoužíva sa tu: jazykové modely, embeddingy, databáza. Adaptéry sú čisté funkcie zo súborov na dáta, preto sa ľahko testujú a dajú sa znova použiť v GitHub Action.

## 13. Štruktúra kódu a CLI

```
core/src/notinspec/
  model.py                  zdieľané tvary (Claim, Snippet, SpecVersion, …)
  adapters/
    targets.py              načítanie konfigurácie cieľov
    history.py              git fetch, výber verzií, export
    openapi/
      load.py               parsovanie, validácia
      refs.py               $ref resolver s ochranou proti cyklom
      normalize.py          operácie, parametre, telá, zabezpečenie
      claims.py             extrakcia štrukturálnych tvrdení
      snippets.py           snippety operácií a tag slice-y
    diff/
      oasdiff.py            spúšťanie oasdiff, parsovanie jeho JSON
      changes.py            tvrdenia removed, párovanie premenovaní
    name_index.py           názvy naprieč verziami
core/tests/adapters/
  fixtures/                 malé špecifikácie, dvojverziové testovacie dáta
  golden/                   očakávané výstupy
```

Príkazy CLI (tenké obaly, celé CLI vlastní rola 1):

```bash
notinspec adapters fetch  --target stripe              # aktualizovať cache repozitára, exportovať verzie
notinspec adapters claims --spec openapi.yaml --out claims.jsonl
notinspec adapters diff   --old v1.yaml --new v2.yaml  # tvrdenia o zmenách medzi dvoma súbormi
notinspec adapters stats  --target stripe              # počty tvrdení podľa typu a verzie
```

`stats` sa hodí hneď na začiatku: ukáže skutočnú veľkosť každého API skôr, než na ňom niekto spustí modely.

## 14. Odovzdávanie ostatným rolám

| Komu | Čo odovzdávam | Čo potrebujem naspäť |
| --- | --- | --- |
| 1 Vedúci / generátor | tvrdenia v dohodnutom tvare, stabilné ID | potreby šablón (napr. príkladové hodnoty zo špecifikácie) |
| 3 Spúšťanie a overovanie | súbory špecifikácie pre každú verziu, index názvov | ktoré kontroly potrebujú ktoré dáta |
| 4 Vyhľadávanie a vyhodnotenie | snippety, slice-y, počty tvrdení podľa typu | pravidlá výberu, napr. čo so zastaranými operáciami |
| 5 Backend a dáta | záznamy `SpecVersion` s hashmi obsahu | ako sa ukladajú verzie a tvrdenia |
| 7 DevOps | oasdiff v image, volume pre cache repozitárov na VM | miesto na disku pre klony a exportované verzie |

Najväčšie riziko závislostí podľa roadmapy je, že roly 1 a 3 budú stavať na odhadnutých tvaroch tvrdení. Predíde sa tomu dohodou na tvaroch v 8. týždni a udržiavaním výstupov testovacích dát aktuálnych.

## 15. Úskalia skutočných špecifikácií

| Problém | Ako sa rieši |
| --- | --- |
| Form-encoded telá (Stripe) | `application/x-www-form-urlencoded` sa berie ako umiestnenie body, rovnako ako JSON |
| Rekurzívne `$ref` | ochrana proti cyklom; zastavenie na limite hĺbky |
| `anyOf` / `oneOf` všade | zjednotenie polí; povinné iba ak je povinné vo všetkých vetvách |
| Obrovské súbory (GitHub) | C YAML loader, parsovanie raz na verziu, cache normalizovaného výstupu podľa hashu obsahu |
| Veľa súborov na API (Twilio) | pevný zoznam súborov na cieľ v konfigurácii |
| Zástupné parametre v ceste premenované medzi verziami | porovnávanie ciest bez ohľadu na zástupné parametre |
| Špecifikácia preformátovaná, nič sa reálne nezmenilo | hash obsahu normalizovaného výstupu; ak je rovnaký, nová verzia nevzniká |
| Neplatná špecifikácia v starom commite | zalogovať, verziu preskočiť, pokračovať so susednými |
| Rozšírenia výrobcov (`x-…`) | v MVP ignorované |
| Schémy, ktoré povoľujú neznáme polia | v adaptéroch sa nič nemení; rola 3 explicitne kontroluje cieľové názvy (FAQ §5) |

## 16. Plán na týždne 8–12

Podľa dohodnutej roadmapy (riadok „Vstupné adaptéry“). Ciele sú orientačné; rozsah aj načasovanie sa môžu posunúť podľa implementácie.

| Týždeň | Cieľ z roadmapy | Konkrétne kroky |
| --- | --- | --- |
| 8 · Začiatok implementácie | začať so spracovaním OpenAPI a získavaním dát potrebných na testovanie | dohodnúť tvary `Claim`, `Snippet`, `SpecVersion` s rolami 1, 3, 5; loader, validátor, `$ref` resolver; testovacia špecifikácia + prvý golden súbor |
| 9 · Vývoj a integrácia | extrahovať overiteľné fakty a snippety zo špecifikácie | normalizácia operácií, tiel a zabezpečenia; všetkých 5 štrukturálnych typov tvrdení; snippety operácií a tag slice-y; príkaz `stats` |
| 10 · Prvý prechod systémom | prepojiť spracovanie vstupu s generovaním úloh, začať s históriou verzií | odovzdať tvrdenia generátoru na testovacej špecifikácii; cache repozitárov, mesačný výber verzií, export verzií; beh na skutočných špecifikáciách Stripe, GitHub, Twilio |
| 11 · Testovanie a prvé výsledky | overiť spracovanie na vybraných vstupoch, riešiť obmedzenia | integrácia oasdiff, tvrdenia `removed`, párovanie premenovaní; index názvov pre rolu 3; opraviť zvláštnosti reálnych špecifikácií nájdené v 10. týždni |
| 12 · Demo a ďalšie kroky | stabilizovať podporovaný rozsah vstupov, zdokumentovať body rozšírenia | golden súbory pre históriu; smoke testy na reálnych špecifikáciách; zdokumentovať podporované vlastnosti OpenAPI, známe medzery a ako pridať nový cieľ |

## 17. Otvorené otázky

Každá položka má navrhnutú odpoveď, ktorú treba potvrdiť s uvedenou rolou.

- [ ] Vytvárajú aj povinné query/path parametre tvrdenia `required-field`, alebo iba polia tela? *Návrh: iba telo, ako hovorí SPEC §2.2.* (vedúci)
- [ ] Limit hĺbky pre vnorené polia tela: 2 úrovne, alebo v MVP iba najvyššia úroveň? *Návrh: 2 úrovne.* (vedúci)
- [ ] Pravidlo verzií: mesačne pre všetky tri ciele, alebo tagy, kde existujú? *Návrh: tagy, kde existujú (pozri §5, známe obmedzenie), inak mesačne.* (vedúci)
- [ ] Ktoré súbory Twilio sú v rozsahu? A zlúčia sa pre Prism, alebo jeden Prism na súbor? (rola 3)
- [ ] Zastarané operácie: vytvárať tvrdenia a nechať sampler, nech ich preskočí, alebo ich preskočiť už v adaptéri? *Návrh: vytvárať ich, označené; rozhoduje sampler.* (rola 4)
- [ ] `history_from` pre každý cieľ: ktorý prvý mesiac? *Návrh: približne 24 mesiacov pred prvým týždenným behom, potom pevne.* (vedúci)
- [ ] Celý dokument pre režim `full`: všetky snippety operácií spojené, alebo surový súbor špecifikácie? *Návrh: spojené snippety (§8).* (rola 4)
- [ ] Kontext pre tvrdenia `removed` v režimoch snippet / full (§8). (roly 1, 4)

Poznámka pre vedúceho, mimo tejto roly: FAQ §5 uvádza príčinu zlyhania `task-mismatch`, ktorú SPEC §2.6 nemá, a príklad ID tvrdenia vo FAQ nemá umiestnenie (§4).
