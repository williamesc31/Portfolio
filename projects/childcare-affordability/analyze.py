"""Summarize the recovered county-year childcare price snapshot."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import write_results,chart,plt
import pandas as pd
import numpy as np
BASE=Path(__file__).resolve().parent

def main():
    df=pd.read_csv(BASE/'data/childcare.csv.gz')
    numeric=['StudyYear','MHI','MCInfant','MFCCInfant']
    for col in numeric:df[col]=pd.to_numeric(df[col],errors='coerce')
    usable=df.dropna(subset=numeric).query('MHI > 0 and MCInfant >= 0 and MFCCInfant >= 0').copy()
    assert len(usable)>0 and usable.StudyYear.nunique()>1
    # MHI is nominal household income. Do not divide a nominal price by MHI_2018.
    usable['annual_center_infant']=usable.MCInfant*52
    usable['affordability_pct']=100*usable.annual_center_infant/usable.MHI
    trend=usable.groupby('StudyYear')[['MCInfant','MFCCInfant']].median()
    latest_year=int(usable.StudyYear.max()); latest=usable[usable.StudyYear==latest_year]
    states=latest.groupby('State_Name').agg(median_weekly_price=('MCInfant','median'),median_burden_pct=('affordability_pct','median'),counties=('County_FIPS_Code','nunique'))
    states.sort_values('median_weekly_price',ascending=False).to_csv(BASE/'outputs/state_summary.csv')
    trend.to_csv(BASE/'outputs/price_trend.csv')
    fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    trend.rename(columns={'MCInfant':'Center infant','MFCCInfant':'Family child care infant'}).plot(ax=axes[0],marker='o')
    axes[0].set(title='Median county weekly prices',xlabel='Study year',ylabel='Nominal dollars per week')
    states.median_burden_pct.nlargest(10).sort_values().plot.barh(ax=axes[1])
    axes[1].set(title=f'County-median burden by state, {latest_year}',xlabel='Annual price / nominal household income (%)',ylabel='')
    chart(BASE,'affordability.svg',fig)
    write_results(BASE,{'source_rows':len(df),'analysis_rows':len(usable),'year_start':int(usable.StudyYear.min()),'year_end':latest_year,
        'latest_counties':int(latest.County_FIPS_Code.nunique()),'latest_median_weekly_center_infant':float(latest.MCInfant.median()),
        'latest_median_burden_pct':float(latest.affordability_pct.median()),'income_denominator':'MHI (nominal), not inflation-adjusted MHI_2018',
        'limits':'The saved snapshot is already filtered to counties with both infant-price measures. County medians are unweighted, not population-weighted state estimates.'})
if __name__=='__main__':main()
