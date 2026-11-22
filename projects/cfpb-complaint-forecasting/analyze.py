from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE=Path(__file__).resolve().parent
root=BASE/'outputs'
df=pd.read_csv(BASE/'data/monthly_counts.csv',parse_dates=['month']).sort_values('month')
assert len(df)==96 and df.month.is_unique
assert list(df.month.dt.strftime('%Y-%m'))==list(pd.date_range('2018-01-01','2025-12-01',freq='MS').strftime('%Y-%m'))
assert ((df.credit_card_new_label+df.checking_savings)==df.api_total).all()
assert ((df.credit_card_new_label+df.credit_card_old_label)==df.credit_card).all()
assert ((df[['credit_card','checking_savings']]>0).all()).all()

df['year']=df.month.dt.year;df['month_num']=df.month.dt.month
annual=df.groupby('year')[['credit_card','checking_savings']].sum().astype(int)
base=df[df.year==2024].set_index('month_num')
test=df[df.year==2025].set_index('month_num')
metrics={}
for col,label in [('credit_card','Credit card'),('checking_savings','Checking or savings account')]:
 actual=test[col].to_numpy(dtype=float); pred=base[col].to_numpy(dtype=float)
 err=actual-pred
 metrics[col]={
   'label':label,'annual_2024':int(annual.loc[2024,col]),'annual_2025':int(annual.loc[2025,col]),
   'growth_pct':float((annual.loc[2025,col]/annual.loc[2024,col]-1)*100),
   'mae':float(np.abs(err).mean()),'rmse':float(np.sqrt(np.mean(err**2))),
   'wape_pct':float(np.abs(err).sum()/actual.sum()*100),
   'bias':float(err.mean()),'q1_mae':float(np.abs(err[:3]).mean()),
   'months_underforecast':int((err>0).sum()),'months_overforecast':int((err<0).sum()),
   'monthly_2025_min':int(actual.min()),'monthly_2025_max':int(actual.max()),
   'monthly_2025_min_month':int(test.index[np.argmin(actual)]),
   'monthly_2025_max_month':int(test.index[np.argmax(actual)]),
   'actual_2025':actual.astype(int).tolist(),'forecast_2025':pred.astype(int).tolist(),
   'cv_2018_2024':float(df[df.year<=2024][col].std()/df[df.year<=2024][col].mean()),
 }
results={'extraction_date':str(df.last_indexed.dropna().iloc[0])[:10],'months':len(df),'range':'2018-01 to 2025-12','last_indexed_values':sorted(df.last_indexed.dropna().unique().tolist()),'annual_counts':annual.to_dict(orient='index'),'baseline_2025':metrics}
(root/'results.json').write_text(json.dumps(results,indent=2))
annual.to_csv(root/'annual_counts.csv')
print(json.dumps(results,indent=2))

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(2,1,figsize=(10,6),sharex=True)
for ax,(col,label,color) in zip(axes,[('credit_card','Credit card','#14466d'),('checking_savings','Checking or savings account','#0a887b')]):
 ax.plot(df.month,df[col],color=color,lw=1.9,label='Published complaints')
 ax.axvspan(pd.Timestamp('2025-01-01'),pd.Timestamp('2025-12-31'),color='#edf2f7',zorder=-1,label='2025 holdout')
 ax.set_ylabel('Monthly count');ax.set_title(label,loc='left',weight='bold',fontsize=11);ax.grid(axis='y',alpha=.2)
 ax.legend(loc='upper left',frameon=False,fontsize=8)
axes[-1].set_xlabel('Date received');fig.suptitle('Monthly CFPB complaints for selected products, 2018–2025',fontsize=13,weight='bold',x=.02,ha='left')
fig.tight_layout(rect=[0,0,1,.95]);fig.savefig(root/'fig1_series.svg',dpi=200,bbox_inches='tight');plt.close(fig)

fig,axes=plt.subplots(2,1,figsize=(10,6),sharex=True)
for ax,(col,label,color) in zip(axes,[('credit_card','Credit card','#14466d'),('checking_savings','Checking or savings account','#0a887b')]):
 ax.plot(test.index,test[col],color=color,lw=2,marker='o',ms=3,label='Actual 2025')
 ax.plot(base.index,base[col],color='#d47734',lw=2,ls='--',marker='s',ms=3,label='Seasonal naïve: 2024 same month')
 ax.set_ylabel('Monthly count');ax.set_title(label,loc='left',weight='bold',fontsize=11);ax.grid(axis='y',alpha=.2);ax.legend(loc='upper left',frameon=False,fontsize=8)
axes[-1].set_xticks(range(1,13),['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
fig.suptitle('2025 holdout versus the 2024 seasonal naïve baseline',fontsize=13,weight='bold',x=.02,ha='left')
fig.tight_layout(rect=[0,0,1,.95]);fig.savefig(root/'fig2_holdout.svg',dpi=200,bbox_inches='tight');plt.close(fig)
