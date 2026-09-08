# tehillim-texttype

## Overview

This repository audits the text-type analysis encoded in the ETCBC BHSA across the 150 Psalms. It extends a published close reading of selected passages into a corpus analysis of clause-level text-type strings, their nesting depth, transitions, relation to received textual divisions, and relation to a supplied psalm-genre classification. The project treats text type as a syntactic registration that can be tested against literary and editorial phenomena without collapsing those phenomena into the same category.

## Data

The input is BHSA's clause-level `txt` feature. Each string records nested text-type domains. `Q`, `N`, and `D` represent quotation, narrative, and discursive domains. The terminal character is the innermost domain. `QNQ`, for example, records a quotation embedded in narrative embedded in quotation. `?` marks a level the ETCBC analysis does not decide.

The 2021 Hebrew Psalms contain 7,283 clauses and 37 attested text-type strings. The repository also reads a runtime CSV that assigns one genre label to each psalm and compares BHSA versions through stable coordinates of book, chapter, verse, and clause index. It includes transcribed published tables for a version-aware replication check.

The `txt` feature is a database analysis whose rule programs are not distributed here. The project reads its results, registers their distribution, and makes its historical variation visible. It cannot independently reproduce the underlying rule system. In particular, undecided values, embedding boundaries, and clause segmentation are facts about an ETCBC analysis that require separate philological assessment.

## Methodology

The pipeline extracts all clauses in canonical order and counts full `txt` strings, terminal domains, and nesting depths. It constructs normalized psalm profiles over the observed strings, detects transitions only between consecutive clauses within a chapter, and distinguishes an entry into a new level, a return from one, and a same-depth switch. It records wayyiqtol, yiqtol, imperative, verbum dicendi, and vocative markers at the receiving clause without treating a marker as a causal explanation.

Cross-book comparison uses clauses rather than chapters as the primary denominator because a psalm and a modern chapter division do not function as equivalent textual units. Transition rates, domain shares, mean nesting depth, and undecided rates are therefore reported per clause. The boundary analysis compares the share of text-type transitions landing at a verse or half-verse beginning with the base rate at which any clause begins that container. Its 95 percent percentile intervals resample chapters, retaining dependence among clauses within the same chapter.

Genre separation calculates Euclidean distances among normalized text-type profiles, then compares same-genre and different-genre psalm pairs through an AUC statistic. A 2,000-draw psalm-label permutation supplies the null. Quotation-opening analysis tests whether a clause opening a quotation level follows a preceding verbum dicendi. Published examples are checked against the BHSA 4b version, then compared with later releases. Each procedure starts with the database's formal representation before extending a claim to genre, division, or literary function.

## Results

The distribution is strongly concentrated in `Q`, which accounts for 5,533 clauses or 76.0 percent. Nesting runs to depth five. The corpus contains 706 text-type transitions across 138 psalms. Twelve psalms are uniform under this feature.

The results separate several patterns that a pooled text-type label would obscure:

| Observation | Result |
| --- | --- |
| Narrative-level entries | 134 entries, all landing on a wayyiqtol clause |
| Undecided clauses | 630 clauses, 287 in a psalm's first verse |
| Verse-boundary lift in Psalms | 11.4 percentage points, 95 percent interval 7.5 to 15.3 |
| Half-verse-boundary lift in Psalms | 5.7 percentage points, 95 percent interval 1.7 to 9.5 |
| Full-profile genre separation | AUC 0.537, permutation p 0.059 |
| Depth plus transition-rate genre separation | AUC 0.519, permutation p 0.177 |

The profile result is weak and the two structural summary measures do not clear the stated permutation test. The observed genre-related signal is concentrated in the `Q` share, a result compatible with the syntactic conditions under which the database assigns `Q`. It does not show that text-type profile recovers a genre taxonomy.

BHSA 4b reproduces the distinct text-type values of every held published example. Later versions differ at one published verse, Psalm 64:8, where the feature changed from `QN` to `N`. This is recorded as versioned database variation rather than treated as an error in the publication or a correction by this repository.

## Limitations

The analysis inherits the ETCBC's clause segmentation and text-type labels. A syntactic label provides a disciplined register of formal configuration, yet it does not by itself identify speaker, genre, rhetorical function, editorial layer, or the literary status of a superscription. The concentration of undecided values in psalm openings makes this constraint unusually visible. First verse is an observable proxy for superscription, not a definition of it.

Cross-book measures remain conditional on corpus composition, preservation of divisions, and the comparability of the selected books. Bootstrap intervals address chapter clustering and do not resolve these conceptual differences. The genre test uses a single supplied label per psalm, so mixed forms and disputed classifications disappear from the target. Association with a received division or a genre label supplies a constrained external check, not validation of either analysis.

Version comparison identifies where a database decision changed. It does not establish that either version is correct. A future audit should use a publicly reviewable clause sample, record competing analyses and unresolved cases, and compare text-type patterns with independently registered syntactic and prosodic divisions. This would test the scope of the feature while preserving disagreement as data.

## Reproducibility

The repository requires Python 3.12 or later, Text-Fabric, and NumPy. BHSA versions are read from a local Text-Fabric checkout, with `4b` available for published-table replication and `2021` used for the reported corpus inventory. The test suite has a 95 percent coverage threshold and treats numerical warnings as errors. Scripts accept explicit version, label-file, and output paths. Fixed seeds govern the bootstrap and permutation procedures.

## Installation

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Usage

```bash
.venv/bin/python -m texttype.scripts.replicate --version 4b
.venv/bin/python -m texttype.scripts.report --book Psalmi
.venv/bin/python -m texttype.scripts.genre_separation /path/to/genre-labels.csv
.venv/bin/python -m texttype.scripts.compare_versions 4b 2021
.venv/bin/python -m pytest tests
```

## References

Efron, Bradley. 1979. [“Bootstrap Methods: Another Look at the Jackknife.”](https://doi.org/10.1214/aos/1176344552) *The Annals of Statistics* 7.1: 1-26.

Bergström, Ulf. [“Reported Direct Speech in the Hebrew Bible and in the Andersen-Forbes Morphology and Syntax Database.”](https://doi.org/10.25159/2663-6573/9319) *Journal for Semitics* 30, no. 2 (2022).

Bosman, Hendrik Jan, and Constantijn J. Sikkel. “A Discourse on Method: Basic Parameters of Computer-Assisted Linguistic Analysis on Word Level.” Pages 85-113 in *Corpus Linguistics and Textual History: A Computer-Assisted Interdisciplinary Approach to the Peshitta*. Assen: Van Gorcum, 2006.

Good, Phillip I. 2000. [*Permutation Tests: A Practical Guide to Resampling Methods for Testing Hypotheses*](https://doi.org/10.1007/978-1-4757-3235-1). Springer.

Kalkman, Gino J. *Verbal Forms in Biblical Hebrew Poetry: Poetic Freedom or Linguistic System?* PhD diss., Amsterdam, 2015.

Montaner, Luis Vegas. “Masoretic Tradition and Syntactic Analysis of the Psalms.” Pages 317-335 in *Tradition and Innovation in Biblical Interpretation: Studies Presented to Professor Eep Talstra on the Occasion of His Sixty-Fifth Birthday*, 2011.

Talstra, Eep. “Singers and Syntax: On the Balance of Grammar and Poetry in Psalm 8.” Pages 11-22 in *Give Ear to My Words: Psalms and Other Poetry in and around the Hebrew Bible*, 1996.

Van Peursen, Wido. [“Tracing Text Types in Biblical Hebrew.”](https://doi.org/10.1163/15685330-12341430) *Vetus Testamentum* 70.1 (2020): 140-155.

Van Peursen, Wido. [“A Computational Approach to Syntactic Diversity in the Hebrew Bible.”](https://doi.org/10.28977/jbtr.2019.4.44.237) *Journal of Biblical Text Research* 44 (2019): 237-253.

Van Peursen, Willem Th., C. J. Sikkel, and Dirk Roorda. [*Hebrew Text Database ETCBC4b*](https://doi.org/10.17026/dans-z6y-skyh). DANS, 2015.

Roorda, Dirk. [“Text-Fabric: Handling Biblical Data with IKEA Logistics.”](https://doi.org/10.7146/hn.v5i2.142740) *HIPHIL Novum* 5.2 (2019): 126-135.

## License

MIT. The BHSA data are licensed separately under CC BY-NC 4.0.
