"""Describe the saved Netflix Global Top 10 snapshot without mixing metrics."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import write_results,chart,plt
import pandas as pd
BASE=Path(__file__).resolve().parent

def main():
    df=pd.read_csv(BASE/'data/weekly_global.csv.gz',parse_dates=['week'])
    popular=pd.read_csv(BASE/'data/most_popular.csv')
    assert not df.duplicated(['week','category','weekly_rank']).any()
    assert df.weekly_rank.between(1,10).all() and (df.weekly_hours_viewed>=0).all()
    df['title_id']=df.show_title+df.season_title.fillna('').map(lambda x:' — '+x if x else '')
    category=df.groupby('category').agg(hours=('weekly_hours_viewed','sum'),listed_records=('weekly_rank','size'))
    title=df.groupby(['category','title_id']).agg(hours=('weekly_hours_viewed','sum'),listed_weeks=('week','nunique'),max_cumulative_weeks=('cumulative_weeks_in_top_10','max')).reset_index()
    category.to_csv(BASE/'outputs/category_hours.csv');title.sort_values('hours',ascending=False).to_csv(BASE/'outputs/title_summary.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(12,5))
    (category.hours.sort_values()/1e9).plot.barh(ax=axes[0]);axes[0].set(title='Hours among listed Top 10 records',xlabel='Billions of hours',ylabel='')
    top=popular.nlargest(10,'views_first_91_days').sort_values('views_first_91_days')
    labels=top.show_title.str.slice(0,24)+top.season_title.fillna('').map(lambda x:' / '+x[:12] if x else '')
    axes[1].barh(labels,top.views_first_91_days/1e6);axes[1].set(title='Saved most-popular snapshot',xlabel='First 91-day views (millions)')
    chart(BASE,'engagement.svg',fig)
    write_results(BASE,{'weekly_rows':len(df),'first_week':str(df.week.min().date()),'last_week':str(df.week.max().date()),
        'distinct_title_seasons':len(title),'categories':category.reset_index().to_dict('records'),
        'top_first_91_day_title':str(popular.loc[popular.views_first_91_days.idxmax(),'show_title']),
        'weeks_with_views':int(df.loc[df.weekly_views.notna(),'week'].nunique()),
        'limits':'Top 10 inclusion is a selected sample, not all Netflix viewing. Hours, weekly views, and first-91-day views measure different things. Snapshot dates are read from the data.'})
if __name__=='__main__':main()
