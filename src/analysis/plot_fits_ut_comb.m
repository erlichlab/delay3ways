function plot_fits_ut_comb(data1_m,full,varargin)
%varargin 3 - most/least patient
%varargin 2 - all/early trials
if varargin{1}==3
   treatment = {'NV' 'SV' 'LV'};
   tid = 'MSL';
   
   %most patient
   figure(1); clf;
   ax = draw.jaxes
   cl1 = colormap(parula(10));
   hold on;
   for tx3=1:numel(treatment)
        log_md = median(table2array(full(:,tx3+1))); % check the median of log k for this particular treatment
        % get std -> remove outliers (+-1*std)
        log_std = std(table2array(full(:,tx3+1)));
        fullar = table2array(full(:,[1,tx3+1,17])); %table to array + noise 17
        data1_ses = data1_m(strncmpi(data1_m.treatment,tid(tx3),1),:);
        % join with logk and noise per each subject
        data1_ses = join(data1_ses,full(:,[tx3+1,17,19]));
        full.id = full.subjid;
        full_most = fullar(fullar(:,2)<log_md & fullar(:,2)>log_md-log_std,:); % most patient < median
        %full_most = fullar(fullar(:,2)<log_md,:); % most patient < median
        tout_most = data1_ses(ismember(data1_ses.id,full_most(:,1)),:);
        info.model = 'hyp'; % default
        info.title = treatment{tx3};
        info.b = [mean(full_most(:,3)) mean(exp(full_most(:,2)))]; 
        choice = tout_most.choice;
        logk = table2array(tout_most(:,17));
        v1 = tout_most.rewmag; 
        t1 = tout_most.delay;
        v2 = tout_most.smag;
        t2 = tout_most.sdelay;
        xhat = discountf(v1,t1,exp(logk),info.model)-discountf(v2,t2,exp(logk),info.model);
        [bx,by,be]=stats.binned(xhat, choice==1, 'n_bins', 10); % Jeff prefers stats.binned
        draw.errorplot(ax,bx,by,be,'Color',(cl1(2*tx3-1,:)));
%         fr = @(x) 1/(1+exp(-x./info.b(1)));
%         [fx,fy] = fplot(fr, [-4 6]);
%         plot(ax,fx,fy,'Color',(cl1(2*tx3-1,:)),'LineWidth',2);
        [gB,gDEV,gSTATS] = glmfit(xhat, choice ==1, 'binomial','link','probit');
        xfit = -4:0.1:6;  % pick x points in a smart way
        yfit = glmval(gB, xfit, 'probit');
        plot(ax,xfit,yfit,'Color',(cl1(2*tx3-1,:)),'LineWidth',2);
        ctxt = treatment{tx3};
        text(-3,0.9-(tx3-1)*0.09,ctxt,'Color',(cl1(2*tx3-1,:)));
        hold on;
   end
    ax.XLim = [-4 6];
    ax.YLim = [0 1];
    ax.YTick = [0 0.5 1];
    ylabel(ax, 'P(later)');
    xlabel(ax, 'U(later) - U(sooner)');
    fsave = '../../figs/Fig50mostp_std_dU_comb_glm.pdf';
    set(gcf,'PaperPosition',[0 0 5 4]);
    set(gcf, 'PaperSize', [5 4]);
    saveas(gcf, fsave,'pdf')
   
   %least patient
   figure(2); clf
      ax = draw.jaxes
   cl1 = colormap(parula(10));
   hold on;
   for tx3=1:numel(treatment)
        log_md = median(table2array(full(:,tx3+1))); % check the median of log k for this particular treatment
        % get std -> remove outliers (+-1*std)
        log_std = std(table2array(full(:,tx3+1)));
        fullar = table2array(full(:,[1,tx3+1,17])); %table to array + noise 17
        data1_ses = data1_m(strncmpi(data1_m.treatment,tid(tx3),1),:);
        % join with logk and noise per each subject
        data1_ses = join(data1_ses,full(:,[tx3+1,17,19]));
        full.id = full.subjid;
        full_least = fullar(fullar(:,2)>=log_md,:); % most patient < median
        %full_least = fullar(fullar(:,2)>=log_md & fullar(:,2)<log_md+log_std,:); % least patient >= median
        tout_least = data1_ses(ismember(data1_ses.id,full_least(:,1)),:);
        info.model = 'hyp'; % default
        info.title = treatment{tx3};
        info.b = [mean(full_least(:,3)) mean(exp(full_least(:,2)))]; 
        choice = tout_least.choice;
        logk = table2array(tout_least(:,17));
        v1 = tout_least.rewmag; 
        t1 = tout_least.delay;
        v2 = tout_least.smag;
        t2 = tout_least.sdelay;
        xhat = discountf(v1,t1,exp(logk),info.model)-discountf(v2,t2,exp(logk),info.model);
        [bx,by,be]=stats.binned(xhat, choice==1, 'n_bins', 10); % Jeff prefers stats.binned
        draw.errorplot(ax,bx,by,be,'Color',(cl1(2*tx3-1,:)));
%         fr = @(x) 1/(1+exp(-x./info.b(1)));
%         [fx,fy] = fplot(fr, [-4 6]);
%         plot(ax,fx,fy,'Color',(cl1(2*tx3-1,:)),'LineWidth',2);
        [gB,gDEV,gSTATS] = glmfit(xhat, choice ==1, 'binomial','link','probit');
        xfit = -4:0.1:6;  % pick x points in a smart way
        yfit = glmval(gB, xfit, 'probit');
        plot(ax,xfit,yfit,'Color',(cl1(2*tx3-1,:)),'LineWidth',2);
        ctxt = treatment{tx3};
        text(-3,0.9-(tx3-1)*0.09,ctxt,'Color',(cl1(2*tx3-1,:)));
        hold on;
   end
    ax.XLim = [-4 6];
    ax.YLim = [0 1];
    ax.YTick = [0 0.5 1];
    ylabel(ax, 'P(later)');
    xlabel(ax, 'U(later) - U(sooner)');
    fsave = '../../figs/Fig50leastp_dU_comb_glm.pdf';
    set(gcf,'PaperPosition',[0 0 5 4]);
    set(gcf, 'PaperSize', [5 4]);
    saveas(gcf, fsave,'pdf')

else
    treatment = {'SV' 'LV'};
    tid = 'SL';
%    treatment = {'DV' 'WV'}; %for DW
%    tid = 'DW';
   
   % all trials
   figure(3); clf;
   ax = draw.jaxes
   cl1 = colormap(parula(6));
   hold on;
   for tx3=1:numel(treatment)
        noisetxt = sprintf('%s_noise',treatment{tx3});
        noise_idx = find(strcmpi(full.Properties.VariableNames,noisetxt));
        logk_idx = find(strcmpi(full.Properties.VariableNames,treatment{tx3}))
        id_idx = find(strcmpi(full.Properties.VariableNames,'id'))
        log_m = mean(table2array(full(:,logk_idx)));
        % get std -> remove outliers (+-1*std)
        log_std = std(table2array(full(:,logk_idx)));
        fullar = table2array(full(:,[id_idx,logk_idx,noise_idx])); 
        data1_ses = data1_m(strncmpi(data1_m.treatment,tid(tx3),1),:);
        % join with logk and noise per each subject
        data1_ses = join(data1_ses,full(:,[logk_idx,noise_idx,id_idx]));
        full_all = fullar; % all participants
        %full_all = fullar(fullar(:,2)>log_m-log_std & fullar(:,2)<log_m+log_std,:); % 1 std
        tout_all = data1_ses(ismember(data1_ses.id,full_all(:,1)),:);
        info.model = 'hyp'; % default
        info.title = treatment{tx3};
        info.b = [mean(full_all(:,3)) mean(exp(full_all(:,2)))]; 
        choice = tout_all.choice;
        logk_idx2 = find(strcmpi(tout_all.Properties.VariableNames,treatment{tx3}));
        logk = table2array(tout_all(:,logk_idx2));
        v1 = tout_all.rewmag; 
%         if tx3 ==2 % for DW
%             t1 = tout_all.delay*7;
%         else
%             t1 = tout_all.delay
%         end 
        t1 = tout_all.delay;
        v2 = tout_all.smag;
        t2 = tout_all.sdelay;
        xhat = v1./(1 + exp(logk).*t1) - v2;
        [bx,by,be]=stats.binned(xhat, choice==1, 'n_bins', 10); % Jeff prefers stats.binned
        if tx3==1
            h1 = draw.errorplot(ax,bx,by,be,'Color',(cl1(2*tx3,:)));
        else
            h2 = draw.errorplot(ax,bx,by,be,'Color',(cl1(2*tx3,:)));
        end
        [gB,gDEV,gSTATS] = glmfit(xhat, choice ==1, 'binomial','link','probit');
        xfit = -4:0.1:6;  
        yfit = glmval(gB, xfit, 'probit');
        if tx3==1
            h3 = plot(ax,xfit,yfit,'Color',(cl1(2*tx3,:)),'LineWidth',2,'LineStyle','--');
        else
            h4 = plot(ax,xfit,yfit,'Color',(cl1(2*tx3,:)),'LineWidth',2,'LineStyle','-.');
        end
        %ctxt = treatment{tx3};
        %text(-3,0.9-(tx3-1)*0.09,ctxt,'Color',(cl1(2*tx3-1,:)));
        hold on;
   end
    ax.XLim = [-4 6];
    ax.YLim = [0 1];
    ax.YTick = [0 0.5 1];
    %legend ([h1(2) h3 h2(2) h4],{'SV','','LV',''},'Location','northwest');
    legend ([h3 h4],{'SV','LV'},'Location','northwest');
    legend boxoff                   % Hides the legend's axes
    ylabel(ax, 'P(later)');
    xlabel(ax, 'U(later) - U(sooner)');
    set(ax,'FontSize',16);
    fsave = '../../figs/F5b.pdf';
    outpos = get(gca,'OuterPosition');
    set(gca,'OuterPosition',[outpos(1) outpos(2) + 0.005 outpos(3) outpos(4)])
    set(gcf,'PaperPosition',[0 0 5 4]);
    set(gcf, 'PaperSize', [5 4]);
    saveas(gcf, fsave,'pdf')
    
   % early
   figure(4); clf;
   ax = draw.jaxes;
   cl1 = colormap(parula(6));
   hold on;
   for tx3=1:numel(treatment)
        noisetxt = sprintf('%s_noise',treatment{tx3});
        noise_idx = find(strcmpi(full.Properties.VariableNames,noisetxt));
        logk_idx = find(strcmpi(full.Properties.VariableNames,treatment{tx3}))
        id_idx = find(strcmpi(full.Properties.VariableNames,'id'))
        log_m = mean(table2array(full(:,logk_idx)));
        % get std -> remove outliers (+-1*std)
        log_std = std(table2array(full(:,logk_idx)));
        fullar = table2array(full(:,[id_idx,logk_idx,noise_idx])); %table to array + noise 
        data1_ses = data1_m(strncmpi(data1_m.treatment,tid(tx3),1),:);
        % join with logk and noise per each subject
        data1_ses = join(data1_ses,full(:,[logk_idx,noise_idx,id_idx]));
        full_all = fullar; % all participants
        %full_all = fullar(fullar(:,2)>log_m-log_std & fullar(:,2)<log_m+log_std,:); % 1 std
        tout_all = data1_ses(ismember(data1_ses.id,full_all(:,1)),:);
        tout_early = tout_all(tout_all.trial<5,:); % just first 4 trials 
        info.model = 'hyp'; % default
        info.title = treatment{tx3};
        info.b = [mean(full_all(:,3)) mean(exp(full_all(:,2)))]; 
        choice = tout_early.choice;
        logk_idx2 = find(strcmpi(tout_early.Properties.VariableNames,treatment{tx3}));
        logk = table2array(tout_early(:,logk_idx2));
        v1 = tout_early.rewmag;
%         if tx3 ==2
%             t1 = tout_early.delay*7;
%         else
%             t1 = tout_early.delay;
%         end
        t1 = tout_early.delay;
        v2 = tout_early.smag;
        t2 = tout_early.sdelay;
        xhat = v1./(1 + exp(logk).*t1) - v2;
        [bx,by,be]=stats.binned(xhat, choice==1, 'n_bins', 10); % Jeff prefers stats.binned
        if tx3==1
            h1 = draw.errorplot(ax,bx,by,be,'Color',(cl1(2*tx3,:)));
        else
            h2 = draw.errorplot(ax,bx,by,be,'Color',(cl1(2*tx3,:)));
        end
        [gB,gDEV,gSTATS] = glmfit(xhat, choice ==1, 'binomial','link','probit');
        xfit = -4:0.1:6;  
        yfit = glmval(gB, xfit, 'probit');
        if tx3==1
            h3 = plot(ax,xfit,yfit,'Color',(cl1(2*tx3,:)),'LineWidth',2,'LineStyle','--');
        else
            h4 = plot(ax,xfit,yfit,'Color',(cl1(2*tx3,:)),'LineWidth',2,'LineStyle','-.');
        end
        %ctxt = treatment{tx3};
        %text(-3,0.9-(tx3-1)*0.09,ctxt,'Color',(cl1(2*tx3,:)));
        hold on;
   end
    ax.XLim = [-4 6];
    ax.YLim = [0 1];
    ax.YTick = [0 0.5 1];
    legend ([h3 h4],{'SV','LV'},'Location','northwest');
    legend boxoff                   % Hides the legend's axes
    ylabel(ax, 'P(later)');
    xlabel(ax, 'U(later) - U(sooner)');
    set(ax,'FontSize',16);
    fsave = '../../figs/F5c.pdf';
    outpos = get(gca,'OuterPosition');
    set(gca,'OuterPosition',[outpos(1) outpos(2) + 0.005 outpos(3) outpos(4)])
    set(gcf,'PaperPosition',[0 0 5 4]);
    set(gcf, 'PaperSize', [5 4]);
    saveas(gcf, fsave,'pdf')
end