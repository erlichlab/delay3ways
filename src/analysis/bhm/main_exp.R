library(brms)
library(rstan)

load('../../../data/all_trials.RData')

# This code is designed to run on a machine (or SLURM node) with more than 10 CPU cores. 
# Even with 10 cores, it will take at least a few days to run.

# Describe the model
main_model = bf(choice ~ inv_logit((rewmag / (1 + exp(logk) * delay) - smag) / noise),
                  noise ~ 0 + treat + (1|subjid), 
                  logk ~ 0 + treat + (treat|subjid),
                  nl = TRUE)

# Fit the model to the data
main_fit = brm(main_model,
             data = all_trials, family = bernoulli(link='identity'),
             prior = c(prior(normal(-5,3), nlpar = 'logk'), prior(normal(1,.5),lb = 0, nlpar = 'noise')),
             inits = "0", 
             chains = 10, iter = 6000, warmup=2000, cores = 10)

# Save the results in case there is a crash in computing later steps
save.image(file='../../../data/main_fit.RData')

# Perform leave-one-out cross validation. 
loo = brms::LOO(fit, nsamples = 4000, cores=10)
save.image(file='../../../data/main_fit.RData')

# Perform k-fold cross validation
kfold <- brms::kfold(fit, K=10, update_args=c(chains = 10, cores = 10))
save.image(file='../../../data/main_fit.RData')

