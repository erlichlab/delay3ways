function fig3c()
load('../../data/posterior_delay3way.mat');
figure(40);clf;
ax = draw.jaxes;
axes(ax);
cl = parula(6);
[f1,x1] = ksdensity(logk_NV); plot(x1,f1,'Color',cl(1,:),'LineWidth',2); hold on;
[f2,x2] = ksdensity(logk_SV); plot(x2,f2,'--','Color',cl(2,:),'LineWidth',2);    %title('SV vs. NV');
hold on; [f3,x3] = ksdensity(logk_LV); plot(x3,f3,'-.','Color',cl(4,:),'LineWidth',2);
%legend ('log(k_{NV})','log(k_{SV})', 'log(k_{LV})','Location','northwest');
legend ('NV','SV', 'LV','Location','northwest');
legend boxoff                   % Hides the legend's axes
xlabel('log(k)','Fontsize',16);
ylabel('probability density estimate','Fontsize',16);
%ylim([0,0.4])
xlim([-7,-1])
set(gca,'FontSize',16);
outpos = get(gca,'OuterPosition');
set(gca,'OuterPosition',[outpos(1) outpos(2) + 0.005 outpos(3) outpos(4)])
set(gcf,'PaperPosition',[0 0 5 4]);
set(gcf, 'PaperSize', [5 4]);
saveas(gcf, '../../figs/F3ac_cout.pdf')