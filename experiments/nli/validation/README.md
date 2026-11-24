# Overenie NLI na reálnej dokumentácii — SCRUM-46

Na 36 nových kontrolných tvrdeniach z dokumentácie urllib3, Trio a hydra-zen som
overil aktuálny produkčný grounding (`ground_claims`). Pôvodných 180 ľudských
anotácií vyhodnocujem samostatne replayom uložených predikcií runu 007; model
sa na tejto vzorke znovu nespúšťa. Výsledky sú v `results.json`, aktuálne
kontrolné vstupy a reálne skóre lokálneho modelu v `scores.json`.

## Výsledky

| Vzorka | Správne ponechané | Nesprávne ponechané | Správne vyradené | Nesprávne vyradené |
| --- | ---: | ---: | ---: | ---: |
| Pôvodných 180 ľudských anotácií, replay historického runu 007 | 86 | 12 | 76 | 6 |
| Nových 36 kontrolných tvrdení, aktuálny core pipeline | 12 | 1 | 23 | 0 |

Keep/drop nových kontrol sa počíta z výsledného statusu `kept` po kontrole
citácie, NLI aj identifikátorov. Trojtriedna matica a `correct_three_way` sú
NLI-only a počítajú iba tvrdenia so skóre; ich počet uvádza `nli_scored_count`.
Pri výbere premisy aj deduplikácii párov rozhoduje priamo core `ground_claims`.

Na ľudských anotáciách je precision ponechaných tvrdení 86/98 (87,8 %) a recall
86/92 (93,5 %). Ide o opätovné vyhodnotenie uložených výsledkov runu 007,
vrátane vyradení pri kontrole citácií. Samostatná trojtriedna matica v JSON
počíta iba prípady, pre ktoré existuje NLI predikcia. Vstupná vzorka je výberová,
s umelo pripravenými negatívnymi tvrdeniami. Tieto pomery neurčujú kvalitu
všetkých tvrdení z produkčnej extrakcie.

Run 007 používal staršie experimentálne pravidlo `local-block`, breadcrumb,
okno 128 a radius 1. Nie je to replay grounding v2. Jeho `provenance` uvádza
zdrojový CSV, ľudské labely a config vrátane hashov, model/revíziu, pôvodný
commit a runtime verzie. Verzie core pravidiel vtedy neboli zaznamenané,
preto sú `null`. Aktuálne verzie patria len k `control_grounding`.

Nové kontroly obsahujú dve sekcie príručky a dve API sekcie z každej knižnice.
Pre každú citáciu je pripravené jedno podporené, jedno odporujúce a jedno
nepodložené tvrdenie. Kontrolné odpovede som pripravil pomocou AI podľa textov
pred spustením modelu. Sú to autorské kontroly s jednoduchými negatívnymi
príkladmi. Nejde o nové nezávislé ľudské anotácie. Ich výsledok sa uvádza
oddelene od pôvodnej ľudskej vzorky.

NLI správne určil všetky tri triedy v 35/36 prípadoch. Chybne podporil
`control-012`: tvrdenie, že `trio.sleep_until` chápe deadline ako UTC timestamp.
Dokumentácia hovorí iba o absolútnom čase podľa interných hodín Trio.
Ani následná kontrola identifikátorov tento prípad nevyradila. Samotné vysoké
NLI skóre preto nestačí na zaručenie vecnej správnosti.

## Reprodukcia

Príkazy sa spúšťajú z koreňa repozitára. Replay používa zaznamenané reálne skóre,
funguje bez torch, sietí a modelových kľúčov.

```sh
uv run python experiments/nli/validation/run.py --recorded experiments/nli/validation/scores.json --out tmp/validation-replay.json
```

Nové meranie skutočným lokálnym modelom potrebuje extra `nli` a model v HF cache.
Pri prvom spustení si váhy stiahne.

```sh
uv sync --all-packages --extra nli
uv run --all-packages --extra nli python experiments/nli/validation/run.py
```

Príklady sú naviazané na konkrétne chunk ID a citácie v commitnutej Sphinx 9 XML
dokumentácii. Zmena citácie vyvolá chybu, namiesto tichého vynechania príkladu.
JSON zaznamenáva hash kontrolných prípadov, vstupných dokumentácií, model,
jeho pinned revíziu, verzie chunkera a grounding pravidiel aj presné premisy.
Rozhodovanie používa argmax. Počas merania sa nevolá žiadny vzdialený LLM.
Chýbajúci chunk sa hlási s číslom prípadu a knižnicou. Nesprávny počet kontrol
vyvolá explicitnú chybu aj s `python -O`. Výstupný priečinok sa vytvorí sám.
Nové živé meranie nahradí `scores.json` iba pármi z daného behu, bez starých
položiek z predchádzajúcej verzie prípadov; replay existujúce skóre nemení.

## Záver a ďalšie overenie

Model zvláda pripravené jednoduché kontroly aj API prose z ďalších dvoch
knižníc. Na pôvodných náročnejších ľudských príkladoch zostávajú nesprávne
ponechania aj vyradenia. Kontrolné dáta a pravidlá som po zhliadnutí skóre
nemenil. Nezávislé ľudské ohodnotenie reálnych extrakcií z novších runov
008/009 zostáva ďalším krokom. Existujúca stránka `labeling/build_008.py`
pripravuje slepú vzorku pre run 008.

Meranie vzniklo 2026-11-23 na CPU so štyrmi torch vláknami. Dňa 2026-11-24 som
po review prešiel na priamy core grounding a zopakoval replay na aktuálnom main;
počty v tabuľke aj identita jedného false keep ostali rovnaké. Opakovanie zo
skóre overuje reprodukovateľnosť, samostatné spustenie modelu môže mať malé
numerické odchýlky podľa prostredia.
