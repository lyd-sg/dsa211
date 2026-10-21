# Topic 2 dataset bake-off, final report

Criteria reverse-engineered from the graded requirements. Cost ratio C_FN/C_FP = 5.0. 15 criteria.


## Ranking

| rank | dataset | origin | passed | best CV AUC | test sens/spec @t | verdict |
|---|---|---|---|---|---|---|
| 1 | Online shoppers intent | Turkey (Asia, transcontinental) | 15/15 | 0.7528 | 0.767 / 0.578 | usable |
| 2 | Taiwan credit default | Taiwan (Asia) | 14/15 | 0.7704 | 0.731 / 0.630 | usable with caveats |
| 3 | Bank marketing | Portugal (CONTROL, not Asian) | 14/15 | 0.7431 | 0.483 / 0.898 | usable with caveats |
| 4 | ACRA firm survival | Singapore (Asia) | 10/15 | 0.7139 | 1.000 / 0.200 | not usable |
| 5 | Contraceptive choice | Indonesia (Asia) | 10/15 | 0.6848 | 0.986 / 0.095 | not usable |
| 6 | Taiwan bankruptcy | Taiwan (Asia) | 10/15 | 0.9166 | 0.564 / 0.952 | not usable |

## Failed criteria, and what each one breaks

**Online shoppers intent** — no failures.

**Taiwan credit default** — 1 failed:

- `Cost can pick a model` = 0.0067 → breaks the **model-choice justification**

**Bank marketing** — 1 failed:

- `Cost can pick a model` = 0.0000 → breaks the **model-choice justification**

**ACRA firm survival** — 5 failed:

- `Numeric features >= 3` = 0 → breaks the **preprocessing + LDA/NB sections**
- `3 distinct confusion matrices` = 2 → breaks the **three-model comparison table**
- `Operating point informative` = 0.1999 → breaks the **threshold extension**
- `Sensitivity not saturated` = 0.9996 → breaks the **threshold + CI discussion**
- `Cost can pick a model` = 0.0001 → breaks the **model-choice justification**

**Contraceptive choice** — 5 failed:

- `Numeric features >= 3` = 2 → breaks the **preprocessing + LDA/NB sections**
- `Operating point informative` = 0.0949 → breaks the **threshold extension**
- `Sensitivity not saturated` = 0.9858 → breaks the **threshold + CI discussion**
- `Cost can pick a model` = 0.0000 → breaks the **model-choice justification**
- `|CV - test AUC| <= 0.03` = 0.0575 → breaks the **CV vs held-out section**

**Taiwan bankruptcy** — 5 failed:

- `Train positives >= 500` = 165 → breaks the **k-fold CV section**
- `Held-out positives >= 100` = 55 → breaks the **CV vs held-out section**
- `Categorical features >= 3` = 2 → breaks the **leakage-free pipeline section**
- `|CV - test AUC| <= 0.03` = 0.0384 → breaks the **CV vs held-out section**
- `Sens 95% CI width <= 0.20` = 0.2536 → breaks the **CV vs held-out section**


## Supporting numbers

|                          | Taiwan credit default   | ACRA firm survival    | Online shoppers intent          | Contraceptive choice   | Bank marketing                | Taiwan bankruptcy   |
|:-------------------------|:------------------------|:----------------------|:--------------------------------|:-----------------------|:------------------------------|:--------------------|
| origin                   | Taiwan (Asia)           | Singapore (Asia)      | Turkey (Asia, transcontinental) | Indonesia (Asia)       | Portugal (CONTROL, not Asian) | Taiwan (Asia)       |
| rows                     | 30000                   | 58807                 | 12330                           | 1473                   | 45211                         | 6819                |
| prevalence               | 0.2212                  | 0.6106926046218988    | 0.15474452554744525             | 0.572980312287848      | 0.11698480458295547           | 0.03226279513125092 |
| n_train_pos              | 4977                    | 26935                 | 1431                            | 633                    | 3967                          | 165                 |
| n_test_pos               | 1659                    | 8978                  | 477                             | 211                    | 1322                          | 55                  |
| max univ AUC (train)     | 0.7106097567729549      | 0.6285914352581372    | 0.7143316188477541              | 0.622595533016036      | 0.6501572578495207            | 0.8871195282793586  |
| n flagged kept           | 0                       | 0                     | 0                               | 0                      | 0                             | 32                  |
| leakage premium          | 0.0                     | 0.07901745060451504   | 0.14133982720674743             | 0.0                    | 0.15827920951032293           | 0.0                 |
| distinct test confusions | 3                       | 2                     | 3                               | 3                      | 3                             | 3                   |
| cost gap best vs 2nd     | 0.0066902794175521295   | 7.261109497527396e-05 | 0.02681421579059386             | 0.0                    | 0.0                           | 0.02862595419847338 |
| n_numeric                | 14                      | 0                     | 8                               | 2                      | 6                             | 93                  |
| n_categorical            | 9                       | 7                     | 8                               | 7                      | 9                             | 2                   |
| final model (AUC)        | Logistic                | LDA                   | Logistic                        | Logistic               | Logistic                      | Logistic            |
| final model (cost)       | Logistic                | Logistic              | Logistic                        | Logistic               | Logistic                      | Logistic            |
| grounds agree            | True                    | False                 | True                            | True                   | True                          | True                |
| best CV AUC              | 0.7704381890417316      | 0.713914306957181     | 0.7528336934682892              | 0.6847871658901936     | 0.7430522023116347            | 0.9165714530636737  |
| AUC spread across 3      | 0.03147199253185107     | 0.09067590509692502   | 0.04835307995854343             | 0.04570960914728839    | 0.01822468315070558           | 0.23595522817587888 |
| separated beyond noise   | True                    | True                  | True                            | True                   | True                          | True                |
| Brier spread across 3    | 0.04901138175054809     | 0.11584105028126548   | 0.3347065507618674              | 0.10697443012902066    | 0.060901418467617874          | 0.7392258283805089  |
| chosen t                 | 0.155                   | 0.185                 | 0.14500000000000002             | 0.23500000000000001    | 0.16                          | 0.115               |
| t moved from 0.5         | 0.345                   | 0.315                 | 0.355                           | 0.265                  | 0.33999999999999997           | 0.385               |
| test sens @t             | 0.7305605786618445      | 0.9995544664736021    | 0.7672955974842768              | 0.985781990521327      | 0.4826021180030257            | 0.5636363636363636  |
| test spec @t             | 0.6300291046053758      | 0.19986023759608665   | 0.5782808902532617              | 0.0949367088607595     | 0.897705640717363             | 0.9515151515151515  |
| test youden @t           | 0.3605896832672202      | 0.19941470406968875   | 0.34557648773753846             | 0.08071869938208653    | 0.3803077587203887            | 0.5151515151515151  |
| min(sens,spec) @t        | 0.6300291046053758      | 0.19986023759608665   | 0.5782808902532617              | 0.0949367088607595     | 0.4826021180030257            | 0.5636363636363636  |
| cost cut vs 0.5          | 0.24248747913188648     | 0.3343804368838198    | 0.3308174309313586              | 0.49008168028004667    | 0.18493718890732394           | 0.2577903682719548  |
| cost cut vs trivial      | 0.2749529190207156      | 0.19784507862550957   | 0.3432564640111811              | 0.07218683651804665    | 0.3065288631207461            | 0.3648484848484849  |
| |CV - test AUC|          | 0.00941245783792699     | 0.007388287690269002  | 0.017128636117971996            | 0.05751891125900532    | 0.011973420501816823          | 0.03841167344934859 |
| sens CI width            | 0.04266254710218598     | 0.0009718326295637958 | 0.07565782428465395             | 0.03611404826241871    | 0.05379476155227042           | 0.25356741292953644 |

## Recommendation

- Highest scoring overall: **Online shoppers intent** (15/15), origin Turkey (Asia, transcontinental).
- **Online shoppers intent** also satisfies the Asian preference, so no trade is needed.
