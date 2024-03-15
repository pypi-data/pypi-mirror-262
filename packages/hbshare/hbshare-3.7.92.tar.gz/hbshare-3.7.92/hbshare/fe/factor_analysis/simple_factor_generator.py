import  numpy as np
import pandas as pd
from hbshare.fe.XZ import  functionality
from hbshare.fe.XZ import db_engine as dbeng
import datetime

util=functionality.Untils()
hbdb=dbeng.HBDB()
localdb=dbeng.PrvFunDB().engine

def get_jjnav_bydate(jjdm_list,date_list):

    sql="select jjdm,jzrq,fqdwjz from st_fund.t_st_gm_rhb where jzrq in ({0}) and jjdm in ({1})"\
        .format(util.list_sql_condition(date_list),
                util.list_sql_condition(jjdm_list))

    jj_nav=hbdb.db2df(sql,db='funduser')

    return  jj_nav

def create_stock_shift_ratio():

    hsl=pd.read_excel(r"E:\GitFolder\hbshare\fe\factor_analysis\换手率.xlsx")
    date_col=hsl.columns.tolist()
    date_col.remove('证券简称')
    date_col.remove('证券代码')
    new_date_col=[]
    date_map=dict()
    hsl['jjdm'] = hsl['证券代码'].str[0:6]
    for i in range(len(date_col)):
        new_date_col.append(date_col[i].replace('H1','0630').replace(' ','').replace('H2', '1231'))

    date_map = dict(zip(date_col,new_date_col))

    outputdf=pd.DataFrame()
    tempdf=pd.DataFrame()
    tempdf['jjdm']=util.get_mutual_stock_funds('20211231')
    tempdf=pd.merge(tempdf,hsl,how='left',on='jjdm')

    for date in date_col:
        tempdf2=tempdf[['jjdm',date]]
        tempdf2['date']=date_map[date]
        tempdf2.rename(columns={date:'hsl'},inplace=True)
        outputdf=pd.concat([outputdf,tempdf2],axis=0)

    outputdf=outputdf[outputdf['hsl'].notnull()]

    outputdf.to_sql('factor_hsl',con=localdb,index=False,if_exists='append')

def read_factors(table_name):

    sql="select * from {}".format(table_name)
    df=pd.read_sql(sql,con=localdb)

    return  df

def bhar(arr):
    return 100 * (np.power(np.cumprod((arr + 100) / 100).tolist()[-1], 1 / len(arr)) - 1)

def get_quarter_ret(arr):

    return  np.cumprod(arr/100+1).tolist()[-1]-1

def hsl_rank2db(dir):

    #get the hsl raw data first
    # sql="select * from factor_hsl  "
    # df=pd.read_sql(sql,con=localdb)
    df=pd.read_csv(dir)
    df['hsl_rank']=df.groupby('date').rank(method='min')
    count=df.groupby('date', as_index=False).count()[['date', 'jjdm']]
    count.rename(columns={'jjdm':'count'},inplace=True)
    df=pd.merge(df,count,how='left',on='date')
    df['hsl_rank']=df['hsl_rank']/df['count']
    df.to_sql('factor_hsl',con=localdb,index=False,if_exists='append')

def save_fund_return_factor2db():

    jjdm_list=util.get_mutual_stock_funds('20211231')

    #get year end date

    sql_script = "SELECT jyrq JYRQ, sfjj SFJJ, sfym SFYM,sfzm SFZM FROM st_main.t_st_gg_jyrl WHERE jyrq >= {0} and jyrq <= {1} and sfjj=0 ".format(
        '20141231', datetime.datetime.today().strftime('%Y%m%d'))
    trade_calander = hbdb.db2df(sql_script, db='alluser').drop('ROW_ID',axis=1).sort_values('JYRQ')
    month_end_list=trade_calander[trade_calander['SFYM']=='1']['JYRQ'].tolist()
    #
    # trade_calander['year'] = trade_calander['JYRQ'].astype(str).str[0:4]
    # year_end_list=trade_calander.groupby('year')['JYRQ'].max().tolist()

    #get month end jj fqnav

    jj_nav=get_jjnav_bydate(jjdm_list,month_end_list)
    jj_nav['month'] = jj_nav['jzrq'].astype(str).str[4:6]
    jj_nav['date']=jj_nav['jzrq']
    jj_nav.set_index('jzrq',inplace=True)
    #get jj year return for each month end date
    jj_nav['quarter_logret']=np.log(jj_nav.groupby('jjdm')['fqdwjz'].pct_change(3)+1)
    jj_nav['half_year_logret']=np.log(jj_nav.groupby('jjdm')['fqdwjz'].pct_change(6)+1)
    jj_nav['year_logret']=np.log(jj_nav.groupby('jjdm')['fqdwjz'].pct_change(12)+1)
    jj_nav['2year_logret'] = np.log(jj_nav.groupby('jjdm')['fqdwjz'].pct_change(24) + 1)
    jj_nav['3year_logret'] = np.log(jj_nav.groupby('jjdm')['fqdwjz'].pct_change(36) + 1)

    jj_nav['year_end_flag']=0
    jj_nav['quarter_end_flag'] = 0
    jj_nav.loc[jj_nav['month']=='12','year_end_flag']=1
    jj_nav.loc[jj_nav['month'].isin(['03','06','09','12'])
    , 'quarter_end_flag'] = 1
    jj_nav['date']=jj_nav['date'].astype(str)

    #localdb.execute('delete from factor_year_ret')
    jj_nav[jj_nav.notnull()].rename(columns={'jzrq':'date'})[['jjdm','quarter_logret','half_year_logret'
        , 'year_logret','2year_logret','3year_logret', 'date','year_end_flag', 'quarter_end_flag']].to_sql('factor_year_ret'
                                                                       ,con=localdb
                                                                       ,index='False'
                                                                       ,if_exists='append')

def save_fund_return_factor_histoyr2db(start_date,end_date):


    sql_script = "SELECT jyrq JYRQ,sfjj SFJJ, sfym SFYM,sfzm SFZM FROM st_main.t_st_gg_jyrl WHERE jyrq >= {} and jyrq <= {}".format(
        start_date, end_date)
    df = hbdb.db2df(sql_script, db='alluser')
    df = df.rename(
        columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                 "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
    date_list=df[(df['isMonthEnd'] == '1') & (df['isOpen'] == '0')]['calendarDate'].tolist()

    fund_data=[]

    for date in date_list:

        jjdm_list=util.get_stock_funds_pool(date,1.5)
        sql="select zbnp,zblb,jjdm,jzrq as date  from st_fund.t_st_gm_rqjhb where jjdm in {0} and jzrq='{1}' and zblb in ('2101','2103','2106','2201','2202') and zbnp!=99999"\
            .format(tuple(jjdm_list),date)
        db_data=hbdb.db2df(sql,db='funduser').pivot_table('zbnp','jjdm','zblb').reset_index()
        db_data['date']=date

        fund_data.append(db_data)

    localdb.execute("delete from funds_ret_history_monthly")
    pd.concat(fund_data,axis=0).to_sql('funds_ret_history_monthly',con=localdb,index=False,if_exists='append')


def save_fund_rank_factor2db():

    #get the quarter end date
    sql= "SELECT jyrq JYRQ, sfym SFYM FROM st_main.t_st_gg_jyrl WHERE jyrq >= {0} and jyrq<={1} and sfjj=0 and sfym=1".format(
        '20160101',datetime.datetime.today().strftime('%Y%m%d'))
    calander = hbdb.db2df(sql, db='alluser')
    calander['month']=calander['JYRQ'].astype(str).str[4:6]
    calander=calander.loc[calander['month'].isin(['03','06','09','12'])]['jsrq'].tolist()
    # calander=calander['JYRQ'].tolist()
    calander.sort()

    result=[[],[],[]]
    result2 = [[], [], []]
    result3=[[],[],[]]
    result4 = [[], [], []]


    for date in calander:
        fund_pool=util.get_mutual_stock_funds(date,2)
        sql = "select jjdm,tjyf,rqzh,hb1y from st_fund.t_st_gm_yhb where jjdm in ({0}) and rq1y!=99999 {1} {2} " \
            .format(util.list_sql_condition(fund_pool)
                    , "and rqzh>='{}'".format( str(int(date[0:4])-5)+date[4:6]+'01')
                    , "and rqzh<='{}'".format(date))
        montly_ret = hbdb.db2df(sql, db='funduser')

        #get quarter,half_yearly,yearly return
        montly_ret['hb1q']=montly_ret.groupby('jjdm')['hb1y'].rolling(3).apply(get_quarter_ret).values
        montly_ret['hb1hy']=montly_ret.groupby('jjdm')['hb1y'].rolling(6).apply(get_quarter_ret).values
        montly_ret['hb1y']=montly_ret.groupby('jjdm')['hb1y'].rolling(12).apply(get_quarter_ret).values
        montly_ret['month']=montly_ret['rqzh'].astype(str).str[4:6]
        first_month=montly_ret['tjyf'].min()
        montly_ret=montly_ret.loc[(montly_ret['month'].isin(['03','06','09','12']))&(montly_ret['tjyf']!=first_month)]


        montly_ret=pd.merge(montly_ret,montly_ret.groupby('tjyf').mean()[['hb1q', 'hb1hy', 'hb1y']].rename(columns={'hb1q':'hb1q_mean'
            , 'hb1hy':'hb1hy_mean'
            , 'hb1y':'hb1y_mean'}),how='left',on='tjyf')

        montly_ret=pd.merge(montly_ret,montly_ret.groupby('tjyf').median()[['hb1q', 'hb1hy', 'hb1y']].rename(columns={'hb1q':'hb1q_median'
            , 'hb1hy':'hb1hy_median'
            , 'hb1y':'hb1y_median'}),how='left',on='tjyf')


        montly_ret=pd.merge(montly_ret
                            ,montly_ret.groupby('tjyf').count()['jjdm'].to_frame('jj_per_month')
                            ,how='left',on='tjyf')

        for col in ['hb1q', 'hb1hy', 'hb1y']:
            #get the winning flag
            montly_ret[col + '_win_mean'] = 0
            montly_ret.loc[montly_ret[col] > montly_ret[col + '_mean']
            , col + '_win_mean'] = 1
            montly_ret[col + '_win_median'] = 0
            montly_ret.loc[montly_ret[col] > montly_ret[col + '_median']
            , col + '_win_median'] = 1

            #get the quarter rank
            montly_ret[col+'_rank']=montly_ret.groupby('tjyf').rank(method='min')['hb1q']
            montly_ret[col + '_rank']=montly_ret[col+'_rank']/montly_ret['jj_per_month']


        sql="select jjdm,ryxm,rydm,rzrq,lrrq,moddt_etl from st_fund.t_st_gm_jjjl where jjdm in ({0}) and rzrq<={1}  and ryzw='基金经理'"\
            .format(util.list_sql_condition(montly_ret['jjdm'].unique().tolist())
                    ,int(date)-10000,date)
        available_manager=hbdb.db2df(sql,db='funduser')
        #date cleaning

        available_manager=available_manager.sort_values('moddt_etl')
        available_manager=available_manager.drop_duplicates(['jjdm','ryxm'],keep='last')

        manager_ret=pd.merge(montly_ret,available_manager,how='left',on='jjdm')
        manager_ret['rz_length'] = manager_ret['rqzh'] - manager_ret['rzrq']
        manager_ret=manager_ret[manager_ret['rz_length']>=10000]
        manager_ret=manager_ret[manager_ret['lrrq']>=manager_ret['rqzh']]

        #get the average rank per manager
        manager_ret2=manager_ret.groupby(['ryxm','tjyf']).mean()[['hb1q_rank', 'hb1hy_rank', 'hb1y_rank']].reset_index()

        tempdf = montly_ret[['jjdm', 'hb1q_rank', 'hb1hy_rank', 'hb1y_rank']].groupby('jjdm').describe()
        tempdf1=montly_ret[['jjdm', 'hb1q_rank', 'hb1hy_rank', 'hb1y_rank']].groupby('jjdm').quantile(0.1)
        tempdf2=montly_ret[['jjdm', 'hb1q_rank', 'hb1hy_rank', 'hb1y_rank']].groupby('jjdm').quantile(0.2)

        tempdf_ma = manager_ret2[['ryxm', 'hb1q_rank', 'hb1hy_rank', 'hb1y_rank']].groupby('ryxm').describe()
        tempdf1_ma=manager_ret2[['ryxm', 'hb1q_rank', 'hb1hy_rank', 'hb1y_rank']].groupby('ryxm').quantile(0.1)
        tempdf2_ma=manager_ret2[['ryxm', 'hb1q_rank', 'hb1hy_rank', 'hb1y_rank']].groupby('ryxm').quantile(0.2)

        for j in range(3):
            col=['hb1q', 'hb1hy', 'hb1y'][j]
            #calculate the winning pro
            out_put = (montly_ret.groupby('jjdm').sum()['{}_win_mean'.format(col)] / montly_ret.groupby('jjdm').count()['{}_win_mean'.format(col)]).to_frame('win_mean')
            out_put['win_median']=montly_ret.groupby('jjdm').sum()['{}_win_median'.format(col)] / montly_ret.groupby('jjdm').count()['{}_win_median'.format(col)]
            out_put['count']=montly_ret.groupby('jjdm').count()['{}_win_median'.format(col)]
            out_put['date']=date
            result[j].append(out_put.reset_index())
            # calculate the winning pro by manager
            out_put = (manager_ret.groupby(['ryxm','jjdm']).sum()['{}_win_mean'.format(col)] / manager_ret.groupby(['ryxm','jjdm']).count()['{}_win_mean'.format(col)]).to_frame('win_mean')
            out_put['win_median']=manager_ret.groupby(['ryxm','jjdm']).sum()['{}_win_median'.format(col)] / manager_ret.groupby(['ryxm','jjdm']).count()['{}_win_median'.format(col)]
            out_put['count']=manager_ret.groupby(['ryxm','jjdm']).count()['hb1y_win_median']
            out_put.reset_index(inplace=True)
            out_put=pd.merge(out_put,manager_ret.groupby(['ryxm']).count()['{}_win_median'.format(col)].to_frame('total_count')
                             ,how='left',on='ryxm')
            for col in ['win_mean','win_median']:
                out_put[col]=out_put[col]*out_put['count']/out_put['total_count']

            out_put['date']=date
            result2[j].append(out_put)

            col = ['hb1q', 'hb1hy', 'hb1y'][j]
            #get the rank quantile
            out_put=tempdf[col+'_rank']
            out_put['10%']=tempdf1[col+'_rank']
            out_put['20%']=tempdf2[col+'_rank']
            result3.append(out_put)

            #get the rank quantile per manager
            out_put=tempdf_ma[col+'_rank']
            out_put['10%']=tempdf1_ma[col+'_rank']
            out_put['20%']=tempdf2_ma[col+'_rank']
            result4.append(out_put)



    name_list = ['quarter', 'half_year', 'year']

    for i in range(3):

        sql="delete from factor_{}_win_pro".format(name_list[i])
        localdb.execute(sql,con=localdb)
        pd.concat(result[i],axis=0).to_sql('factor_{}_win_pro'.format(name_list[i])
                                           ,con=localdb,index=False,if_exists='append')

        sql="delete from factor_manager_{}_win_pro".format(name_list[i])
        localdb.execute(sql,con=localdb)
        pd.concat(result2[i],axis=0).to_sql('factor_manager_{}_win_pro'.format(name_list[i])
                                           ,con=localdb,index=False,if_exists='append')

        sql="delete from factor_{}_distribution".format(name_list[i])
        localdb.execute(sql,con=localdb)
        pd.concat(result[i],axis=0).to_sql('factor_{}_distribution'.format(name_list[i])
                                           ,con=localdb,index=False,if_exists='append')

        sql="delete from factor_manager_{}_distribution".format(name_list[i])
        localdb.execute(sql,con=localdb)
        pd.concat(result2[i],axis=0).to_sql('factor_manager_{}_distribution'.format(name_list[i])
                                           ,con=localdb,index=False,if_exists='append')

def save_fund_size2db(start_date):

    sql= "SELECT distinct(jsrq) as jsrq FROM st_fund.t_st_gm_zcpz WHERE jsrq >= {0} and jsrq<={1} ".format(
        start_date,datetime.datetime.today().strftime('%Y%m%d'))
    calander = hbdb.db2df(sql, db='funduser').sort_values('jsrq')
    calander['month_year']=calander['jsrq'].astype(str).str[0:6]
    calander.drop_duplicates('month_year',keep='last',inplace=True)
    calander['month']=calander['jsrq'].astype(str).str[4:6]
    calander=calander.loc[calander['month'].isin(['03','06','09','12'])]['jsrq'].tolist()
    calander.sort()

    fund_size_df=[]

    for date in calander:
        fund_pool = util.get_mutual_stock_funds(str(date), 2)
        sql="select jjdm,jjzzc,jsrq from st_fund.t_st_gm_zcpz where jsrq='{0}' and jjdm in ({1})"\
            .format(date,util.list_sql_condition(fund_pool))
        fund_size_df.append(hbdb.db2df(sql,db='funduser'))

    fund_size_df=pd.concat(fund_size_df,axis=0).reset_index(drop=True)
    fund_size_df.rename(columns={'jsrq': 'date'}, inplace=True)

    sql = "delete from factor_size where date>='{}'".format(start_date)
    localdb.execute(sql, con=localdb)
    fund_size_df.to_sql('factor_size'
                        , con=localdb, index=False, if_exists='append')

def save_informationratio2db(rolling='2106'):

    sql= "SELECT distinct(tjrq) as tjrq from  st_fund.t_st_gm_zqjxxbl where tjrq>=20151231 "
    calander = hbdb.db2df(sql, db='funduser')
    calander['month_year']=calander['tjrq'].astype(str).str[0:6]
    calander.drop_duplicates('month_year',keep='last',inplace=True)
    calander['month']=calander['tjrq'].astype(str).str[4:6]
    calander=calander.loc[calander['month'].isin(['03','06','09','12'])]['tjrq'].tolist()
    # calander=calander['tjrq'].tolist()
    calander.sort()

    data=[]
    for date in calander:
        print(date)
        fund_pool = util.get_potient_mutual_stock_funds(str(date))
        sql="select jjdm,tjrq,zbnp as info_ratio from st_fund.t_st_gm_zqjxxbl where zblb='{2}' and tjrq={0} and jjdm in ({1}) and zbnp!=99999 "\
            .format(int(date),util.list_sql_condition(fund_pool),rolling)
        data.append(hbdb.db2df(sql,db='funduser'))

    data=pd.concat(data,axis=0).reset_index(drop=True)
    data.rename(columns={'tjrq':'date'},inplace=True)
    data['zblb']=rolling

    sql = "delete from factor_infor_ratio where zblb='{}'".format(rolling)
    localdb.execute(sql, con=localdb)
    data.to_sql('factor_infor_ratio', con=localdb, index=False, if_exists='append')

def save_share_change2db():

    sql = "SELECT distinct(jsrq) as tjrq from  st_fund.t_st_gm_fecyrbd where jsrq>=20151231 "
    calander = hbdb.db2df(sql, db='funduser').sort_values('tjrq')
    calander['month_year'] = calander['tjrq'].astype(str).str[0:6]
    calander.drop_duplicates('month_year', keep='last', inplace=True)
    calander['month'] = calander['tjrq'].astype(str).str[4:6]
    calander = calander.loc[calander['month'].isin(['03', '06', '09', '12'])]['tjrq'].tolist()
    calander.sort()

    data = []
    for date in calander:
        fund_pool = util.get_mutual_stock_funds(date, 2)
        sql = "select jjdm,jsrq,jgcybl,cyrs  from st_fund.t_st_gm_fecyrbd where jsrq='{0}' and jjdm in ({1}) " \
            .format(date, util.list_sql_condition(fund_pool))
        data.append(hbdb.db2df(sql, db='funduser'))

    data = pd.concat(data, axis=0).reset_index(drop=True)

    data['month']=data['jsrq'].astype(str).str[4:6]
    for col in ['jgcybl','cyrs']:
        data[col+'_pct_change']=data.groupby('jjdm')[col].pct_change()
        data[col + '_pct_change_same_month'] = data.groupby(['jjdm','month'])[col].pct_change()
        data.loc[data[col+'_pct_change']==np.inf,col+'_pct_change']=1
        data.loc[data[col + '_pct_change_same_month'] == np.inf, col + '_pct_change_same_month'] = 1

    data.rename(columns={'jsrq': 'date'}, inplace=True)
    data.drop('month',axis=1,inplace=True)
    sql = "delete from factor_share "
    localdb.execute(sql, con=localdb)
    data.to_sql('factor_share', con=localdb, index=False, if_exists='append')

def save_sortino2db(rolling='2201'):

    sql= "SELECT distinct(tjrq) as tjrq from  st_fund.t_st_gm_zqjxxbl where tjrq>=20151231 "
    calander = hbdb.db2df(sql, db='funduser')
    calander['month_year']=calander['tjrq'].astype(str).str[0:6]
    calander.drop_duplicates('month_year',keep='last',inplace=True)
    calander['month']=calander['tjrq'].astype(str).str[4:6]
    calander=calander.loc[calander['month'].isin(['03','06','09','12'])]['tjrq'].tolist()
    # calander=calander['tjrq'].tolist()
    calander.sort()

    data=[]
    for date in calander:
        fund_pool = util.get_mutual_stock_funds(str(date), 2)
        sql="select jjdm,tjrq,zbnp as sortino from st_fund.t_st_gm_zqjstn where zblb='{2}' and tjrq={0} and jjdm in ({1}) and zbnp!=99999 "\
            .format(int(date),util.list_sql_condition(fund_pool),rolling)
        data.append(hbdb.db2df(sql,db='funduser'))

    data=pd.concat(data,axis=0).reset_index(drop=True)
    data.rename(columns={'tjrq':'date'},inplace=True)
    data['zblb']=rolling

    # sql = "delete from factor_sortino where zblb='{}'".format(rolling)
    # localdb.execute(sql, con=localdb)
    data.to_sql('factor_sortino', con=localdb, index=False, if_exists='append')

def save_manager_data2db(rolling='2201'):

    sql= "SELECT distinct(tjrq) as tjrq from  st_fund.t_st_gm_zqjxxbl where tjrq>=20151231 "
    calander = hbdb.db2df(sql, db='funduser')
    calander['month_year']=calander['tjrq'].astype(str).str[0:6]
    calander.drop_duplicates('month_year',keep='last',inplace=True)
    calander['month']=calander['tjrq'].astype(str).str[4:6]
    calander=calander.loc[calander['month'].isin(['03','06','09','12'])]['tjrq'].tolist()
    # calander=calander['tjrq'].tolist()
    calander.sort()

    data=[]
    for date in calander:

        fund_pool = util.get_mutual_stock_funds(str(date), 2)
        sql="select rydm,dbjj from st_fund.t_st_gm_jlzgcptj where jsrq>='{0}' and jsrq<='{1}' and dbjj in ({2})"\
            .format(str(date)[0:6]+'01',str(date)[0:6]+'31',util.list_sql_condition(fund_pool))
        fund_manager_map=hbdb.db2df(sql,db='funduser')

        sql="select rydm,jzrq,zbnp as sharp from st_fund.t_st_gm_jlzqjxpbl where zblb='{2}' and jzrq>='{0}' and jzrq<='{1}' and rydm in ({3}) and zbnp!=99999 and zslx=1"\
            .format(str(date)[0:6]+'15',str(date)[0:6]+'31',rolling,util.list_sql_condition(fund_manager_map['rydm'].tolist()))
        sharp=hbdb.db2df(sql,db='funduser').sort_values('jzrq').drop_duplicates('rydm',keep='last')

        sql="select rydm,jzrq,zbnp as sortino from st_fund.t_st_gm_jlzqjstn where zblb='{2}' and jzrq>='{0}' and jzrq<='{1}' and rydm in ({3}) and zbnp!=99999 and zslx=1"\
            .format(str(date)[0:6]+'15',str(date)[0:6]+'31',rolling,util.list_sql_condition(fund_manager_map['rydm'].tolist()))
        sortino=hbdb.db2df(sql,db='funduser').sort_values('jzrq').drop_duplicates('rydm',keep='last')

        sql="select rydm,jzrq,zbnp as calmar from st_fund.t_st_gm_jlqjkmbl where zblb='{2}' and jzrq>='{0}' and jzrq<='{1}' and rydm in ({3}) and zbnp!=99999 and zslx=1"\
            .format(str(date)[0:6]+'15',str(date)[0:6]+'31',rolling,util.list_sql_condition(fund_manager_map['rydm'].tolist()))
        calmar=hbdb.db2df(sql,db='funduser').sort_values('jzrq').drop_duplicates('rydm',keep='last')

        sql="select rydm,jzrq,zbnp as annual_ret from st_fund.t_st_gm_jlrqjhb where zblb='{2}' and jzrq>='{0}' and jzrq<='{1}' and rydm in ({3}) and zbnp!=99999 and zslx=1"\
            .format(str(date)[0:6]+'15',str(date)[0:6]+'31',rolling,util.list_sql_condition(fund_manager_map['rydm'].tolist()))
        annual_ret=hbdb.db2df(sql,db='funduser').sort_values('jzrq').drop_duplicates('rydm',keep='last')


        manager_df=pd.merge(fund_manager_map,sharp,how='inner',on='rydm')
        manager_df=pd.merge(manager_df,sortino,how='outer',on=['rydm','jzrq']).fillna(0)
        manager_df=pd.merge(manager_df,calmar,how='outer',on=['rydm','jzrq']).fillna(0)
        manager_df=pd.merge(manager_df,annual_ret,how='outer',on=['rydm','jzrq']).fillna(0)

        data.append(manager_df)

    data=pd.concat(data,axis=0).reset_index(drop=True)
    data.rename(columns={'jzrq':'date'},inplace=True)
    data['zblb']=rolling

    # sql = "delete from factor_sortino where zblb='{}'".format(rolling)
    # localdb.execute(sql, con=localdb)
    data.to_sql('factor_manager_data', con=localdb, index=False, if_exists='append')

def manager_alpha(asofdate,reg_date):

    jjdm_list=util.get_bmk_funds_list(asofdate)

    #get manager sample fund
    #
    # max_date=hbdb.db2df("select max(jsrq) as maxdate from  st_fund.t_st_gm_jlzgcptj"
    #                     ,db='funduser')['maxdate'].iloc[0]
    # sql="select rydm,dbjj from st_fund.t_st_gm_jlzgcptj where jsrq='{0}' and dbjj in ({1})"\
    #     .format(max_date,util.list_sql_condition(jjdm_list))
    # jjdm_pool=hbdb.db2df(sql,db='funduser')



    #get factor ret
    industry_zqdm_list=['801010','801030','801040','801050','801080','801110',
                              '801120','801130','801140','801150','801160','801170',
                              '801180','801200','801210','801230','801710','801720',
                              '801730','801740','801750','801760','801770','801780',
                              '801790','801880','801890','801950','801960','801970','801980']
    main_index_zqdm_list=['000001','399001','399006','HSI001','CBA00301']
    # main_index_zqdm_list = ['000001','HSI001', 'CBA00301']
    style_zqdm_list=['399370','399371','399314','399315','399316']
    zqdm_list=main_index_zqdm_list+style_zqdm_list+industry_zqdm_list
    sql="select zqdm,tjrq,hb1z from st_market.t_st_zs_zhb where zqdm in ({0}) and abs(hb1z)!=99999 and rqzh>='{1}' and rqzh<='{2}'"\
        .format(util.list_sql_condition(zqdm_list)
                ,str(int(reg_date[0:4])-2)+reg_date[4:],reg_date)

    factor_ret=hbdb.db2df(sql, db='alluser').pivot_table('hb1z','tjrq','zqdm')
    factor_ret=factor_ret[factor_ret['000001'].notnull()]
    index_list=factor_ret.columns.tolist()

    #正交处理
    import sympy
    L=[]
    for index in index_list:
        L.append(sympy.Matrix(factor_ret[index].tolist()))
    L = sympy.GramSchmidt(L)

    for i in range(1,len(index_list)):
        factor_ret[index_list[i]]=L[i][0:]
        factor_ret[index_list[i]]=factor_ret[index_list[i]].astype(float)

    result=pd.DataFrame(index=jjdm_list)
    result['asofdate']=asofdate
    result['reg_date']=reg_date

    import statsmodels.api as sm
    for jjdm in result.index:
        # print(jjdm)
        #get fund weekly return
        sql="select hb1z,tjrq from st_fund.t_st_gm_zhb where jjdm='{0}' and rqzh>='{1}' and rqzh<='{2}' and hb1z!=99999 "\
            .format(jjdm,str(int(reg_date[0:4])-2)+reg_date[4:],reg_date)
        ret_data=hbdb.db2df(sql,db='funduser')
        if(len(ret_data)<=90):
            continue
        ols_data=pd.merge(ret_data,factor_ret,how='inner',on='tjrq')
        ols_data['alpha']=1
        reg_res = sm.OLS(ols_data['hb1z'].values, ols_data[['alpha']+index_list].values).fit()
        result.loc[jjdm,'alpha']=reg_res.params[0]
        result.loc[jjdm, 'rsquar'] = reg_res.rsquared


    #
    result=result.reset_index().rename(columns={'index':'jjdm'})
    result=result[result['alpha'].notnull()]

    #
    # result=pd.merge(result,jjdm_pool,how='left',left_on='jjdm',right_on='dbjj').drop(['dbjj','jjdm'],axis=1)


    #get manager name
    sql="select ryxm,rydm,jjdm from st_fund.t_st_gm_jjjl where jjdm in ({0}) and lrrq>='{1}'"\
        .format(util.list_sql_condition(result['jjdm'].unique().tolist()),reg_date)
    manager_name=hbdb.db2df(sql,db='funduser')
    manager_name['rydm']=manager_name['rydm'].astype(str)

    result=pd.merge(result,manager_name,how='left',on='jjdm').drop('rydm',axis=1)
    result['new_factor']=0.9*result['alpha']+0.1/result['rsquar']
    #
    localdb.execute("delete from factor_manager_alpha where asofdate='{0}' and reg_date='{1}'"
                    .format(asofdate,reg_date))
    result.to_sql('factor_manager_alpha',con=localdb,index=False,if_exists='append')

def save_theme_ir2db():


    orginal_pool=\
        pd.read_sql("SELECT * from theme_pool where theme in ('HB周期','HBTMT','HB医药','HB大金融', 'HB消费', 'HB制造')  ",
                    con=localdb)


    sql="select * from theme_daily_ret "
    theme_daily_ret=pd.read_sql(sql,con=localdb)


    asofdate_list=orginal_pool.sort_values('asofdate')['asofdate'].unique()
    factor_df=[]
    for i in range(2,len(asofdate_list)) :

        start_date=asofdate_list[i-1]
        end_date=asofdate_list[i]


        for theme in ['大金融', '消费', 'TMT', '周期', '制造', '医药']:

            temp_jj_list=\
                orginal_pool[(orginal_pool['theme']=='HB'+theme)
                             &(orginal_pool['asofdate']==start_date)]['jjdm'].tolist()

            sql = "select jzrq,jjdm,hbdr from st_fund.t_st_gm_rhb where jzrq<'{0}' and jjdm in ({1}) and jzrq>='{2}' " \
                .format(end_date,
                        util.list_sql_condition(temp_jj_list),
                        str(int(start_date[0:4])-1)+start_date[4:])
            jj_daily_ret = hbdb.db2df(sql, db='funduser')
            jj_daily_ret=pd.merge(jj_daily_ret,theme_daily_ret[['jzrq']+[theme]]
                                  ,how='inner',on='jzrq').sort_values(['jjdm','jzrq'])
            jj_daily_ret['ext_ret']=jj_daily_ret['hbdr']-jj_daily_ret[theme]
            jj_daily_ret['ir']=\
                (jj_daily_ret.groupby('jjdm').rolling(120).mean()[['ext_ret']]/jj_daily_ret.groupby('jjdm').rolling(120).std()[['ext_ret']])['ext_ret'].tolist()
            jj_daily_ret['theme_name']=theme
            factor_df.append(jj_daily_ret[jj_daily_ret['ir'].notnull()][['jjdm','jzrq','ir','theme_name']])


    factor_df=pd.concat(factor_df,axis=0)

    factor_df.rename(columns={'jzrq':'date'}).to_sql('factor_theme_ir',index=False,if_exists='append',con=localdb)


    # rolling_window=120
    # jj_daily_ret=pd.merge(jj_daily_ret,theme_daily_ret,how='inner',on='jzrq').sort_values(['jjdm','jzrq'])
    # jj_daily_ret['ext_ret'] = jj_daily_ret['hbdr']/100 - jj_daily_ret[theme_name.replace('HB', '')]
    # jj_daily_ret['ir_theme'] = (jj_daily_ret.groupby('jjdm')[['ext_ret']].rolling(rolling_window).mean() / jj_daily_ret.groupby('jjdm')[
    #     ['ext_ret']].rolling(rolling_window).std())['ext_ret'].tolist()

class For_outsider:

    def __init__(self):

        from sqlalchemy import create_engine
        sql_info={'Sql_ip': '192.168.223.152',
                     'Sql_user': 'admin',
                     'Sql_pass': 'mysql',
                     'Database': 'fe_data_outsider',
                     'port': '3306'}

        #set up the engine
        self.localdb= create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(
            sql_info['Sql_user'], sql_info['Sql_pass'],
            sql_info['Sql_ip'], sql_info['port'], sql_info['Database']))

    @staticmethod
    def get_stock_fund(asofdate):

        sql="select jjdm,jjmc,clrq  from st_fund.t_st_gm_jjxx where cpfl='2' and (ejfl='13' or ejfl='35' or ejfl='37') and jjzt='0' and clrq<='{0}'  ".format(asofdate)
        stock_jjdm=hbdb.db2df(sql,db='funduser').sort_values(['clrq','jjdm'])
        stock_jjdm.drop_duplicates(['jjmc'],keep='first',inplace=True)

        return  stock_jjdm['jjdm'].unique().tolist()

    @staticmethod
    def get_bond_fund(asofdate):

        sql="select jjdm,jjmc,clrq from st_fund.t_st_gm_jjxx where cpfl='2' and (ejfl='22' or ejfl='23' or ejfl='24' or ejfl='27' or ejfl='28') and jjzt='0' and clrq<='{0}'  "\
            .format(asofdate)
        bond_jjdm=hbdb.db2df(sql,db='funduser').sort_values(['clrq','jjdm'])
        bond_jjdm.drop_duplicates(['jjmc'],keep='first',inplace=True)

        return  bond_jjdm['jjdm'].unique().tolist()

    def save_monthly_features_factors2db(self,jjdm_list):

        #read alpha wind data from local excel
        alpha=pd.read_excel(r"E:\GitFolder\docs\机构用数据\wind_data.xlsx",sheet_name='alpha').T
        alpha.columns=alpha.iloc[0]
        alpha=alpha.iloc[2:-1]
        alpha.rename(columns={'基金代码':'date'},inplace=True)
        alpha['date']=alpha['date'].astype(str).str[0:10].str.replace('-','')
        alpha=alpha.set_index('date').T

        #read beta wind data from local excel
        beta=pd.read_excel(r"E:\GitFolder\docs\机构用数据\wind_data.xlsx",sheet_name='beta').T
        beta.columns=beta.iloc[0]
        beta=beta.iloc[2:-1]
        beta.rename(columns={'基金代码':'date'},inplace=True)
        beta['date']=beta['date'].astype(str).str[0:10].str.replace('-','')
        beta=beta.set_index('date').T

        #read alpha wind data from local excel
        timing=pd.read_excel(r"E:\GitFolder\docs\机构用数据\wind_data.xlsx",sheet_name='选时能力').T
        timing.columns=timing.iloc[0]
        timing=timing.iloc[2:-1]
        timing.rename(columns={'基金代码':'date'},inplace=True)
        timing['date']=timing['date'].astype(str).str[0:10].str.replace('-','')
        timing=timing.set_index('date').T


        date_list=timing.columns

        for date in date_list:

            sql="select jjdm,hb1y,rqzh as date from st_fund.t_st_gm_yhb where tjyf ='{0}' and jjdm in ({1}) and hb1y!=99999"\
                .format(date[0:6]
            ,util.list_sql_condition(jjdm_list))

            month_ret=hbdb.db2df(sql,db='funduser')
            monthly_factors=month_ret.copy()
            month_end=str(month_ret['date'].iloc[0])

            sql="select jjdm,zbnp as sharp_ratio,tjrq as date from st_fund.t_st_gm_zqjxpbl where tjrq >='{0}' and tjrq<='{1}' and jjdm in ({2}) and zblb='2101' and zbnp!=99999"\
                .format(month_end[0:6]+'20',month_end[0:6]+'31'
                        ,util.list_sql_condition(jjdm_list))
            sharp_ratio=hbdb.db2df(sql,db='funduser').drop_duplicates('jjdm',keep='last')
            monthly_factors=pd.merge(monthly_factors,sharp_ratio.drop('date',axis=1),how='outer',on='jjdm')

            sql="select jjdm,zbnp as vol,tjrq as date from st_fund.t_st_gm_zqjbdl where tjrq >='{0}' and tjrq<='{1}' and jjdm in ({2}) and zblb='2101' and zbnp!=99999"\
                .format(month_end[0:6]+'20',month_end[0:6]+'31'
                        ,util.list_sql_condition(jjdm_list))
            std=hbdb.db2df(sql,db='funduser').drop_duplicates('jjdm',keep='last')
            monthly_factors=pd.merge(monthly_factors,std.drop('date',axis=1),how='outer',on='jjdm')

            sql="select jjdm,zbnp as max_db,jzrq as date from st_fund.t_st_gm_rqjzdhc where jzrq >='{0}' and jzrq<='{1}' and jjdm in ({2}) and zblb='2101' and zbnp!=99999"\
                .format(month_end[0:6]+'20',month_end[0:6]+'31'
                        ,util.list_sql_condition(jjdm_list))
            max_drawback=hbdb.db2df(sql,db='funduser').drop_duplicates('jjdm',keep='last')
            monthly_factors=pd.merge(monthly_factors,max_drawback.drop('date',axis=1),how='outer',on='jjdm')

            sql="select jjdm,zbnp as sortino,tjrq as date from st_fund.t_st_gm_zqjstn where tjrq >='{0}' and tjrq <='{1}' and  jjdm in ({2}) and zblb='2101' and zbnp!=99999"\
                .format(month_end[0:6]+'20',month_end[0:6]+'31',
                        util.list_sql_condition(jjdm_list))
            sortino=hbdb.db2df(sql,db='funduser').drop_duplicates('jjdm',keep='last')
            monthly_factors=pd.merge(monthly_factors,sortino.drop('date',axis=1),how='outer',on='jjdm')

            sql = "select jjdm,zbnp as Calmar,jzrq as date from st_fund.t_st_gm_rqjkmbl where jzrq >='{0}' and jzrq<='{1}' and jjdm in ({2}) and zblb='2101' and zbnp!=99999" \
                .format(month_end[0:6]+'20',month_end[0:6]+'31'
                        , util.list_sql_condition(jjdm_list))
            calmar = hbdb.db2df(sql, db='funduser').drop_duplicates('jjdm',keep='last')
            monthly_factors=pd.merge(monthly_factors,calmar.drop('date',axis=1),how='outer',on='jjdm')

            sql = "select jjdm,zbnp as annual_ret,jzrq as date from st_fund.t_st_gm_rqjhb where jzrq >='{0}' and jzrq<='{1}' and jjdm in ({2}) and zblb='2201' and zbnp!=99999 " \
                .format(month_end[0:6]+'20',month_end[0:6]+'31', util.list_sql_condition(jjdm_list))
            annual_ret = hbdb.db2df(sql, db='funduser').drop_duplicates('jjdm',keep='last')
            monthly_factors=pd.merge(monthly_factors,annual_ret.drop('date',axis=1),how='outer',on='jjdm')

            alpha_temp=alpha[date].to_frame('alpha')
            alpha_temp['jjdm'] = alpha_temp.index.astype(str).str[0:6]

            beta_temp=beta[date].to_frame('beta')
            beta_temp['jjdm'] = beta_temp.index.astype(str).str[0:6]

            timing_temp=timing[date].to_frame('timing')
            timing_temp['jjdm'] = timing_temp.index.astype(str).str[0:6]

            monthly_factors=pd.merge(monthly_factors,alpha_temp,how='outer',on='jjdm')
            monthly_factors=pd.merge(monthly_factors,beta_temp,how='outer',on='jjdm')
            monthly_factors=pd.merge(monthly_factors,timing_temp,how='outer',on='jjdm')

            monthly_factors['date']=date


            self.localdb.execute("delete from monthly_factors_zy where date='{0}'".format(date))
            (monthly_factors.fillna(0)).to_sql('monthly_factors_zy',con=self.localdb,index=False,if_exists='append')
            print(date+" Done")

    def save_quarterly_features_factors2db(self,jjdm_list):

        date_list=pd.read_sql("select distinct(date) as date from monthly_factors_zy"
                              ,con=self.localdb)['date'].tolist()
        date_list.sort()
        date_list=pd.DataFrame(data=date_list,columns=['date'])
        date_list['month']=date_list['date'].astype(str).str[4:6]
        date_list=date_list[date_list['month'].isin(['03','06','09','12'])]

        for date in date_list['date']:

            sql="select jjzzc,jjdm from st_fund.t_st_gm_zcpz where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}' "\
                .format(util.list_sql_condition(jjdm_list),date[0:6]+'01',date[0:6]+'31')
            size_factro=hbdb.db2df(sql,db='funduser').drop_duplicates('jjdm',keep='last')

            sql="select jjdm,data_value as liquidity from st_fund.r_st_nav_attr_df where style_factor='liquidity' and data_type='exposure' and jjdm in ({0}) and tjrq>='{1}' and tjrq<='{2}'"\
                .format(util.list_sql_condition(jjdm_list),date[0:6]+'01',date[0:6]+'31')
            vol_factor=hbdb.db2df(sql,db='funduser').drop_duplicates('jjdm',keep='last')

            quarterly_factors=pd.merge(size_factro,vol_factor,how='outer',on='jjdm').fillna(0)
            quarterly_factors['date']=date

            # self.localdb.execute("delete from monthly_factors_zy where date='{0}'".format(date))
            quarterly_factors.to_sql('quarterly_factors_zy',con=self.localdb,index=False,if_exists='append')
            print(date+" Done")



if __name__ == '__main__':


    #save_theme_ir2db()
    # for year in ['2015']:
    #     print(year)
        #
        # manager_alpha(year+'1231',str(int(year)+1)+'0630')
        # manager_alpha(year+'1231', str(int(year)+1)+'0330')
        # manager_alpha(year+'0630', year+'1231')
        # manager_alpha(year+'0630',year+'0930')



    # save_manager_data2db('2201')
    # save_manager_data2db('2106')

    # fo=For_outsider()
    #
    # fo.save_monthly_features_factors2db(fo.get_stock_fund('20220801')
    #                                    +fo.get_bond_fund('20220801'))

    # fo.save_quarterly_features_factors2db(fo.get_stock_fund('20220801')
    #                                    +fo.get_bond_fund('20220801'))

    #save_fund_rank_factor2db()

    #save_share_change2db()

    # save_sortino2db(rolling='2201')
    # save_sortino2db(rolling='2202')
    # save_sortino2db(rolling='2106')

    # save_informationratio2db('2106')
    # save_informationratio2db('2103')
    # save_informationratio2db('2101')
    # save_informationratio2db('2201')
    #save_informationratio2db('2203')

    #
    # save_fund_return_factor_histoyr2db('20200101', '20231211')
    save_fund_size2db('20231201')

    #save_fund_return_factor2db()

    #save_fund_return_factor2db()

    # df=read_factors('factor_hsl')
    # df=df.groupby('jjdm').min()
    # df=df[df['hsl'] >= 350]
    #
    # jjdm_list=df.index.tolist()
    # jjdm_con=util.list_sql_condition(jjdm_list)
    #
    # sql="""select jjdm,hb1n,rqzh from st_fund.t_st_gm_nhb
    # where hb1n!=99999 and jjdm in ({0}) and tjnf in ('2015','2016','2017','2018','2019','2020','2021')"""\
    #     .format(jjdm_con)
    # ret=hbdb.db2df(sql,db='funduser')
    # ret=ret.groupby('jjdm')['hb1n'].apply(bhar)
    # ret.to_csv('hlsret.csv',encoding='gbk')


    print('')