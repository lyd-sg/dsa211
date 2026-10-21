# Project decisions and open questions

**Source:** Group meeting minutes provided in this project and the professor's subsequent first-pass instruction. These notes distinguish **agreed directions** from **unresolved details**; they are not empirical findings.

## Agreed direction

1. **Prediction only**, rather than an inference-focused report.
2. Compare **all three taught approaches**: logistic regression, Naive Bayes, and discriminant analysis (LDA; QDA can be documented when applicable). Do not presuppose a winning model.
3. **First-pass baseline:** attempt all model families with all original candidate predictors *as-is*, even where a family's distributional assumptions seem questionable. Record warnings and failures. Perform subsequent transformations, variable selection and other model-specific adjustments under cross-validation. Technical category encoding needed to fit a model is distinct from dropping/binarising predictors to improve performance.
4. **Nominal predictor encoding:** never treat operating-system, browser, region or traffic-source codes as numerical rankings.
5. **Zero-heavy numeric predictors:** investigate binary representations later, after the initial baselines; EDA alone is not proof that binarisation improves prediction.
6. **Business cost proposals from meeting minutes:** FP cost = CAC; FN cost = discount applied to AOV. This is the group's proposed mapping, **not yet validated or implemented**. The older fixed `C_FN/C_FP=5` analysis must not be described as reflecting it.
7. Investigate candidate solutions before asking the professor.

## Customer scenarios raised in meeting

- Customer buys once.
- Customer buys in year 1 and again the next year.
- Customer begins purchasing this year and buys again within that year.
- A random one-observation-per-customer convention was discussed. **Do not apply this without resolving** whether unique customer IDs and repeated customer histories can be identified from the session-level data.

## Questions to resolve

- Whether a 75/25 (existing notebook) or different train/test split should be retained. Professor left the ratio to the group; the course CV workflow allows commonly used 20–30% holdouts.
- Model-specific treatment of the **mixed numeric/categorical predictors** after researching options.
- Whether customer uniqueness needs to be addressed and, if so, whether that is feasible for a session-level dataset.
- Decision/action definitions required before assigning CAC or discount × AOV to FP and FN, and before selecting a cost-based threshold.
- Timing/availability of `PageValues` at actual prediction time, and how an **all-predictor first pass** is distinguished from a later leakage-safe operational specification.

These are recorded as unresolved; they have not been settled by this housekeeping pull request.
