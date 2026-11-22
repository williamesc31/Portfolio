"""Create anonymous appointment aggregates from the recovered visitor-log ZIP."""
from pathlib import Path
from zipfile import ZipFile
import argparse,json,hashlib
import pandas as pd
BASE=Path(__file__).resolve().parent
PAIRS={'date':['APPT_START_DATE','Appointment Start Date'],
       'canceled':['APPT_CANCEL_DATE','Appointment Cancel Date'],
       'access':['ACCESS_TYPE','Access Type']}

def first_present(frame,columns):
    result=pd.Series(pd.NA,index=frame.index,dtype='string')
    for name in columns:
        if name in frame:
            values=frame[name].str.strip().replace('',pd.NA)
            result=result.fillna(values)
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('source_zip',type=Path);args=parser.parse_args()
    usecols={x for v in PAIRS.values() for x in v};parts=[];rows=0;invalid=0
    with ZipFile(args.source_zip) as archive:
        csv=next(n for n in archive.namelist() if n.lower().endswith('.csv'))
        with archive.open(csv) as source:
            for chunk in pd.read_csv(source,usecols=lambda c:c in usecols,dtype='string',chunksize=100000):
                rows+=len(chunk)
                date=pd.to_datetime(first_present(chunk,PAIRS['date']),format='mixed',errors='coerce')
                cancel=pd.to_datetime(first_present(chunk,PAIRS['canceled']),format='mixed',errors='coerce')
                good=date.notna()&date.dt.year.between(2009,2026);invalid+=int((~good).sum())
                ready=pd.DataFrame({'month':date[good].dt.strftime('%Y-%m'),
                    'weekday':date[good].dt.dayofweek,'canceled':cancel[good].notna(),
                    'access_type':first_present(chunk,PAIRS['access'])[good].fillna('Unknown')})
                parts.append(ready.groupby(['month','weekday','canceled','access_type'],dropna=False).size().rename('records').reset_index())
    result=pd.concat(parts).groupby(['month','weekday','canceled','access_type'],as_index=False)['records'].sum()
    (BASE/'data').mkdir(exist_ok=True)
    result.to_csv(BASE/'data/appointment_counts.csv',index=False)
    info={'source_archive':args.source_zip.name,'source_sha256':hashlib.sha256(args.source_zip.read_bytes()).hexdigest(),
        'source_records':rows,'excluded_missing_or_out_of_range_appointment_dates':invalid,'retained_records':int(result.records.sum()),
        'aggregation':'Appointment month, weekday, cancellation indicator, access type. No visitor names or identifiers retained.',
        'schema_handling':'Coalesce corresponding legacy and display-name columns; do not rename them into duplicate column labels.'}
    (BASE/'data/provenance.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info))
if __name__=='__main__':main()
