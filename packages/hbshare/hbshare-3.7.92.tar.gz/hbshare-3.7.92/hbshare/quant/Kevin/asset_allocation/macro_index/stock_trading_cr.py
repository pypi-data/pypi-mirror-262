"""
股票市场集中度指标
"""
import pandas as pd
import requests
import json
import hbshare as hbs
from hbshare.quant.Kevin.asset_allocation.macro_index.util import create_table, delete_duplicate_records, WriteToDB


class TradingCRNCalculator:
    def __init__(self, start_date, end_date, is_increment=1):
        self.start_date = start_date
        self.end_date = end_date
        self.is_increment = is_increment
        self.table_name = 'mac_stock_trading_cr'
        self._init_api_params()

    def _init_api_params(self):
        self.url = 'http://fdc-query.intelnal.howbuy.com/query/data/commonapi?dataTrack=xxxxx'
        self.headers = {'Content-Type': 'application/json'}
        self.post_body = {"database": "readonly"}

    def fetch_data_batch(self, sql_script):
        post_body = self.post_body.copy()
        post_body['sql'] = sql_script
        post_body["ifByPage"] = False
        res = requests.post(url=self.url, data=json.dumps(post_body), headers=self.headers).json()
        n = res['pages']
        all_data = []
        for i in range(1, n + 1):
            post_body["ifByPage"] = True
            post_body['pageNum'] = i
            res = requests.post(url=self.url, data=json.dumps(post_body), headers=self.headers).json()
            all_data.append(pd.DataFrame(res['data']))
        all_data = pd.concat(all_data)

        return all_data

    def get_stock_trading_cr(self):
        # calendar
        sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM st_main.t_st_gg_jyrl WHERE JYRQ >= {} and JYRQ <= {}".format(
            self.start_date.replace('-', ''), self.end_date.replace('-', ''))
        res = hbs.db_data_query('alluser', sql_script, page_size=5000)
        df = pd.DataFrame(res['data']).rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                     "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)
        trading_day_list = df[df['isOpen'] == 1]['calendarDate'].tolist()
        # calculate
        cr5_list, cr10_list, avg_mkt_list = [], [], []
        from tqdm import tqdm
        for date in tqdm(trading_day_list):
            sql_script = "SELECT SYMBOL, TDATE, VATURNOVER, TCAP FROM finchina.CHDQUOTE WHERE TDATE = {}".format(date)
            df = self.fetch_data_batch(sql_script)
            df = df[df['SYMBOL'].str[0].isin(['0', '3', '6'])]
            df.rename(columns={"SYMBOL": "ticker", "TDATE": "tradeDate", "TCAP": "marketValue",
                               "VATURNOVER": "turnoverValue"}, inplace=True)
            df.reset_index(drop=True, inplace=True)
            # 剔除停牌、没有成交额的数据
            df = df[df['turnoverValue'] > 0.]
            quantile_5, quantile_10 = df['turnoverValue'].quantile(0.95), df['turnoverValue'].quantile(0.90)
            cr5 = df[df['turnoverValue'] >= quantile_5]['turnoverValue'].sum() / df['turnoverValue'].sum()
            cr10 = df[df['turnoverValue'] >= quantile_10]['turnoverValue'].sum() / df['turnoverValue'].sum()
            cr5_list.append(cr5)
            cr10_list.append(cr10)

            avg_mkt = (df['turnoverValue'] * df['marketValue']).sum() / df['turnoverValue'].sum() / 1e+8
            avg_mkt_list.append(avg_mkt)

        results = pd.DataFrame(
            {"trade_date": trading_day_list, "cr5": cr5_list, "cr10": cr10_list, "avg_mkt": avg_mkt_list})
        # 上证综指走势
        sql_script = ("SELECT JYRQ as TRADEDATE, ZQDM, SPJG as TCLOSE FROM st_market.t_st_zs_hq WHERE "
                      "ZQDM = '{}' and JYRQ >= {} and JYRQ <= {}").format(
            '000001', trading_day_list[0], trading_day_list[-1])
        res = hbs.db_data_query('alluser', sql_script, page_size=5000)
        df = pd.DataFrame(res['data'])
        df['TRADEDATE'] = df['TRADEDATE'].map(str)
        df = df.rename(columns={"TRADEDATE": "trade_date", "TCLOSE": "close"})[['trade_date', 'close']]

        df = pd.merge(results, df, on='trade_date')

        return df

    def get_construct_result(self):
        if self.is_increment == 1:
            data = self.get_stock_trading_cr()
            sql_script = "delete from {} where trade_date in ({})".format(
                self.table_name, ','.join(data['trade_date'].tolist()))
            # delete first
            delete_duplicate_records(sql_script)
            # add new records
            WriteToDB().write_to_db(data, self.table_name)
        else:
            sql_script = """
                create table mac_stock_trading_cr(
                id int auto_increment primary key,
                trade_date date not null unique,
                cr5 decimal(5, 4),
                cr10 decimal(5, 4),
                avg_mkt decimal(7, 2),
                close decimal(7, 2)) 
            """
            create_table(self.table_name, sql_script)
            data = self.get_stock_trading_cr()
            WriteToDB().write_to_db(data, self.table_name)


if __name__ == '__main__':
    TradingCRNCalculator('2022-02-01', '2022-02-20', is_increment=1).get_construct_result()
    # TradingCRNCalculator('2019-01-02', '2019-01-12', is_increment=1).get_construct_result()