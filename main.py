import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from qqplot import qqplot
from dataframe_process import add_timeinseconds_col
from utils import filter_prec, rmse, stdev, sum_chunk, time_convert
from src import settings

def main():
    met_stn_data_path=os.path.join(settings.data_path,'AB_RMF_bonsai_meteorological.txt')


    df = pd.read_csv(met_stn_data_path,sep=" |\t",header=None,usecols=[0,1,2],names=['Date','Time','prec'],engine='python')

    df,full_list=add_timeinseconds_col(df)
    time_list_mswep=full_list[::12]
    Prec2 = df.prec



    Prec_station_3H=Prec2[:210324].values.reshape(-1, 12).sum(1)
    Prec_station_3H_16_20=Prec_station_3H[5839:]#precipitation from 2016 jan 01
    time_list_gsmap_station=time_list_mswep[5839:]

    cmorph_timeseries_WISKI=os.path.join(settings.data_path,"cmorph_timeseries_WISKI.txt")
    cmorph_data = np.loadtxt(cmorph_timeseries_WISKI)
    time=cmorph_data[:,0]
    NHours=np.size(time)
    cmorph_prec_B1=cmorph_data[:,5]
    cmorph_prec_B1_3H=sum_chunk(cmorph_prec_B1,3)
    cmorph_prec_B1_3H=cmorph_prec_B1_3H[:17527]
    cmorph_prec_B2=cmorph_data[:,8]
    cmorph_prec_B2_3H=sum_chunk(cmorph_prec_B2,3)
    cmorph_prec_B2_3H=cmorph_prec_B2_3H[:17527]
    cmorph_time_list=cmorph_data[:,3]
    cmorph_time_list_3H=cmorph_time_list[::3]

    imerg_timeseries_WISKI = os.path.join(settings.data_path,"imerg_timeseries_WISKI.txt")
    imerg_data = np.loadtxt(imerg_timeseries_WISKI)
    time2=imerg_data[:,0]
    NHours2=np.size(time2)
    imerg_prec_B1=imerg_data[:,5]
    imerg_prec_B1_3H=sum_chunk(imerg_prec_B1,6)#accumulated every 3 hours (6 times 30min)
    imerg_prec_B1_3H=imerg_prec_B1_3H[:17527]
    imerg_prec_B2=imerg_data[:,8]
    imerg_prec_B2_3H=sum_chunk(imerg_prec_B2,6)#accumulated every 3 hours
    imerg_prec_B2_3H=imerg_prec_B2_3H[:17527]
    imerg_time=imerg_data[:,3]
    imerg_time_list_3H=imerg_time[::6] #time stamp every 3 hours

    gsmap_timeseries_WISKI = os.path.join(settings.data_path,"gsmap_timeseries_WISKI.txt")
    gsmap_data = np.loadtxt(gsmap_timeseries_WISKI)
    time3=gsmap_data[:,0]
    NHours3=np.size(time3)
    gsmap_prec_B1=gsmap_data[:,5]
    gsmap_prec_B2=gsmap_data[:,8]
    gsmap_year=gsmap_data[:,0]
    gsmap_month=gsmap_data[:,1]
    gsmap_day=gsmap_data[:,2]
    gsmap_hour=gsmap_data[:,3]
    gsmap_time_list=np.zeros(len(gsmap_year))
    index=0
    for index in range(len(gsmap_year)):
        gsmap_time_list[index]=time_convert(int(gsmap_year[index]),int(gsmap_month[index]),int(gsmap_day[index]),int(gsmap_hour[index]),0)
    gsmap_time_list_16_20=gsmap_time_list[:35064]
    gsmap_time_list_16_20_3H=gsmap_time_list_16_20[::3]
    gsmap_prec_B1_2016_2020=gsmap_prec_B1[:35064]
    gsmap_prec_B1_16_20_3H=sum_chunk(gsmap_prec_B1_2016_2020,3)
    gsmap_prec_B2_2016_2020=gsmap_prec_B2[:35064]
    gsmap_prec_B2_16_20_3H=sum_chunk(gsmap_prec_B2_2016_2020,3)

    mswep_timeseries_WISKI = os.path.join(settings.data_path,"mswep_timeseries_WISKI.txt")
    mswep_data = np.loadtxt(mswep_timeseries_WISKI)
    time4=mswep_data[:,0]
    NHours4=np.size(time4)
    mswep_prec_B1=mswep_data[:,5]
    mswep_prec_B2=mswep_data[:,8]
    mswep_time=mswep_data[:,3]
    mswep_time_list = [(x-613608)*3600 for x in mswep_time]
    mswep_prec_B1=mswep_prec_B1[:17527]
    mswep_prec_B2=mswep_prec_B2[:17527]


    mswep_prec_B1_3H_filter,Prec_station_3H_filter_m1=filter_prec(mswep_prec_B1,Prec_station_3H,0.2)
    rmse_mswep1=rmse(mswep_prec_B1_3H_filter,Prec_station_3H_filter_m1)
    corr_mswep1 = np.corrcoef(mswep_prec_B1_3H_filter,Prec_station_3H_filter_m1)
    std_mswep1=stdev(mswep_prec_B1_3H_filter)
    std_Bonsai=stdev(Prec_station_3H_filter_m1)

    mswep_prec_B2_3H_filter,Prec_station_3H_filter_m2=filter_prec(mswep_prec_B2,Prec_station_3H,0.2)
    rmse_mswep2=rmse(mswep_prec_B2_3H_filter,Prec_station_3H_filter_m2)
    corr_mswep2 = np.corrcoef(mswep_prec_B2_3H_filter,Prec_station_3H_filter_m2)
    std_mswep2=stdev(mswep_prec_B2_3H_filter)


    print('Bonsai_std=',std_Bonsai)


    print('MSWEP1: std, corr,rmse:', std_mswep1,corr_mswep1[0,1],rmse_mswep1)
    print('MSWEP2: std, corr,rmse:', std_mswep2,corr_mswep2[0,1],rmse_mswep2)

    cmorph_prec_B1_3H_filter,Prec_station_3H_filter_c1=filter_prec(cmorph_prec_B1_3H,Prec_station_3H,0.2)
    rmse_cmorph1=rmse(cmorph_prec_B1_3H_filter,Prec_station_3H_filter_c1)
    corr_cmorph1 = np.corrcoef(cmorph_prec_B1_3H_filter,Prec_station_3H_filter_c1)
    std_cmorph1=stdev(cmorph_prec_B1_3H_filter)
    cmorph_prec_B2_3H_filter,Prec_station_3H_filter_c2=filter_prec(cmorph_prec_B2_3H,Prec_station_3H,0.2)
    rmse_cmorph2=rmse(cmorph_prec_B2_3H_filter,Prec_station_3H_filter_c2)
    corr_cmorph2 = np.corrcoef(cmorph_prec_B2_3H_filter,Prec_station_3H_filter_c2)
    std_cmorph2=stdev(cmorph_prec_B2_3H_filter)



    print('cmorph1: std, corr,rmse:', std_cmorph1,corr_cmorph1[0,1],rmse_cmorph1)
    print('cmorph2: std, corr,rmse:', std_cmorph2,corr_cmorph2[0,1],rmse_cmorph2)

    imerg_prec_B1_3H_filter,Prec_station_3H_filter_i1=filter_prec(imerg_prec_B1_3H,Prec_station_3H,0.2)
    rmse_imerg1=rmse(imerg_prec_B1_3H_filter,Prec_station_3H_filter_i1)
    corr_imerg1 = np.corrcoef(imerg_prec_B1_3H_filter,Prec_station_3H_filter_i1)
    std_imerg1=stdev(imerg_prec_B1_3H_filter)
    imerg_prec_B2_3H_filter,Prec_station_3H_filter_i2=filter_prec(imerg_prec_B2_3H,Prec_station_3H,0.2)
    rmse_imerg2=rmse(imerg_prec_B2_3H_filter,Prec_station_3H_filter_i2)
    corr_imerg2 = np.corrcoef(imerg_prec_B2_3H_filter,Prec_station_3H_filter_i2)
    std_imerg2=stdev(imerg_prec_B2_3H_filter)


    print('imerg1: std, corr,rmse:', std_imerg1,corr_imerg1[0,1],rmse_imerg1)
    print('imerg2: std, corr,rmse:', std_imerg2,corr_imerg2[0,1],rmse_imerg2)


    gsmap_prec_B1_3H_filter,Prec_station_3H_filter_gsmap_g1=filter_prec(gsmap_prec_B1_16_20_3H,Prec_station_3H_16_20,0.2)
    rmse_gsmap1=rmse(gsmap_prec_B1_3H_filter,Prec_station_3H_filter_gsmap_g1)
    corr_gsmap1 = np.corrcoef(gsmap_prec_B1_3H_filter,Prec_station_3H_filter_gsmap_g1)
    std_gsmap1=stdev(gsmap_prec_B1_3H_filter)
    gsmap_prec_B2_3H_filter,Prec_station_3H_filter_gsmap_g2=filter_prec(gsmap_prec_B2_16_20_3H,Prec_station_3H_16_20,0.2)
    rmse_gsmap2=rmse(gsmap_prec_B2_3H_filter,Prec_station_3H_filter_gsmap_g2)
    corr_gsmap2 = np.corrcoef(gsmap_prec_B2_3H_filter,Prec_station_3H_filter_gsmap_g2)
    std_gsmap2=stdev(gsmap_prec_B2_3H_filter)


    print('gsmap1: std, corr,rmse:', std_gsmap1,corr_gsmap1[0,1],rmse_gsmap1)
    print('gsmap2: std, corr,rmse:', std_gsmap2,corr_gsmap2[0,1],rmse_gsmap2)


    filter=0.2
    Prec_station_3H_filter = [i for i in Prec_station_3H if i >= filter]
    Prec_station_3H__16_20_filter = [i for i in Prec_station_3H_16_20 if i >= filter]

    fig = plt.figure(figsize=(10,10))
    ax = plt.gca()
    qqplot(Prec_station_3H_filter, cmorph_prec_B1_3H_filter, c='r', alpha=0.5,marker='o',linestyle="None", label='CMORPH Grid1', ms=29)
    qqplot(Prec_station_3H_filter, imerg_prec_B1_3H_filter, c='b', alpha=0.5,marker='o',linestyle="None",  label='IMERG Grid1', ms=29)
    qqplot(Prec_station_3H_filter, gsmap_prec_B1_3H_filter, c='g', marker='o',alpha=0.5,linestyle="None",  label='GSMaP Grid1', ms=29)
    qqplot(Prec_station_3H_filter, mswep_prec_B1_3H_filter, c='m', alpha=0.5,marker='o',linestyle="None",  label='MSWEP Grid1', ms=29)
    plt.plot(imerg_prec_B1_3H_filter,imerg_prec_B1_3H_filter,c='k')
    qqplot(Prec_station_3H_filter, cmorph_prec_B2_3H_filter, c='r', alpha=0.5,marker='^',linestyle="None",  label='CMORPH Grid2', ms=29)
    qqplot(Prec_station_3H_filter, imerg_prec_B2_3H_filter, c='b', alpha=0.5,marker='^',linestyle="None",  label='IMERG Grid2', ms=29)
    qqplot(Prec_station_3H_filter, gsmap_prec_B2_3H_filter, c='g', alpha=0.5,marker='^',linestyle="None",  label='GSMaP Grid2', ms=29)
    qqplot(Prec_station_3H_filter, mswep_prec_B2_3H_filter, c='m', alpha=0.5, marker='^',linestyle="None", label='MSWEP Grid2', ms=29)
    plt.xlabel('Station quantile prec. (mm/3h)',fontsize = 40)
    plt.ylabel('Satellite quantile prec. (mm/3h)',fontsize = 40)
    plt.suptitle('Fortress Bonsai',fontsize=40)
    ax.tick_params(axis="x")
    ax.tick_params(axis="y")
    plt.xticks(fontsize=40)
    plt.yticks(fontsize=40)
    plt.legend(loc='lower right', frameon=False, prop={'size': 20});
    plt.tight_layout()
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(os.path.join(settings.output_path,'QQplot_Bonsai_satellites_grid1_grid2_3H_filterlog.pdf'))
    fig.savefig(os.path.join(settings.output_path,'QQplot_Bonsai_satellites_grid1_grid2_3H_filterlog.png'))
    
if __name__ == '__main__':
    main()
    