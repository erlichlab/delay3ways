% CHOICE_PROB                Softmax - binary logit choice probability
% 
%     P = softmax(x,params,model);
%
%     INPUTS
%     U1      - values for delayed option (LL)
%     U2      - values for immediate option (SS)
%     params  - Parameters corresponding to MODEL
%              (1) beta is softmax temperature
%              (2) kd is individual delay coefficient; k for heuristic
%              models are all params from regression.
%              (3) alpha is constant relative risk aversion (CRRA)
%              coefficient, where exists / or kwt wait time-dependent delay coefficient
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
function P = softmax(x,params,model)
v1 = x(:,1); %later
t1 = x(:,2); %later
v2 = x(:,3); %sooner
t2 = x(:,4); %sooner

k = params(2:end);
beta = params(1);

if strcmp(model,'hyptimetr')
    trial = x(:,5);
    U1 = discountf(v1,t1,k,model,trial);
    U2 = discountf(v2,t2,k,model,trial);
    P = exp(U1/beta)./(exp(U1/beta) + exp(U2/beta));
elseif strcmp(model,'hyptimewt')
    wait = x(:,5);
    U1 = discountf(v1,t1,k,model,wait);
    U2 = discountf(v2,t2,k,model,wait);
    P = exp(U1/beta)./(exp(U1/beta) + exp(U2/beta));
else
    U1 = discountf(v1,t1,k,model);
    U2 = discountf(v2,t2,k,model);
    P = exp(U1/beta)./(exp(U1/beta) + exp(U2/beta));
end
