### Master script to create figures

- `master.m`. Run this function to generate all the figures.

### MLE fitting

- `fit_discount_loo.m`: fmincon -> one can define several utility forms: hyperbolic, exponential, with curvature or not - and choose between two decision rules: softmax and matching, including leave one out cross validation
- Necessary functions for the fits: `discountf.m` - defines utility depending on the specified model, `softmax.m` - sofmax decision rule, `matchrule.m` - matching decision rule

### TODO

Include the R code for the hierarchical Bayesian model.