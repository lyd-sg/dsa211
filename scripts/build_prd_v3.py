"""Build PRD v3 notebook by reusing the executed PRD v2 notebook's EDA and baseline cells.
Do not run this script after looking at v3 holdout results to revise model choices.
"""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
source = nbf.read(ROOT / "online_shoppers_revised.ipynb", as_version=4)

def md(s):
    return nbf.v4.new_markdown_cell(s.strip())
def code(s):
    return nbf.v4.new_code_cell(s.strip())
def original(i):
    c=source.cells[i].copy()
    c.pop("execution_count",None)
    c.pop("outputs",None)
    if c.cell_type=="code":
        c["execution_count"]=None
        c["outputs"]=[]
    if i in (24,26):
        c.source=c.source.replace("ARTIFACTS/'prd_v2_", "V3_ART/'")
    if i==23:
        c.source=c.source.replace("ARTIFACTS/'training_winner_oof_probability_histogram.png'",
                                  "V3_ART/'winner_oof_probability_histogram.png'")
    if i==4:
        c.source += "\nprint(f'Interpretation: training prevalence is {y_train.mean():.2%}, so accuracy alone can reward predicting no purchase. Preserve 125 identical rows, but note dependence risk across folds.')\n"
    if i==6:
        c.source += "\nprint(f'Interpretation: Informational has {num_summary.loc[\"Informational\",\"zero share\"]:.1%} zeros, Informational_Duration {num_summary.loc[\"Informational_Duration\",\"zero share\"]:.1%} zeros, and ProductRelated_Duration skew={num_summary.loc[\"ProductRelated_Duration\",\"skew\"]:.2f}. These motivate, but do not validate, presence and log1p trials.')\n"
    if i==8:
        c.source += "\nprint(f'Interpretation: {int((Xtr.Browser.value_counts()<50).sum())} Browser and {int((Xtr.TrafficType.value_counts()<50).sum())} TrafficType levels have fewer than 50 training rows. Fold-fitted pooling is a hypothesis, not a guaranteed gain; all six categories remain nominal.')\n"
    if i==17:
        c.source += "\nprint(f'Interpretation: operational Logit starts at CV mean AUC {OP16.loc[\"Operational16 | Logit\",\"mean ROC-AUC\"]:.4f}, versus {ALL17.loc[\"All17 | Logit\",\"mean ROC-AUC\"]:.4f} with PageValues. Exclusion is a timing precaution, not proof of leakage.')\n"
    if i==26:
        c.source=c.source.replace('SEVEN_CV.loc[SEVEN_CV.candidate.eq(WINNER_LABEL),"mean_fold_ap"].iloc[0]',
                                  'FINALISTS.loc[FINALISTS.candidate.eq(WINNER_LABEL),"mean_ap"].iloc[0]')
    return c

cells = [
md("""
# Predicting Online Purchases — PRD 3.0
### DSA211 · Prediction-only · four sequential classification pathways

**Research question.** How accurately can browsing-session characteristics distinguish sessions ending in a purchase (Revenue=1), and which defensible taught-classifier specification gives the best **mean five-fold training ROC-AUC**?

**Design.** Start with four all-17 feature-timing diagnostics, establish four 16-source operational baselines, then evaluate an EDA-motivated 3–5 step sequence independently for Logit, LDA, Gaussian NB and Bernoulli NB. Use a local **one-standard-error** criterion to retain/reject each modification. Select one finalist per pathway, then a winner by mean CV AUC.

**Secondary illustration.** A hypothetical sales-agent upsell uses **S$3** assistance cost, **30%** conditional upsell success and **S$50** gross margin. The resulting **0.20** cost cutoff is an *assumption-based decision threshold*, not empirical evidence of upsell uplift. Source: [approved PRD v3.0](docs/PRD_v3.md).
"""),
md("""
## 0. Fixed analysis protocol
**Purpose.** Make development comparisons reproducible and preserve the reserved set for one frozen v3 check.

**Method.** Use the v2 stratified 80/20 partition (seed 42) and the same five shuffled stratified training folds (seed 42) for every specification. Any median, category pooling, encoding, scaling or penalty parameter is fitted **inside the applicable fold**; L4/D4 tune on three *inner* training folds. The project already exposed the reserved set in historical versions, so v3's check is **not pristine across the entire development history**.

**Interpretation.** ROC-AUC measures discrimination, AP contextualises minority-class ranking and does not establish probability calibration or treatment effects. The selected model cannot be revised after checking v3's reserved-set result.
"""),
original(2), original(3), original(4), original(5), original(6), original(7), original(8), original(9), original(10),
code(r'''
# Reuse v2's source variables, data split, folds and basic model-evaluation contract.
# New v3 changes are deliberately isolated in this fold-fitted representation and evaluator.
from sklearn.model_selection import GridSearchCV
from sklearn.calibration import calibration_curve

V3_ART=ARTIFACTS/'prd_v3'
V3_ART.mkdir(parents=True,exist_ok=True)
C_GRID=[0.05,0.2,1.0,5.0,20.0]
SHRINKAGE_GRID=[0.0,0.1,0.3,0.6,0.9]
RARE_MIN_COUNT=50
INNER_FOLDS=3
FAMILY_ORDER=['Logit','LDA','GaussianNB','BernoulliNB']

class FoldSafeFeatures(BaseEstimator, TransformerMixin):
    """Train-fold-only feature engineering. Categorical levels are never treated as ordinal."""
    def __init__(self, family='Logit', columns=(), log_activity=False,
                 presence=False, rare_pool=False, special_binary=False,
                 drop_features=(), median_cols=(), scale=False):
        self.family=family
        self.columns=columns
        self.log_activity=log_activity
        self.presence=presence
        self.rare_pool=rare_pool
        self.special_binary=special_binary
        self.drop_features=drop_features
        self.median_cols=median_cols
        self.scale=scale

    def _blocks(self,X):
        active=[c for c in self.columns if c not in self.drop_features]
        cats=[c for c in CAT if c in active]
        nums=[c for c in active if c not in cats]
        z=pd.DataFrame(index=X.index)
        for c in nums:
            value=X[c].astype(float)
            if self.family=='BernoulliNB':
                if c in self.median_cols:
                    z[c]=(value>self.medians_[c]).astype(float)
                elif c=='Weekend':
                    z[c]=value
                else:
                    z[c]=(value>0).astype(float)
            elif self.special_binary and c=='SpecialDay':
                z[c]=(value>0).astype(float)
            elif self.log_activity and c in ACTIVITY:
                z[c]=np.log1p(value)
            else:
                z[c]=value
        if self.presence:
            for c in ('Informational','Informational_Duration'):
                if c in active:
                    z[c+'__positive']=(X[c].astype(float)>0).astype(float)
        cat=pd.DataFrame(index=X.index)
        for c in cats:
            values=X[c].astype(str)
            if self.rare_pool and c in ('Browser','TrafficType'):
                values=values.where(values.isin(self.major_levels_[c]),'__OTHER__')
            cat[c]=values
        return z,cat

    def fit(self,X,y=None):
        self.n_features_in_=X.shape[1]
        self.feature_names_in_=np.asarray(X.columns,dtype=object)
        self.major_levels_={}
        for c in ('Browser','TrafficType'):
            if c in X and self.rare_pool:
                counts=X[c].astype(str).value_counts()
                self.major_levels_[c]=set(counts.index[counts>=RARE_MIN_COUNT])
        self.medians_={c:float(X[c].median()) for c in self.median_cols}
        num,cat=self._blocks(X)
        self.numeric_names_=list(num.columns)
        self.categorical_names_=list(cat.columns)
        self.encoder_=OneHotEncoder(
            drop='first' if self.family in ('Logit','LDA') else None,
            handle_unknown='ignore',sparse_output=False
        )
        if self.categorical_names_:
            self.encoder_.fit(cat)
        transformed=self._encode(num,cat)
        if self.scale:
            self.scaler_=StandardScaler().fit(transformed)
        return self

    def _encode(self,num,cat):
        blocks=[num.to_numpy(dtype=float)]
        if self.categorical_names_:
            blocks.append(self.encoder_.transform(cat))
        Z=np.column_stack(blocks)
        if not np.isfinite(Z).all():
            raise ValueError('Non-finite preprocessing output')
        return Z

    def transform(self,X):
        num,cat=self._blocks(X)
        Z=self._encode(num,cat)
        return self.scaler_.transform(Z) if self.scale else Z

    def get_feature_names_out(self,input_features=None):
        names=list(self.numeric_names_)
        if self.categorical_names_:
            names+=list(self.encoder_.get_feature_names_out(self.categorical_names_))
        return np.asarray(names,dtype=object)

def build_model(family,config=None,columns=SAFE):
    cfg=dict(config or {})
    tune=cfg.pop('tune',None)
    pre=FoldSafeFeatures(family=family,columns=tuple(columns),**cfg)
    if family=='Logit':
        if tune=='logit':
            clf=LogisticRegression(solver='lbfgs',max_iter=1600,tol=1e-6)
        else:
            clf=LogisticRegression(C=np.inf,solver='newton-cg',tol=1e-8,max_iter=2000)
    elif family=='LDA':
        clf=LinearDiscriminantAnalysis(solver='lsqr' if tune=='lda' else 'svd')
    elif family=='GaussianNB':
        clf=GaussianNB()
    elif family=='BernoulliNB':
        clf=BernoulliNB(binarize=None)
    else:
        raise ValueError(family)
    pipe=Pipeline([('pre',pre),('clf',clf)])
    if tune:
        params={'clf__C':C_GRID} if tune=='logit' else {'clf__shrinkage':SHRINKAGE_GRID}
        inner=StratifiedKFold(n_splits=INNER_FOLDS,shuffle=True,random_state=SEED)
        return GridSearchCV(pipe,params,cv=inner,scoring='roc_auc',n_jobs=1,refit=True,error_score='raise')
    return pipe

def make_pipeline(columns,family,estimator=None):
    if estimator is not None:
        raise ValueError('v3 uses explicit configurations, not replacement estimators')
    return build_model(family,{},columns)

def compact_numerical_label(result):
    return result.get('numerical_status','UNKNOWN')

def run_spec(label,family,columns,pipeline_factory=None):
    oof=np.full(len(ytr),np.nan)
    folds=[]; warning_rows=[]
    for fold,(fit_idx,val_idx) in enumerate(FOLD_INDICES,1):
        fit_x=Xtr.iloc[fit_idx][columns]
        val_x=Xtr.iloc[val_idx][columns]
        fit_y=ytr.iloc[fit_idx]
        val_y=ytr.iloc[val_idx]
        fitted=pipeline_factory() if pipeline_factory is not None else make_pipeline(columns,family)
        mark_progress(label,fold,'start',n_fit=len(fit_idx),n_validation=len(val_idx))
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            fitted.fit(fit_x,fit_y)
            prob=np.asarray(fitted.predict_proba(val_x)[:,1],dtype=float)
        actual=fitted.best_estimator_ if isinstance(fitted,GridSearchCV) else fitted
        clf=actual.named_steps['clf']
        params=['coef_','intercept_','theta_','var_','class_prior_','feature_log_prob_',
                'means_','priors_','scalings_','class_log_prior_']
        finite=all(np.isfinite(np.asarray(getattr(clf,k),dtype=float)).all()
                   for k in params if hasattr(clf,k))
        if not finite or not np.isfinite(prob).all() or np.any((prob<0)|(prob>1)):
            raise RuntimeError(f'{label} fold {fold}: invalid model parameters/probabilities')
        oof[val_idx]=prob
        for w in caught:
            warning_rows.append({'candidate':label,'fold':fold,
                                 'warning_type':w.category.__name__,
                                 'message':str(w.message)[:350]})
        best=fitted.best_params_ if isinstance(fitted,GridSearchCV) else {}
        row={'candidate':label,'family':family,'fold':fold,'fit_status':'OK',
             'n_fit':len(fit_idx),'n_validation':len(val_idx),
             'roc_auc':float(roc_auc_score(val_y,prob)),
             'average_precision':float(average_precision_score(val_y,prob)),
             'design_rank':np.nan,'design_columns':actual.named_steps['pre'].transform(fit_x.iloc[:1]).shape[1],
             'finite_model_parameters':bool(finite),'finite_probabilities':True,
             'probabilities_in_0_1':True,'inner_cv_best_params':json.dumps(best),
             'numerical_status':'FINITE_WITH_WARNINGS_REVIEW_REQUIRED' if caught else 'FINITE_FIT'}
        folds.append(row)
        mark_progress(label,fold,'complete',roc_auc=row['roc_auc'])
    if np.isnan(oof).any():
        raise RuntimeError(f'{label}: incomplete OOF coverage')
    auc=np.array([x['roc_auc'] for x in folds],dtype=float)
    ap=np.array([x['average_precision'] for x in folds],dtype=float)
    return {'candidate':label,'family':family,'stage':'all17' if len(columns)==len(ALL) else 'operational16',
            'status':'SCORED','numerical_status':'FINITE_WITH_WARNINGS_REVIEW_REQUIRED' if warning_rows else 'FINITE_FIT',
            'folds':folds,'oof':oof,'warnings':warning_rows,'failure':'',
            'mean_fold_auc':float(auc.mean()),
            'fold_auc_sd':float(auc.std(ddof=1)),
            'fold_auc_se':float(auc.std(ddof=1)/np.sqrt(K)),
            'mean_fold_ap':float(ap.mean()),
            'fold_ap_sd':float(ap.std(ddof=1)),
            'fold_ap_se':float(ap.std(ddof=1)/np.sqrt(K)),
            'pooled_oof_auc':float(roc_auc_score(ytr,oof)),
            'pooled_oof_ap':float(average_precision_score(ytr,oof))}

RESULTS={}; FOLD_ROWS=[]; WARNING_ROWS=[]
'''),
original(12),original(13),original(14),original(15),original(16),original(17),
md("""
## 7. Four sequential EDA-guided development pathways
**Purpose.** Test improvements, not assume that transformations automatically help.

**Method.** Each pathway starts at its 16-source baseline and tries four changes **one at a time**. After a rejection, the next change is applied to the *last accepted* recipe. Retain a challenger only if its mean five-fold AUC exceeds the incumbent by **more than one challenger SE** (course-based one-SE simplicity rule). L4 and D4 use three-fold inner CV to tune the penalty/shrinkage without viewing any outer validation outcomes.

**Interpretation.** All 20 proposed baseline/revision specifications are documented, including rejected ones, and each retained finalist is selected within its own family. This heuristic does not prove statistical significance.
"""),
code(r'''
# Predeclare the ordered list of single changes. Edits are cumulative only if accepted.
PATHS={
 'Logit':[('L1','log1p six activity magnitudes',{'log_activity':True}),
          ('L2','separate informational positive-presence indicators',{'presence':True}),
          ('L3','fold-fitted pooling of rare Browser/TrafficType levels',{'rare_pool':True}),
          ('L4','standardised L2 logistic with inner-CV C',{'scale':True,'tune':'logit'})],
 'LDA':[('D1','log1p six activity magnitudes',{'log_activity':True}),
        ('D2','binarise SpecialDay>0',{'special_binary':True}),
        ('D3','fold-fitted rare nominal-level pooling',{'rare_pool':True}),
        ('D4','inner-CV covariance shrinkage',{'tune':'lda'})],
 'GaussianNB':[('G1','log1p six activity magnitudes',{'log_activity':True}),
               ('G2','remove BounceRates, retaining ExitRates',{'remove':'BounceRates'}),
               ('G3','remove ProductRelated, retaining duration',{'remove':'ProductRelated'}),
               ('G4','remove SpecialDay Gaussian marginal',{'remove':'SpecialDay'})],
 'BernoulliNB':[('B1','ProductRelated: presence to training-fold median',{'median':'ProductRelated'}),
                ('B2','ProductRelated_Duration: training-fold median',{'median':'ProductRelated_Duration'}),
                ('B3','ExitRates: training-fold median',{'median':'ExitRates'}),
                ('B4','remove BounceRates',{'remove':'BounceRates'})]}

PATH_FINALISTS={}; PATH_FINAL_CONFIGS={}; ATTEMPTS=[]
for fam in FAMILY_ORDER:
    prefix={'Logit':'L','LDA':'D','GaussianNB':'G','BernoulliNB':'B'}[fam]
    baseline=f'Operational16 | {fam}'
    incumbent_label=baseline
    incumbent_cfg={}
    b=RESULTS[baseline]
    ATTEMPTS.append({'pathway':fam,'step':prefix+'0','candidate':baseline,
          'parent':'—','single_change':'16-source operational baseline',
          'eda_reason':'Four all-16 operational reference models',
          'mean_auc':b['mean_fold_auc'],'auc_sd':b['fold_auc_sd'],
          'auc_se':b['fold_auc_se'],'mean_ap':b['mean_fold_ap'],
          'delta_auc':np.nan,'accepted':True,'decision':'Baseline'})
    for step,reason,change in PATHS[fam]:
        cfg=incumbent_cfg.copy()
        if 'remove' in change:
            cfg['drop_features']=tuple([*cfg.get('drop_features',()),change['remove']])
        elif 'median' in change:
            cfg['median_cols']=tuple([*cfg.get('median_cols',()),change['median']])
        else:
            cfg.update(change)
        label=step+' | '+fam
        print(f'Testing {label} (against {incumbent_label})',flush=True)
        res=run_spec(label,fam,SAFE,
            pipeline_factory=lambda f=fam,c=cfg:build_model(f,c,SAFE))
        RESULTS[label]=res
        FOLD_ROWS.extend(res['folds'])
        WARNING_ROWS.extend(res['warnings'])
        prior=RESULTS[incumbent_label]
        gain=res['mean_fold_auc']-prior['mean_fold_auc']
        accept=bool(gain>res['fold_auc_se'])
        ATTEMPTS.append({'pathway':fam,'step':step,'candidate':label,
            'parent':incumbent_label,'single_change':reason,
            'eda_reason':reason,
            'mean_auc':res['mean_fold_auc'],'auc_sd':res['fold_auc_sd'],
            'auc_se':res['fold_auc_se'],'mean_ap':res['mean_fold_ap'],
            'delta_auc':gain,'accepted':accept,
            'decision':'Retain' if accept else 'Revert (within 1 SE or no gain)'})
        if accept:
            incumbent_label=label
            incumbent_cfg=cfg
    PATH_FINALISTS[fam]=incumbent_label
    PATH_FINAL_CONFIGS[fam]=incumbent_cfg.copy()

ATTEMPTS_DF=pd.DataFrame(ATTEMPTS)
assert len(ATTEMPTS_DF)==20
assert len(PATH_FINALISTS)==4
display(ATTEMPTS_DF[['step','pathway','parent','single_change','mean_auc','auc_se','mean_ap','delta_auc','decision']].round(5))
ATTEMPTS_DF.to_csv(V3_ART/'all_attempts_ledger.csv',index=False)
pd.DataFrame([{'pathway':f,'finalist':PATH_FINALISTS[f],'configuration':json.dumps(PATH_FINAL_CONFIGS[f])}
              for f in FAMILY_ORDER]).to_csv(V3_ART/'retained_pathways.csv',index=False)
print('Retained finalists:',PATH_FINALISTS)
print('Interpretation: retained revisions',ATTEMPTS_DF.loc[ATTEMPTS_DF.accepted & ATTEMPTS_DF.step.str[-1].ne('0'),'step'].tolist(),
      '; reverted revisions',ATTEMPTS_DF.loc[~ATTEMPTS_DF.accepted,'step'].tolist(),
      '. Retentions reflect the local one-SE comparison, not significance tests.')
'''),
md("""
## 8. Four finalists and winner selection
**Purpose.** Select one predictive model without considering the hypothetical costs.

**Method.** Rank the four retained pathway finalists by **mean outer-fold ROC-AUC**; include AP and fold SD/SE as context. ROC overlays use pooled training OOF predictions for visualisation; the *mean of five AUCs*, not pooled AUC, determines the winner.

**Interpretation.** Small differences in mean AUC do not prove superiority. Sequential comparison may make CV performance optimistic.
"""),
code(r'''
FINALIST_ROWS=[]
OOF_ROWS=[]
FOLD_SCORE_ROWS=[]
for fam in FAMILY_ORDER:
    label=PATH_FINALISTS[fam]
    r=RESULTS[label]
    assert r['status']=='SCORED' and len(r['folds'])==K
    coverage=np.zeros(len(ytr),dtype=int)
    for (fit_idx,val_idx),fr in zip(FOLD_INDICES,r['folds']):
        coverage[val_idx]+=1
        yy=ytr.iloc[val_idx].to_numpy()
        pp=r['oof'][val_idx]
        assert abs(roc_auc_score(yy,pp)-fr['roc_auc'])<1e-12
        assert abs(average_precision_score(yy,pp)-fr['average_precision'])<1e-12
        FOLD_SCORE_ROWS.append({'family':fam,'finalist':label,'fold':fr['fold'],
                'roc_auc':fr['roc_auc'],'average_precision':fr['average_precision']})
    assert np.all(coverage==1)
    FINALIST_ROWS.append({'pathway':fam,'candidate':label,'mean_auc':r['mean_fold_auc'],
            'auc_sd':r['fold_auc_sd'],'auc_se':r['fold_auc_se'],
            'mean_ap':r['mean_fold_ap'],'pooled_oof_auc':r['pooled_oof_auc']})
    for row_id,yy,pp in zip(Xtr.index,ytr.to_numpy(),r['oof']):
        OOF_ROWS.append({'finalist':label,'row_id':int(row_id),'observed':int(yy),'oof_probability':float(pp)})
FINALISTS=pd.DataFrame(FINALIST_ROWS).sort_values(['mean_auc','candidate'],ascending=[False,True]).reset_index(drop=True)
WINNER_LABEL=str(FINALISTS.iloc[0]['candidate'])
WINNER_FAMILY=str(FINALISTS.iloc[0]['pathway'])
WINNER_CONFIG=PATH_FINAL_CONFIGS[WINNER_FAMILY].copy()
WINNER_OOF=np.asarray(RESULTS[WINNER_LABEL]['oof'],dtype=float)
BASE_RATE=float(ytr.mean())
FINALISTS.to_csv(V3_ART/'four_finalists.csv',index=False)
pd.DataFrame(FOLD_SCORE_ROWS).to_csv(V3_ART/'finalist_fold_scores.csv',index=False)
pd.DataFrame(OOF_ROWS).to_csv(V3_ART/'finalist_oof_scores.csv',index=False,float_format='%.17g')
display(FINALISTS[['pathway','candidate','mean_auc','auc_sd','auc_se','mean_ap']].round(5))
fig,ax=plt.subplots(figsize=(7.2,5.6))
for fam in FAMILY_ORDER:
    label=PATH_FINALISTS[fam]
    fpr,tpr,_=roc_curve(ytr,RESULTS[label]['oof'])
    ax.plot(fpr,tpr,lw=1.65,label=f'{fam}: {RESULTS[label]["mean_fold_auc"]:.3f} mean AUC')
ax.plot([0,1],[0,1],'k--',lw=1,label='Chance')
ax.set(xlabel='False positive rate (1 − specificity)',ylabel='True positive rate (sensitivity)',
       title='Training OOF ROC curves — four retained finalists')
ax.legend(loc='lower right',fontsize=8)
ax.grid(alpha=.2);fig.tight_layout()
fig.savefig(V3_ART/'four_finalists_roc.png',dpi=160,bbox_inches='tight')
display(fig);plt.close(fig)
print(f'Winner: {WINNER_LABEL} | five-fold mean AUC {float(FINALISTS.iloc[0]["mean_auc"]):.5f}')
print(f'Interpretation: winner AUC exceeds the runner-up by {float(FINALISTS.iloc[0].mean_auc-FINALISTS.iloc[1].mean_auc):.4f}; this descriptive gap does not establish significance or calibrated probabilities.')
'''),
md("""
## 9. Winner's training OOF scores and precision–recall behaviour
**Purpose.** See how buyer/nonbuyer scores overlap and whether minority-class detection is informative.

**Method.** Show one class-separated score histogram and one training OOF precision–recall curve, with the observed buyer prevalence as the no-skill reference. A simple reliability summary follows for the 0.20 decision assumption.

**Interpretation.** ROC-AUC/AP measure ordering, not well-calibrated probabilities. The financial cutoff is only decision-optimal under the stated assumptions *and* sufficiently calibrated probabilities.
"""),
original(24),original(26),
code(r'''
# Descriptive calibration check, no calibration model is fitted or chosen from holdout.
reliability=pd.DataFrame({'actual':ytr.to_numpy(),'predicted':WINNER_OOF})
reliability['bucket']=pd.cut(reliability.predicted,bins=np.linspace(0,1,11),include_lowest=True)
reliability=reliability.groupby('bucket',observed=True).agg(
    n=('actual','size'),observed_purchase_rate=('actual','mean'),mean_predicted_probability=('predicted','mean')).reset_index()
display(reliability.round(4))
reliability.to_csv(V3_ART/'winner_oof_reliability.csv',index=False)
near=reliability.loc[reliability['mean_predicted_probability'].between(.1,.3)]
print('Interpretation: OOF observed purchase frequency should be compared to mean predicted score around 0.20; upper score buckets are sparse, so probability quality is not established by AUC alone.')
display(near[['bucket','n','observed_purchase_rate','mean_predicted_probability']].round(4))
'''),
md("""
## 10. Four threshold references
**Purpose.** Compare classification trade-offs with the hypothetical upselling decision.

**Method.** A prediction of Buy occurs if **p ≥ t**. Use the training buyer prevalence, 0.500, the nearest empirical sensitivity–specificity crossover, and the **fixed assumption-derived 0.200**. Here false positives mean contacting nonbuyers, whereas false negatives mean leaving actual buyers without upsell assistance.

**Payoffs (hypothetical, not observed).** S$3 per agent contact; conditional upsell probability 30% and incremental gross margin S$50. Expected net benefit of contacting an actual buyer = 0.3×50−3 = **S$12**; contacting a nonbuyer = **−S$3**. Thus relative error costs C_FP=3, C_FN=12, and t*=3/(3+12)=**0.20**. Equivalently, contact when 15p−3 > 0 (with equality classified Buy for reproducibility). These costs do not measure any intervention effect from UCI.
"""),
code(r'''
def threshold_measures(y_true,prob,threshold):
    true=np.asarray(y_true,dtype=int)
    pred=(np.asarray(prob,dtype=float)>=float(threshold)).astype(int)
    tn,fp,fn,tp=confusion_matrix(true,pred,labels=[0,1]).ravel()
    return {'threshold':float(threshold),'TP':int(tp),'FP':int(fp),'TN':int(tn),'FN':int(fn),
            'sensitivity':float(tp/(tp+fn)),'specificity':float(tn/(tn+fp)),
            'precision':float(tp/(tp+fp)) if tp+fp else np.nan,
            'hypothetical_relative_loss_SGD':int(3*fp+12*fn)}
_,_,roc_candidates=roc_curve(ytr,WINNER_OOF,drop_intermediate=False)
cutoffs=np.unique(np.r_[roc_candidates[np.isfinite(roc_candidates)&(roc_candidates>=0)&(roc_candidates<=1)],0.,1.])
THRESHOLD_CURVE=pd.DataFrame([threshold_measures(ytr,WINNER_OOF,t) for t in cutoffs])
THRESHOLD_CURVE['gap']=(THRESHOLD_CURVE.sensitivity-THRESHOLD_CURVE.specificity).abs()
CROSSOVER=THRESHOLD_CURVE.sort_values(['gap','threshold'],kind='stable').iloc[0]
CROSSOVER_THRESHOLD=float(CROSSOVER.threshold)
THRESHOLD_REFS=[('Training prevalence',BASE_RATE),('Conventional 0.500',0.5),
                ('Sensitivity–specificity crossover',CROSSOVER_THRESHOLD),
                ('Cost-based (hypothetical)',0.2)]
THRESHOLD_TABLE=pd.DataFrame([{'reference':label,**threshold_measures(ytr,WINNER_OOF,t)}
                              for label,t in THRESHOLD_REFS])
assert len(THRESHOLD_TABLE)==4
assert THRESHOLD_TABLE[['TP','FP','TN','FN']].sum(axis=1).eq(len(ytr)).all()
assert np.isclose(THRESHOLD_TABLE.loc[3,'threshold'],0.2)
THRESHOLD_TABLE.to_csv(V3_ART/'four_threshold_references.csv',index=False)
THRESHOLD_CURVE.to_csv(V3_ART/'threshold_curves.csv',index=False)
display(THRESHOLD_TABLE.round(4))
fig,ax=plt.subplots(figsize=(7.2,4.8))
ax.plot(THRESHOLD_CURVE.threshold,THRESHOLD_CURVE.sensitivity,label='Sensitivity')
ax.plot(THRESHOLD_CURVE.threshold,THRESHOLD_CURVE.specificity,label='Specificity')
ax.axvline(CROSSOVER_THRESHOLD,ls='--',color='tab:green',lw=1.4,label=f'Crossover {CROSSOVER_THRESHOLD:.3f}')
ax.axvline(0.2,ls=':',color='tab:red',lw=1.7,label='Hypothetical cost threshold 0.200')
ax.scatter([CROSSOVER_THRESHOLD],[float(CROSSOVER.sensitivity)],color='tab:green',s=40,zorder=5)
ax.set(xlabel='Purchase-probability threshold',ylabel='Rate',ylim=(0,1.02),
       title='Training OOF sensitivity and specificity')
ax.grid(alpha=.2);ax.legend(fontsize=8);fig.tight_layout()
fig.savefig(V3_ART/'sensitivity_specificity.png',dpi=160,bbox_inches='tight')
display(fig);plt.close(fig)
print('Financial threshold 0.20 is fixed independently of observed confusion matrices.')
print(f'Interpretation: at 0.20, {int(THRESHOLD_TABLE.iloc[3].TP):,} buyers would be contacted and {int(THRESHOLD_TABLE.iloc[3].FP):,} nonbuyers contacted in training OOF predictions; this is a hypothetical cost trade-off, not observed upsell value.')
'''),
md("""
## 11. Cost-assumption sensitivity (no revenue simulation)
**Purpose.** Show how the hypothetical decision changes when the unknown upsell rate differs.

**Method.** Keep the S$3 contact cost and S$50 incremental gross margin fixed. Set conditional upsell success q=20%, 30% or 40%. Theoretical threshold t=s/(q×g), provided the assumed upsell benefit exceeds contact cost.

**Interpretation.** These are *input assumptions*, not estimated purchase uplift. The UCI data contain no agent assignments or upsell outcomes.
"""),
code(r'''
COST_SENSITIVITY=pd.DataFrame([{'assumed_upsell_success_q':q,'agent_cost_SGD':3.,
 'incremental_gross_margin_SGD':50.,'net_TP_value_SGD':q*50-3,
 'C_FP_SGD':3.,'C_FN_SGD':q*50-3.,
 'theoretical_probability_cutoff':3/(q*50)}
 for q in [.20,.30,.40]])
assert np.allclose(COST_SENSITIVITY.theoretical_probability_cutoff,[.30,.20,.15])
display(COST_SENSITIVITY.round(4))
COST_SENSITIVITY.to_csv(V3_ART/'upsell_sensitivity.csv',index=False)
'''),
md("""
## 12. Frozen reserved-set check and final full-data refit
**Purpose.** Check the already-selected recipe once, then fit the identical family/representation on all records for the final model.

**Method.** Refit the winner on the 9,864 training rows (retuning a predeclared inner CV grid, if selected), check finite parameters and probabilities, perform **one v3 reserved-set** ROC-AUC/AP/threshold check on the original 2,466 records, and only then refit the unchanged recipe on all 12,330 rows. No post-test tuning or candidate change.

**Qualification.** The reserved observations have been used in historical project versions, so this check is held out *for this v3 protocol*, not a pristine lifetime-independent validation.
"""),
code(r'''

# Independent recomputation of *every* attempted CV fold from the saved OOF vectors.
# This checks correctness, not a second feature search, and uses no reserved outcomes.
def independently_audit_training_results():
    audits=[]
    known_labels=list(RESULTS)
    assert len(known_labels)==24, f'Expected four all-17 diagnostics and 20 operational trials, found {len(known_labels)}'
    assert set(ATTEMPTS_DF.candidate)==set(known_labels)-set(f'All17 | {f}' for f in FAMILY_ORDER)
    for name,res in RESULTS.items():
        p=np.asarray(res['oof'],dtype=float)
        assert p.shape==(len(ytr),) and np.isfinite(p).all()
        fold_aucs=[];fold_aps=[]
        for (fit_idx,val_idx),record in zip(FOLD_INDICES,res['folds']):
            assert record['fit_status']=='OK'
            yy=ytr.iloc[val_idx].to_numpy()
            auc=float(roc_auc_score(yy,p[val_idx]))
            ap=float(average_precision_score(yy,p[val_idx]))
            assert np.isclose(auc,record['roc_auc'],atol=1e-12,rtol=0)
            assert np.isclose(ap,record['average_precision'],atol=1e-12,rtol=0)
            fold_aucs.append(auc);fold_aps.append(ap)
        avg=float(np.mean(fold_aucs))
        sd=float(np.std(fold_aucs,ddof=1))
        se=float(sd/np.sqrt(K))
        assert np.isclose(avg,res['mean_fold_auc'],atol=1e-12,rtol=0)
        assert np.isclose(sd,res['fold_auc_sd'],atol=1e-12,rtol=0)
        assert np.isclose(se,res['fold_auc_se'],atol=1e-12,rtol=0)
        assert np.isclose(np.mean(fold_aps),res['mean_fold_ap'],atol=1e-12,rtol=0)
        audits.append({'candidate':name,'folds_verified':len(fold_aucs),'mean_auc':avg,'auc_sd':sd,'auc_se':se})
    for _,trial in ATTEMPTS_DF.iterrows():
        if trial.step.endswith('0'):
            continue
        challenger=RESULTS[trial.candidate]
        parent=RESULTS[trial.parent]
        delta=challenger['mean_fold_auc']-parent['mean_fold_auc']
        assert np.isclose(delta,trial.delta_auc,atol=1e-12,rtol=0)
        assert bool(delta>challenger['fold_auc_se'])==bool(trial.accepted)
    for _,row in THRESHOLD_TABLE.iterrows():
        counted=threshold_measures(ytr,WINNER_OOF,float(row.threshold))
        for key in ('TP','FP','TN','FN'):
            assert counted[key]==int(row[key])
        assert sum(counted[k] for k in ('TP','FP','TN','FN'))==len(ytr)
        for key in ('sensitivity','specificity','precision'):
            assert np.isclose(counted[key],row[key],atol=1e-12,rtol=0)
    assert len(FINALISTS)==4 and FINALISTS.mean_auc.iloc[0]==FINALISTS.mean_auc.max()
    return {'status':'PASS','cv_candidates_verified':len(audits),
            'individual_fold_scores_verified':sum(q['folds_verified'] for q in audits),
            'sequential_decisions_verified':16,'threshold_rows_verified':len(THRESHOLD_TABLE),
            'winner':WINNER_LABEL,'test_data_used_in_verification':False}
TRAINING_AUDIT=independently_audit_training_results()
with (V3_ART/'independent_training_audit.json').open('w') as f:
    json.dump(TRAINING_AUDIT,f,indent=2,allow_nan=False)
print('Independent training evidence audit:',TRAINING_AUDIT)

def validate_fitted_model(model,X,description):
    actual=model.best_estimator_ if isinstance(model,GridSearchCV) else model
    estimator=actual.named_steps['clf']
    numbers=[np.asarray(getattr(estimator,k),dtype=float)
        for k in ('coef_','intercept_','theta_','var_','class_prior_','feature_log_prob_','means_','priors_')
        if hasattr(estimator,k)]
    if not numbers or not all(np.isfinite(a).all() for a in numbers):
        raise RuntimeError(f'{description}: finite parameter audit failed')
    sample=model.predict_proba(X)[:,1]
    if not np.isfinite(sample).all() or ((sample<0)|(sample>1)).any():
        raise RuntimeError(f'{description}: invalid probability output')
    design=actual.named_steps['pre'].transform(X)
    n_cols=int(design.shape[1])
    rank=int(np.linalg.matrix_rank(design[:min(3000,len(design))]))
    max_coef=(float(np.max(np.abs(estimator.coef_))) if hasattr(estimator,'coef_') else None)
    return {'description':description,'finite_parameters':True,
            'encoded_columns':n_cols,'sample_design_rank':rank,
            'max_absolute_coefficient':max_coef,
            'probability_min':float(sample.min()),'probability_max':float(sample.max()),
            'chosen_inner_CV_params':model.best_params_ if isinstance(model,GridSearchCV) else {}}

SELECTED_TRAIN_MODEL=build_model(WINNER_FAMILY,WINNER_CONFIG,SAFE)
with warnings.catch_warnings(record=True) as train_warnings:
    warnings.simplefilter('always')
    SELECTED_TRAIN_MODEL.fit(Xtr[SAFE],ytr)
TRAIN_AUDIT=validate_fitted_model(SELECTED_TRAIN_MODEL,Xtr[SAFE],'Frozen training fit')
if any(issubclass(w.category,ConvergenceWarning) for w in train_warnings):
    raise RuntimeError('Frozen training fit convergence warning; inspect before external claims')
print('Frozen training fit passed parameter and probability checks.')

# Do not access any holdout outcome until the winner, four thresholds and training refit
# are fully frozen above. The source is re-read, avoiding any earlier holdout exposure.
reserved=pd.read_csv(data_path)
reserved.insert(0,'_row_id',np.arange(len(reserved),dtype=int))
reserved=reserved.set_index('_row_id').loc[test_ids]
X_test=reserved[SAFE].copy()
X_test[CAT]=X_test[CAT].astype('string')
X_test['Weekend']=X_test['Weekend'].astype(int)
y_test=reserved[TARGET].astype(int)
del reserved
assert len(X_test)==2466 and len(y_test)==2466
test_prob=np.asarray(SELECTED_TRAIN_MODEL.predict_proba(X_test)[:,1],dtype=float)
TEST_AUDIT={'n_test':int(len(y_test)),
   'roc_auc':float(roc_auc_score(y_test,test_prob)),
   'average_precision':float(average_precision_score(y_test,test_prob)),
   'cost_threshold_0_20':threshold_measures(y_test,test_prob,.20)}
display(pd.DataFrame([{'sample':'Reserved v3 check (historically previously used)',
            'n':TEST_AUDIT['n_test'],'ROC-AUC':TEST_AUDIT['roc_auc'],
            'AP':TEST_AUDIT['average_precision'],**TEST_AUDIT['cost_threshold_0_20']}]).round(4))
print('This v3 holdout was examined once AFTER freezing the training selection. Prior historical reuse prevents a pristine-independent-test claim.')

# Final all-data refit uses the same selected pathway recipe, no new model selection.
all_rows=pd.read_csv(data_path)
assert len(all_rows)==12330 and set(all_rows.columns)==EXPECTED
all_rows[CAT]=all_rows[CAT].astype('string')
all_rows['Weekend']=all_rows['Weekend'].astype(int)
FINAL_PIPELINE=build_model(WINNER_FAMILY,WINNER_CONFIG,SAFE)
with warnings.catch_warnings(record=True) as final_warnings:
    warnings.simplefilter('always')
    FINAL_PIPELINE.fit(all_rows[SAFE],all_rows[TARGET].astype(int))
FINAL_AUDIT=validate_fitted_model(FINAL_PIPELINE,all_rows[SAFE],'Final all-data refit')
if any(issubclass(w.category,ConvergenceWarning) for w in final_warnings):
    raise RuntimeError('Final full-data refit convergence warning; inspect before external claims')

RUN_METADATA={'prd':'v3.0','data_sha256':source_hash,
 'random_state':SEED,'training_rows':len(ytr),'test_rows':len(y_test),
 'final_rows':len(all_rows),'cv_folds':K,'inner_folds':INNER_FOLDS,
 'selected_model':WINNER_LABEL,'selected_family':WINNER_FAMILY,
 'selected_recipe':WINNER_CONFIG,'four_finalists':PATH_FINALISTS,
 'test_check':TEST_AUDIT,'train_fit_audit':TRAIN_AUDIT,'final_fit_audit':FINAL_AUDIT,
 'train_warnings':[str(w.message) for w in train_warnings],
 'final_warnings':[str(w.message) for w in final_warnings],
 'historically_pristine_holdout':False,
 'training_evidence_audit':TRAINING_AUDIT,
 'versions':{'python':platform.python_version(),'pandas':pd.__version__,
            'numpy':np.__version__,'scipy':scipy.__version__,'sklearn':sklearn.__version__}}
with (V3_ART/'run_metadata.json').open('w') as f:
    json.dump(RUN_METADATA,f,indent=2,allow_nan=False,default=str)
pd.DataFrame(FOLD_ROWS).to_csv(V3_ART/'all_attempt_fold_scores.csv',index=False)
pd.DataFrame(WARNING_ROWS).to_csv(V3_ART/'fit_warnings.csv',index=False)
pd.DataFrame({'row_id':Xtr.index,'observed':ytr.to_numpy(),
              'winner_oof_probability':WINNER_OOF}).to_csv(V3_ART/'winner_oof.csv',index=False)
pd.DataFrame({'row_id':test_ids,'observed':y_test.to_numpy(),
              'test_probability':test_prob}).to_csv(V3_ART/'frozen_holdout_scores.csv',index=False)
print('Final all-data fit verified for:',WINNER_LABEL)
print('Interpretation: reserved-set ROC-AUC is a version-specific check, not independent of earlier project exploration; no specifications were revised after seeing this result.')
'''),
md("""
## 13. Findings, interpretation and limitations
**Statistical conclusion** is generated directly from the verified CV, threshold and reserved-set objects below; no old v2 model result is carried over.

**Limitations.** (i) Predictive rather than causal: no observed upsell response, so S$3/S$12 and 0.20 are illustrative only. (ii) AUC/AP do not demonstrate calibration: verify the OOF reliability table before acting on the 0.20 threshold. (iii) Gaussian marginals and within-class NB independence are approximations; LDA assumes shared covariance and class-Gaussian structure, while Logit needs a suitable functional form. (iv) Rare nominal levels, correlated features, duplicates and session-aggregate availability complicate generalisation. (v) Sequential selection can inflate winner CV AUC. (vi) Reserved test observations were used historically and are not pristine across project versions.
"""),
code(r'''
row=FINALISTS.iloc[0]
business=THRESHOLD_TABLE.loc[THRESHOLD_TABLE.reference.eq('Cost-based (hypothetical)')].iloc[0]
print('PRD 3.0 PROJECT SUMMARY')
print(f"Four pathway finalists: {PATH_FINALISTS}")
print(f"Winner: {WINNER_LABEL}; mean five-fold ROC-AUC={row.mean_auc:.5f} (SD={row.auc_sd:.5f}; SE={row.auc_se:.5f}); mean AP={row.mean_ap:.5f}.")
print(f"Training buyer prevalence: {BASE_RATE:.4f}; OOF pooled AP: {average_precision_score(ytr,WINNER_OOF):.5f}.")
print(f"Fixed cost cutoff 0.200: TP={int(business.TP)}, FP={int(business.FP)}, TN={int(business.TN)}, FN={int(business.FN)}, sensitivity={business.sensitivity:.4f}, specificity={business.specificity:.4f}, precision={business.precision:.4f}.")
print(f"Reserved v3 check: ROC-AUC={TEST_AUDIT['roc_auc']:.5f}; AP={TEST_AUDIT['average_precision']:.5f} (historical prior use caveat).")
print("All 20 attempts recorded; numerical diagnostics and provenance in artifacts/prd_v3.")
print('Do not interpret illustrative upsell threshold as causal uplift, calibrated economic optimality, or deployment approval.')
''')]

book=nbf.v4.new_notebook(cells=cells,metadata=source.metadata)
for c in book.cells:
    if c.cell_type=='code':
        c.execution_count=None
        c.outputs=[]
nbf.validate(book)
output=ROOT/'online_shoppers_prd_v3.ipynb'
nbf.write(book,output)
print(f'Built {output.name}: {len(book.cells)} cells (reused v2 EDA and baseline stages).')
