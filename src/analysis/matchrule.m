% CHOICE_PROB                Matching rule choice probability
% 
%     P = matchrule(x,params,model);
%
%     INPUTS
%     U1      - values for delayed option (LL)
%     U2      - values for immediate option (SS)
%     params  - Parameters corresponding to MODEL
%              (1) beta is matching rule noise/temperature
%              (2) kd is delay coefficient 
%              (3) alpha is constant relative risk aversion (CRRA)
%              coefficient, where exists/ or kwt wait time-dependent delay coefficient
%                   13/12 update - just power function
%              (4) theta is wait time curvature
%     model   - String indicating which model to fit; currently valid are:
%               'exp'       - exponential
%               'hyp'       - Mazur's one-parameter hyperbolic
%               'expcu'     - exponential + curvature (risk attitudes)
%               'hypcu'     - hyperbolic + curvature
%               'hyptime*'   - hyperbolic, time-dependent k; 'tr'-trial
%               number dependent; 'wt'-total waittime dependent
%     OUTPUTS
%     P       - choice probabilities for the *LONGER* option
function P = matchrule(x,params,model)
v1 = x(:,1);
t1 = x(:,2);
v2 = x(:,3); 
t2 = x(:,4);

k = params(2:end);
beta = params(1);

if strcmp(model,'hyptimetr')
    trial = x(:,5);
    U1 = discountf(v1,t1,k,model,trial);
    U2 = discountf(v2,t2,k,model,trial);
    
elseif strcmp(model,'hyptimewt')
    wait = x(:,5);
    U1 = discountf(v1,t1,k,model,wait);
    U2 = discountf(v2,t2,k,model,wait);
else
    U1 = discountf(v1,t1,k,model);
    U2 = discountf(v2,t2,k,model);
end
P = (U1.^(1/beta))./(U1.^(1/beta) + U2.^(1/beta));