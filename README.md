# Data Science Portfolio

Applied machine learning, reproducible analysis, and data storytelling with an interest in financial services and customer experience.

**[Explore the portfolio website](https://williamesc31.github.io/Portfolio/)**

## Projects

Every project below contains a README, a runnable Python entry point, data or documented fixtures, and saved results. The ten default analysis commands passed end-to-end verification in Python 3.12. See [VERIFICATION.json](VERIFICATION.json) for the actual execution record, environment, and input/code hashes.

| Project | Focus | Source and results |
| --- | --- | --- |
| Credit Risk Default Prediction | Classification and the default-recall tradeoff | [Project](projects/credit-risk-prediction) |
| Bank Marketing Under Distribution Shift | Ordered validation, pre-call features, and model auditing | [Project](projects/bank-marketing-targeting) |
| Consumer Complaint Trends and Forecasting | CFPB label harmonization and seasonal baseline evaluation | [Project](projects/cfpb-complaint-forecasting) |
| Childcare Prices and Household Affordability | County prices and a consistent nominal-income denominator | [Project](projects/childcare-affordability) |
| Netflix Top 10 Engagement Analysis | Distinct viewing metrics and snapshot coverage | [Project](projects/netflix-engagement) |
| Airport Complaint Patterns | Volume trends, category totals, and denominator limits | [Project](projects/tsa-complaints) |
| Movie Discovery with Content Similarity | Genres, tags, TF-IDF, and cosine similarity | [Project](projects/movie-recommendations) |
| Lottery Frequencies Without Prediction Claims | Draw validation and descriptive frequencies | [Project](projects/lottery-number-analysis) |
| Public Appointment Log Analysis | Schema harmonization and anonymous aggregation | [Project](projects/white-house-visits) |
| Invoice Extraction and Arithmetic Validation | Supported-layout parsing and exact decimal checks | [Project](projects/invoice-extraction) |

## Run the portfolio analyses

Use Python 3.12. From the repository root:

```bash
python -m venv .venv
# Activate .venv using the command for your operating system.
python -m pip install -r requirements.txt
python scripts/run_all.py
```

For one project, run its `analyze.py` directly. All ten default commands use bundled snapshots or explicit fixtures. They require no API keys, paid model services, or GPUs. The visitor-log preparation script is an optional prior stage; its published aggregate snapshot is already included.

After rerunning the analyses, refresh the website catalog and README result summaries with:

```bash
python scripts/build_portfolio.py
```

## Repository layout

- `projects/<descriptive-name>/`: README, executable analysis, input snapshot, and outputs.
- `projects/common.py`: shared plotting and JSON helpers.
- `docs/`: GitHub Pages site, downloadable READMEs, and result illustrations.
- `scripts/`: repository-wide verification and documentation generation.
- `SOURCE_MANIFEST.json`: recovered input hashes and transformation notes.
- `PORTFOLIO_NOTES.md`: refactoring decisions and interpretation limits.

Dataset snapshots are fixed historical inputs. Their dates and scope are stated in each README. The MovieLens data retain the GroupLens usage conditions in [their data notice](projects/movie-recommendations/data/LICENSE.md); datasets are not relicensed as original portfolio code. Fictional invoice fixtures are labeled as regression examples. Fresh model results replace historical figures that could not be independently reproduced.

## Website and contact

The website includes About, Projects, and Contact sections and links directly to each project folder. GitHub Pages publishes the `docs` directory from `main`.

[GitHub profile](https://github.com/williamesc31) · [Repository](https://github.com/williamesc31/Portfolio)
