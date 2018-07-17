function fig3ab()
load('../../data/delay3way.mat');
% data prepare
full_a = table2array(full(:,:)); % full(:,:) instead of full
n_idx = find(strcmpi(full.Properties.VariableNames,'NV'));
ne_idx = find(strcmpi(full.Properties.VariableNames,'NVsd'));
s_idx = find(strcmpi(full.Properties.VariableNames,'SV'));
se_idx = find(strcmpi(full.Properties.VariableNames,'SVsd'));
l_idx = find(strcmpi(full.Properties.VariableNames,'LV'));
le_idx = find(strcmpi(full.Properties.VariableNames,'LVsd'));
fn(:,1) = full_a(:,n_idx);
fn(:,2) = full_a(:,ne_idx);
fn(:,3) = fn(:,2);
fs(:,1) = full_a(:,s_idx);
fs(:,2) = full_a(:,se_idx);
fs(:,3) = fs(:,2);
fl(:,1) = full_a(:,l_idx);
fl(:,2) = full_a(:,le_idx);
fl(:,3) = fl(:,2);

% Fig 3 A
figure(10);clf
colormap parula
y = fn;
x = fs;
z = fn;
e = errbar(x(:,1),y(:,1),y(:,2),y(:,3),'Color', [0.6 0.6 0.6]);
hold on;
ex = errbar(x(:,1),y(:,1),x(:,2),x(:,3),'horiz','Color', [0.6 0.6 0.6]);
ylabel('log(k_{NV}), k_{NV} ~ 1/sec');
xlabel('log(k_{SV}), k_{SV} ~ 1/sec');
set (gca,'FontSize', 16);
set(gca,'Xtick',[-8 -4 0]);
set(gca,'Ytick',[-8 -4 0]);
[tau_k,tau_k_p] = corr(y(:,1),x(:,1));
if tau_k_p<0.01
starp='**';
elseif tau_k_p<0.05
starp='*';
else
starp='';
end
txt = sprintf('Pearson r = %5.2f %s',tau_k,starp);
text(-9,3,txt,'FontSize', 16);
fitresult = fit(x(:,1),y(:,1),'poly1'); % or lowess - local linear regression (surface)
p22 = predint(fitresult,[-10 ; unique(x(:,1)) ; 4],0.95,'functional','on');
xshade = [-10 ; unique(x(:,1)) ; 4];
ptch = patch([xshade; flipud(xshade)], [p22(:,2); flipud(p22(:,1))], 'g');
ptch.FaceAlpha = 0.1;
ptch.EdgeAlpha = 0;
scatter(x(:,1),y(:,1),40,z(:,1),'filled','MarkerEdgeColor',[0.3 0.3 0.3]);
h = lsline;
p2 = polyfit(get(h,'xdata'),get(h,'ydata'),1);
un = draw.unity;
xlim([-10,4]);
ylim([-10,4]);
hold on;
cax = colorbar;
ylabel(cax, 'log(k_{NV})');
set(gcf,'PaperPosition',[0 0 5 4]);
set(gcf, 'PaperSize', [5 4]);
saveas(gcf, '../../figs/F3ac_a.pdf')

% Fig 3 B
x = fs;
z = fn;
y = fl;
figure(11);clf
colormap parula
e = errbar(x(:,1),y(:,1),y(:,2),y(:,3),'Color', [0.6 0.6 0.6]);
hold on;
ex = errbar(x(:,1),y(:,1),x(:,2),x(:,3),'horiz','Color', [0.6 0.6 0.6]);
ylabel('log(k_{LV}), k_{LV} ~ 1/day');
xlabel('log(k_{SV}), k_{SV} ~ 1/sec');
set (gca,'FontSize', 16);
set(gca,'Xtick',[-8 -4 0]);
set(gca,'Ytick',[-8 -4 0]);
[tau_k,tau_k_p] = corr(x(:,1),y(:,1));
if tau_k_p<0.01
starp='**';
elseif tau_k_p<0.05
starp='*';
else
starp='';
end
txt = sprintf('Pearson r = %5.2f %s',tau_k,starp);
text(-9,3,txt,'FontSize', 16);
fitresult2 = fit(x(:,1),y(:,1),'poly1'); % or lowess - local linear regression (surface)
p23 = predint(fitresult2,[-10 ; unique(x(:,1)) ; 4],0.95,'functional','on');
xshade = [-10 ; unique(x(:,1)) ; 4];
ptch2 = patch([xshade; flipud(xshade)], [p23(:,2); flipud(p23(:,1))], 'g');
ptch2.FaceAlpha = 0.1;
ptch2.EdgeAlpha = 0;
scatter(x(:,1),y(:,1),40,z(:,1),'filled','MarkerEdgeColor',[0.3 0.3 0.3])
h = lsline;
p2 = polyfit(get(h,'xdata'),get(h,'ydata'),1)
un = draw.unity;
xlim([-10,4]);
ylim([-10,4]);
hold on;
cax = colorbar;
ylabel(cax, 'log(k_{NV})');
set(gcf,'PaperPosition',[0 0 5 4]);
set(gcf, 'PaperSize', [5 4]);
saveas(gcf, '../../figs/F3ac_b.pdf')