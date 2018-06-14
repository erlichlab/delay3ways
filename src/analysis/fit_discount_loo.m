% FIT_DISCOUNT_LOO      Fit a variety of probabilistic discounting models
% with leave one out cross validation
% 
%     [info,p] = fit_discount_loo(choice,x,model,rule,varargin);
%
%     Fits a binary logit model (or matching decision rule) by maximum likelihood.
%
%     INPUTS
%     choice      - Dependent variable. The data should be *ungrouped*,
%                   such that CHOICE is a column of 0s and 1s, where 1 indicates 
%                   a choice of the larger option.
%     x           - values for immediate option, values for delayed option,
%                   vectors of delay, trial / or total wait time
%     model       - String indicating which model to fit; currently valid are:
%                     '*0'      - no lapse
%                     'exp'       - exponential
%                     'hyp'       - Mazur's one-parameter hyperbolic
%                     'expcu'     - exponential + curvature (CRRA risk attitudes)
%                     'hypcu'     - hyperbolic + curvature
%                     'hyptime*'   - hyperbolic, time-dependent k; 'tr'-trial
%                      number dependent; 'wt'-total waittime dependent ->
%                      params has 5 parameters (instead of 4), x has 5
%                      variables (instead of 4)
%                   Multiple models can be fit by passing in a cell array
%                   of strings. 
%     rule         - String indicating which decision rule to use; currently valid are:
%                     'softmax'   - binary logit choice probability
%                     'matchrule' - matching rule choice probability 
%     varargin{1}   - input a variety of initial values for models to check if they converge to the same
%                   values
%     OUTPUTS
%     info       - data structure with following fields:
%                     .nobs      - number of observations
%                     .nb        - number of parameters
%                     .optimizer - function minimizer used
%                     .exitflag  - see FMINSEARCH
%                     .b         - fitted parameters; note that for all the
%                                  available models, the first element of B
%                                  is a noise term for the logistic
%                                  function, the remaining elements are
%                                  parameters for the selected discount
%                                  functions. eg., for model='exp', B(2) is
%                                  the time constant of the exponential
%                                  decay.
%                     .LL        - log-likelihood evaluated at maximum
%                     .LL0       - restricted (minimal model) log-likelihood
%                     .AIC       - Akaike's Information Criterion 
%                     .BIC       - Schwartz's Bayesian Information Criterion 
%                     .r2        - pseudo r-squared
%                   This is a struct array if multiple models are fit.
%     p           - Estimated choice probabilities evaluated at the values
%                   delays specified by the inputs v1(LL), t1(LL delay), v2(SS), t2(SS delay). This is
%                   a cell array if multiple models are fit.
function [info,p] = fit_discount_loo(choice,x,model,rule,varargin)

% If multiple model fits requested, loop and pack
if iscell(model)
   for i = 1:length(model)
       if isempty(varargin)
           [info(i),p{i}] = fit_discount_loo(choice,x,model{i},rule);
       else
            v1 = varargin{1};
            [info(i),p{i}] = fit_discount_loo(choice,x,model{i},rule,v1);
       end
   end
   return;
end

nobs = length(choice);
% bounds for inverse temperature (params(1))1/beta -> 0 -all actions have nearly the same probability
%            1/beta -> inf  - the probability of the action with the highest expected reward tend to 1
%            k (params(2)): from 0 and up, the larger the k parameter, the steeper the discounting of future rewards.      
%            alpha (params(3): alpha > 1 -> risk seeking (convex), 
%            alpha < 1 -> risk averse (concave), alpha = 1 -> risk neutral
switch model
  case {'exp', 'hyp'}
     if isempty(varargin)
        b0 = [1000 0.00004];
     else
        b0 = varargin{1};
     end
     lb = [0.0000001 0];
     ub = [100000    30];
     params = nan(numel(choice),2);
  case {'expcu', 'hypcu'}
     if isempty(varargin)
        b0 = [1000 0.4 0.5];
     else
        b0 = varargin{1};
     end
     lb = [0.0000001 0 -10];
     ub = [100000    25 10];
     params = nan(numel(choice),3);
  case {'hyptimetr', 'hyptimewt'}
     if isempty(varargin)
        b0 = [1000 0.04 0.1 0.5]; %-> refitting bad fits
     else
        b0 = varargin{1};
     end
     lb = [0.0000001 0 0 -10];
     ub = [100000    1000 1000 10];
     params = nan(numel(choice),4);             
  otherwise
    error('fit_discount_loo:bounds','Do not know about model %s', model);
 end


% Fit model, using FMINCON and leave one out cross validation

trials=1:numel(choice);
L = nan(numel(choice),1); % likelihood
exflag = nan(numel(choice),1); % exitflag - whether the model converged (1 - converged, 2 - did not)

for tri=1:numel(choice)
    this_trial = trials==tri;
    Xl = x(~this_trial, :);
    Xlo = x(this_trial, :);
    chlo = choice(this_trial);
    chl = choice(~this_trial);
    f = @(X)l_negLL (X,chl,Xl,model,rule ) ;  % see function def'n for details below
    exitflag = 2;
    try_times = 500;
    while exitflag ~= 1 && try_times>0 % run till it converges with different initial parameters - random walk
        try
        b1 = b0+randn(size(b0))*.2; 
        % if random walk gets beyond bounds catch it
        for pr=1:numel(b0)
            if gt(b1(pr),transpose(ub(pr)))
                b0(pr) = min(b1(pr),transpose(ub(pr)));
            elseif lt(b1(pr),transpose(lb(pr)))
                b0(pr) = max(b1(pr),transpose(lb(pr)));
            else
                b0(pr) = b1(pr);
            end
        end
        
        [b,negLL,exitflag,convg,g,H] = fmincon(f,b0,[],[],[],[],lb,ub); 
        try_times = try_times - 1;
        fprintf('trial: %d\n', tri)
        catch ME
            fprintf('Objective fuction is undefined at initial points\n')
        end
    end
    params(tri,1:numel(b))=b;  
    exflag(tri,1)=exitflag;
    b0 = b; % use estimated coefficient as initial value next round
        if exitflag ~= 1 % trap occasional failures
             fprintf('Optimization FAILED, #iterations = %g\n',convg.iterations);
        else
            fprintf('Optimization CONVERGED, #iterations = %g\n',convg.iterations);
        end
    % Choice probabilities (for LONGER)
    if strcmp(rule,'softmax') % softmax 
       p = softmax(Xlo,b,model);
    elseif strcmp(rule,'matchrule') % matching rule 
       p = matchrule(Xlo,b,model);
    end
    if chlo ==1
        L(tri) = p; % if choice is 1 (Later), then likelihood = choice probability
    else
        L(tri) = 1- p;
    end 
     
end
% Log-likelihood - sum of loglikelihoods at each "leave one out"
logl = log(L);
lgl = logl(~isinf(logl)); % if there are any zeros -> then log(l) will be -INF and sum will be -INF

LL = sum(lgl(~isnan(lgl))); % if there are any nans -> then log(l) will be NAN and sum will be NAN

LL0 = sum((choice==1).*log(0.5) + (1 - (choice==1)).*log(0.5));

info.nobs = nobs;
info.nb = length(b);
info.model = model;
info.exitflag = exflag;
info.b = b;
info.likelihood = L;
info.LL = LL;
info.LL0 = LL0;
info.AIC = -2*LL + 2*length(b);
info.BIC = -2*LL + length(b)*log(nobs);
info.r2 = 1 - LL/LL0;
info.params = params;
%----- NEGATIVE LOG Likelihood
function nll = l_negLL(params,choice,x,model,rule,varargin)
% params: Parameters corresponding to MODEL
%              (1) beta is softmax/matching rule temperature
%              (2) kd is delay coefficient 
%              (3) alpha is constant relative risk aversion (CRRA)
%              coefficient, where exists / or kwt wait time-dependent delay coefficient
%              (4) theta is wait time curvature for time model
% model:  String indicating which model to fit; currently valid are:
%               'exp'       - exponential
%               'hyp'       - Mazur's one-parameter hyperbolic
%               'expcu'     - exponential + curvature (risk attitudes)
%               'hypcu'     - hyperbolic + curvature
%               'hyptime*'   - hyperbolic, time-dependent k; 'tr'-trial
%               number dependent; 'wt'-total waittime dependent
% rule:   String indicating which decision rule to use; currently valid are:
%               'softmax'   - binary logit choice probability
%               'matchrule' - matching rule choice probability
% varargin:      fitting with specified initial values
 

if strcmp(rule,'softmax') % softmax 
   P = softmax(x,params,model);
elseif strcmp(rule,'matchrule') % matching rule 
   P = matchrule(x,params,model);
else
    'you are in trouble'
end

% Trap log(0)
ind = P == 1;
P(ind) = 0.999999;
ind = P == 0;
P(ind) = 0.000001;
% Log-likelihood
err = (choice==1).*log(P) + (1 - (choice==1)).*log(1-P);
% Sum of -log-likelihood
nll = -sum(err);
