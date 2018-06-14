% DISCOUNTF                   Discount value
% 
%     y = discountf(v,t,params,model, varargin);
%
%     INPUTS
%     v      - values
%     t      - delays
%     params - (1) kd is individual delay coefficient 
%              (2) alpha is constant relative risk aversion (CRRA)
%              coefficient / or kwt wait time-dependent delay coefficient
%                   13/12 update - just power function
%              (3) theta is wait time curvature
%     model  - String indicating which model to fit. Currently valid are:
%               'exp'       - exponential
%               'hyp'       - Mazur's one-parameter hyperbolic
%               'expcu'     - exponential + curvature (constant relative risk aversion form)
%               'hypcu'     - hyperbolic + curvature
%               'hyptime*'   - hyperbolic, time-dependent k; 'tr'-trial
%               number dependent; 'wt'-total waittime dependent
%
%     OUTPUTS
%     y     - discounted values
function y = discountf(v,t,params,model, varargin)
kd = params(1);
if strcmp(model,'exp') % exponential 
   y = v.*exp(-kd.*t);
elseif strcmp(model,'hyp') % hyperbolic 
   y = v./(1+kd.*t);
elseif strcmp(model,'expcu') % exponential + curvature
    alpha = params(2);
    y = (v.^(alpha)).*exp(-kd.*t);
elseif strcmp(model,'hypcu') % hyperbolic + curvature
    alpha = params(2);
    y = (v.^(alpha))./(1+kd.*t);
elseif strcmp(model,'hyptimetr') % hyperbolic + time-dependent
    kwt = params(2);
    theta = params(3);
    trial = varargin{1};
    y = v./(1+(kd+kwt.*(trial.^theta)).*t);
elseif strcmp(model,'hyptimewt') % hyperbolic + time-dependent
    kwt = params(2);
    theta = params(3);
    wait = varargin{1};
    y = v./(1+(kd+kwt.*(wait.^theta)).*t);
end