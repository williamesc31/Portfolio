"""Analyze anonymous aggregates of public White House appointment records."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import write_results,chart,plt
import pandas as pd
BASE=Path(__file__).resolve().parent

def main():
    df=pd.read_csv(BASE/'data/appointment_counts.csv')
    provenance=json.loads((BASE/'data/provenance.json').read_text())
    assert (df.records>0).all() and df.weekday.between(0,6).all()
    assert int(df.records.sum())==provenance['retained_records']
    monthly=df.groupby('month').records.sum().sort_index()
    weekdays=df.groupby('weekday').records.sum().reindex(range(7),fill_value=0)
    canceled=df.loc[df.canceled.astype(str).str.lower()=='true','records'].sum()
    monthly.rename('appointment_records').to_csv(BASE/'outputs/monthly_records.csv')
    fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    axes[0].plot(pd.to_datetime(monthly.index+'-01'),monthly.values);axes[0].set(title='Appointment records by month',xlabel='Appointment date',ylabel='Records')
    axes[1].bar(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],weekdays.values);axes[1].set(title='Appointment records by weekday',ylabel='Records')
    chart(BASE,'appointment_patterns.svg',fig)
    write_results(BASE,{'retained_records':int(df.records.sum()),'first_month':str(monthly.index.min()),'last_month':str(monthly.index.max()),
        'busiest_month':str(monthly.idxmax()),'canceled_record_share':float(canceled/df.records.sum()),'aggregate_rows':len(df),
        'excluded_date_records':provenance['excluded_missing_or_out_of_range_appointment_dates'],
        'limits':'Records describe appointments, not unique visitors, confirmed attendance, political influence, or access probability. Release practices and schema differences affect coverage.'})
if __name__=='__main__':main()
