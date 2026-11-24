# Hostované CI – SCRUM-24

## Čo funguje

Existujúca GitHub Action zabalí vstupy cez `notinspec pack`, pošle archív s GitHub OIDC
tokenom a čaká na výsledok. Server teraz poskytuje skutočné endpointy podľa SPEC §11.1:

- `POST /api/uploads`: kontrola podpisu RS256, issuer, audience `notinspec`, platnosti tokenu,
  registrovaného číselného ID repozitára, workflow, udalosti a verejnej viditeľnosti.
  `push` a `workflow_dispatch` sú povolené len z registrovanej predvolenej vetvy.
- Archív sa skontroluje a uloží podľa SHA-256. Limit archívu je 25 MiB; streamované telo
  requestu má navyše 64 KiB na multipart obálku. Platí aj prípadný nižší limit projektu.
- PostgreSQL fronta: rovnaký GitHub run a attempt vráti rovnaký beh, odlišné dáta HTTP 409.
  Commit a číslo PR sa berú z overeného tokenu, nie z klientských metadát.
- Worker spustí existujúce parsovanie, chunkovanie a voliteľne extrakciu + grounding claimov.
  Používa rovnaké core funkcie ako CLI; pre extrakciu iba povolené bezplatné FIIT modely.
- `GET /api/runs/{id}` vráti stav, chybu a text komentára. Artefakty aj claims sa uložia do DB,
  pre existujúce webové demo ostane aj priečinok behu na zdieľanom volume.
- `POST /api/pr-closed` zatiaľ idempotentne zaznamená udalosť do `pr_closed`.
  Zamietanie kandidátov golden setu na ňu musí napojiť golden-set pipeline.

Workeri držia PostgreSQL advisory lock po celý beh. Pád procesu uvoľní zámok a stav
`running` možno obnoviť. Ak už existujú dokončené artefakty, ďalší pokus dokončí zápis
do DB bez ďalšieho volania modelov. Surové odpovede sa priebežne appendujú samostatnými
transakciami a aj do trvalého JSONL journalu mimo dočasného priečinka behu. Pri výpadku DB
ostáva journal na volume; jeho import po výpadku je manuálny, nie automatická synchronizácia.

## Zapnutie

Databázové PR #55/#56 sú od 2026-11-24 v `main`; CI vetvy sú na tento stav aktualizované.
Zostáva samostatná zmena závislostí `core/hosted-deps` (#61), implementácia
`core/hosted-ci` (#62) a konfigurácia `devops/hosted-ci-wiring` (#63), v tomto poradí.
Najprv treba zlúčiť a nasadiť tieto zmeny, zálohovať DB, aplikovať migrácie a registrovať
repozitár. Bez registrácie server upload odmietne. Funkcia je štandardne vypnutá.

```sh
uv sync --locked --all-packages
export DATABASE_URL='postgresql://USER:PASSWORD@HOST:5432/notinspec'
uv run notinspec db upgrade
uv run notinspec db add-project PROJECT --repository OWNER/REPO --repository-id NUMERIC_ID \
  --workflow OWNER/REPO/.github/workflows/notinspec.yml
```

API aj worker potrebujú `NOTINSPEC_UPLOADS_ENABLED=1`, rovnakú DB, spoločný
`NOTINSPEC_UPLOADS_DIR` a `NOTINSPEC_RUNS_DIR`, plus `NOTINSPEC_PUBLIC_URL`.
Pre reálnu extrakciu worker potrebuje aj `NOTINSPEC_HOSTED_CLAIMS=1`, `FIIT_API_KEY`
a vopred stiahnutý lokálny NLI model podľa `docs/DEPLOY.md`. Pri vypnutej extrakcii sa
vykoná iba ingestion. Pred zapnutím na VM treba dohodnúť kapacitu a limity celých dokumentácií.
Samotná konfigurácia nespúšťa migrácie automaticky a nemení produkciu.

## Overenie

```sh
TEST_DATABASE_URL=postgresql://postgres:LOCAL_PASSWORD@localhost:5432/notinspec_test \
  uv run pytest core/tests/db core/tests/test_oidc.py api/tests/test_hosted.py
```

DB testy používajú izolovanú schému pre každý test a skutočný PostgreSQL. Kontrolujú HTTP
upload → frontu → worker → výsledok, replay, súbeh workerov, obnovu po publikovaní artefaktov
a zachovanie raw odpovede pri chybe DB. Test claim pipeline replayuje reálne nahraté FIIT
odpovede na 4 urllib3 chunkoch a používa fake NLI; overuje uloženie 153 claimov a 8 raw volaní.
Je to integračný test ukladania, nie meranie presnosti NLI. Autentifikácia je testovaná
skutočnými RSA podpismi s lokálnym testovacím kľúčom, bez kontaktovania GitHubu.
Žiadny z týchto automatizovaných testov nevolá živé LLM.

## Čo ešte bráni uzavretiu celého CI toolu

Chýba prepojenie generovania testovacích úloh, golden setu, schvaľovania kandidátov,
spúšťania modelov pod testom a vyhodnotenia L0–L4 s baseline. Výstup preto má
`verdict: null`; úspešný ingestion/grounding sa nikdy neoznačuje ako regresné `pass`.
Existujúca Action pri tom správne zobrazí „no result“. Tiež treba overiť reálny GitHub
OIDC tok na nasadenej VM a PR po schválení závislostí. Produkčné nasadenie ani kompletný
regresný výsledok tento PR nepredstiera. Pôvodný Action stub ostáva zmluvným testom klienta.

V `main` už existujú deterministické referencie a generátory L0/L1
(`notinspec.tasks`, PR #44), ale ešte netvoria kompletnú hodnotiacu pipeline workera.
Pribudla aj krížová kontrola K2 (PR #54). Samotná dostupnosť týchto modulov
nemení význam `verdict: null` a nepredstavuje overený regresný výsledok.
