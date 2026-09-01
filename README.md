# tehillim-texttype

Text-type analysis of all 150 psalms from BHSA's `txt` feature, extending an analysis van Peursen
published on two psalms.

## The question

Van Peursen, *Tracing Text Types in Biblical Hebrew* (Vetus Testamentum 70, 2020), argues that
text type in Biblical Hebrew is defined by syntax rather than by genre, and demonstrates it with
four hand-set tables: Judges 9:54, Genesis 43:32, Psalm 105:1-11 and Psalm 64:2-8. His Psalm 105
table shows a quotation opening into narrative and then into a further quotation, giving the
sequence Q, QN, QNQ.

The article presents examples. This repository asks the same question across the Psalter.

## The data

`txt` is a BHSA clause feature holding the full text-type string, where each character records one
level of embedding and the last character is the `domain` feature. `Q` is quotation, `N` is
narrative, `D` is discursive, `?` marks a clause whose text type syntax does not decide. A clause
labelled `QNQ` is a quotation inside a narrative inside a quotation.

The rule programs that compute `txt` belong to the ETCBC and are not published. This repository
reads the feature and does not reproduce it.

## Findings

Run against BHSA 2021.

**The corpus is 7,283 clauses carrying 37 distinct text-type strings.**

| `txt` | clauses | share | psalms |
|---|---|---|---|
| `Q` | 5,533 | 76.0% | 142 |
| `QN` | 437 | 6.0% | 50 |
| `?` | 366 | 5.0% | 122 |
| `QQ` | 274 | 3.8% | 54 |
| `?Q` | 115 | 1.6% | 9 |
| `QND` | 88 | 1.2% | 17 |
| `QNQ` | 73 | 1.0% | 11 |
| `NQND` | 59 | 0.8% | 1 |

Embedding runs to depth five. Clause counts by depth: 5,947 at one, 944 at two, 276 at three, 108
at four, 8 at five.

**A psalm is rarely one text type.** 706 transitions occur across 138 of the 150 psalms. Twelve
psalms are uniform: Psalm 1 is `D` throughout, Psalm 133 is `?` throughout, and ten others are `Q`
throughout (43, 111, 112, 113, 117, 135, 146, 147, 149, 150).

**Transitions into narrative carry the formal marker van Peursen names, in 120 of 128 cases.** He
states that a wayyiqtol marks the shift to `N`. Of the 128 transitions into `QN`, 111 land on a
clause containing a wayyiqtol and 9 more land on a clause containing a wayyiqtol together with a
verb of speaking. Eight land on a clause carrying neither marker. This module registers which
markers are present and does not assign a cause.

**`txt` values changed between BHSA versions.** Comparing 4b, the version cited in the article,
against 2021: 97 clause positions differ, 1.3% of the Psalter, confined to Psalms 24, 64, 78, 97
and 107. One of them is Psalm 64:8, which the article prints as `QN` and which BHSA has read as `N`
since version `c`. The clause is the one where the article observes that "many Bible translations
do not recognize the 'narrative' character of the wayyiqtol form and translate here with a future
tense, thus e.g. RSV."

Psalm 105:1-11 reproduces the published table exactly.

## Layout

| path | contents |
|---|---|
| `src/library/bhsa.py` | loads a BHSA version from the local clone |
| `src/texttype/corpus.py` | the Psalter's clauses with their text-type strings |
| `src/texttype/inventory.py` | attested text-type strings, by clause and psalm frequency |
| `src/texttype/profile.py` | per-psalm composition as a matrix over the attested strings |
| `src/texttype/transitions.py` | where the text type changes between consecutive clauses |
| `src/texttype/triggers.py` | formal markers present in a clause, registered without a cause |
| `src/texttype/drift.py` | text-type differences for one clause position across two versions |

A clause position is identified by psalm, verse and index within the verse, so it resolves across
BHSA versions where node numbers do not.

## Usage

```bash
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
```

```bash
.venv/bin/python -m texttype.scripts.report
.venv/bin/python -m texttype.scripts.transition_markers --to QN
.venv/bin/python -m texttype.scripts.compare_versions 4b 2021
```

BHSA is read from `~/Developer/hebrew/bhsa/tf/<version>`. The whole-Psalter analysis takes 26
milliseconds after the corpus loads.

## Test

```bash
.venv/bin/pytest && .venv/bin/ruff check . && .venv/bin/mypy --strict src
```

## Citations

**Text-type analysis**

> van Peursen, Wido. "Tracing Text Types in Biblical Hebrew." *Vetus Testamentum* 70, no. 1 (2020):
> 140-155. https://doi.org/10.1163/15685330-12341394.

**Hebrew text and linguistic annotations**

> van Peursen, Willem Th., C. J. Sikkel, and Dirk Roorda. *Hebrew Text Database ETCBC4b*. Version
> 2. Amsterdam: DANS Data Station Social Sciences and Humanities, 2015.
> https://doi.org/10.17026/dans-z6y-skyh. Licensed CC BY-NC 4.0.

**Software used to read that dataset**

> Roorda, Dirk. *Text-Fabric*. Zenodo. https://doi.org/10.5281/zenodo.592193.

The BHSA licence is non-commercial and requires attribution through the persistent identifier
above, so any reuse of this work inherits that condition.

## Family

* [tehillim](https://github.com/rdtaylorjr/tehillim): computational analysis of the Hebrew psalms
* [tehillim-embeddings](https://github.com/rdtaylorjr/tehillim-embeddings): representation vectors
* [tehillim-benchmarks](https://github.com/rdtaylorjr/tehillim-benchmarks): evaluation
* [bhsa](https://github.com/etcbc/bhsa): the core text and linguistic annotation

## License

MIT

## Author

* [Russell D. Taylor Jr.](mailto:rdtaylorjr@gatech.edu)
