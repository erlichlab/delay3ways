function fig4ab()
load('../../data/delay3way.mat');
% data preparation
nc_a = table2array(full_nc);
n_idx = find(strcmpi(full_nc.Properties.VariableNames,'NV'));
ne_idx = find(strcmpi(full_nc.Properties.VariableNames,'NVsd'));
s_idx = find(strcmpi(full_nc.Properties.VariableNames,'SV'));
se_idx = find(strcmpi(full_nc.Properties.VariableNames,'SVsd'));
l_idx = find(strcmpi(full_nc.Properties.VariableNames,'LV'));
le_idx = find(strcmpi(full_nc.Properties.VariableNames,'LVsd'));
fn_nc(:,1) = nc_a(:,n_idx);
fn_nc(:,2) = nc_a(:,ne_idx);
fn_nc(:,3) = fn_nc(:,2);
fs_nc(:,1) = nc_a(:,s_idx);
fs_nc(:,2) = nc_a(:,se_idx);
fs_nc(:,3) = fs_nc(:,2);
fl_nc(:,1) = nc_a(:,l_idx);
fl_nc(:,2) = nc_a(:,le_idx);
fl_nc(:,3) = fl_nc(:,2);

% Fig 4 A
figure(20);clf
colormap parula
y = fn_nc;
x = fs_nc;
z = fn_nc;
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
text(-9,0.5,txt,'FontSize', 16);
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
saveas(gcf, '../../figs/NC_F4ac_a.pdf')

% Fig 4 B
x = fs_nc;
z = fn_nc;
y = fl_nc;
figure(21);clf
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
text(-9,0.5,txt,'FontSize', 16);
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
saveas(gcf, '../../figs/NC_F4ac_b.pdf')