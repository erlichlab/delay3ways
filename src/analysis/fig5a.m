function fig5a()
load('../../data/delay3way.mat');
% data prepare
d_idx = find(strcmpi(full_dw.Properties.VariableNames,'DV'));
de_idx = find(strcmpi(full_dw.Properties.VariableNames,'DVsd'));
w_idx = find(strcmpi(full_dw.Properties.VariableNames,'WV'));
we_idx = find(strcmpi(full_dw.Properties.VariableNames,'WVsd'));
odw_idx = find(strcmpi(full_dw.Properties.VariableNames,'order'));
dw_a = table2array(full_dw);
fd(:,1) = dw_a(:,d_idx);
fd(:,2) = dw_a(:,de_idx);
fd(:,3) = fd(:,2);
fw(:,1) = dw_a(:,w_idx);
fw(:,2) = dw_a(:,we_idx);
fw(:,3) = fw(:,2);
order = dw_a(:,odw_idx);
% Fig. 5A
figure(30);clf
colormap spring
y = fd;
x = fw;
z = order;
e = errbar(x(:,1),y(:,1),y(:,2),y(:,3),'Color', [0.6 0.6 0.6]);
hold on;
ex = errbar(x(:,1),y(:,1),x(:,2),x(:,3),'horiz','Color', [0.6 0.6 0.6]);
ylabel('log(k_{DV}), k_{DV} ~ 1/day');
xlabel('log(k_{WV}), k_{WV} ~ 1/day');
set (gca,'FontSize', 12);
set(gca,'Xtick',[-10 -6 -2]);
set(gca,'Ytick',[-10 -6 -2]);
[tau_k,tau_k_p] = corr(y(:,1),x(:,1));
if tau_k_p<0.01
starp='**';
elseif tau_k_p<0.05
starp='*';
else
starp='';
end
txt = sprintf('Pearson r = %5.2f %s',tau_k,starp);
text(-11,-3.5,txt,'FontSize', 16);
fitresult = fit(x(:,1),y(:,1),'poly1'); % or lowess - local linear regression (surface)
p22 = predint(fitresult,[-12 ; unique(x(:,1)) ; 0],0.95,'functional','on');
xshade = [-12 ; unique(x(:,1)) ; 0];
ptch = patch([xshade; flipud(xshade)], [p22(:,2); flipud(p22(:,1))], 'm');
ptch.FaceAlpha = 0.1;
ptch.EdgeAlpha = 0;
scatter(x(:,1),y(:,1),40,z(:,1),'filled','MarkerEdgeColor',[0.3 0.3 0.3]);
h = lsline;
p2 = polyfit(get(h,'xdata'),get(h,'ydata'),1);
un = draw.unity;
xlim([-12,0]);
ylim([-12,0]);
set(gca,'FontSize',16);
set(gcf,'PaperPosition',[0 0 5 4]);
set(gcf, 'PaperSize', [5 4]);
saveas(gcf, '../../figs/DW_F5ac_a.pdf')
