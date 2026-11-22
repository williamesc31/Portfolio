"""Reproduce loan-default classification from the bundled public dataset."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import write_results, chart, plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.base import clone
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, average_precision_score, precision_score, recall_score, f1_score, confusion_matrix, RocCurveDisplay

BASE=Path(__file__).resolve().parent

def main():
    data=pd.read_csv(BASE/'data/credit_risk.csv.gz')
    rows=len(data); duplicates=int(data.duplicated().sum())
    data=data.drop_duplicates().copy()
    invalid_age=~data.person_age.between(18,100)
    data=data.loc[~invalid_age].copy()
    invalid_employment=(data.person_emp_length<0)|(data.person_emp_length>data.person_age-14)
    data.loc[invalid_employment,'person_emp_length']=np.nan
    data=data.loc[(data.person_income>0)&(data.loan_amnt>0)].copy()
    data['loan_to_income']=data.loan_amnt/data.person_income
    data['emp_to_age']=data.person_emp_length/data.person_age
    data['log_income']=np.log1p(data.person_income)
    data['log_loan_amount']=np.log1p(data.loan_amnt)
    numeric=['person_age','log_income','person_emp_length','log_loan_amount','loan_int_rate','loan_to_income','emp_to_age']
    categorical=['person_home_ownership','loan_intent']
    X=data[numeric+categorical]; y=data.loan_status.astype(int)
    assert set(y)=={0,1} and np.isfinite(X[numeric].dropna().to_numpy()).all()
    train,test=train_test_split(np.arange(len(data)),test_size=.2,stratify=y,random_state=42)
    prep=ColumnTransformer([
        ('numeric',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())]),numeric),
        ('category',Pipeline([('impute',SimpleImputer(strategy='most_frequent')),('encode',OneHotEncoder(handle_unknown='ignore'))]),categorical)])
    estimators={'logistic_regression':LogisticRegression(max_iter=1500,class_weight='balanced'),
                'random_forest':RandomForestClassifier(n_estimators=160,max_depth=20,class_weight='balanced',random_state=42,n_jobs=2)}
    results={}; fig,axes=plt.subplots(1,2,figsize=(10,4))
    for name,estimator in estimators.items():
        pipeline=Pipeline([('prepare',clone(prep)),('model',estimator)])
        pipeline.fit(X.iloc[train],y.iloc[train])
        score=pipeline.predict_proba(X.iloc[test])[:,1]; predicted=(score>=.5).astype(int)
        results[name]={'test_accuracy':float(accuracy_score(y.iloc[test],predicted)),
            'test_roc_auc':float(roc_auc_score(y.iloc[test],score)),
            'test_average_precision':float(average_precision_score(y.iloc[test],score)),
            'default_precision':float(precision_score(y.iloc[test],predicted,zero_division=0)),
            'default_recall':float(recall_score(y.iloc[test],predicted)),
            'default_f1':float(f1_score(y.iloc[test],predicted)),
            'confusion_matrix':confusion_matrix(y.iloc[test],predicted).tolist()}
        RocCurveDisplay.from_predictions(y.iloc[test],score,name=name.replace('_',' ').title(),ax=axes[0])
    metrics=pd.DataFrame(results).T
    metrics[['test_accuracy','default_recall','default_f1']].plot.bar(ax=axes[1],rot=15)
    axes[0].set_title('Held-out ROC curves');axes[1].set(title='Performance at threshold 0.50',ylim=(0,1),ylabel='Score')
    axes[1].legend(fontsize=8)
    chart(BASE,'model_comparison.svg',fig)
    write_results(BASE,{'source_rows':rows,'exact_duplicates_removed':duplicates,'invalid_age_rows_removed':int(invalid_age.sum()),
        'employment_values_imputed':int(invalid_employment.sum()),'analysis_rows':len(data),'train_rows':len(train),'test_rows':len(test),
        'test_default_rate':float(y.iloc[test].mean()),'split':'Stratified 80/20, random_state=42','features':numeric+categorical,
        'models':results,'limits':'Interest rate is a loan-pricing-stage feature. This is a dataset benchmark, not a validated lending policy.'})

if __name__=='__main__':main()
