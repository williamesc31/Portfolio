"""Generate consistent project READMEs and the static website project catalog."""
from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parents[1]
REPO='https://github.com/williamesc31/Portfolio'
CONFIG=[
 dict(id='credit',slug='credit-risk-prediction',name='Credit Risk Default Prediction',category='ml',label='CLASSIFICATION',
 description='Compare classification models while examining the tradeoff between default recall and overall accuracy.',
 question='How well can borrower and loan-pricing information identify default risk in a held-out dataset?',
 approach='Remove exact duplicates and invalid ages, handle impossible employment lengths, and engineer income and employment ratios. Fit imputation, scaling, and one-hot encoding only on the training partition. Compare logistic regression and a fixed Random Forest on a stratified 80/20 holdout.',
 tools='Python · pandas · scikit-learn · Classification pipelines',
 lesson='Higher accuracy does not guarantee better default recall. Loan interest rate is available at the pricing stage, so the prediction point must be stated.',
 source='Recovered credit_risk_dataset.csv, 32,581 records. This portfolio version was rebuilt and rerun from that CSV; it is not the original saved model. Original dataset attribution: Kaggle Credit Risk Dataset.',
 chart='model_comparison.svg'),
 dict(id='bank',slug='bank-marketing-targeting',name='Bank Marketing Under Distribution Shift',category='ml',label='TEMPORAL VALIDATION',
 description='Evaluate campaign targeting with pre-call features and ordered validation and test periods.',
 question='Do campaign models retain useful ranking performance when evaluated on later observations?',
 approach='Use 41,188 ordered UCI bank-marketing contacts. Exclude call duration, split the records 60/20/20 in their supplied order, fit preprocessing on training data, and select a model using validation average precision. Refit on earlier records and evaluate on the last period. Include cumulative gains and a descriptive age-group audit.',
 tools='Python · scikit-learn · Average precision · Model auditing',
 lesson='The validation period is difficult and response prevalence shifts sharply across periods. The model is not presented as ready for operational deployment or as proof of improved campaign outcomes.',
 source='UCI Bank Marketing, bank-additional-full.csv. https://archive.ics.uci.edu/dataset/222/bank+marketing . Adapted from the recovered bank-marketing analysis; paths were made project-relative and preprocessing instances isolated per model.',
 chart='figure2_test_discrimination.svg'),
 dict(id='cfpb',slug='cfpb-complaint-forecasting',name='Consumer Complaint Trends and Forecasting',category='analysis',label='TIME SERIES',
 description='Harmonize product labels and test a seasonal baseline against 2025 complaint counts.',
 question='How well does a same-month prior-year forecast track changes in published financial-product complaints?',
 approach='Validate a complete 96-month calendar from 2018 through 2025. Combine old and new credit-card product labels, summarize annual counts, and compare each 2025 month with its 2024 counterpart. Report MAE, RMSE, weighted absolute percentage error, and bias.',
 tools='Python · pandas · Time-series validation · Forecast evaluation',
 lesson='A reproducible baseline can still underforecast every month. Public complaint counts are not a measure of all customer problems or the number of unique consumers.',
 source='Recovered CFPB API aggregate snapshot, indexed November 15, 2026. Original query URLs are retained in data/monthly_counts.csv. Source: https://www.consumerfinance.gov/data-research/consumer-complaints/ . Refactored from the saved current-course analysis; no live API calls occur during reproduction.',
 chart='fig2_holdout.svg'),
 dict(id='childcare',slug='childcare-affordability',name='Childcare Prices and Household Affordability',category='analysis',label='AFFORDABILITY ANALYSIS',
 description='Connect county childcare prices to household income using a consistent dollar basis.',
 question='How do childcare prices and income burdens vary across counties and states in the saved snapshot?',
 approach='Use the recovered 23,342-row county-year subset. Annualize weekly infant-care prices and divide by nominal household income (MHI). Summarize unweighted county medians by study year and state, then distinguish price levels from affordability burden.',
 tools='Python · pandas · Data cleaning · Geographic comparisons',
 lesson='Mixing nominal prices with an inflation-adjusted income denominator changes the interpretation. County medians also should not be described as population-weighted statewide estimates.',
 source='U.S. Department of Labor National Database of Childcare Prices, recovered 2008–2018 analysis subset. https://www.dol.gov/agencies/wb/topics/featured-childcare . The subset already excludes counties missing the required care-price measures. Rebuilt from the recovered analysis notebook and CSV with a corrected income denominator.',
 chart='affordability.svg'),
 dict(id='netflix',slug='netflix-engagement',name='Netflix Top 10 Engagement Analysis',category='analysis',label='DATA STORYTELLING',
 description='Separate watch-time, views, and title persistence in a saved Netflix Top 10 snapshot.',
 question='What do the saved Top 10 lists show about category watch-time and the reach of popular titles?',
 approach='Convert the recovered source workbooks to CSV, check rank-key uniqueness, identify title-season combinations, and summarize category hours. Analyze the most-popular first-91-day table separately from weekly records. Dates are derived from the actual files.',
 tools='Python · pandas · Data validation · Visual storytelling',
 lesson='Top 10 data describe selected titles. They do not cover the entire catalog, and hours, weekly views, and first-91-day views should not be combined as one metric.',
 source='Netflix Tudum Global Top 10 and Most Popular source workbooks recovered from the earlier data story. https://www.netflix.com/tudum/top10/ . Weekly snapshot coverage is July 2021–April 2024. The published CSVs retain the original workbook records; source hashes are in SOURCE_MANIFEST.json.',
 chart='engagement.svg'),
 dict(id='tsa',slug='tsa-complaints',name='Airport Complaint Patterns',category='analysis',label='SERVICE OPERATIONS',
 description='Explore complaint trends and category concentration while distinguishing volume from service rates.',
 question='Where are complaint counts concentrated, and how do they change over time?',
 approach='Parse monthly airport records, create a three-month moving average, and rank airports by total recorded complaints. Aggregate the recovered category table by month and cleaned category label, then reconcile its total with the airport table.',
 tools='Python · pandas · Aggregation · Service-quality analysis',
 lesson='Complaint counts need passenger-volume denominators before they can support airport service-rate comparisons. Totals can be reconciled without claiming a causal explanation.',
 source='Recovered complaints-by-airport(1).csv and complaints-by-category(1).csv from the earlier TSA data-story project. Category airport detail is aggregated before publication. Original file hashes and transformation notes are in SOURCE_MANIFEST.json. A definitive original download URL was not retained in the recovered source files.',
 chart='complaints.svg'),
 dict(id='movies',slug='movie-recommendations',name='Movie Discovery with Content Similarity',category='ml',label='RECOMMENDATION SYSTEMS',
 description='Recommend movies using TF-IDF representations of genres and user-generated tags.',
 question='Which movies have similar genre and tag content to a selected title?',
 approach='Validate MovieLens movie and tag schemas, aggregate tags by movie, build unigram and bigram TF-IDF features, and rank candidates by cosine similarity. Exclude the query movie and use deterministic ID-based tie-breaking.',
 tools='Python · scikit-learn · TF-IDF · Cosine similarity',
 lesson='The recovered file called ratings.csv is a tags table. The implementation therefore uses content similarity and does not claim collaborative-filtering performance or predictive recommendation accuracy.',
 source='GroupLens MovieLens latest-small. https://grouplens.org/datasets/movielens/latest/ . Recovered movies(1).csv and the tags table mislabeled ratings.csv. Data remain under the GroupLens usage conditions linked in data/LICENSE.md. Attribution: Harper, F. M., and Konstan, J. A. (2015), The MovieLens Datasets: History and Context, https://doi.org/10.1145/2827872 .',
 chart='recommendations.svg'),
 dict(id='lottery',slug='lottery-number-analysis',name='Lottery Frequencies Without Prediction Claims',category='analysis',label='STATISTICAL COMMUNICATION',
 description='Describe historical main-number frequencies and explain why apparent patterns are not forecasts.',
 question='What descriptive patterns appear in the saved draw histories, and what cannot be inferred from them?',
 approach='Parse draw dates and winning-number fields for Powerball, Mega Millions, and Pick 10. Check the expected number of unique main balls in each draw, exclude special balls, and summarize observed frequencies and coverage dates.',
 tools='Python · pandas · Validation · Statistical visualization',
 lesson='Game rules and eligible number pools changed across these histories. Pooled counts do not establish predictability and are not used as future-draw probability estimates.',
 source='New York Open Data lottery draw CSVs recovered from the earlier lottery data-story project. https://data.ny.gov/ . The saved filenames identify the April 21, 2024 export. This portfolio script refactors the original notebook into a reproducible descriptive analysis.',
 chart='frequencies.svg'),
 dict(id='visits',slug='white-house-visits',name='Public Appointment Log Analysis',category='analysis',label='SCHEMA HARMONIZATION',
 description='Coalesce two log schemas and analyze anonymous appointment aggregates.',
 question='What appointment patterns remain visible after harmonizing the source columns and removing personal identifiers?',
 approach='Stream the recovered 1.2-million-record CSV inside its ZIP. Coalesce matching legacy and display-name date columns rather than renaming them into duplicate labels. Aggregate appointment month, weekday, cancellation indicator, and access type. Publish only aggregate counts.',
 tools='Python · Chunked CSV loading · Schema repair · Aggregation',
 lesson='Appointments are not unique visitors or confirmed attendance. Aggregating the source supports reproducible trend analysis while omitting names and identifiers from the repository.',
 source='Recovered white_house_combined_download.zip from the earlier visitor-log project. The source archive hash and row counts are retained in data/provenance.json. Only anonymous aggregates are published. prepare_snapshot.py can regenerate the aggregate snapshot when the original ZIP is supplied.',
 chart='appointment_patterns.svg'),
 dict(id='invoice',slug='invoice-extraction',name='Invoice Extraction and Arithmetic Validation',category='text',label='STRUCTURED TEXT',
 description='Convert a documented invoice text layout into structured JSON and reject inconsistent totals.',
 question='Can invoice fields and line items be extracted into a consistent structure with verifiable arithmetic?',
 approach='Use anchored field extraction, an explicit quantity/description/unit-price grammar, ISO date checks, and Decimal arithmetic. Process three fictional valid fixtures and verify that a deliberately inconsistent total is rejected. Return structured JSON for a supplied text file.',
 tools='Python · Regular expressions · Decimal · Data validation',
 lesson='A schema and arithmetic checks make extraction errors visible. This release supports a defined text layout and does not claim OCR, arbitrary-layout handling, or LLM benchmark performance.',
 source='A new local portfolio implementation based on earlier invoice-extraction coursework. The bundled invoices are explicitly fictional fixtures created for regression checks. The earlier paid-API notebook is not required or represented as tested in this release.',chart=None)
]

def result_text(project,r):
    key=project['id']
    if key=='credit':
        rf=r['models']['random_forest'];lr=r['models']['logistic_regression']
        return f"On {r['test_rows']:,} held-out records, Random Forest achieved {rf['test_accuracy']:.1%} accuracy, {rf['test_roc_auc']:.3f} ROC-AUC, and {rf['default_recall']:.1%} default recall. Logistic regression achieved {lr['test_accuracy']:.1%} accuracy and {lr['default_recall']:.1%} default recall. These are fresh portfolio-run results, not the historical figures from an earlier notebook."
    if key=='bank':
        chosen=r['selected_by_validation_avg_precision'];v=r['validation'][chosen];t=r['test'][chosen]
        return f"{chosen} was selected by validation average precision ({v['avg_precision']:.3f}, versus a {r['data']['splits']['validation']['rate']:.3f} validation response rate). Its later-period ROC-AUC was {t['roc_auc']:.3f}. Selecting the top 20% captured {t['top20']['capture']:.1%} of subscriptions in that test period. The weak validation result is a material limitation."
    if key=='cfpb':
        a=r['baseline_2025']['credit_card'];b=r['baseline_2025']['checking_savings']
        return f"The 2025 seasonal baseline had {a['wape_pct']:.1f}% weighted absolute percentage error for credit cards and {b['wape_pct']:.1f}% for checking/savings. Both product series were underforecast in all 12 months. The snapshot covers {r['months']} months."
    if key=='childcare':return f"The saved subset contains {r['analysis_rows']:,} county-year rows covering {r['year_start']}–{r['year_end']}. In {r['year_end']}, the median county weekly center-infant price was ${r['latest_median_weekly_center_infant']:,.2f}; the median annualized-price-to-nominal-income ratio was {r['latest_median_burden_pct']:.1f}%."
    if key=='netflix':return f"The weekly snapshot has {r['weekly_rows']:,} records and {r['distinct_title_seasons']:,} title-season combinations, from {r['first_week']} through {r['last_week']}. {r['top_first_91_day_title']} leads the saved most-popular table by first-91-day views. Weekly views are available in only {r['weeks_with_views']} weeks."
    if key=='tsa':return f"The airport snapshot records {r['total_airport_complaints']:,} complaints across {r['airports']} airport codes from {r['first_month']} through {r['last_month']}. The ten largest airport totals account for {r['top_10_airports_share']:.1%} of the volume. Airport and category totals reconcile."
    if key=='movies':return f"The content index covers {r['movies']:,} movies and {r['tag_rows']:,} tag records. For {r['query']}, the highest-ranked recommendation is {r['recommendations'][0]['title']} with cosine similarity {r['recommendations'][0]['similarity']:.3f}. This is a similarity demonstration, not a held-out accuracy score."
    if key=='lottery':return 'The snapshot contains '+', '.join(f"{v['draws']:,} {name} draws" for name,v in r['games'].items())+'. Each draw passes the configured main-ball count and within-draw uniqueness checks. Frequencies are reported without predictive claims.'
    if key=='visits':return f"The aggregate snapshot accounts for {r['retained_records']:,} appointment records from {r['first_month']} through {r['last_month']}, using {r['aggregate_rows']} aggregate rows. No individual visitor names or identifiers are published."
    return f"All {r['valid_fixtures_processed']} valid fictional fixtures were processed, and the inconsistent-total fixture was rejected. These are regression checks for supported layouts, not a real-world extraction benchmark."

def main():
    web=[]
    for project in CONFIG:
        folder=ROOT/'projects'/project['slug'];r=json.loads((folder/'outputs/results.json').read_text())
        result=result_text(project,r)
        chart=project.get('chart')
        readme=f"# {project['name']}\n\n{project['description']}\n\n## Question\n\n{project['question']}\n\n## Approach\n\n{project['approach']}\n\n## Reproduce\n\nFrom the repository root, using Python 3.12:\n\n```bash\npython -m pip install -r requirements.txt\npython projects/{project['slug']}/analyze.py\n```\n\nThe default command uses bundled snapshots, writes `outputs/results.json`, and requires no API key, GPU, or live data service. Shared chart and JSON helpers are in `projects/common.py`.\n\n## Verified results\n\n{result}\n\nThe saved machine-readable results are in [outputs/results.json](outputs/results.json). Repository-wide execution evidence and input/code hashes are in [VERIFICATION.json](../../VERIFICATION.json).\n"
        if chart:readme+=f"\n![{project['name']} results](outputs/{chart})\n"
        readme+=f"\n## Interpretation and limitations\n\n{project['lesson']}\n\n## Data and provenance\n\n{project['source']}\n\n## Tools\n\n{project['tools']}\n"
        if project['id']=='movies':readme+='\nTo query a different movie, pass `--title "Jumanji (1995)"`. The title must exactly match `data/movies.csv.gz`.\n'
        if project['id']=='invoice':readme+='\nTo parse another supported text invoice, pass `--input path/to/invoice.txt`. Input fields and the line-item layout are demonstrated in `data/invoice_001.txt`. Invalid or inconsistent inputs raise a clear error.\n'
        (folder/'README.md').write_text(readme)
        dest=ROOT/'docs/readmes'/f"{project['slug']}.md";dest.parent.mkdir(exist_ok=True);dest.write_text(readme.replace('](outputs/',f']({REPO}/blob/main/projects/{project["slug"]}/outputs/').replace('](../../VERIFICATION.json)',f']({REPO}/blob/main/VERIFICATION.json)'))
        entry={k:v for k,v in project.items() if k not in ('source','chart')}
        entry['result']=result;entry['readme']=f"readmes/{project['slug']}.md";entry['repository']=f"{REPO}/tree/main/projects/{project['slug']}"
        if chart:
            image=ROOT/'docs/assets'/f"{project['slug']}.svg";image.parent.mkdir(exist_ok=True)
            shutil.copyfile(folder/'outputs'/chart,image);entry['image']=f"assets/{project['slug']}.svg"
        web.append(entry)
    (ROOT/'projects/catalog.json').write_text(json.dumps(web,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'docs/projects-data.js').write_text('const projects = '+json.dumps(web,indent=2,ensure_ascii=False)+';\n')
    print('Generated 10 project READMEs, downloads, and the website catalog.')
if __name__=='__main__':main()
