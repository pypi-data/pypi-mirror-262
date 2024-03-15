# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def get_date(start_date, end_date):
    calendar_df = HBDB().read_cal(start_date, end_date)
    calendar_df = calendar_df.rename(columns={'jyrq': 'CALENDAR_DATE', 'sfjj': 'IS_OPEN', 'sfzm': 'IS_WEEK_END', 'sfym': 'IS_MONTH_END'})
    calendar_df['CALENDAR_DATE'] = calendar_df['CALENDAR_DATE'].astype(str)
    calendar_df = calendar_df.sort_values('CALENDAR_DATE')
    calendar_df['IS_OPEN'] = calendar_df['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
    calendar_df['YEAR_MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[:6])
    calendar_df['MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:6])
    calendar_df['MONTH_DAY'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:])
    calendar_df = calendar_df[(calendar_df['CALENDAR_DATE'] >= start_date) & (calendar_df['CALENDAR_DATE'] <= end_date)]
    trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    trade_df = trade_df[(trade_df['TRADE_DATE'] >= start_date) & (trade_df['TRADE_DATE'] <= end_date)]
    report_df = calendar_df.drop_duplicates('YEAR_MONTH', keep='last').rename(columns={'CALENDAR_DATE': 'REPORT_DATE'})
    report_df = report_df[report_df['MONTH_DAY'].isin(['0331', '0630', '0930', '1231'])]
    report_df = report_df[(report_df['REPORT_DATE'] >= start_date) & (report_df['REPORT_DATE'] <= end_date)]
    report_trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    report_trade_df = report_trade_df.sort_values('TRADE_DATE').drop_duplicates('YEAR_MONTH', keep='last')
    report_trade_df = report_trade_df[report_trade_df['MONTH'].isin(['03', '06', '09', '12'])]
    report_trade_df = report_trade_df[(report_trade_df['TRADE_DATE'] >= start_date) & (report_trade_df['TRADE_DATE'] <= end_date)]
    calendar_trade_df = calendar_df[['CALENDAR_DATE']].merge(trade_df[['TRADE_DATE']], left_on=['CALENDAR_DATE'], right_on=['TRADE_DATE'], how='left')
    calendar_trade_df['TRADE_DATE'] = calendar_trade_df['TRADE_DATE'].fillna(method='ffill')
    calendar_trade_df = calendar_trade_df[(calendar_trade_df['TRADE_DATE'] >= start_date) & (calendar_trade_df['TRADE_DATE'] <= end_date)]
    return calendar_df, report_df, trade_df, report_trade_df, calendar_trade_df


def cal_drawdown(ser):
    df = pd.DataFrame(ser)
    df.columns = ['NAV']
    df = df.sort_index()
    df['IDX'] = range(len(df))
    df['HIGHEST'] = df['NAV'].cummax()
    df['DRAWDOWN'] = (df['NAV'] - df['HIGHEST']) / df['HIGHEST']
    return min(df['DRAWDOWN'])


class Analysis:
    def __init__(self, start_date, end_date, data_path):
        self.start_date = start_date
        self.end_date = end_date
        self.data_path = data_path
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.start_date, self.end_date)

    def index_compare(self):
        market_index_data = HBDB().read_index_daily_k_given_date_and_indexs(self.start_date, ['000300', '000852', '932000'])
        market_index_data['jyrq'] = market_index_data['jyrq'].astype(str)
        market_index_data = market_index_data.pivot(index='jyrq', columns='zqdm', values='spjg').sort_index()
        market_index_data = market_index_data[['000300', '000852', '932000']]
        market_index_data = market_index_data.rename(columns={'000300': '沪深300', '000852': '中证1000', '932000': '中证2000'})
        howbuy_index_data = HBDB().read_private_index_daily_k_given_indexs(['HB1001', 'HB1002'], self.start_date, self.end_date)
        howbuy_index_data['TRADE_DATE'] = howbuy_index_data['TRADE_DATE'].astype(str)
        howbuy_index_data = howbuy_index_data.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX').sort_index()
        howbuy_index_data = howbuy_index_data[['HB1001', 'HB1002']]
        howbuy_index_data = howbuy_index_data.rename(columns={'HB1001': '好买主观多头', 'HB1002': '好买量化多头'})
        index_data = market_index_data.merge(howbuy_index_data, left_index=True, right_index=True, how='right')
        index_data.index = map(lambda x: datetime.strptime(x, '%Y%m%d'), index_data.index)
        index_data = index_data.dropna().sort_index()
        index_data.to_excel('{0}index_data.xlsx'.format(self.data_path))
        return

    def fund_compare(self, fund_dict):
        fund_data = HBDB().read_overseas_nav_given_codes(fund_dict.keys())
        fund_data = fund_data[['jjdm', 'jzrq', 'fqdwjz']].rename(columns={'jjdm': 'FUND_CODE', 'jzrq': 'TRADE_DATE', 'fqdwjz': 'ADJ_NAV'})
        fund_data['TRADE_DATE'] = fund_data['TRADE_DATE'].astype(str)
        fund_data = fund_data.pivot(index='TRADE_DATE', columns='FUND_CODE', values='ADJ_NAV').sort_index()
        fund_data = fund_data[(fund_data.index >= self.start_date) & (fund_data.index <= self.end_date)]
        # fund_data.iloc[0] = fund_data.iloc[0].fillna(1)
        fund_data = fund_data / fund_data.iloc[0]
        fund_data = fund_data.rename(columns=fund_dict)
        fund_data.index = map(lambda x: datetime.strptime(x, '%Y%m%d'), fund_data.index)
        fund_data.to_excel('{}fund_data.xlsx'.format(self.data_path))

        fund_data = HBDB().read_overseas_nav_given_codes(fund_dict.keys())
        fund_data = fund_data[['jjdm', 'jzrq', 'fqdwjz']].rename(columns={'jjdm': 'FUND_CODE', 'jzrq': 'TRADE_DATE', 'fqdwjz': 'ADJ_NAV'})
        fund_data['TRADE_DATE'] = fund_data['TRADE_DATE'].astype(str)
        fund_data = fund_data.pivot(index='TRADE_DATE', columns='FUND_CODE', values='ADJ_NAV').sort_index()
        fund_data = fund_data[(fund_data.index >= self.start_date) & (fund_data.index <= self.end_date)]
        fund_data = fund_data.interpolate()
        fund_data = fund_data[fund_data.index.isin(self.trade_df[self.trade_df['IS_MONTH_END'] == '1']['TRADE_DATE'].unique().tolist())]
        fund_data = fund_data.reset_index()
        fund_data['YEAR_MONTH'] = fund_data['TRADE_DATE'].apply(lambda x: str(x)[:6])
        fund_data = fund_data.set_index('YEAR_MONTH').drop('TRADE_DATE', axis=1)
        fund_performance_list = []
        for fund_id in fund_dict.keys():
            fund_performance = pd.DataFrame(index=['收益率', '年化收益率', '年化波动率', '最大回撤', 'Sharpe', 'Calmar', '2024年收益', '2023年收益', '2022年收益', '2021年收益'], columns=[fund_id])
            fund_data_id = fund_data[fund_id]
            fund_ret_id = fund_data_id.pct_change()
            fund_data_2021 = fund_data_id[(fund_data_id.index >= '202012') & (fund_data_id.index <= '202112')]
            fund_data_2022 = fund_data_id[(fund_data_id.index >= '202112') & (fund_data_id.index <= '202212')]
            fund_data_2023 = fund_data_id[(fund_data_id.index >= '202212') & (fund_data_id.index <= '202312')]
            fund_data_2024 = fund_data_id[(fund_data_id.index >= '202312') & (fund_data_id.index <= '202412')]
            fund_performance.loc['收益率', fund_id] = fund_data_id.iloc[-1] / fund_data_id.iloc[0] - 1
            fund_performance.loc['年化收益率', fund_id] = (fund_data_id.iloc[-1] / fund_data_id.iloc[0]) ** (12.0 / (len(fund_data_id) - 1)) - 1.0
            fund_performance.loc['年化波动率', fund_id] = np.std(fund_ret_id.dropna(), ddof=1) * np.sqrt(12)
            fund_performance.loc['最大回撤', fund_id] = cal_drawdown(fund_data_id)
            fund_performance.loc['Sharpe', fund_id] = (fund_performance.loc['年化收益率', fund_id] - 0.015) / fund_performance.loc['年化波动率', fund_id]
            fund_performance.loc['Calmar', fund_id] = fund_performance.loc['年化收益率', fund_id] / abs(fund_performance.loc['最大回撤', fund_id])
            fund_performance.loc['2024年收益', fund_id] = fund_data_2024.iloc[-1] / fund_data_2024.iloc[0] - 1
            fund_performance.loc['2023年收益', fund_id] = fund_data_2023.iloc[-1] / fund_data_2023.iloc[0] - 1
            fund_performance.loc['2022年收益', fund_id] = fund_data_2022.iloc[-1] / fund_data_2022.iloc[0] - 1
            fund_performance.loc['2021年收益', fund_id] = fund_data_2021.iloc[-1] / fund_data_2021.iloc[0] - 1
            fund_performance_list.append(fund_performance)
        fund_performance = pd.concat(fund_performance_list, axis=1)
        fund_performance = fund_performance.rename(columns=fund_dict)
        fund_performance.to_excel('{}fund_performance.xlsx'.format(self.data_path))
        return


if __name__ == '__main__':
    start_date = '20231229'
    end_date = '20240301'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/analysis/'
    analysis = Analysis(start_date, end_date, data_path)
    analysis.index_compare()

    fund_dict_1 = {
        'SEH477': '元盛',
        'SJR333': '黑翼',
        'SY2594': '半夏',
        'H04097': 'AHL',
        'H04113': 'ASPECT',
        'H04117': 'BHA',
        'H00044': 'MILLENIUM',
        'H04088': 'JJJ'
    }
    fund_dict_2 = {
        'SNL399': '仁桥',
        'P48965': '文多',
        'SK8618': '睿璞',
        'S20717': '巨杉',
        'S20769': '信璞',
        'SS5789': '明汯',
        'SLS817': '诚奇',
        'SJH866': '衍复',
        'SGP682': '世纪前沿',
        'H04134': '标普ETF',
        'H04136': '纳指ETF',
        'H04145': '日本ETF',
        'H04143': '印度ETF',
    }
    analysis.fund_compare(fund_dict_2)