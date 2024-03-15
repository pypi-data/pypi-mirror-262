import pandas as pd
import hbshare as hbs
import numpy as np
from hbshare.fe.XZ import db_engine
import hbshare
import time

hbdb=db_engine.HBDB()
localdb=db_engine.PrvFunDB().engine
hbs.set_token("qwertyuisdfghjkxcvbn1000")

# 取数据
def get_df(sql, db, page_size=2000):
    data = hbs.db_data_query(db, sql, page_size=page_size, timeout=120)
    pages = data['pages']
    data = pd.DataFrame(data['data'])
    if pages > 1:
        for page in range(2, pages + 1):
            temp_data = hbs.db_data_query(db, sql, page_size=page_size, page_num=page, timeout=120)
            data = pd.concat([data, pd.DataFrame(temp_data['data'])], axis=0)
    return data

def index_cjl(start_date,end_date):
    from datetime import datetime


    # 000300.SH	沪深300
    # 000905.SH	中证500
    # 000852.SH	中证1000
    # 932000.CSI 中证2000
    # 8841431.WI 万得微盘股指数

    # 指数成交量时序
    sql_zs = "select jyrq 交易日期, zqdm 证券代码,  cjjs 成交量,zsz from st_market.t_st_zs_hq \
              where jyrq >={0} and jyrq <={1} and zqdm in (000300,000905,000852,932000)".format(start_date, end_date)

    zs_cjl = get_df(sql_zs, db='alluser')
    zs_cjl_pivot = zs_cjl.pivot_table(values='成交量', index='交易日期', columns='证券代码')
    zs_cjl_pivot.columns=['沪深300','中证1000','中证500','中证2000']
    # 万得微盘股指数成交量时序
    # from WindPy import w
    # w.start()
    # wind_wp_cjl = w.wsd("8841431.WI", "amt", wind_start, wind_end, "unit=1", usedf=True)[1].reset_index(
    #     drop=False).rename(columns={"index": "交易日期", "AMT": "万得微盘股指数"})
    # w.stop()
    # wind_wp_cjl['交易日期'] = pd.to_datetime(wind_wp_cjl['交易日期']).dt.strftime('%Y%m%d')
    # wind_wp_cjl['交易日期'] = wind_wp_cjl['交易日期'].astype(int)

    # zs_cjl_ts = pd.merge(zs_cjl_pivot, wind_wp_cjl, how='left', on='交易日期')
    zs_cjl_ts=zs_cjl_pivot.copy()
    # 上证指数 000001.SH
    # 深证A指 399107.SZ
    # 创业板综 399102.SZ

    # 全市场成交量时序
    sql_market = "select jyrq 交易日期, zqdm 证券代码,  cjjs 成交量 from st_market.t_st_zs_hq \
              where jyrq >={0} and jyrq <={1} and zqdm ='881001'".format(start_date, end_date)

    market_cjl = get_df(sql_market, db='alluser')
    market_cjl_pivot = market_cjl.pivot_table(values='成交量', index='交易日期', columns='证券代码')
    # market_cjl_pivot.columns=['上证指数','深证成指','创业版指']
    # market_cjl_pivot['全市场'] = market_cjl_pivot['上证指数'] + market_cjl_pivot['创业版指'] + market_cjl_pivot[
    #     '深证成指']
    #
    # market_cjl_ts = market_cjl_pivot[['全市场']]
    market_cjl_pivot.columns=['全市场']
    market_cjl_ts = market_cjl_pivot[['全市场']]

    # 合并 指数与全市场成交量时序
    zs_market_cjl_ts = pd.merge(zs_cjl_ts, market_cjl_ts, on='交易日期', how='left')
    zs_market_cjl_ts['中证1000_成交量占比'] = 100 * (zs_market_cjl_ts['中证1000'] / zs_market_cjl_ts['全市场'])
    zs_market_cjl_ts['中证2000_成交量占比'] = 100 * (zs_market_cjl_ts['中证2000'] / zs_market_cjl_ts['全市场'])
    zs_market_cjl_ts['中证500_成交量占比'] = 100 * (zs_market_cjl_ts['中证500'] / zs_market_cjl_ts['全市场'])
    zs_market_cjl_ts['沪深300_成交量占比'] = 100 * (zs_market_cjl_ts['沪深300'] / zs_market_cjl_ts['全市场'])
    # zs_market_cjl_ts['万得微盘股指数_成交量占比'] = 100 * (
    #             zs_market_cjl_ts['万得微盘股指数'] / zs_market_cjl_ts['全市场'])

    # 指数成交量时序
    cjl_index_ts = zs_market_cjl_ts[['沪深300', '中证500', '中证1000',
                                     '中证2000', '全市场']]

    # 指数成交量占比时序
    cjl_index_pct_ts = zs_market_cjl_ts[['沪深300_成交量占比', '中证500_成交量占比', '中证1000_成交量占比',
                                         '中证2000_成交量占比','全市场']]
    cjl_index_pct_ts['其他股票成交量']=100-cjl_index_pct_ts[['沪深300_成交量占比', '中证500_成交量占比', '中证1000_成交量占比',
                                         '中证2000_成交量占比']].sum(axis=1)


    return cjl_index_pct_ts.reset_index(drop=False)

def stock_A_cjl(start_date, end_date):
    # 个股成交量时序
    import hbshare
    import time

    def download_hbs_by_page(
            db_name_symbol: str, sql: str, page_num: int, data_name='') -> pd.DataFrame:
        """
        Core Function：下载基金信息并记录下载时间，确认是否全部提取成功

            :db_name_symbol: 好买数据库映射，查询地址：http://fdc.howbuy.qa/hbshare/_book/FDC/common/
            :sql: SQL提取代码，先访问字典：http://fpc.intelnal.howbuy.com/#/console/dict
            :page_num: 下载总页数 (0<N<inf)，根据行数确定
            :data_name: print记录正在下载的数据类别，一般就是要保存的文件名称
        """

        # Check data pages
        first_data = hbshare.db_data_query(db_name_symbol, sql, page_size=1e4, page_num=1)
        print(f'数据总数：{first_data["total"]}；总页数：{first_data["pages"]}')
        max_page = first_data["pages"]
        if max_page > page_num:
            raise TypeError(
                f'the pages for collection is {max_page} more than input page {page_num}, consider increase page_num')
        else:
            page_num = max_page  # Decrease downloading time

        # Reading Data from Websites (Better download again for accuracy!)
        start_time = time.time()
        data_comb = pd.DataFrame()
        for i in range(page_num):
            i = int(i + 1)  # 从第一页开始读取
            print(f'开始读取{i}页数据！ Save file name: {data_name}')
            data = hbshare.db_data_query(db_name_symbol, sql, page_size=1e4, page_num=i)  # 最多5000行
            data_df = pd.DataFrame(data['data'])
            data_comb = pd.concat([data_comb, data_df], axis=0)
        end_time = time.time()
        during_time = round((end_time - start_time) / 60, 2)
        print(f'共用时：{during_time}分钟！')

        # Drop some duplicated data for some collections
        data_final = data_comb.drop_duplicates()  # 第一遍去重
        # Check if old data and new data have something in common
        ori_cols = data_comb.shape[0]
        new_cols = data_final.shape[0]
        if ori_cols == 0.0:
            print(f'{data_name} 无提取到的数据！')
        else:
            print(
                f'{data_name} 下载完毕！数据非重叠率：{round(new_cols / ori_cols, 4)}(数据行数：{new_cols})！')

        return data_final

    sql = "select TDATE,SYMBOL,PCHG,VATURNOVER,TURNOVER,TCAP from finchina.CHDQUOTE where TDATE>='{0}' and TDATE<='{1}' ".format(
        start_date, end_date)
    stock_data = download_hbs_by_page('readonly', sql, page_num=300, data_name='Data in CHDQUOTE')

    stock_cjl = stock_data[['TDATE', 'SYMBOL', 'VATURNOVER']]
    stock_cjl = stock_cjl.rename(columns={"TDATE": "交易日期", "SYMBOL": "个股代码", "VATURNOVER": "成交量"})
    stock_cjl_final = stock_cjl.pivot_table(values='成交量', index='交易日期', columns='个股代码')

    # 个股成交量总和时序
    stock_total_cjl_ts = stock_cjl_final.copy()
    stock_total_cjl_ts['全A股'] = stock_total_cjl_ts.apply(lambda x: x.sum(), axis='columns')
    all_stock_total_cjl_ts = stock_total_cjl_ts[['全A股']].reset_index()

    # first_5%
    first_5pct = int(stock_cjl_final.shape[1] * 0.05)

    # first_10%
    first_10pct = int(stock_cjl_final.shape[1] * 0.1)

    stock_cjl_ts = stock_cjl_final.T
    stock_cjl_ts = stock_cjl_ts.sort_values(by=stock_cjl_ts.columns.to_list(), ascending=False)

    # 前5%/10%成交量
    cjl_first_5pct = stock_cjl_ts.iloc[:first_5pct, :].T
    cjl_first_5pct['前5%成交量'] = cjl_first_5pct.apply(lambda x: x.sum(), axis='columns')
    cjl_first_5pct = cjl_first_5pct[['前5%成交量']].reset_index()

    cjl_first_10pct = stock_cjl_ts.iloc[:first_10pct, :].T
    cjl_first_10pct['前10%成交量'] = cjl_first_10pct.apply(lambda x: x.sum(), axis='columns')
    cjl_first_10pct = cjl_first_10pct[['前10%成交量']].reset_index()

    cjl_first_5pct_10pct = pd.merge(cjl_first_5pct, cjl_first_10pct, on='交易日期', how='left')
    cjl_first_5pct_10pct = pd.merge(cjl_first_5pct_10pct, all_stock_total_cjl_ts, on='交易日期', how='left')

    cjl_first_5pct_10pct['前5%成交量占比'] = 100 * (
            cjl_first_5pct_10pct['前5%成交量'] / cjl_first_5pct_10pct['全A股'])
    cjl_first_5pct_10pct['前10%成交量占比'] = 100 * (
            cjl_first_5pct_10pct['前10%成交量'] / cjl_first_5pct_10pct['全A股'])

    # 前5%/10%成交量时序
    cjl_first_5pct_10pct_ts = cjl_first_5pct_10pct[['交易日期', '前5%成交量', '前10%成交量', '全A股']]

    # 个股成交量集中度时序
    cjl_pct_first_5pct_10pct_ts = cjl_first_5pct_10pct[['交易日期', '前5%成交量占比', '前10%成交量占比']]


    localdb.execute("delete from stock_narrow where `交易日期`>='{}' ".format(cjl_pct_first_5pct_10pct_ts['交易日期'].min()))
    cjl_pct_first_5pct_10pct_ts.to_sql('stock_narrow',if_exists='append',index=False,con=localdb)

def etf_cjl(start_date,end_date):
    etf_path = r"E:\GitFolder\docs\基金池跟踪\量化基金池\ETF.xlsx"

    etf = pd.read_excel(etf_path)
    etf['基金代码'] = etf['证券代码'].str[0:6]

    # sql_etf = "select jjdm 基金代码, zqmc 基金名称 from st_fund.t_st_gm_jjjy where jyrq ={0} ".format(end_date)
    # eft=get_df(sql_etf, db='funduser')


    for col in list(etf['证券简称'].unique()):
        if "300" in col:
            etf.loc[etf[etf['证券简称'] == col].index, 'type'] = "300"

        if "500" in col:
            etf.loc[etf[etf['证券简称'] == col].index, 'type'] = "500"

        if "1000" in col:
            etf.loc[etf[etf['证券简称'] == col].index, 'type'] = "1000"

        if "2000" in col:
            etf.loc[etf[etf['证券简称'] == col].index, 'type'] = "2000"

    etf_dm = tuple(etf['证券代码'].str[0:6].unique())

    sql_etf = "select jyrq 交易日期, jjdm 基金代码, zqmc 基金名称, cjjs 成交量 from st_fund.t_st_gm_jjjy \
               where jyrq >={0} and jyrq <={1} and jjdm in {2}".format(start_date, end_date, etf_dm)

    etf_cjl = get_df(sql_etf, db='funduser')
    etf_cjl = pd.merge(etf_cjl, etf[['基金代码', 'type']], on='基金代码', how='left')

    etf_cjl_300 = etf_cjl[etf_cjl['type'] == '300']
    etf_cjl_300 = etf_cjl_300.pivot_table(values='成交量', index='交易日期', columns='基金名称')
    etf_cjl_300['300成交量'] = etf_cjl_300.apply(lambda x: x.sum(), axis='columns')

    etf_cjl_500 = etf_cjl[etf_cjl['type'] == '500']
    etf_cjl_500 = etf_cjl_500.pivot_table(values='成交量', index='交易日期', columns='基金名称')
    etf_cjl_500['500成交量'] = etf_cjl_500.apply(lambda x: x.sum(), axis='columns')

    etf_cjl_1000 = etf_cjl[etf_cjl['type'] == '1000']
    etf_cjl_1000 = etf_cjl_1000.pivot_table(values='成交量', index='交易日期', columns='基金名称')
    etf_cjl_1000['1000成交量'] = etf_cjl_1000.apply(lambda x: x.sum(), axis='columns')

    etf_cjl_2000 = etf_cjl[etf_cjl['type'] == '2000']
    etf_cjl_2000 = etf_cjl_2000.pivot_table(values='成交量', index='交易日期', columns='基金名称')
    etf_cjl_2000['2000成交量'] = etf_cjl_2000.apply(lambda x: x.sum(), axis='columns')

    etf_cjl_300 = etf_cjl_300.reset_index()
    etf_cjl_300 = etf_cjl_300[['交易日期', '300成交量']]

    etf_cjl_500 = etf_cjl_500.reset_index()
    etf_cjl_500 = etf_cjl_500[['交易日期', '500成交量']]

    etf_cjl_1000 = etf_cjl_1000.reset_index()
    etf_cjl_1000 = etf_cjl_1000[['交易日期', '1000成交量']]

    etf_cjl_2000 = etf_cjl_2000.reset_index()
    etf_cjl_2000 = etf_cjl_2000[['交易日期', '2000成交量']]

    etf_cjls = pd.merge(etf_cjl_300, etf_cjl_500, on='交易日期', how='left')
    etf_cjls = pd.merge(etf_cjls, etf_cjl_1000, on='交易日期', how='left')
    etf_cjls = pd.merge(etf_cjls, etf_cjl_2000, on='交易日期', how='left')

    return  etf_cjls
def index_return(end_date):
    # def wind_date(date):
    #     from datetime import datetime
    #     wind_date = datetime.strptime(str(date), '%Y%m%d').strftime('%Y-%m-%d')
    #     return wind_date
    #
    #     # 指数日涨跌幅

    sql_index_d_ret = "select zqdm 指数代码, hbdr 日涨跌幅 from st_market.t_st_zs_rhb\
                          where zqdm in (000300,000905,000852,932000,8841431) and jyrq = {}".format(end_date)
    index_d_ret = get_df(sql_index_d_ret, db='alluser')

    index_d_ret.loc[index_d_ret[index_d_ret['指数代码'] == '000300'].index, '指数名称'] = '沪深300'
    index_d_ret.loc[index_d_ret[index_d_ret['指数代码'] == '000905'].index, '指数名称'] = '中证500'
    index_d_ret.loc[index_d_ret[index_d_ret['指数代码'] == '000852'].index, '指数名称'] = '中证1000'
    index_d_ret.loc[index_d_ret[index_d_ret['指数代码'] == '932000'].index, '指数名称'] = '中证2000'
    index_d_ret.loc[index_d_ret[index_d_ret['指数代码'] == '8841431'].index, '指数名称'] = '万得微盘股指数'

    # 指数区间涨跌幅
    sql_index_rret = "select zqdm 指数代码, zbnp 区间回报, zblb from st_market.t_st_zs_rqjhb \
                      where zblb in ('2101','2103','2106','2201') \
                      and zqdm in (000300,000905,000852,932000,8841431) \
                      and jyrq = {}  and zbnp!=99999".format(end_date)

    index_rret = get_df(sql_index_rret, db='alluser')
    index_rret = index_rret.pivot_table(values='区间回报', index='指数代码', columns='zblb')
    index_rret.columns = ['近1月', '近3月', '近6月', '近1年']
    index_rret = index_rret.reset_index()

    index_rret.loc[index_rret[index_rret['指数代码'] == '000300'].index, '指数名称'] = '沪深300'
    index_rret.loc[index_rret[index_rret['指数代码'] == '000905'].index, '指数名称'] = '中证500'
    index_rret.loc[index_rret[index_rret['指数代码'] == '000852'].index, '指数名称'] = '中证1000'
    index_rret.loc[index_rret[index_rret['指数代码'] == '932000'].index, '指数名称'] = '中证2000'
    index_rret.loc[index_rret[index_rret['指数代码'] == '8841431'].index, '指数名称'] = '万得微盘股指数'

    index_d_ret = index_d_ret[['指数代码', '指数名称', '日涨跌幅']]
    index_rret = index_rret[['指数代码', '指数名称', '近1月', '近3月', '近6月', '近1年']]

    all_index_ret = pd.merge(index_d_ret, index_rret, on=['指数代码', '指数名称'], how='left')
    all_index_ret['统计日期'] = end_date
    all_index_ret = all_index_ret[['指数代码', '指数名称', '统计日期', '日涨跌幅', '近1月', '近3月', '近6月', '近1年']]



    # 指数日涨跌幅时序
    sql_index_ts_ret = "select jyrq 交易日期 ,zqdm 指数代码, hbdr 日涨跌幅 from st_market.t_st_zs_rhb\
                       where zqdm in (000300,000905,000852,932000,8841431)\
                       and jyrq >= {0} and jyrq <= {1}".format(end_date - 10000, end_date)
    index_ts_ret = get_df(sql_index_ts_ret, db='alluser')

    index_ts_ret.loc[index_ts_ret[index_ts_ret['指数代码'] == '000300'].index, '指数名称'] = '沪深300'
    index_ts_ret.loc[index_ts_ret[index_ts_ret['指数代码'] == '000905'].index, '指数名称'] = '中证500'
    index_ts_ret.loc[index_ts_ret[index_ts_ret['指数代码'] == '000852'].index, '指数名称'] = '中证1000'
    index_ts_ret.loc[index_ts_ret[index_ts_ret['指数代码'] == '932000'].index, '指数名称'] = '中证2000'
    index_ts_ret.loc[index_ts_ret[index_ts_ret['指数代码'] == '8841431'].index, '指数名称'] = '万得微盘股指数'

    index_ts_ret_pivot = index_ts_ret.pivot_table(values='日涨跌幅', index='交易日期', columns='指数名称')
    index_ts_ret_final = index_ts_ret_pivot
    index_ts_ret_final=(index_ts_ret_final/100+1).cumprod()

    return all_index_ret, index_ts_ret_final
def relative_index(start_date, end_date):


    # 个股日涨跌幅
    import hbshare
    import time

    def download_hbs_by_page(
            db_name_symbol: str, sql: str, page_num: int, data_name='') -> pd.DataFrame:
        """
        Core Function：下载基金信息并记录下载时间，确认是否全部提取成功

            :db_name_symbol: 好买数据库映射，查询地址：http://fdc.howbuy.qa/hbshare/_book/FDC/common/
            :sql: SQL提取代码，先访问字典：http://fpc.intelnal.howbuy.com/#/console/dict
            :page_num: 下载总页数 (0<N<inf)，根据行数确定
            :data_name: print记录正在下载的数据类别，一般就是要保存的文件名称
        """

        # Check data pages
        first_data = hbshare.db_data_query(db_name_symbol, sql, page_size=1e4, page_num=1)
        print(f'数据总数：{first_data["total"]}；总页数：{first_data["pages"]}')
        max_page = first_data["pages"]
        if max_page > page_num:
            raise TypeError(
                f'the pages for collection is {max_page} more than input page {page_num}, consider increase page_num')
        else:
            page_num = max_page  # Decrease downloading time

        # Reading Data from Websites (Better download again for accuracy!)
        start_time = time.time()
        data_comb = pd.DataFrame()
        for i in range(page_num):
            i = int(i + 1)  # 从第一页开始读取
            print(f'开始读取{i}页数据！ Save file name: {data_name}')
            data = hbshare.db_data_query(db_name_symbol, sql, page_size=1e4, page_num=i)  # 最多5000行
            data_df = pd.DataFrame(data['data'])
            data_comb = pd.concat([data_comb, data_df], axis=0)
        end_time = time.time()
        during_time = round((end_time - start_time) / 60, 2)
        print(f'共用时：{during_time}分钟！')

        # Drop some duplicated data for some collections
        data_final = data_comb.drop_duplicates()  # 第一遍去重
        # Check if old data and new data have something in common
        ori_cols = data_comb.shape[0]
        new_cols = data_final.shape[0]
        if ori_cols == 0.0:
            print(f'{data_name} 无提取到的数据！')
        else:
            print(
                f'{data_name} 下载完毕！数据非重叠率：{round(new_cols / ori_cols, 4)}(数据行数：{new_cols})！')

        return data_final

    sql = "select TDATE,SYMBOL,PCHG,VATURNOVER,TURNOVER,TCAP from finchina.CHDQUOTE where TDATE>='{0}' and TDATE<='{1}' ".format(
        start_date, end_date)
    stock_data = download_hbs_by_page('readonly', sql, page_num=1000, data_name='Data in CHDQUOTE')

    stock_ret = stock_data[['TDATE', 'SYMBOL', 'PCHG']]
    stock_ret = stock_ret.rename(columns={"TDATE": "交易日期", "SYMBOL": "个股代码", "PCHG": "日涨跌幅"})
    stock_ret_ts = stock_ret.pivot_table(values='日涨跌幅', index='交易日期', columns='个股代码')
    stock_ret_ts=(stock_ret_ts / 100 + 1).cumprod() - 1
    stock_ret_ts['A股中位数涨跌幅'] = stock_ret_ts.apply(lambda x: x.median(), axis='columns')

    # A股每日中位数涨跌幅
    stock_median_ret_ts = stock_ret_ts[['A股中位数涨跌幅']].reset_index()

    # 指数日涨跌幅
    sql_index_d_ret = "select jyrq 交易日期 ,zqdm 指数代码, hbdr 日涨跌幅 from st_market.t_st_zs_rhb\
                          where zqdm in (000852,000905) and jyrq>={0} and jyrq<={1}".format(start_date, end_date)
    index_d_ret = get_df(sql_index_d_ret, db='alluser')
    index_d_ret.loc[index_d_ret[index_d_ret['指数代码'] == '000905'].index, '指数名称'] = '中证500'
    index_d_ret.loc[index_d_ret[index_d_ret['指数代码'] == '000852'].index, '指数名称'] = '中证1000'
    index_ts_ret = index_d_ret.pivot_table(values='日涨跌幅', index='交易日期', columns='指数名称')
    index_ts_ret=(index_ts_ret / 100 + 1).cumprod() - 1

    # 合并
    relative_ret = pd.merge(stock_median_ret_ts, index_ts_ret, on='交易日期', how='left')
    relative_ret = relative_ret.dropna(subset=['中证500', '中证1000'])

    relative_ret['中证500累计超额'] = relative_ret['A股中位数涨跌幅']-relative_ret['中证500']
    relative_ret['中证1000累计超额'] = relative_ret['A股中位数涨跌幅']-relative_ret['中证1000']

    # relative_1000ret_ts = relative_ret[['交易日期', '中证500累计超额']].set_index('交易日期')
    # relative_2000ret_ts = relative_ret[['交易日期', '中证1000累计超额']].set_index('交易日期')
    #
    # relative_1000ret_ts_nav = (relative_1000ret_ts / 100 + 1).cumprod()
    # relative_2000ret_ts_nav = (relative_2000ret_ts / 100 + 1).cumprod()
    #
    # output=pd.merge(relative_1000ret_ts_nav,relative_2000ret_ts_nav,how='inner',left_index=True,right_index=True)
    # localdb.execute("delete from stock_relative_ret")
    relative_ret[['交易日期','中证500累计超额','中证1000累计超额']].to_sql('stock_relative_ret',con=localdb,if_exists='replace',index=False)

def save_3800_index2db(start_date,end_date):

    import hbshare
    import time

    sql = "select cfgdm from st_market.t_st_zs_zscfgqz where zqdm in ('000300','000905','000852','932000') and m_opt_type!='03' "
    index_info = hbdb.db2df(sql, db='alluser')

    stock_A_path = r"E:\GitFolder\docs\基金池跟踪\量化基金池\A股.xlsx"

    all_zqdm = pd.read_excel(stock_A_path)
    all_zqdm = all_zqdm['证券代码'].str[0:6].tolist()
    # all_zqdm=index_info.copy()['cfgdm'].tolist()
    # all_zqdm.append('301231')
    # all_zqdm.append('300472')

    zqdm_3800=list(set(all_zqdm).difference(set(index_info['cfgdm'])))

    def download_hbs_by_page(
            db_name_symbol: str, sql: str, page_num: int, data_name='') -> pd.DataFrame:
        """
        Core Function：下载基金信息并记录下载时间，确认是否全部提取成功

            :db_name_symbol: 好买数据库映射，查询地址：http://fdc.howbuy.qa/hbshare/_book/FDC/common/
            :sql: SQL提取代码，先访问字典：http://fpc.intelnal.howbuy.com/#/console/dict
            :page_num: 下载总页数 (0<N<inf)，根据行数确定
            :data_name: print记录正在下载的数据类别，一般就是要保存的文件名称
        """

        # Check data pages
        first_data = hbshare.db_data_query(db_name_symbol, sql, page_size=1e4, page_num=1)
        print(f'数据总数：{first_data["total"]}；总页数：{first_data["pages"]}')
        max_page = first_data["pages"]
        if max_page > page_num:
            raise TypeError(
                f'the pages for collection is {max_page} more than input page {page_num}, consider increase page_num')
        else:
            page_num = max_page  # Decrease downloading time

        # Reading Data from Websites (Better download again for accuracy!)
        start_time = time.time()
        data_comb = pd.DataFrame()
        for i in range(page_num):
            i = int(i + 1)  # 从第一页开始读取
            print(f'开始读取{i}页数据！ Save file name: {data_name}')
            data = hbshare.db_data_query(db_name_symbol, sql, page_size=1e4, page_num=i)  # 最多5000行
            data_df = pd.DataFrame(data['data'])
            data_comb = pd.concat([data_comb, data_df], axis=0)
        end_time = time.time()
        during_time = round((end_time - start_time) / 60, 2)
        print(f'共用时：{during_time}分钟！')

        # Drop some duplicated data for some collections
        data_final = data_comb.drop_duplicates()  # 第一遍去重
        # Check if old data and new data have something in common
        ori_cols = data_comb.shape[0]
        new_cols = data_final.shape[0]
        if ori_cols == 0.0:
            print(f'{data_name} 无提取到的数据！')
        else:
            print(
                f'{data_name} 下载完毕！数据非重叠率：{round(new_cols / ori_cols, 4)}(数据行数：{new_cols})！')

        return data_final


    sql = "select TDATE as jyrq,SYMBOL as zqdm,PCHG,VATURNOVER ,TURNOVER ,MCAP,TCLOSE from finchina.CHDQUOTE where TDATE>='{0}' and TDATE<='{1}' and PCHG<=20 and PCHG>=-20 and 'S' not in SNAME ".format(start_date,end_date)
    index_data=download_hbs_by_page('readonly', sql, page_num=400, data_name='Data in CHDQUOTE')

    index_data=index_data[index_data['ZQDM'].isin(zqdm_3800)]
    index_data=pd.merge(index_data,
                        index_data.groupby('JYRQ')['MCAP'].sum().to_frame('total_mv'),how='left',on='JYRQ')
    index_data['w']=index_data['MCAP']/index_data['total_mv']



    index_data['60_days_max']=index_data.groupby('ZQDM')['TCLOSE'].rolling(60).max().reset_index().sort_values('level_1')['TCLOSE']
    index_data['ma_20']=index_data.groupby('ZQDM')['TCLOSE'].rolling(20).mean().reset_index().sort_values('level_1')['TCLOSE']

    index_data['new_highest']=0
    index_data.loc[index_data['60_days_max']==index_data['TCLOSE'],'new_highest']=1
    index_data['new_highest_w']=index_data['new_highest']*index_data['w']

    index_data['above_ma20']=0
    index_data.loc[index_data['TCLOSE']>index_data['ma_20'],'above_ma20']=1
    index_data['above_ma20_w']=index_data['above_ma20']*index_data['w']

    for col in ['PCHG','TURNOVER','VATURNOVER','total_mv']:
        index_data[col]=index_data[col]*index_data['w']

    index_data=index_data.groupby('JYRQ')[['PCHG', 'TURNOVER','VATURNOVER','new_highest_w','above_ma20_w','total_mv']].sum().reset_index()
    index_data=index_data.iloc[60:]
    localdb.execute("delete from mimic_index_3800 where JYRQ>='{0}' and JYRQ<='{1}'".format(index_data['JYRQ'].min(),index_data['JYRQ'].max()))
    index_data.to_sql('mimic_index_3800',if_exists='append',index=False,con=localdb)

def save_index_narrow_factor(start_date,end_date):


    def download_hbs_by_page(
            db_name_symbol: str, sql: str, page_num: int, data_name='') -> pd.DataFrame:
        """
        Core Function：下载基金信息并记录下载时间，确认是否全部提取成功

            :db_name_symbol: 好买数据库映射，查询地址：http://fdc.howbuy.qa/hbshare/_book/FDC/common/
            :sql: SQL提取代码，先访问字典：http://fpc.intelnal.howbuy.com/#/console/dict
            :page_num: 下载总页数 (0<N<inf)，根据行数确定
            :data_name: print记录正在下载的数据类别，一般就是要保存的文件名称
        """

        # Check data pages
        first_data = hbshare.db_data_query(db_name_symbol, sql, page_size=1e4, page_num=1)
        print(f'数据总数：{first_data["total"]}；总页数：{first_data["pages"]}')
        max_page = first_data["pages"]
        if max_page > page_num:
            raise TypeError(
                f'the pages for collection is {max_page} more than input page {page_num}, consider increase page_num')
        else:
            page_num = max_page  # Decrease downloading time

        # Reading Data from Websites (Better download again for accuracy!)
        start_time = time.time()
        data_comb = pd.DataFrame()
        for i in range(page_num):
            i = int(i + 1)  # 从第一页开始读取
            print(f'开始读取{i}页数据！ Save file name: {data_name}')
            data = hbshare.db_data_query(db_name_symbol, sql, page_size=1e4, page_num=i)  # 最多5000行
            data_df = pd.DataFrame(data['data'])
            data_comb = pd.concat([data_comb, data_df], axis=0)
        end_time = time.time()
        during_time = round((end_time - start_time) / 60, 2)
        print(f'共用时：{during_time}分钟！')

        # Drop some duplicated data for some collections
        data_final = data_comb.drop_duplicates()  # 第一遍去重
        # Check if old data and new data have something in common
        ori_cols = data_comb.shape[0]
        new_cols = data_final.shape[0]
        if ori_cols == 0.0:
            print(f'{data_name} 无提取到的数据！')
        else:
            print(
                f'{data_name} 下载完毕！数据非重叠率：{round(new_cols / ori_cols, 4)}(数据行数：{new_cols})！')

        return data_final


    sql = "select TDATE ,SYMBOL ,TCLOSE from finchina.CHDQUOTE where TDATE>='{0}' and TDATE<='{1}' ".format(start_date,end_date)
    extra_info=download_hbs_by_page('readonly', sql, page_num=400, data_name='Data in CHDQUOTE').drop('ROW_ID',axis=1)
    extra_info.columns=['zqdm','jyrq','spjg']

    # sql = ("select zqdm,jyrq,spjg,hsbl from  st_ashare.t_st_ag_gpjy where zqdm in {0} and jyrq>='{1}' and jyrq<='{2}'"
    #        .format(tuple(index_info['cfgdm'].iloc[0:10]), start_date, end_date))
    # extra_info = hbdb.db2df(sql, db='alluser')

    def sub_func(index_code,extra_info):

        sql = ("select cfgdm,qz from st_market.t_st_zs_zscfgqz where zqdm='{0}' and m_opt_type!='03'"
               .format(index_code))
        index_info = hbdb.db2df(sql, db='alluser')

        extra_info=extra_info[extra_info['zqdm'].isin(index_info['cfgdm'])]

        extra_info = pd.merge(extra_info, index_info, how='left',
                              left_on='zqdm', right_on='cfgdm').drop('cfgdm', axis=1)

        extra_info['60_days_max'] = extra_info.groupby('zqdm')['spjg'].rolling(60).max().reset_index().sort_values('level_1')['spjg']
        extra_info['ma_20'] = extra_info.groupby('zqdm')['spjg'].rolling(20).mean().reset_index().sort_values('level_1')['spjg']

        extra_info['new_highest'] = 0
        extra_info.loc[extra_info['60_days_max'] == extra_info['spjg'], 'new_highest'] = 1
        extra_info['new_highest_w_'+index_code] = extra_info['new_highest'] * extra_info['qz']

        extra_info['above_ma20'] = 0
        extra_info.loc[extra_info['spjg'] > extra_info['ma_20'], 'above_ma20'] = 1
        extra_info['above_ma20_w_'+index_code] = extra_info['above_ma20'] * extra_info['qz']

        index_factors_a = extra_info.groupby('jyrq')[['new_highest_w_'+index_code, 'above_ma20_w_'+index_code]].sum()

        return index_factors_a
    output_list=[]

    for index_code in ['000016','000300','000905','000852','932000','399370','399371']:
        output_list.append(sub_func(index_code,extra_info))

    output_list=pd.concat(output_list,axis=1)
    output_list=output_list.iloc[60:]
    localdb.execute("delete from index_narrow_factors where jyrq>='{0}' and jyrq<='{1}'".format(output_list.index.min(),output_list.index.max()))
    output_list.to_sql('index_narrow_factors',if_exists='append',index=True,con=localdb)

def save_index_narrow2localfile(start_date,end_date,index_code):

    #start_date='20180101'
    # end_date='20240301'
    # index_code='399371'
    sql = ("select cfgdm,qz from st_market.t_st_zs_zscfgqz where zqdm='{0}' and m_opt_type!='03'"
    .format(index_code))

    index_info = hbdb.db2df(sql, db='alluser')

    sql = ("select jyrq,zsz from st_market.t_st_zs_hq where  zqdm = {0} and jyrq>='{1}' and jyrq<='{2}' "
           .format(index_code, start_date, end_date))
    index_ret = hbdb.db2df(sql, db='alluser')

    sql = (
        "select jyrq,new_highest_w_{2} as new_highest_w ,above_ma20_w_{2} as above_ma20_w  from index_narrow_factors where  jyrq>='{0}' and jyrq<='{1}' "
        .format(start_date, end_date, index_code))
    index_factors_a = pd.read_sql(sql, con=localdb).set_index('jyrq')

    index_factors_a = pd.merge(index_factors_a, index_ret, how='left', on='jyrq')

    sql_zs = "select jyrq 交易日期, zqdm 证券代码,  cjjs 成交量,zsz from st_market.t_st_zs_hq \
                                              where jyrq >={0} and jyrq <={1} and zqdm in ({2},881001)".format(
        start_date, end_date,index_code)

    zs_cjl = get_df(sql_zs, db='alluser')
    index_cjl = zs_cjl.pivot_table(values='成交量', index='交易日期', columns='证券代码')
    index_cjl['clj_w'] = index_cjl[index_code] / index_cjl['881001']

    narrow_factors = (
        pd.merge(index_factors_a, index_cjl[['clj_w', '881001', index_code]], how='left', left_on='jyrq',
                 right_on='交易日期'))

    narrow_factors['hsl'] = narrow_factors[index_code] / narrow_factors['zsz']
    narrow_factors = narrow_factors[['jyrq', 'new_highest_w', 'above_ma20_w', 'clj_w', 'hsl']].set_index('jyrq')

    import sklearn.preprocessing as pp

    for col in narrow_factors.columns:
        narrow_factors.loc[(narrow_factors[col] >= narrow_factors.quantile(0.975)[col]) | (
                    narrow_factors[col] <= narrow_factors.quantile(0.025)[col]), col] = np.nan
    narrow_factors[narrow_factors.columns] = pp.StandardScaler().fit_transform(narrow_factors)

    (narrow_factors.mean(axis=1).to_frame(index_code).rolling(60).mean().iloc[60:]).to_excel("{}_narrow.xlsx".format(index_code))



if __name__ == '__main__':

    #save_index_narrow2localfile('20180101', '20240301', '399370')
    # stock_A_cjl('20230226', '20240301')

    # save_index_narrow_factor('20231101', '20240301')
    # relative_index('20210101', '20240301')



    # save_3800_index2db('20190101', '20191231')
    # save_3800_index2db('20191001', '20200229')
    # save_3800_index2db('20201001', '20210229')
    # save_3800_index2db('20211001', '20220229')
    # save_3800_index2db('20221101', '20231231')
    # save_3800_index2db('20231001', '20240301')

    # save_index_narrow_factor('20190101', '20191231')
    # save_index_narrow_factor('20191001', '20201231')
    # save_index_narrow_factor('20201001', '20211231')
    # save_index_narrow_factor('20211001', '20221231')
    # save_index_narrow_factor('20221001', '20231231')
    # save_index_narrow_factor('20231001', '20240301')



    print('')