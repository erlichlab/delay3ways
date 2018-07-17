### Master script to create figures

- `master.m`. Run this function to generate all the main figures.

### MLE fitting

- `fit_discount_loo.m`: fmincon -> one can define several utility forms: hyperbolic, exponential, with curvature or not - and choose between two decision rules: softmax and matching, including leave one out cross validation
- Necessary functions for the fits: `discountf.m` - defines utility depending on the specified model, `softmax.m` - sofmax decision rule, `matchrule.m` - matching decision rule

### R Code

R code in `bhm` can be used to redo the `brms` fits and also the statistics for the time-adaptation effects. 

ToDo: a full RMarkdown document that generates all tables and stats from the paper.