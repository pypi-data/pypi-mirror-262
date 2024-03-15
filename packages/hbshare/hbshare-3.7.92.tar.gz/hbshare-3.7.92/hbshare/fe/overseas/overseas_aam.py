# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
line_color_list = ['#F04950', '#6268A2', '#959595', '#333335', '#EE703F', '#7E4A9B', '#8A662C',
                  '#44488E', '#BA67E9', '#3FAEEE']
bar_color_list = ['#C94649', '#EEB2B4', '#E1777A', '#D57C56', '#E39A79', '#DB8A66', '#E5B88C',
                  '#8588B7', '#B4B6D1', '#55598D', '#628497', '#A9C6CB', '#866EA9', '#B79BC7',
                  '#7D7D7E', '#CACACA', '#A7A7A8', '#606063', '#C4C4C4', '#99999B', '#B7B7B7']
area_color_list = ['#D55659', '#E1777A', '#DB8A66', '#E5B88C', '#EEB2B4', '#D57C56', '#E39A79',
                   '#8588B7', '#626697', '#866EA9', '#B79BC7', '#B4B6D1', '#628497', '#A9C6CB',
                   '#7D7D7E', '#A7A7A8', '#99999B', '#B7B7B7', '#CACACA', '#969696', '#C4C4C4']
new_color_list = ['#F04950', '#959595', '#6268A2', '#333335', '#D57C56', '#628497']


def quantile_definition(idxs, col, daily_df):
    part_df = daily_df.iloc[list(map(int, idxs))].copy(deep=True)
    q = (1.0 - np.count_nonzero(part_df[col].iloc[-1] < part_df[col]) / len(part_df)) if len(part_df[col].dropna()) != 0 else np.nan
    return q


def cal_drawdown(ser):
    df = pd.DataFrame(ser)
    df.columns = ['NAV']
    df = df.sort_index()
    df['IDX'] = range(len(df))
    df['HIGHEST'] = df['NAV'].cummax()
    df['DRAWDOWN'] = (df['NAV'] - df['HIGHEST']) / df['HIGHEST']
    return min(df['DRAWDOWN'])


class OverseasAssetAllocation:
    def __init__(self, start_date, end_date, data_path):
        self.start_date = start_date
        self.end_date = end_date
        self.data_path = data_path
        self.index_list = ['SPX Index', 'TPX Index', 'SENSEX Index']
        self.index_name_dict = {
            'SPX Index': '标普500指数', 'CCMP Index': '纳斯达克综合指数', 'TPX Index': '日本东证指数',
            'VN30 Index': '越南VN30指数', 'SENSEX Index': '印度孟买30指数', 'DAX Index': '德国DAX30指数'
        }
        self.index_weight_dict = {
            'SPX Index': 0.60, 'TPX Index': 0.20, 'SENSEX Index': 0.20
        }
        self.load()

    def load(self):
        # 交易日历
        self.cal = HBDB().read_overseas_cal('76')
        self.cal['rq'] = self.cal['rq'].astype(str)
        self.trade_cal = self.cal[self.cal['sfjy'] == '1']
        self.monthly_cal = self.cal[self.cal['sfym'] == '1']

        # 指数数据
        self.overseas_index_daily_k = HBDB().read_overseas_index_daily_k_given_indexs(self.index_list)
        self.overseas_index_daily_k.to_hdf('{0}overseas_index_daily_k.hdf'.format(self.data_path), key='table', mode='w')
        self.overseas_index_daily_k = pd.read_hdf('{0}overseas_index_daily_k.hdf'.format(self.data_path), key='table')
        self.overseas_index_daily_k['jyrq'] = self.overseas_index_daily_k['jyrq'].astype(str)
        self.overseas_index_daily_k = self.overseas_index_daily_k[(self.overseas_index_daily_k['jyrq'] >= self.start_date) & (self.overseas_index_daily_k['jyrq'] <= self.end_date)]

        self.overseas_index_finance = HBDB().read_overseas_index_finance_given_indexs(self.index_list)
        self.overseas_index_finance.to_hdf('{0}overseas_index_finance.hdf'.format(self.data_path), key='table', mode='w')
        self.overseas_index_finance = pd.read_hdf('{0}overseas_index_finance.hdf'.format(self.data_path), key='table')
        self.overseas_index_finance['jyrq'] = self.overseas_index_finance['jyrq'].astype(str)
        self.overseas_index_finance = self.overseas_index_finance[(self.overseas_index_finance['jyrq'] >= self.start_date) & (self.overseas_index_finance['jyrq'] <= self.end_date)]

        self.overseas_index_best = HBDB().read_overseas_index_best_given_indexs(self.index_list)
        self.overseas_index_best.to_hdf('{0}overseas_index_best.hdf'.format(self.data_path), key='table', mode='w')
        self.overseas_index_best = pd.read_hdf('{0}overseas_index_best.hdf'.format(self.data_path), key='table')
        self.overseas_index_best['jyrq'] = self.overseas_index_best['jyrq'].astype(str)
        self.overseas_index_best = self.overseas_index_best[(self.overseas_index_best['jyrq'] >= self.start_date) & (self.overseas_index_best['jyrq'] <= self.end_date)]
        return

    def strategy(self, w_p, w_b, ret, q, strategy_name):
        ret_p = (w_p.shift() * ret).dropna().sum(axis=1)
        ret_b = (w_b.shift() * ret).dropna().sum(axis=1)
        df = pd.concat([ret_p, ret_b], axis=1)
        df.columns = ['P_RET', 'B_RET']
        df['E_RET'] = df['P_RET'] - df['B_RET']
        df.iloc[0] = 0.0
        df['P_NAV'] = (df['P_RET'] + 1.0).cumprod()
        df['B_NAV'] = (df['B_RET'] + 1.0).cumprod()
        df['E_NAV'] = (df['E_RET'] + 1.0).cumprod()
        df.index = map(lambda x: datetime.strptime(x, '%Y%m%d'), df.index)

        fig, ax = plt.subplots(figsize=(6, 3))
        ax_r = ax.twinx()
        ax.plot(df.index, df['P_NAV'].values, color=line_color_list[0], label='中枢调整', linewidth=1)
        ax.plot(df.index, df['B_NAV'].values, color=line_color_list[1], label='中枢配置', linewidth=1)
        ax_r.fill_between(df.index, 0, df['E_NAV'], color=line_color_list[2], label='超额净值（右轴）', linewidth=1, alpha=0.5)
        ax_r.set_ylim([0.95, 1.15])
        h1, l1 = ax.get_legend_handles_labels()
        h2, l2 = ax_r.get_legend_handles_labels()
        plt.legend(handles=h1 + h2, labels=l1 + l2, loc=8, bbox_to_anchor=(0.5, -0.25), ncol=3, frameon=False)
        plt.tight_layout()
        sns.despine(top=True, right=False, left=False, bottom=False)
        plt.savefig('{0}{1}.png'.format(self.data_path, strategy_name))

        performance = pd.DataFrame(index=['年化收益率', '年化波动率', '最大回撤', '夏普比率（Rf=1.5%）', '卡玛比率', '投资胜率（月收益率战胜基准）', '投资胜率（月收益率大于0）', '投资损益比'], columns=['指标值'])
        performance.loc['年化收益率', '指标值'] = (df['P_NAV'].iloc[-1] / df['P_NAV'].iloc[0]) ** (q / float(len(df) - 1)) - 1.0
        performance.loc['年化波动率', '指标值'] = np.std(df['P_RET'].dropna(), ddof=1) * np.sqrt(q)
        performance.loc['最大回撤', '指标值'] = cal_drawdown(df['P_NAV'])
        performance.loc['夏普比率（Rf=1.5%）', '指标值'] = (performance.loc['年化收益率', '指标值'] - 0.015) / performance.loc['年化波动率', '指标值']
        performance.loc['卡玛比率', '指标值'] = performance.loc['年化收益率', '指标值'] / performance.loc['最大回撤', '指标值'] * (-1)
        performance.loc['投资胜率（月收益率战胜基准）', '指标值'] = len(df[df['E_RET'] > 0]) / float(len(df.dropna()))
        performance.loc['投资胜率（月收益率大于0）', '指标值'] = len(df[df['P_RET'] > 0]) / float(len(df.dropna()))
        performance.loc['投资损益比', '指标值'] = df[df['P_RET'] > 0]['P_RET'].mean() / df[df['P_RET'] < 0]['P_RET'].mean() * (-1.0)
        performance.to_excel('{0}{1}.xlsx'.format(self.data_path, strategy_name))
        return

    def test(self):
        # 月度收益率
        nav = self.overseas_index_daily_k.pivot(index='jyrq', columns='bzzsdm', values='px_last').sort_index()
        nav = nav[self.index_list].rename(columns=self.index_name_dict)
        nav = nav.dropna()
        nav_monthly = nav[nav.index.isin(self.monthly_cal['rq'].unique().tolist())].sort_index()
        ret_monthly = nav_monthly.pct_change().dropna()

        # EPS/BEST_EPS增长率排序策略
        eps = self.overseas_index_best.pivot(index='jyrq', columns='bzzsdm', values='best_eps').sort_index()
        # eps = self.overseas_index_finance.pivot(index='jyrq', columns='bzzsdm', values='trail_12m_eps_bef_xo_item').sort_index()
        eps = eps[self.index_list].rename(columns=self.index_name_dict)
        eps = eps.dropna()
        eps_monthly = eps[eps.index.isin(self.monthly_cal['rq'].unique().tolist())].sort_index()
        weight_adj = eps_monthly.rolling(12).mean().pct_change(12).dropna()
        weight_adj = weight_adj.rank(axis=1)
        weight_adj = weight_adj.replace({3: 0.10, 2: 0.00, 1: -0.10})

        weight_b1 = pd.DataFrame(np.ones(weight_adj.shape), index=weight_adj.index.tolist(), columns=self.index_list)
        for col in self.index_list:
            weight_b1[col] = weight_b1[col] * self.index_weight_dict[col]
        weight_b1 = weight_b1[self.index_list].rename(columns=self.index_name_dict)
        weight_p1 = weight_b1 + weight_adj
        weight_p1 = weight_p1.apply(lambda x: x / x.sum() if x.sum() != 0 else 1.0 / weight_adj.shape[1], axis=1)
        self.strategy(weight_p1, weight_b1, ret_monthly, 12, 'BEST_EPS增长率排序策略_622_10')
        # self.strategy(weight_p1, weight_b1, ret_monthly, 12, 'EPS增长率排序策略（等权基准）')
        return


if __name__ == '__main__':
    start_date = '20111231'
    end_date = '20240301'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/overseas_asset_allocation/'
    OverseasAssetAllocation(start_date, end_date, data_path).test()