"""Analyze airport complaint counts and category concentrations."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import write_results,chart,plt
import pandas as pd
BASE=Path(__file__).resolve().parent

def main():
    airport=pd.read_csv(BASE/'data/complaints_by_airport.csv.gz')
    category=pd.read_csv(BASE/'data/monthly_categories.csv')
    airport['date']=pd.to_datetime(airport.year_month+'-01',errors='raise')
    category['date']=pd.to_datetime(category.year_month+'-01',errors='raise')
    assert (airport['count']>=0).all() and (category['count']>=0).all()
    monthly=airport.groupby('date')['count'].sum().sort_index()
    top=airport.groupby('airport')['count'].sum().sort_values(ascending=False)
    cats=category.groupby('category_label')['count'].sum().sort_values(ascending=False)
    monthly.rename('count').to_csv(BASE/'outputs/monthly_complaints.csv')
    top.rename('complaints').to_csv(BASE/'outputs/airport_totals.csv')
    cats.rename('complaints').to_csv(BASE/'outputs/category_totals.csv')
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    monthly.plot(ax=axes[0],alpha=.5,label='Monthly');monthly.rolling(3,min_periods=1).mean().plot(ax=axes[0],label='3-month average')
    axes[0].set(title='Complaint volume in the saved snapshot',xlabel='Month',ylabel='Complaints');axes[0].legend()
    top.head(10).sort_values().plot.barh(ax=axes[1]);axes[1].set(title='Top airports by raw complaint count',xlabel='Complaints',ylabel='Airport code')
    chart(BASE,'complaints.svg',fig)
    write_results(BASE,{'airport_rows':len(airport),'first_month':str(monthly.index.min().date()),'last_month':str(monthly.index.max().date()),
        'total_airport_complaints':int(monthly.sum()),'airports':len(top),'top_airport':str(top.index[0]),
        'top_10_airports_share':float(top.head(10).sum()/top.sum()),'top_category':str(cats.index[0]),
        'category_total':int(cats.sum()),'airport_and_category_totals_match':bool(cats.sum()==monthly.sum()),
        'limits':'Raw complaints are not rates per passenger. High-volume airports can have more complaints simply because they serve more travelers. A complaint may be categorized differently across source tables.'})
if __name__=='__main__':main()
