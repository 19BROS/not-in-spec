# Embeddingy pre diff a cross-checks — SCRUM-54

Zmeral som `sentence-transformers/all-MiniLM-L6-v2` na reálnych tvrdeniach runu
009 a na kontrolovaných úpravách textu dokumentácie. Odporúčanie je používať
embeddingy na výber kandidátov pre cross-checks. Pri rozhodovaní, čo znovu
spustiť po zmene dokumentácie, má zostať rozhodujúci obsahový hash a väzby
medzi chunkmi, tvrdeniami a testami.

## Cross-checks

Vstup tvorí 63 ponechaných tvrdení zo štyroch urllib3 chunkov. Medzi rôznymi
extraktormi v rámci rovnakého chunku existuje 280 párov. Pre 101 párov sú
v repozitári uložené skutočné NLI skóre v oboch smeroch. To je dnešný
prefilter podľa prekrývania premís. Tieto skóre dávajú 22 duplicít,
11 jednostranných entailmentov a 7 obojstranných NLI kontradikcií.

Každé tvrdenie vyberá top-k najpodobnejších tvrdení druhého extraktora
v rovnakom chunku. Pár sa použije, ak ho vyberie aspoň jedna strana.
Pri zhodnej podobnosti rozhoduje poradie vstupu.

| top-k | Vybrané páry z 280 | Zachované známe duplicity | Jednostranné entailmenty | NLI kontradikcie |
| --- | ---: | ---: | ---: | ---: |
| 1 | 35 | 22/22 | 7/11 | 0/7 |
| 2 | 80 | 22/22 | 11/11 | 7/7 |
| 3 | 117 | 22/22 | 11/11 | 7/7 |
| 5 | 186 | 22/22 | 11/11 | 7/7 |
| 8 | 255 | 22/22 | 11/11 | 7/7 |

Top-2 by na tejto vzorke potrebovalo 80 párov namiesto 101 dnešného
prefiltra, o 20,8 % menej. Všetky známe pozitívne NLI vzťahy zachovalo.
Je to výsledok na malom už použitom súbore, na ktorom sme skúšali aj k.
NLI skóre sú silver referencia. Podľa existujúcich testov sú tu všetky
kontradikcie falošné poplachy. Zachovanie týchto vzťahov preto neznamená
100 % recall skutočných problémov v dokumentácii. Pre zvyšných 179 párov
referencia chýba.

Pre K5b medzi chunkmi by som overil top-k výber v rámci celého projektu
na novej anotovanej vzorke. Tú tento experiment nemá. Do produkcie sa
žiadny nový prefilter nezapína a top-2 zatiaľ nie je potvrdené nastavenie.

## Diff a opakované spúšťanie

Po review som opravil dva prípady a meranie zopakoval. Zmena jednotky teraz
mení prose `the given number of seconds` na `the given number of milliseconds`;
signatúra `trio.sleep(seconds: float)` zostáva rovnaká. Negácia mení skoršie
`will not work by default` na `will work by default` v sekcii o TLS.
Všetkých päť úprav model vidí pred limitom 256 wordpieces a pri každej sa
menia skutočné vstupné tokeny, čo `results.json` kontroluje pre oba texty.

| Zmena | Cosine | Zmena v okne pred/po | Vstupné tokeny sa zmenili |
| --- | ---: | --- | --- |
| `True` → `False` | 0,997797 | áno / áno | áno |
| Jednotka v prose: sekundy → milisekundy | 0,983042 | áno / áno | áno |
| Odstránenie negácie v TLS prose | 0,996643 | áno / áno | áno |
| TLS 1.2 → TLS 1.0 | 0,999982 | áno / áno | áno |
| `ProxyManager` → `PoolManager` | 0,998233 | áno / áno | áno |
| Medzera navyše, formátovacia kontrola | 1,000000 | áno / áno | nie |
| Pôvodná negácia za limitom, kontrola skracovania | 1,000000 | nie / nie | nie |

Pravidlo „pri podobnosti aspoň 0,99 nič nespúšťaj“ by vynechalo **4 z 5**
viditeľných významových zmien; pri 0,95 by vynechalo všetkých päť. Zmena
jednotky je pod 0,99, takže pôvodný záver o piatich z piatich pri 0,99 bol
nesprávny. Cross-check výsledky v prvej tabuľke ostali po opakovaní rovnaké.

Pôvodnú negáciu `isn’t required` → `is required` na konci Client Certificates
ponechávam ako samostatný `truncation_control`: oba texty majú rovnakých prvých
256 tokenov, a preto nejde o meranie reakcie modelu na negáciu. Je uvedená
v `encoding_blind_spots` a nepočíta sa do `diff_skipping_audit` viditeľných zmien.

`content_hash_changed` je pri týchto riadených náhradách true z konštrukcie;
nie je to samostatný benchmark detektora. Ide o SHA-256 surového textu, preto
aj medzera navyše vynúti rerun. Takýto konzervatívny postup stojí výpočty navyše
pri formátovacích zmenách; produkcia má používať svoj existujúci `Chunk.content_hash`.

Odporúčaný postup pre diff:

1. Identita chunku a hash určia pridané, odstránené a zmenené vstupy.
2. Zmena obnoví všetky závislé tvrdenia a testy. Zmena verzií pravidiel
   alebo modelu musí tiež obnoviť dotknuté výsledky.
3. Embedding môže určiť poradie kontroly alebo navrhnúť súvisiace sekcie.
   Vysoká podobnosť sama nesmie vyradiť zmenený chunk z opakovaného behu.

## Reprodukcia

```sh
uv sync --all-packages --extra nli
uv run --all-packages --extra nli python experiments/embeddings/benchmark.py
```

Výsledky sú v `results.json`. Vektory zostávajú v gitignored
`tmp/embedding-vectors.json`. Opakovanie použije cache iba pri zhode
modelu, pinned revízie, všetkých vstupných textov a nastavení `ENCODING`
(limit, pooling, normalizácia, dtype, tokenizer, padding, truncation, batch a vlákna).
Zmena limitu alebo pooling už preto nepoužije staré vektory. Vymazanie tohto
jedného cache súboru vynúti nové kódovanie. Žiadny LLM kľúč sa nepoužíva.

Model používa revíziu `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, masked
mean pooling a L2 normalizáciu podľa [model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).
Limit je 256 wordpieces. Päť unikátnych dlhých vstupov bolo skrátených, čo je ďalší
dôvod nevyužívať podobnosť celej sekcie ako záruku nezmeneného významu.
Kódovanie po načítaní váh trvalo v opravenom behu 3,215 s na CPU so štyrmi
vláknami. Tento čas nezahŕňa stiahnutie ani načítanie modelu. Meranie
vzniklo 2026-11-23 a po review bolo zopakované 2026-11-24. Pri použití cache
je timing pôvodného kódovania, nie nové meranie výkonu; časy závisia od hardvéru.
