function plot_fits_bin3(choice,x,info,mcl,adcl,varargin)
% varargin if you want to narrow the bins / no varargin - default: 5 groups for 5 delays
% vs. 3 bins
v1 = x(:,1); 
t1 = x(:,2); 
v2 = x(:,3);  % 4 short reward
t2 = x(:,4);  % 0 short delay
td = x(:,5); % discrete groups of delays
if isempty(varargin)
    ax = draw.jaxes;
    cl1 = colormap(parula(10)); %spring
    rd = [v1 t1];
    rdz = [rd choice];
    rdzt = array2table(rdz);
    udelay = unique(rdzt.rdz2); % unique categories of delays
    for id = 1:5
        rdzt1 = rdzt(rdzt.rdz2 == udelay(id),{'rdz1','rdz3'});
        dmeans = grpstats(rdzt1,'rdz1','mean');
        ciL = grpstats(rdzt1,'rdz1',@(x)stats.binoci(x,'low',0.05));
        ciU = grpstats(rdzt1,'rdz1',@(x)stats.binoci(x,'high',0.05));
        crew = table2array(dmeans(:,1));
        cch = table2array(dmeans(:,3));
        cciL = table2array(ciL(:,3));
        cciU = table2array(ciU(:,3));
        ccl = cl1(2*id-1,:)*mcl+adcl*ones(size(cl1(2*id-1,:)));
        pl5r = errbar(crew+(id-1)*0.25,cch,(cch-cciL),(cciU-cch),'Color',ccl);
        hold on;
        pl5s = scatter(crew+(id-1)*0.25,cch,40,'filled','MarkerFaceColor',ccl);
        fr = @(r) exp(discountf(r,udelay(id),info.b(2),info.model)/info.b(1))./(exp(discountf(r,udelay(id),info.b(2),info.model)/info.b(1)) + exp(discountf(4,0,info.b(2),info.model)/info.b(1)));
        [fx,fy] = fplot(fr, [-1 12]);
        plot(fx+(id-1)*0.25,fy,'Color',(cl1(2*id-1,:)*mcl+adcl*ones(size(cl1(2*id-1,:)))),'LineWidth',2);
        if strcmp(info.title,'SV')
            ctxt = sprintf('delay = %2.1f',udelay(id));
            text(-0.5,1.4-(id-1)*0.15,ctxt,'Color',(cl1(2*id-1,:)*mcl+adcl*ones(size(cl1(2*id-1,:)))),'FontSize', 16);
        end
        hold on
    end
else
    ax = draw.jaxes;
    cl1 = colormap(parula(6)); %spring
    rd = [v1 t1];
    rdz = [rd choice td];
    rdzt = array2table(rdz);
    delaybin = unique(rdzt.rdz4); % unique categories of delays
    for id = 1:numel(delaybin)
        rdzt1 = rdzt(rdzt.rdz4 == delaybin(id),{'rdz1','rdz2','rdz3'});
        rdzch1 = rdzt(rdzt.rdz4 == delaybin(id),{'rdz1','rdz3'});
        dmeans = grpstats(rdzt1,'rdz1','mean');
        ciL = grpstats(rdzch1,'rdz1',@(x)stats.binoci(x,'low',0.05));
        ciU = grpstats(rdzch1,'rdz1',@(x)stats.binoci(x,'high',0.05));
        crew = table2array(dmeans(:,1));
        cdel = table2array(dmeans(:,3));
        cch = table2array(dmeans(:,4));
        cciL = table2array(ciL(:,3));
        cciU = table2array(ciU(:,3));
        ccl = cl1(2*id-1,:)*mcl+adcl*ones(size(cl1(2*id-1,:)));
        pl5r = errbar(crew+(id-1)*0.25,cch,(cch-cciL),(cciU-cch),'Color',ccl);
        hold on;
        pl5s = scatter(crew+(id-1)*0.25,cch,40,'filled','MarkerFaceColor',ccl);
        fr = @(r) exp(discountf(r,mean(cdel),info.b(2),info.model)/info.b(1))./(exp(discountf(r,mean(cdel),info.b(2),info.model)/info.b(1)) + exp(discountf(4,0,info.b(2),info.model)/info.b(1)));
        [fx,fy] = fplot(fr, [-1 12]);
        plot(fx+(id-1)*0.25,fy,'Color',(cl1(2*id-1,:)*mcl+adcl*ones(size(cl1(2*id-1,:)))),'LineWidth',2);
        if strcmp(info.title,'SV')
            if id==1
                ctxt = 'short delay';
            elseif id==2
                ctxt = 'medium delay';
            else
                ctxt = 'long delay';
            end
            text(-0.5,1.4-(id-1)*0.09,ctxt,'Color',(cl1(2*id-1,:)*mcl+adcl*ones(size(cl1(2*id-1,:)))),'FontSize', 16);
        end
        hold on
    end
end
ax.XLim = [-1 12];
ax.YLim = [0 1.5];
ax.YTick = [0 0.5 1];
ylabel(ax, 'P(later)');
xlabel(ax, 'Reward Magnitude');
set(ax,'FontSize',16);
k = info.b(2);
temp = info.b(1);
txt = sprintf('\nk = %2.3f \n\\tau = %5.2f',k,temp);
text(9,1.3,txt,'FontSize', 16);
text(5.5,1.3,info.title,'fontsize',20);
