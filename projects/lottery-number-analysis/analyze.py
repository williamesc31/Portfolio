"""Describe lottery snapshots; historical frequencies are not predictions."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import write_results,chart,plt
import pandas as pd
BASE=Path(__file__).resolve().parent

def main():
    rows=[];games={};fig,axes=plt.subplots(3,1,figsize=(10,8))
    for ax,(file,name,count) in zip(axes,[('powerball.csv','Powerball',5),('mega_millions.csv','Mega Millions',5),('pick_10.csv.gz','Pick 10',20)]):
        data=pd.read_csv(BASE/'data'/file);dates=pd.to_datetime(data['Draw Date'],errors='raise')
        numbers=data['Winning Numbers'].astype(str).str.split().map(lambda values:[int(v) for v in values[:count]])
        assert numbers.map(len).eq(count).all() and numbers.map(lambda x:len(set(x))).eq(count).all()
        obs=pd.Series([v for draw in numbers for v in draw],dtype=int);frequency=obs.value_counts().sort_index()
        ax.bar(frequency.index,frequency.values,width=.85);ax.set(title=f'{name}: observed main-number frequencies',xlabel='Number',ylabel='Occurrences')
        games[name]={'draws':len(data),'first_draw':str(dates.min().date()),'last_draw':str(dates.max().date()),'main_number_observations':len(obs),
            'most_frequent_observed_number':int(frequency.idxmax()),'most_frequent_count':int(frequency.max())}
        rows.extend({'game':name,'number':int(number),'occurrences':int(n)} for number,n in frequency.items())
    chart(BASE,'frequencies.svg',fig)
    pd.DataFrame(rows).to_csv(BASE/'outputs/frequencies.csv',index=False)
    write_results(BASE,{'games':games,'special_balls':'Excluded from main-number counts',
        'limits':'Games changed number pools and rules during these histories. Pooled counts are descriptive and are not a uniform-probability test, evidence of predictability, or a strategy for future draws.'})
if __name__=='__main__':main()
