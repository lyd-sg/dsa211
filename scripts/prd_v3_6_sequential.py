# PRD v3.6 — sequential one-SE selection.
# This script is included verbatim in notebook Section 7; it operates on the
# fixed v3.4 experiment definitions, data, evaluator and shared outer folds.

ORIGINAL_BUILD_MODEL=build_model

def _inner_one_se_refit(results):
    mean=np.asarray(results['mean_test_score'],dtype=float)
    best=int(np.argmax(mean))
    vals=np.array([results[f'split{i}_test_score'][best] for i in range(INNER_FOLDS)],
                  dtype=float)
    cutoff=float(mean[best]-vals.std(ddof=1)/np.sqrt(INNER_FOLDS))
    candidates=np.flatnonzero(mean>=cutoff-1e-12)
    params=results['params']
    key='clf__shrinkage' if 'clf__shrinkage' in params[0] else 'clf__C'
    if key=='clf__shrinkage':
        return int(max(candidates,key=lambda i:(float(params[int(i)][key]),mean[int(i)])))
    return int(min(candidates,key=lambda i:(float(params[int(i)][key]),-mean[int(i)])))

def build_model(family,config=None,columns=SAFE):
    est=ORIGINAL_BUILD_MODEL(family,config,columns)
    if isinstance(est,GridSearchCV):
        # The same original fixed inner grids, but strongest-penalty within 1 SE.
        est.refit=_inner_one_se_refit
    return est

PATH_FINALISTS={}; PATH_FINAL_CONFIGS={}; ATTEMPTS=[]; STAGE_FINALISTS={}

def active_sources(cfg):
    removed=set(cfg.get('drop_features',()))
    if cfg.get('drop_nominal',False):
        removed.update(CAT)
    return [c for c in SAFE if c not in removed]

def apply_change_to_incumbent(fam,step,base,change):
    cfg=base.copy()
    active=set(active_sources(cfg))
    if 'remove' in change:
        x=change['remove']
        # Preserve the semantic preconditions in the original trial descriptions.
        # A historical "drop X, retain Y" trial cannot silently drop both X and Y.
        required_retained={'G2':('ExitRates',),
            'G3':('ProductRelated_Duration',),
            'G5':('BounceRates',),
            'G6':('ProductRelated',)}
        missing=[c for c in required_retained.get(step,()) if c not in active]
        if missing:
            return None,f'{step} requires already removed retained counterpart(s): {missing}'
        if x not in active:
            return None,f'{x} already dropped'
        cfg['drop_features']=tuple(dict.fromkeys([*cfg.get('drop_features',()),x]))
    elif 'median' in change:
        x=change['median']
        if x not in active:
            return None,f'{x} already dropped'
        if x in cfg.get('median_cols',()):
            return None,f'{x} already median-binarised'
        cfg['median_cols']=tuple(dict.fromkeys([*cfg.get('median_cols',()),x]))
    elif change.get('backward_select',False):
        if len(active)<=1:
            return None,'Backward selection requires at least two remaining sources'
        # D15 substitutes an unshrunk LDA model for an inherited D4 tuned covariance.
        cfg.pop('tune',None)
        cfg['backward_select']=True
    else:
        for key,value in change.items():
            requires={
                'special_binary':['SpecialDay'],
                'special_categorical':['SpecialDay'],
                'bounce_piecewise':['BounceRates'],
                'bounce_binned':['BounceRates'],
                'avg_product_duration':['ProductRelated','ProductRelated_Duration'],
            }.get(key,[])
            if key in ('log_cols','presence_cols','quadratic_cols','winsor_cols','drop_features'):
                requires=list(value)
            # G5/G6 are historical v3.2 drop_features proposals, unlike G2/G3
            # which used the older 'remove' spelling. Enforce their counterpart
            # prerequisites here as well, before creating a candidate.
            if key=='drop_features' and step in ('G5','G6'):
                counterpart={'G5':'BounceRates','G6':'ProductRelated'}[step]
                if counterpart not in active:
                    return None,f'{step} cannot retain previously deleted {counterpart}'
            missing=[c for c in requires if c not in active]
            if missing:
                return None,f'Previously dropped predictor(s) required by {key}: {missing}'
            if key in ('log_cols','presence_cols','quadratic_cols','winsor_cols'):
                already=set(cfg.get(key,()))
                if key=='log_cols' and cfg.get('log_activity'):
                    already.update(ACTIVITY)
                new=[c for c in value if c not in already]
                if not new:
                    return None,f'{key} already applies to these sources'
                cfg[key]=tuple(dict.fromkeys([*cfg.get(key,()),*new]))
            elif key=='drop_features':
                cfg[key]=tuple(dict.fromkeys([*cfg.get(key,()),*value]))
            elif key=='drop_nominal':
                if not set(CAT)&active:
                    return None,'Nominal sources already dropped'
                cfg[key]=bool(value)
            elif key=='log_activity':
                if cfg.get(key,False) or not set(ACTIVITY)&active:
                    return None,'Activity log1p already active or activity sources absent'
                cfg[key]=bool(value)
            elif key=='presence':
                if cfg.get(key,False) or not {'Informational','Informational_Duration'}&active:
                    return None,'Informational presence already active or sources absent'
                cfg[key]=bool(value)
            elif key=='rare_pool':
                if cfg.get(key,False) or not {'Browser','TrafficType'}&active:
                    return None,'Rare category pooling already active or sources absent'
                cfg[key]=bool(value)
            elif key=='special_binary':
                cfg.pop('special_categorical',None)
                cfg[key]=bool(value)
            elif key=='special_categorical':
                cfg.pop('special_binary',None)
                cfg[key]=bool(value)
            elif key=='bounce_piecewise':
                cfg.pop('bounce_binned',None)
                cfg['quadratic_cols']=tuple(x for x in cfg.get('quadratic_cols',())
                                            if x!='BounceRates')
                cfg[key]=bool(value)
            elif key=='bounce_binned':
                cfg.pop('bounce_piecewise',None)
                cfg['quadratic_cols']=tuple(x for x in cfg.get('quadratic_cols',())
                                            if x!='BounceRates')
                cfg[key]=bool(value)
            else:
                # This includes replacing (not stacking) logistic penalties.
                cfg[key]=value
    if cfg==base:
        return None,'No actual change from retained configuration'
    return cfg,None

def model_size(fam,result):
    column='nonzero_coefficients' if fam=='Logit' else 'design_columns'
    vals=[]
    for fr in result['folds']:
        n=fr[column]
        # Existing v3.4 evaluator omits nonzero counts for unpenalised Logit
        # and Ridge; all estimated encoded coefficients count as active.
        if fam=='Logit' and (n is None or pd.isna(n)):
            n=fr['design_columns']
        vals.append(float(n))
    assert len(vals)==K and np.isfinite(vals).all() and min(vals)>=0
    return float(np.mean(vals))

def choose_pair(fam,incumbent,candidate):
    n0=model_size(fam,incumbent);n1=model_size(fam,candidate)
    best=(incumbent if incumbent['mean_fold_auc']>=candidate['mean_fold_auc']
          else candidate)
    cutoff=best['mean_fold_auc']-best['fold_auc_se']
    eligible=[(incumbent,n0,0),(candidate,n1,1)]
    eligible=[(r,n,i) for r,n,i in eligible if r['mean_fold_auc']>=cutoff-1e-12]
    selected=min(eligible,key=lambda v:(v[1],-v[0]['mean_fold_auc'],v[2]))[0]
    return selected['candidate'],float(cutoff),best['candidate']

def run_v36_family(fam):
    prefix={'Logit':'L','LDA':'D','GaussianNB':'G','BernoulliNB':'B'}[fam]
    baseline=f'Operational16 | {fam}'
    retained=baseline;config={}
    b=RESULTS[baseline]
    ATTEMPTS.append({'pathway':fam,'step':prefix+'0','candidate':baseline,
      'parent':'—','trial_version':'v3.1','single_change':'16-source baseline',
      'status':'SCORED','mean_auc':b['mean_fold_auc'],'auc_se':b['fold_auc_se'],
      'mean_ap':b['mean_fold_ap'],'complexity':model_size(fam,b),
      'source_count':16.,'one_se_cutoff':np.nan,'accepted':True,
      'retained_after_step':baseline,'decision':'BASELINE',
      'skip_reason':'','config':json.dumps(config)})
    phases=[('v3.1',PATHS[fam]),('v3.2',EXTRA_PATHS[fam]),
            ('v3.3',V33_EXTRAS[fam]),('v3.4',V34_EXTRAS[fam])]
    for version,changes in phases:
        for step,description,change in changes:
            label=f'{step} | {fam}';parent=retained
            proposal,skip=apply_change_to_incumbent(fam,step,config,change)
            if skip:
                ATTEMPTS.append({'pathway':fam,'step':step,'candidate':label,
                  'parent':parent,'trial_version':version,'single_change':description,
                  'status':'SKIPPED_INAPPLICABLE','mean_auc':np.nan,'auc_se':np.nan,
                  'mean_ap':np.nan,'complexity':np.nan,'source_count':np.nan,
                  'one_se_cutoff':np.nan,'accepted':False,
                  'retained_after_step':parent,'decision':'SKIPPED_INAPPLICABLE',
                  'skip_reason':skip,'config':json.dumps(config)})
                print(f'{label}: SKIPPED_INAPPLICABLE — {skip}',flush=True)
                continue
            assert step!='G7' or 'ProductRelated_Duration' in active_sources(proposal)
            print(f'{label}: recomputing on retained {parent}',flush=True)
            r=run_spec(label,fam,SAFE,
                       pipeline_factory=lambda f=fam,c=proposal:build_model(f,c,SAFE))
            RESULTS[label]=r; FOLD_ROWS.extend(r['folds'])
            WARNING_ROWS.extend(r['warnings'])
            prior=RESULTS[parent]
            selected,cutoff,best=choose_pair(fam,prior,r)
            accepted=(selected==label)
            n0=model_size(fam,prior);n1=model_size(fam,r)
            if accepted:
                retained=label;config=proposal.copy()
            if accepted:
                decision='ACCEPT_SIMPLER' if n1<n0-1e-12 else 'ACCEPT_HIGHER_AUC'
            else:
                decision='RETAIN_SIMPLER' if n0<n1-1e-12 else 'RETAIN_HIGHER_AUC_OR_TIE'
            count=(float(np.mean([x['selected_source_count'] for x in r['folds']]))
                   if step=='D15' else float(len(active_sources(proposal))))
            ATTEMPTS.append({'pathway':fam,'step':step,'candidate':label,
              'parent':parent,'trial_version':version,'single_change':description,
              'status':'SCORED','mean_auc':r['mean_fold_auc'],
              'auc_se':r['fold_auc_se'],'mean_ap':r['mean_fold_ap'],
              'complexity':n1,'source_count':count,
              'one_se_cutoff':cutoff,'best_at_step':best,'accepted':accepted,
              'retained_after_step':retained,'decision':decision,
              'skip_reason':'','config':json.dumps(proposal)})
        STAGE_FINALISTS[(version,fam)]=retained
    PATH_FINALISTS[fam]=retained
    PATH_FINAL_CONFIGS[fam]=config.copy()
    print(f'FINAL {fam}: {retained}; AUC={RESULTS[retained]["mean_fold_auc"]:.5f}',
          flush=True)

def display_family(family):
    history=pd.DataFrame([x for x in ATTEMPTS if x['pathway']==family])
    assert len(history)=={'Logit':13,'LDA':13,'GaussianNB':10,'BernoulliNB':5}[family]
    display(history[['step','trial_version','parent','single_change','status',
        'mean_auc','auc_se','mean_ap','complexity','source_count','one_se_cutoff',
        'decision','retained_after_step','skip_reason']].round(5))
