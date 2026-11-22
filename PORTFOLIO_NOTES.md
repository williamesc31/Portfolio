# Portfolio release notes

This release replaces the earlier milestone shell with ten executable portfolio projects. Entries without recoverable working code were replaced by stronger projects recovered from earlier coursework.

## Reproduction scope

Each default analysis command runs with the repository snapshots and the packages in requirements.txt. Commands resolve their input paths relative to their script, so they do not depend on a machine-specific working directory. There are no API keys, paid endpoints, GPU requirements, or runtime dataset downloads in the ten default workflows.

Some pipelines were refactored or rebuilt for this portfolio release rather than recovered byte-for-byte from old notebooks. In particular, credit-risk modeling was rebuilt from the recovered CSV; movie discovery uses genres and tags because the recovered file labeled ratings.csv is a tags table; invoice extraction is a local parser with fictional fixtures. Those scopes are described in the project READMEs. Historical model metrics and missing fine-tuned model artifacts are not presented as verified results of this release.

## Data repairs and interpretation

- Credit risk removes exact duplicate records and invalid ages, and imputes impossible employment lengths. All learned preprocessing is fitted only on training data.
- Bank marketing excludes call duration and separates ordered training, validation, and test periods. Weak validation performance and shifts in response rates are reported rather than hidden.
- CFPB preserves the saved 96-month snapshot and its source-query URLs, including the harmonization of older credit-card labels.
- Childcare uses nominal MHI with nominal childcare prices rather than mixing those prices with the inflation-adjusted MHI_2018 denominator.
- Netflix derives dates from its actual 2021–2024 snapshot and keeps hours, weekly views, and first-91-day views distinct.
- TSA reports counts rather than passenger-adjusted complaint rates.
- Movie recommendations use content similarity; no collaborative-filtering or predictive-accuracy claim is made.
- Lottery frequencies exclude special balls and are descriptive. Changes in game rules preclude a pooled uniform-probability interpretation.
- White House data coalesce the two source schemas. Only anonymous aggregates are published; individual names and identifiers are omitted.
- Invoice fixtures test layout parsing, ISO dates, and exact decimal arithmetic. They are regression examples, not a real-world extraction benchmark or an LLM evaluation.

The final website links directly to each project folder and its reproducible results. The Contact section links to the supplied GitHub identity; no email address has been inferred from commit metadata.

Larger source CSV snapshots are stored with lossless gzip compression; pandas reads them directly. Published summaries still use plain JSON, CSV, and SVG.
