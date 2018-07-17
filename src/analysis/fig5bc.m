function fig5bc()
load('../../data/delay3way.mat');
% remove violations
toDelete = isnan(all_trials.choice);
all_trials(toDelete,:) = [];
subjects = unique(all_trials.id);
% remove the NV1
for sb = 1:numel(subjects)
    data1_sub = all_trials(all_trials.id==subjects(sb),:);
    sessions = unique(data1_sub.sessid);
    for ss = 1:numel(sessions)
        data1_subss = data1_sub(data1_sub.sessid==sessions(ss),:);
        data1_subss.trial = transpose(1: size(data1_subss,1));
        if ss==1
            data1_s = data1_subss;
        else
            data1_s = [data1_s;data1_subss];
        end
    end
    data1_subses = data1_s(data1_s.sessid~=sessions(1),:); 
    
    if sb==1
        data1_m = data1_subses;
    else
        data1_m = [data1_m;data1_subses];
    end
end
plot_fits_ut_comb(data1_m,full(:,:),2); %varargin 2 treatments all/early trials 
%full(:,:) instead of full
