"""Bank marketing: ordered UCI records with pre-call features only."""
from pathlib import Path
import io, json, urllib.request, zipfile
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (average_precision_score, roc_auc_score, precision_score,
                             recall_score, f1_score, confusion_matrix, roc_curve,
                             precision_recall_curve)
from sklearn.inspection import permutation_importance

BASE=Path(__file__).resolve().parent
DATA=BASE/'data/bank_marketing.csv.gz'
FIG=BASE/'outputs'; FIG.mkdir(exist_ok=True)
URL='https://archive.ics.uci.edu/static/public/222/bank+marketing.zip'
if not DATA.exists():
    with urllib.request.urlopen(URL, timeout=90) as response:
        outer=zipfile.ZipFile(io.BytesIO(response.read()))
        inner=zipfile.ZipFile(io.BytesIO(outer.read('bank-additional.zip')))
        DATA.parent.mkdir(parents=True,exist_ok=True)
        DATA.write_bytes(inner.read('bank-additional/bank-additional-full.csv'))
df=pd.read_csv(DATA,sep=';')
assert df.shape==(41188,21) and set(df.y)=={'yes','no'}
assert not df.isna().any().any()
# Each row is a contact, not necessarily a unique client; retain identical rows.
# All features refer to data available before or at the start of this contact.
X=df.drop(columns=['y','duration'])
y=(df.y=='yes').astype(int)
n=len(df); a=int(n*.6); b=int(n*.8)
X_train,X_val,X_test=X.iloc[:a],X.iloc[a:b],X.iloc[b:]
y_train,y_val,y_test=y.iloc[:a],y.iloc[a:b],y.iloc[b:]
num=X.select_dtypes(include='number').columns.tolist(); cat=X.select_dtypes(exclude='number').columns.tolist()
prep=ColumnTransformer([
    ('numeric',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())]),num),
    ('categorical',Pipeline([('impute',SimpleImputer(strategy='most_frequent')),
                             ('encode',OneHotEncoder(handle_unknown='ignore'))]),cat)
])
models={
 'Logistic regression':Pipeline([('prep',clone(prep)),('model',LogisticRegression(max_iter=2000))]),
 'Random forest':Pipeline([('prep',clone(prep)),('model',RandomForestClassifier(n_estimators=160,min_samples_leaf=20,max_features='sqrt',random_state=42,n_jobs=2))])
}
def top_k_stats(actual, probabilities, frac=.2):
    k=int(np.ceil(len(actual)*frac)); pos=np.argsort(-probabilities,kind='stable')[:k]
    positives=int(np.asarray(actual)[pos].sum())
    return {'k':k,'positives':positives,'precision':positives/k,
            'lift':(positives/k)/float(np.mean(actual)),
            'capture':positives/int(np.sum(actual))}
def summary(actual, probabilities):
    pred=(probabilities>=.5).astype(int)
    return {'roc_auc':roc_auc_score(actual,probabilities),'avg_precision':average_precision_score(actual,probabilities),
            'precision_at_05':precision_score(actual,pred,zero_division=0),
            'recall_at_05':recall_score(actual,pred,zero_division=0),
            'f1_at_05':f1_score(actual,pred,zero_division=0),'confusion_matrix':confusion_matrix(actual,pred).tolist(),
            'top20':top_k_stats(actual,probabilities)}
result={'data':{'rows':n,'columns':df.columns.tolist(),'duplicates':int(df.duplicated().sum()),
                'overall_subscriptions':int(y.sum()),'unknowns':{c:int((df[c]=='unknown').sum()) for c in cat},
                'splits':{s:{'n':len(t),'positives':int(t.sum()),'rate':float(t.mean())} for s,t in
                          [('train',y_train),('validation',y_val),('test',y_test)]}}}
val={}
for name,model in models.items():
    model.fit(X_train,y_train)
    val[name]=summary(y_val,model.predict_proba(X_val)[:,1])
chosen=max(val,key=lambda name:val[name]['avg_precision'])
# Interpret the model trained on the first 60% using genuinely held-out validation records.
imp=permutation_importance(models[chosen],X_val,y_val,n_repeats=3,random_state=42,scoring='average_precision',n_jobs=1)
importance=sorted(zip(X.columns,imp.importances_mean),key=lambda item:item[1],reverse=True)
# Final models train on all earlier observations. Validation determines selection only.
test={}; probabilities={}
for name,model in models.items():
    model.fit(X.iloc[:b],y.iloc[:b]); probabilities[name]=model.predict_proba(X_test)[:,1]
    test[name]=summary(y_test,probabilities[name])
result['validation']=val;result['selected_by_validation_avg_precision']=chosen;result['test']=test
# Audits are descriptive: group differences are not proof of unlawful discrimination.
p=probabilities[chosen]
selected=np.zeros(len(y_test),dtype=bool)
selected[np.argsort(-p,kind='stable')[:int(np.ceil(len(p)*.2))]]=True
age_groups=pd.cut(X_test.age,[0,34,54,120],labels=['17–34','35–54','55+'])
result['age_audit']={}
for group in age_groups.cat.categories:
    mask=np.asarray(age_groups==group)
    result['age_audit'][str(group)]={'n':int(mask.sum()),'response_rate':float(y_test[mask].mean()),
                                   'selected_rate':float(selected[mask].mean()),
                                   'selected_n':int(selected[mask].sum())}
# Shuffle original columns on the untouched middle period; scores show association, not causation.
result['permutation_importance_validation_ap_drop']=dict((k,float(v)) for k,v in importance)
(BASE/'outputs').mkdir(exist_ok=True)
(BASE/'outputs/results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
plt.rcParams.update({'font.size':10,'figure.dpi':150,'axes.spines.top':False,'axes.spines.right':False})
colors=['#596f9b','#dd8b4b','#398c82']
fig,ax=plt.subplots(figsize=(7.5,3.3)); labels=['Train (first 60%)','Validation (next 20%)','Test (last 20%)']
ax.bar(labels,[y_train.mean()*100,y_val.mean()*100,y_test.mean()*100],color=colors)
ax.set(ylabel='Term deposit subscriptions (%)',title='Subscription rate rises across the ordered campaign records',ylim=(0,37))
for i,v in enumerate([y_train.mean(),y_val.mean(),y_test.mean()]):ax.text(i,v*100+1,f'{v*100:.1f}%',ha='center')
fig.tight_layout();fig.savefig(FIG/'figure1_temporal_shift.svg');plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(9.2,3.5))
for i,(name,pred) in enumerate(probabilities.items()):
    fpr,tpr,_=roc_curve(y_test,pred);pr,re,_=precision_recall_curve(y_test,pred)
    axs[0].plot(fpr,tpr,color=colors[i],label=f'{name} (AUC {test[name]["roc_auc"]:.3f})')
    axs[1].plot(re,pr,color=colors[i],label=f'{name} (AP {test[name]["avg_precision"]:.3f})')
axs[0].plot([0,1],[0,1],color='#777',linestyle=':',label='Random ranking')
axs[1].axhline(y_test.mean(),color='#777',linestyle=':',label=f'Prevalence {y_test.mean():.3f}')
axs[0].set(xlabel='False positive rate',ylabel='True positive rate',title='ROC on later campaigns')
axs[1].set(xlabel='Recall',ylabel='Precision',title='Precision and recall on later campaigns')
for ax in axs:ax.legend(fontsize=7,loc='best')
fig.tight_layout();fig.savefig(FIG/'figure2_test_discrimination.svg');plt.close(fig)
fig,ax=plt.subplots(figsize=(7.5,3.6)); z=np.arange(1,len(y_test)+1)/len(y_test)
for i,(name,pred) in enumerate(probabilities.items()):
    hits=np.cumsum(np.asarray(y_test)[np.argsort(-pred,kind='stable')])/int(y_test.sum())
    ax.plot(z,hits,color=colors[i],label=name)
ax.plot([0,1],[0,1],linestyle=':',color='#777',label='Random selection')
ax.axvline(.2,color='#aaa',linestyle='--',linewidth=.8)
ax.set(xlabel='Share of contacts selected, ranked by model score',ylabel='Share of all subscriptions captured',title='Cumulative gains in the final time period')
ax.legend(fontsize=8);fig.tight_layout();fig.savefig(FIG/'figure3_cumulative_gains.svg');plt.close(fig)
fig,ax=plt.subplots(figsize=(7.5,4.0)); top=importance[:9][::-1]
ax.barh([k for k,v in top],[v for k,v in top],color='#398c82')
ax.set(xlabel='Decrease in validation average precision after shuffling',title=f'Which inputs matter to {chosen.lower()}?')
fig.tight_layout();fig.savefig(FIG/'figure4_permutation_importance.svg');plt.close(fig)
fig,ax=plt.subplots(figsize=(7.5,3.5)); keys=list(result['age_audit'])
ix=np.arange(len(keys));width=.34
ax.bar(ix-width/2,[result['age_audit'][k]['response_rate']*100 for k in keys],width,label='Observed response',color='#596f9b')
ax.bar(ix+width/2,[result['age_audit'][k]['selected_rate']*100 for k in keys],width,label='Selected in top 20%',color='#dd8b4b')
ax.set(xticks=ix,xticklabels=keys,ylabel='Share of age group (%)',title='Age group audit on later campaigns');ax.legend()
fig.tight_layout();fig.savefig(FIG/'figure5_age_audit.svg');plt.close(fig)
print(json.dumps(result,indent=2))
