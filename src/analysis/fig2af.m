function fig2af()
load('~/repos/delay3ways/data/delay3way.mat');
% remove violations
toDelete = isnan(all_trials.choice);
all_trials(toDelete,:) = [];
subjects = unique(all_trials.id);
for sb = 1:numel(subjects)
    data1_sub = all_trials(all_trials.id==subjects(sb),:);
    sessions = unique(data1_sub.sessid);
    data1_subses = data1_sub(data1_sub.sessid~=sessions(1),:); % remove the NV1
    % NV1 has a significantly higher proportion of first-order violations
    % than NV2 and NV3 and, thus was removed from analysis (SI Results)
    if sb==1
        data1_m = data1_subses;
    else
        data1_m = [data1_m;data1_subses];
    end
end
treatment = {'NV' 'SV' 'LV'};
tid = 'MSL';
    for tx3=1:3 
        noisetxt = sprintf('%s_noise',treatment{tx3});
        noise_idx = find(strcmpi(full.Properties.VariableNames,noisetxt));
        logk_idx = find(strcmpi(full.Properties.VariableNames,treatment{tx3}));
        % check the median of log k for this particular treatment -> 
        % 50% median split into more and less patient subjects
        log_md = median(table2array(full(:,logk_idx))); 
        % get std -> remove outliers (+-1*std)
        log_std = std(table2array(full(:,logk_idx)));
        fullar = table2array(full(:,[1,logk_idx,noise_idx])); %table to array
        data1_ses = data1_m(strncmpi(data1_m.treatment,tid(tx3),1),:);
        % join with logk and noise per each subject
        id_idx = find(strcmpi(full.Properties.VariableNames,'id'))
        data1_ses = join(data1_ses,full(:,[logk_idx,noise_idx,id_idx]));
        % most patient < median
        full_most = fullar(fullar(:,2)<log_md & fullar(:,2)>log_md-log_std,:); 
        % least patient >= median
        full_least = fullar(fullar(:,2)>=log_md & fullar(:,2)<log_md+log_std,:); 
        tout_most = data1_ses(ismember(data1_ses.id,full_most(:,1)),:);
        tout_least = data1_ses(ismember(data1_ses.id,full_least(:,1)),:);
        % if bin in 3 delays
        edgesd = [0 7 15 70];
        tout_most.blockd = discretize(tout_most.delay,edgesd); % 3 bins of delays
        tout_least.blockd = discretize(tout_least.delay,edgesd); % 3 bins of delays
        info.model = 'hyp'; % default
        info.title = treatment{tx3};
        if tx3==1
            mcl = 3/4;% use shades 1/2
            adcl = 0;
        elseif tx3==2
            mcl = 1; 
            adcl = 0;
        else
            mcl = 1/2;% use tints
            adcl = 1/2;
        end
        figname = sprintf('Most_%s',treatment{tx3});  
        figure('Name',figname,'NumberTitle','off');clf %most
        info.b = [mean(full_most(:,3)) mean(exp(full_most(:,2)))];
        noise_idx = find(strcmpi(tout_most.Properties.VariableNames,noisetxt));
        logk_idx = find(strcmpi(tout_most.Properties.VariableNames,treatment{tx3}));
        D = [tout_most.rewmag tout_most.delay tout_most.smag tout_most.sdelay tout_most.blockd table2array(tout_most(:,logk_idx)) table2array(tout_most(:,noise_idx))];
        choice = tout_most.choice;
        plot_fits_bin3(choice,D,info,mcl,adcl);
        fsave = sprintf('~/repos/delay3ways/data/F2m_%d.pdf',tx3);
        outpos = get(gca,'OuterPosition');
        set(gca,'OuterPosition',[outpos(1) outpos(2) + 0.005 outpos(3) outpos(4)])
        set(gcf,'PaperPosition',[0 0 5 4]);
        set(gcf, 'PaperSize', [5 4]);
        %saveas(gcf, fsave,'pdf')
        figname = sprintf('Least_%s',treatment{tx3});  
        figure('Name',figname,'NumberTitle','off');clf %least
        info.b = [mean(full_least(:,3)) mean(exp(full_least(:,2)))]; 
        logk_idx2 = find(strcmpi(tout_least.Properties.VariableNames,treatment{tx3}));
        noise_idx2 = find(strcmpi(tout_least.Properties.VariableNames,noisetxt));
        D = [tout_least.rewmag tout_least.delay tout_least.smag tout_least.sdelay tout_least.blockd  table2array(tout_least(:,logk_idx2)) table2array(tout_least(:,noise_idx2))];
        choice = tout_least.choice;
        plot_fits_bin3(choice,D,info,mcl,adcl);
        fsave = sprintf('~/repos/delay3ways/data/F2l_%d.pdf',tx3);
        outpos = get(gca,'OuterPosition');
        set(gca,'OuterPosition',[outpos(1) outpos(2) + 0.005 outpos(3) outpos(4)])
        set(gcf,'PaperPosition',[0 0 5 4]);
        set(gcf, 'PaperSize', [5 4]);
        %saveas(gcf, fsave,'pdf')
    end