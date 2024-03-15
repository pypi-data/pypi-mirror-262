# -*- coding: utf-8 -*-

from hbshare.fe.asset_allocation.efficient_frontier_solver import EF
from hbshare.fe.asset_allocation.mean_variance_solver import MaxReturn, MinRisk, MaxUtility, MSR
from hbshare.fe.asset_allocation.data_loader import Loader
from hbshare.fe.common.util.exception import InputParameterError
from hbshare.fe.common.util.logger import logger
from hbshare.fe.common.util.verifier import verify_type
from datetime import datetime
from multiprocessing import Pool
from numpy import linalg as la
import numpy as np
import pandas as pd

import logging
import os
if not os.path.exists('log_file/'):
    os.makedirs('log_file/')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler('log_file/mean_variance_log_{0}.txt'.format(datetime.today().strftime('%Y%m%d')))
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_alpha_ret(r, b_r, rf, q):
    b_r.columns = ['BMK']
    rf = rf / q
    beta = (pd.concat([r, b_r], axis=1) - rf).cov().iloc[-1]
    b_var = beta['BMK']
    beta = beta / b_var if b_var > 0 else beta
    beta = beta.drop('BMK')
    alpha_ret = r.mean() - rf - beta * (b_r.mean()['BMK'] - rf)
    alpha_ret = pd.DataFrame(alpha_ret) * q
    return alpha_ret

def get_alpha_cov(r, b_r, rf, q):
    b_r.columns = ['BMK']
    rf = rf / q
    beta = (pd.concat([r, b_r], axis=1) - rf).cov().iloc[-1]
    b_var = beta['BMK']
    beta = beta / b_var if b_var > 0 else beta
    beta = beta.drop('BMK')
    alpha_ret = pd.DataFrame(index=r.index, columns=r.columns)
    for col in r.columns:
        alpha_ret[col] = r[col] - rf - beta[col] * (b_r['BMK'] - rf)
    alpha_ret = alpha_ret.sort_index()
    alpha_cov = alpha_ret.cov()
    if len(np.shape(alpha_cov)) == 0:
        alpha_cov = np.array([[alpha_cov]])
    alpha_cov = np.nan_to_num(alpha_cov)
    alpha_cov = pd.DataFrame(alpha_cov) * q
    return alpha_cov

def isPD(A):
    try:
        _ = la.cholesky(A)
        return True
    except la.LinAlgError:
        return False

def nearestPD(A):
    B = (A + A.T) / 2.0
    _, s, V = la.svd(B)
    H = np.dot(V.T, np.dot(np.diag(s), V))
    A2 = (B + H) / 2.0
    A3 = (A2 + A2.T) / 2.0
    if isPD(A3):
        return A3
    spacing = np.spacing(la.norm(A))
    I = np.eye(A.shape[0])
    k = 1
    while not isPD(A3):
        mineig = np.min(np.real(la.eigvals(A3)))
        A3 += I * (-mineig * k**2 + spacing)
        k += 1
    return A3

def correct_cov(cov):
    if not isPD(cov):
        cov = nearestPD(cov)
    min_eig = np.min(np.real(np.linalg.eigvals(cov)))
    if min_eig < 0:
        cov -= 10 * min_eig * np.eye(*cov.shape)
    return cov

class MeanVariance:
    def __init__(self, asset_type, asset_list, asset_type_dict, method, start_date, end_date, is_reblance, reblance_type, n, frequency, compute_return_days, compute_risk_days,
                       lb_list=None, ub_list=None, asset_category_dict=None, category_lb_list=None, category_ub_list=None, total_weight=None,
                       target_risk=None, target_return=None, risk_aversion=None, risk_free_rate=None, benchmark=None, processes=16):
        self.asset_type = asset_type
        self.asset_list = asset_list
        self.asset_type_dict = asset_type_dict
        self.asset_type_df = pd.DataFrame.from_dict(self.asset_type_dict, orient='index', columns=['TYPE'])
        self.method = method
        self.start_date = start_date
        self.end_date = end_date
        self.is_reblance = is_reblance
        self.reblance_type = reblance_type
        self.n = n
        self.frequency = frequency
        self.compute_return_days = compute_return_days
        self.compute_risk_days = compute_risk_days
        self.lb_list = [0.0] * len(self.asset_list) if lb_list is None or lb_list == [] else lb_list
        self.ub_list = [1.0] * len(self.asset_list) if ub_list is None or ub_list == [] else ub_list
        self.asset_category_dict = {} if asset_category_dict is None else asset_category_dict
        self.asset_category_df = pd.DataFrame.from_dict(self.asset_category_dict, orient='index', columns=['CATEGORY'])
        self.category_lb_list = [0.0, 0.0, 0.0, 0.0] if category_lb_list is None or category_lb_list == [] else category_lb_list
        self.category_ub_list = [1.0, 1.0, 1.0, 1.0] if category_ub_list is None or category_ub_list == [] else category_ub_list
        self.total_weight = 1.0 if total_weight is None else total_weight
        self.target_risk = 0.03 if target_risk is None else target_risk
        self.target_return = 0.05 if target_return is None else target_return
        self.risk_aversion = 3.0 if risk_aversion is None else risk_aversion
        self.risk_free_rate = 0.03 if risk_free_rate is None else risk_free_rate
        self.benchmark = '000300' if benchmark is None or benchmark == '' else benchmark
        self.processes = processes
        self._verify_input_param()
        self._load()
        self._init_data()

    def _verify_input_param(self):
        verify_type(self.asset_type, 'asset_type', str)
        verify_type(self.asset_list, 'asset_list', list)
        verify_type(self.asset_type_dict, 'asset_type_dict', dict)
        verify_type(self.asset_type_df, 'asset_type_df', pd.DataFrame)
        verify_type(self.method, 'method', str)
        verify_type(self.start_date, 'start_date', str)
        verify_type(self.end_date, 'end_date', str)
        verify_type(self.is_reblance, 'is_reblance', bool)
        verify_type(self.reblance_type, 'reblance_type', str)
        verify_type(self.n, 'n', int)
        verify_type(self.frequency, 'frequency', str)
        verify_type(self.compute_return_days, 'compute_return_days', int)
        verify_type(self.compute_risk_days, 'compute_risk_days', int)
        verify_type(self.lb_list, 'lb_list', list)
        verify_type(self.ub_list, 'ub_list', list)
        verify_type(self.asset_category_dict, 'asset_category_dict', dict)
        verify_type(self.asset_category_df, 'asset_category_df', pd.DataFrame)
        verify_type(self.category_lb_list, 'category_lb_list', list)
        verify_type(self.category_ub_list, 'category_ub_list', list)
        verify_type(self.total_weight, 'total_weight', float)
        verify_type(self.target_risk, 'target_risk', float)
        verify_type(self.target_return, 'target_return', float)
        verify_type(self.risk_aversion, 'risk_aversion', float)
        verify_type(self.risk_free_rate, 'risk_free_rate', float)
        verify_type(self.benchmark, 'benchmark', str)
        verify_type(self.processes, 'processes', int)
        if self.asset_type not in ['index', 'fund']:
            msg = "asset_type not supported, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len(self.asset_list) == 0:
            msg = "asset_list is empty, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len(self.asset_type_dict) != len(self.asset_list):
            msg = "the length of asset_type_dict is not the same with asset_list, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.method not in ['max_return', 'min_risk', 'max_utility', 'max_sr', 'max_ir']:
            msg = "method not supported, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.reblance_type not in ['init_weight', 'init_target']:
            msg = "reblance_type not supported, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.n <= 0:
            msg = "n must be larger than 0, check your input"
            logger.error(msg)
        if self.frequency not in ['day', 'week', 'month', 'quarter', 'year']:
            msg = "frequency not supported, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.compute_return_days <= 0:
            msg = "compute_return_days must be larger than 0, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.compute_risk_days <= 0:
            msg = "compute_risk_days must be larger than 0, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len(self.lb_list) != len(self.asset_list) or len(self.ub_list) != len(self.asset_list):
            msg = "lb_list or ub_list must be the same length with asset_list, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len([i for i in self.lb_list if (i >= 0.0 and i <= 1.0)]) != len(self.asset_list):
            msg = "lb must be between 0 and 1, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len([i for i in self.ub_list if (i >= 0.0 and i <= 1.0)]) != len(self.asset_list):
            msg = "ub must be between 0 and 1, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.asset_type == 'fund' and len(self.asset_category_dict) != len(self.asset_list):
            msg = "the length of asset_category_dict is not the same with asset_list, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len(self.category_lb_list) != 4 or len(self.category_ub_list) != 4:
            msg = "the length of category_lb_list or category_ub_list must be 4, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len([i for i in self.category_lb_list if (i >= 0.0 and i <= 1.0)]) != 4:
            msg = "category_lb_list must be between 0 and 1, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if len([i for i in self.category_ub_list if (i >= 0.0 and i <= 1.0)]) != 4:
            msg = "category_ub_list must be between 0 and 1, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if not (self.total_weight >= 0.0 and self.total_weight <= 1.0):
            msg = "total_weight must be between 0 and 1, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.target_risk <= 0:
            msg = "target_risk must be larger than 0, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.risk_aversion <= 0:
            msg = "risk_aversion must be larger than 0, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.risk_free_rate <= 0:
            msg = "risk_free_rate must be larger than 0, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.processes <= 0:
            msg = "processes must be larger than 0, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)

    def _load(self):
        self.calendar_df = Loader().read_cal('19900101', self.end_date)
        self.calendar_df = self.calendar_df.rename(columns={'jyrq': 'CALENDAR_DATE', 'sfjj': 'IS_OPEN', 'sfzm': 'IS_WEEK_END', 'sfym': 'IS_MONTH_END'})
        self.calendar_df['CALENDAR_DATE'] = self.calendar_df['CALENDAR_DATE'].astype(str)
        self.calendar_df = self.calendar_df.sort_values('CALENDAR_DATE')
        self.calendar_df['IS_OPEN'] = self.calendar_df['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
        self.calendar_df['IS_WEEK_END'] = self.calendar_df['IS_WEEK_END'].fillna(0).astype(int)
        self.calendar_df['IS_MONTH_END'] = self.calendar_df['IS_MONTH_END'].fillna(0).astype(int)
        self.calendar_df['YEAR_MONTH'] = self.calendar_df['CALENDAR_DATE'].apply(lambda x: x[:6])
        self.calendar_df['MONTH'] = self.calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:6])
        self.calendar_df['MONTH_DAY'] = self.calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:])
        self.calendar_df['IS_QUARTER_END'] = np.where((self.calendar_df['IS_MONTH_END'] == 1) & (self.calendar_df['MONTH'].isin(['03', '06', '09', '12'])), 1, 0)
        self.calendar_df['IS_QUARTER_END'] = self.calendar_df['IS_QUARTER_END'].astype(int)
        self.calendar_df['IS_SEASON_END'] = np.where(self.calendar_df['MONTH_DAY'].isin(['0331', '0630', '0930', '1231']), 1, 0)
        self.calendar_df['IS_SEASON_END'] = self.calendar_df['IS_SEASON_END'].astype(int)
        self.trade_cal = self.calendar_df[self.calendar_df['IS_OPEN'] == 1]
        self.trade_cal['TRADE_DATE'] = self.trade_cal['CALENDAR_DATE']
        self.calendar_df = self.calendar_df.merge(self.trade_cal[['CALENDAR_DATE', 'TRADE_DATE']], on=['CALENDAR_DATE'], how='left')
        self.calendar_df['TRADE_DATE'] = self.calendar_df['TRADE_DATE'].fillna(method='ffill')
        self.calendar_df = self.calendar_df[['CALENDAR_DATE', 'IS_OPEN', 'IS_WEEK_END', 'IS_MONTH_END', 'IS_QUARTER_END', 'IS_SEASON_END', 'TRADE_DATE', 'YEAR_MONTH', 'MONTH', 'MONTH_DAY']]

        self.window = max(self.compute_return_days, self.compute_risk_days)
        self.start_date_backup = self.trade_cal[self.trade_cal['TRADE_DATE'] <= self.start_date]['TRADE_DATE'].unique().tolist()[-self.window - 40]

        if self.method == 'max_ir':
            self.benchmark_nav_df = Loader().read_index_daily_k_given_indexs(mutual_indexs=[self.benchmark], private_indexs=[self.benchmark], market_indexs=[self.benchmark], start=self.start_date_backup, end=self.end_date)
            self.benchmark_nav_df = self.benchmark_nav_df[['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX']] if len(self.benchmark_nav_df) != 0 else pd.DataFrame(columns=['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX'])
            self.benchmark_nav_df = self.benchmark_nav_df.drop_duplicates()
            self.benchmark_nav_df['TRADE_DATE'] = self.benchmark_nav_df['TRADE_DATE'].astype(str)
            self.benchmark_nav_df = self.benchmark_nav_df.pivot(index='TRADE_DATE', columns='INDEX_CODE', values='CLOSE_INDEX')
            self.benchmark_nav_df = self.benchmark_nav_df.sort_index()

            if len(self.benchmark_nav_df.dropna()) == 0:
                msg = "no benchmark nav data, check your input"
                logger.error(msg)
                raise InputParameterError(message=msg)

        if self.asset_type == 'index':
            group_size = 10
            group = int(len(self.asset_type_df) / group_size) + 1 if len(self.asset_type_df) % group_size > 0 else int(len(self.asset_type_df) / group_size) + 0
            nav_df_list = []
            for i in range(group):
                asset_type_df = self.asset_type_df.iloc[i * group_size: (i + 1) * group_size]
                mutual_indexs = asset_type_df[asset_type_df['TYPE'] == 'MUTUAL_INDEX'].index.unique().tolist()
                private_indexs = asset_type_df[asset_type_df['TYPE'] == 'PRIVATE_INDEX'].index.unique().tolist()
                market_indexs = asset_type_df[asset_type_df['TYPE'] == 'MARKET_INDEX'].index.unique().tolist()
                nav_df_group = Loader().read_index_daily_k_given_indexs(mutual_indexs=mutual_indexs, private_indexs=private_indexs, market_indexs=market_indexs, start=self.start_date_backup, end=self.end_date)
                nav_df_group = nav_df_group[['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX']] if len(nav_df_group) != 0 else pd.DataFrame(columns=['INDEX_CODE', 'TRADE_DATE', 'CLOSE_INDEX'])
                nav_df_list.append(nav_df_group)
            self.nav_df = pd.concat(nav_df_list)
            self.nav_df = self.nav_df.drop_duplicates()
            self.nav_df['TRADE_DATE'] = self.nav_df['TRADE_DATE'].astype(str)
            self.nav_df = self.nav_df.pivot(index='TRADE_DATE', columns='INDEX_CODE', values='CLOSE_INDEX')
            self.nav_df = self.nav_df.sort_index()

        if self.asset_type == 'fund':
            group_size = 10
            group = int(len(self.asset_type_df) / group_size) + 1 if len(self.asset_type_df) % group_size > 0 else int(len(self.asset_type_df) / group_size) + 0
            nav_df_list = []
            for i in range(group):
                asset_type_df = self.asset_type_df.iloc[i * group_size: (i + 1) * group_size]
                mutual_codes = asset_type_df[asset_type_df['TYPE'] == 'MUTUAL_FUND'].index.unique().tolist()
                private_codes = asset_type_df[asset_type_df['TYPE'] == 'PRIVATE_FUND'].index.unique().tolist()
                nav_df_group = Loader().read_fund_cumret_given_codes(mutual_codes=mutual_codes, private_codes=private_codes, start=self.start_date_backup, end=self.end_date)
                nav_df_group = nav_df_group[['FUND_CODE', 'TRADE_DATE', 'ADJ_NAV']] if len(nav_df_group) != 0 else pd.DataFrame(columns=['FUND_CODE', 'TRADE_DATE', 'ADJ_NAV'])
                nav_df_list.append(nav_df_group)
            self.nav_df = pd.concat(nav_df_list)
            self.nav_df = self.nav_df.drop_duplicates()
            self.nav_df['TRADE_DATE'] = self.nav_df['TRADE_DATE'].astype(str)
            self.nav_df = self.nav_df.pivot(index='TRADE_DATE', columns='FUND_CODE', values='ADJ_NAV')
            self.nav_df = self.nav_df.sort_index()

        logger.debug('data_start_date')
        logger.debug(self.start_date_backup)
        logger.debug('data_end_date')
        logger.debug(self.end_date)
        logger.debug('nav_df')
        logger.debug(self.nav_df.to_json())

        nan_nav_list = [asset for asset in self.asset_list if asset not in self.nav_df.columns]
        if len(nan_nav_list) == 0:
            self.nav_df = self.nav_df[self.asset_list].sort_index()
        else:
            msg = "{0} no nav data".format(','.join(nan_nav_list))
            logger.error(msg)
            raise InputParameterError(message=msg)
        return

    def _init_data(self):
        # 确定再平衡时点
        if len(self.trade_cal[(self.trade_cal['TRADE_DATE'] >= self.start_date) & (self.trade_cal['TRADE_DATE'] <= self.end_date)]) == 0:
            msg = "no reblance dates between start_date and end_date, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        else:
            self.start_trade_date = self.trade_cal[self.trade_cal['TRADE_DATE'] >= self.start_date]['TRADE_DATE'].values[0]
            if not self.is_reblance:
                reblance_list = [self.start_trade_date]
            else:
                if self.frequency == 'day':
                    reblance_list = self.calendar_df[self.calendar_df['IS_OPEN'] == 1]['TRADE_DATE'].unique().tolist()
                    reblance_list = [date for date in reblance_list if (date >= self.start_trade_date) and (date <= self.end_date)]
                    reblance_list = reblance_list[::self.n]
                elif self.frequency == 'week':
                    reblance_list = self.calendar_df[self.calendar_df['IS_OPEN'] == 1]['TRADE_DATE'].unique().tolist()
                    reblance_list = [date for date in reblance_list if (date >= self.start_trade_date) and (date <= self.end_date)]
                    reblance_list = reblance_list[::self.n * 5]
                elif self.frequency == 'month':
                    reblance_list = self.calendar_df['YEAR_MONTH'].unique().tolist()
                    reblance_list = [date for date in reblance_list if (date >= self.start_trade_date[:6]) and (date <= self.end_date[:6])]
                    reblance_list = reblance_list[::self.n]
                    reblance_list = [date + self.start_trade_date[6:] for date in reblance_list]
                    reblance_list = [date for date in reblance_list if (date >= self.start_trade_date) and (date <= self.end_date)]
                    reblance_list = [self.calendar_df[(self.calendar_df['IS_OPEN'] == 1) & (self.calendar_df['CALENDAR_DATE'] <= date)]['TRADE_DATE'].iloc[-1] for date in reblance_list]
                elif self.frequency == 'quarter':
                    reblance_list = self.calendar_df['YEAR_MONTH'].unique().tolist()
                    reblance_list = [date for date in reblance_list if (date >= self.start_trade_date[:6]) and (date <= self.end_date[:6])]
                    reblance_list = reblance_list[::self.n * 3]
                    reblance_list = [date + self.start_trade_date[6:] for date in reblance_list]
                    reblance_list = [date for date in reblance_list if (date >= self.start_trade_date) and (date <= self.end_date)]
                    reblance_list = [self.calendar_df[(self.calendar_df['IS_OPEN'] == 1) & (self.calendar_df['CALENDAR_DATE'] <= date)]['TRADE_DATE'].iloc[-1] for date in reblance_list]
                elif self.frequency == 'year':
                    reblance_list = self.calendar_df['YEAR_MONTH'].unique().tolist()
                    reblance_list = [date for date in reblance_list if (date >= self.start_trade_date[:6]) and (date <= self.end_date[:6])]
                    reblance_list = reblance_list[::self.n * 12]
                    reblance_list = [date + self.start_trade_date[6:] for date in reblance_list]
                    reblance_list = [date for date in reblance_list if (date >= self.start_trade_date) and (date <= self.end_date)]
                    reblance_list = [self.calendar_df[(self.calendar_df['IS_OPEN'] == 1) & (self.calendar_df['CALENDAR_DATE'] <= date)]['TRADE_DATE'].iloc[-1] for date in reblance_list]
                else:
                    reblance_list = [self.start_trade_date]

            logger.debug('reblance_list')
            logger.debug(reblance_list)

        # 确定每个再平衡时点所需数据
        calendar_day_list = self.calendar_df['CALENDAR_DATE'].unique().tolist()
        trading_day_list = self.calendar_df[self.calendar_df['IS_OPEN'] == 1]['TRADE_DATE'].unique().tolist()
        if self.asset_type == 'index' and len(self.asset_type_df[self.asset_type_df['TYPE'] == 'PRIVATE_INDEX']) > 0:
            date_list = self.calendar_df[self.calendar_df['IS_WEEK_END'] == 1]['TRADE_DATE'].unique().tolist()
            self.q = 52
        elif self.asset_type == 'fund' and len(self.asset_type_df[self.asset_type_df['TYPE'] == 'PRIVATE_FUND']) > 0:
            date_list = self.calendar_df[self.calendar_df['IS_WEEK_END'] == 1]['TRADE_DATE'].unique().tolist()
            self.q = 52
        else:
            date_list = self.calendar_df[self.calendar_df['IS_OPEN'] == 1]['TRADE_DATE'].unique().tolist()
            self.q = 250
        preprocessed_data = dict()
        self.reason_df = pd.DataFrame(index=reblance_list, columns=['原因'])
        if not (self.nav_df.empty or self.nav_df.reindex(date_list).interpolate().dropna(how='all').empty or self.nav_df.dropna(axis=1, how='all').shape[1] != len(self.asset_list)):
            nav_df = self.nav_df.reindex(calendar_day_list).interpolate().sort_index()
            nav_df = nav_df.reindex(date_list)
            ret_df = nav_df.pct_change()
            if self.method == 'max_ir':
                if not (self.benchmark_nav_df.empty or self.benchmark_nav_df.reindex(date_list).interpolate().dropna(how='all').empty):
                    benchmark_nav_df = self.benchmark_nav_df.reindex(date_list).interpolate().dropna(how='all').sort_index()
                    benchmark_ret_df = benchmark_nav_df.pct_change().dropna(how='all')
                    for date in reblance_list:
                        interval_data = dict()
                        ret_start = [td for td in trading_day_list if td <= date][-self.compute_return_days]
                        cov_start = [td for td in trading_day_list if td <= date][-self.compute_risk_days]
                        end = date
                        ret_need_length = len(ret_df[(ret_df.index >= ret_start) & (ret_df.index < end)])
                        ret_density = [len(self.nav_df[(self.nav_df.index >= ret_start) & (self.nav_df.index < end)][[asset]].dropna()) / float(ret_need_length) if ret_need_length != 0 else 0.0 for asset in self.asset_list]
                        cov_need_length = len(ret_df[(ret_df.index >= cov_start) & (ret_df.index < end)])
                        cov_density = [len(self.nav_df[(self.nav_df.index >= cov_start) & (self.nav_df.index < end)][[asset]].dropna()) / float(cov_need_length) if cov_need_length != 0 else 0.0 for asset in self.asset_list]
                        if min(ret_density) < 0.3 or min(cov_density) < 0.3:
                            ret_density_ser = pd.Series(ret_density)
                            ret_density_ser = ret_density_ser[ret_density_ser < 0.3]
                            cov_density_ser = pd.Series(cov_density)
                            cov_density_ser = cov_density_ser[cov_density_ser < 0.3]
                            if min(ret_density) < 0.3 and min(cov_density) >= 0.3:
                                self.reason_df.loc[date] = '{0}：{1}当期净值数据不足，无法计算预期收益！'.format(date, ','.join([self.asset_list[i] for i in ret_density_ser.index.tolist()]))
                            if min(ret_density) >= 0.3 and min(cov_density) < 0.3:
                                self.reason_df.loc[date] = '{0}：{1}当期净值数据不足，无法计算预期风险！'.format(date, ','.join([self.asset_list[i] for i in cov_density_ser.index.tolist()]))
                            if min(ret_density) < 0.3 and min(cov_density) < 0.3:
                                self.reason_df.loc[date] = '{0}：{1}当期净值数据不足，无法计算预期收益/风险！'.format(date, ','.join([self.asset_list[i] for i in list(set(ret_density_ser.index.tolist() + cov_density_ser.index.tolist()))]))
                            interval_data['ret_df_ori'] = pd.DataFrame()
                            interval_data['ret_df_ori'] = pd.DataFrame()
                            interval_data['ret_df'] = pd.DataFrame()
                            interval_data['cov_df'] = pd.DataFrame()
                            preprocessed_data[date] = interval_data
                        else:
                            interval_data['ret_df_ori'] = pd.DataFrame(ret_df[(ret_df.index >= ret_start) & (ret_df.index < end)].mean() * self.q)
                            interval_data['cov_df_ori'] = ret_df[(ret_df.index >= cov_start) & (ret_df.index < end)].cov() * self.q
                            interval_data['cov_df_ori'] = correct_cov(interval_data['cov_df_ori'])
                            interval_data['ret_df'] = get_alpha_ret(ret_df[(ret_df.index >= ret_start) & (ret_df.index < end)], benchmark_ret_df[(benchmark_ret_df.index >= ret_start) & (benchmark_ret_df.index < end)], self.risk_free_rate, self.q)
                            interval_data['cov_df'] = get_alpha_cov(ret_df[(ret_df.index >= cov_start) & (ret_df.index < end)], benchmark_ret_df[(benchmark_ret_df.index >= cov_start) & (benchmark_ret_df.index < end)], self.risk_free_rate, self.q)
                            interval_data['cov_df'] = correct_cov(interval_data['cov_df'])
                            preprocessed_data[date] = interval_data
                else:
                    for date in reblance_list:
                        self.reason_df.loc[date] = '{0}：{1}当期净值数据不足，无法计算预期收益/风险！'.format(date, ','.join(self.asset_list))
                        interval_data = dict()
                        interval_data['ret_df_ori'] = pd.DataFrame()
                        interval_data['ret_df_ori'] = pd.DataFrame()
                        interval_data['ret_df'] = pd.DataFrame()
                        interval_data['cov_df'] = pd.DataFrame()
                        preprocessed_data[date] = interval_data
            else:
                for date in reblance_list:
                    interval_data = dict()
                    ret_start = [td for td in trading_day_list if td <= date][-self.compute_return_days]
                    cov_start = [td for td in trading_day_list if td <= date][-self.compute_risk_days]
                    end = date
                    ret_need_length = len(ret_df[(ret_df.index >= ret_start) & (ret_df.index < end)])
                    ret_density = [len(self.nav_df[(self.nav_df.index >= ret_start) & (self.nav_df.index < end)][[asset]].dropna()) / float(ret_need_length) if ret_need_length != 0 else 0.0 for asset in self.asset_list]
                    cov_need_length = len(ret_df[(ret_df.index >= cov_start) & (ret_df.index < end)])
                    cov_density = [len(self.nav_df[(self.nav_df.index >= cov_start) & (self.nav_df.index < end)][[asset]].dropna()) / float(cov_need_length) if cov_need_length != 0 else 0.0 for asset in self.asset_list]
                    if min(ret_density) < 0.3 or min(cov_density) < 0.3:
                        ret_density_ser = pd.Series(ret_density)
                        ret_density_ser = ret_density_ser[ret_density_ser < 0.3]
                        cov_density_ser = pd.Series(cov_density)
                        cov_density_ser = cov_density_ser[cov_density_ser < 0.3]
                        if min(ret_density) < 0.3 and min(cov_density) >= 0.3:
                            self.reason_df.loc[date] = '{0}：{1}当期净值数据不足，无法计算预期收益！'.format(date, ','.join([self.asset_list[i] for i in ret_density_ser.index.tolist()]))
                        if min(ret_density) >= 0.3 and min(cov_density) < 0.3:
                            self.reason_df.loc[date] = '{0}：{1}当期净值数据不足，无法计算预期风险！'.format(date, ','.join([self.asset_list[i] for i in cov_density_ser.index.tolist()]))
                        if min(ret_density) < 0.3 and min(cov_density) < 0.3:
                            self.reason_df.loc[date] = '{0}：{1}当期净值数据不足，无法计算预期收益/风险！'.format(date, ','.join([self.asset_list[i] for i in list(set(ret_density_ser.index.tolist() + cov_density_ser.index.tolist()))]))
                        interval_data['ret_df_ori'] = pd.DataFrame()
                        interval_data['ret_df_ori'] = pd.DataFrame()
                        interval_data['ret_df'] = pd.DataFrame()
                        interval_data['cov_df'] = pd.DataFrame()
                        preprocessed_data[date] = interval_data
                    else:
                        if self.method == 'max_sr':
                            interval_data['ret_df_ori'] = pd.DataFrame(ret_df[(ret_df.index >= ret_start) & (ret_df.index < end)].mean() * self.q)
                            interval_data['cov_df_ori'] = ret_df[(ret_df.index >= cov_start) & (ret_df.index < end)].cov() * self.q
                            interval_data['cov_df_ori'] = correct_cov(interval_data['cov_df_ori'])
                            interval_data['ret_df'] = pd.DataFrame((ret_df[(ret_df.index >= ret_start) & (ret_df.index < end)] - self.risk_free_rate / self.q).mean() * self.q)
                            interval_data['cov_df'] = (ret_df[(ret_df.index >= cov_start) & (ret_df.index < end)] - self.risk_free_rate / self.q).cov() * self.q
                            interval_data['cov_df'] = correct_cov(interval_data['cov_df'])
                        else:
                            interval_data['ret_df_ori'] = pd.DataFrame(ret_df[(ret_df.index >= ret_start) & (ret_df.index < end)].mean() * self.q)
                            interval_data['cov_df_ori'] = ret_df[(ret_df.index >= cov_start) & (ret_df.index < end)].cov() * self.q
                            interval_data['cov_df_ori'] = correct_cov(interval_data['cov_df_ori'])
                            interval_data['ret_df'] = pd.DataFrame(ret_df[(ret_df.index >= ret_start) & (ret_df.index < end)].mean() * self.q)
                            interval_data['cov_df'] = ret_df[(ret_df.index >= cov_start) & (ret_df.index < end)].cov() * self.q
                            interval_data['cov_df'] = correct_cov(interval_data['cov_df'])
                        preprocessed_data[date] = interval_data
        else:
            for date in reblance_list:
                self.reason_df.loc[date] = '{0}：{1}当期净值数据不足，无法计算预期收益/风险！'.format(date, ','.join(self.asset_list))
                interval_data = dict()
                interval_data['ret_df_ori'] = pd.DataFrame()
                interval_data['ret_df_ori'] = pd.DataFrame()
                interval_data['ret_df'] = pd.DataFrame()
                interval_data['cov_df'] = pd.DataFrame()
                preprocessed_data[date] = interval_data
        self.preprocessed_data = preprocessed_data
        # ret_df_list, cov_df_list = [], []
        # for date in sorted(list(self.preprocessed_data.keys())):
        #     ret_df_list.append(self.preprocessed_data[date]['ret_df'])
        #     cov_df_list.append(self.preprocessed_data[date]['cov_df'])
        # all_ret_df = pd.concat(ret_df_list)
        # all_cov_df = pd.concat(cov_df_list)
        # if len(all_ret_df) == 0 and len(all_cov_df) != 0:
        #     print('no enough nav data for computing return model!')
        # if len(all_ret_df) != 0 and len(all_cov_df) == 0:
        #     print('no enough nav data for computing risk model!')
        # if len(all_ret_df) == 0 and len(all_cov_df) == 0:
        #     print('no enough nav data for computing return model and risk model!')

        logger.debug('preprocessed_data')
        logger.debug(self.preprocessed_data)
        return

    def get_optimal_one_process(self, date, period_data):
        if period_data['ret_df'].empty or period_data['cov_df'].empty:
            weight = pd.DataFrame(index=[date], columns=self.asset_list + ['cash'])
            status = pd.DataFrame(index=[date], columns=['优化状态'], data=['infeasible'])
            status = status.merge(self.reason_df, left_index=True, right_index=True, how='left')
            ef_weight = pd.DataFrame(index=range(22), columns=['date', 'group'] + self.asset_list + ['cash', 'sigma', 'r'])
            ef_weight['date'] = date
            ef_weight['group'] = list(range(21)) + ['result']
        else:
            try:
                if self.method == 'max_return':
                    self.ret = period_data['ret_df']
                    self.cov = period_data['cov_df']
                    logger.debug('OPT Parameters In')
                    for p in [date, self.method, self.asset_type, self.asset_list, self.ret, self.cov, self.target_risk, self.lb_list, self.ub_list, self.asset_category_df, self.category_lb_list, self.category_ub_list, self.total_weight]:
                        logger.debug(p)
                    weight, status = MaxReturn(self.asset_type, self.asset_list, self.ret, self.cov, self.target_risk, self.lb_list, self.ub_list, self.asset_category_df, self.category_lb_list, self.category_ub_list, self.total_weight).solve()
                    weight = pd.DataFrame(weight, columns=[date]).T
                    reason = '{0}：模型当期无优化解！'.format(date) if status == 'infeasible' else np.nan
                    status = pd.DataFrame(index=[date], columns=['优化状态', '原因'], data=[[status, reason]])
                elif self.method == 'min_risk':
                    self.ret = period_data['ret_df']
                    self.cov = period_data['cov_df']
                    logger.debug('OPT Parameters In')
                    for p in [date, self.method, self.asset_type, self.asset_list, self.ret, self.cov, self.target_return, self.lb_list, self.ub_list, self.asset_category_df, self.category_lb_list, self.category_ub_list, self.total_weight]:
                        logger.debug(p)
                    weight, status = MinRisk(self.asset_type, self.asset_list, self.ret, self.cov, self.target_return, self.lb_list, self.ub_list, self.asset_category_df, self.category_lb_list, self.category_ub_list, self.total_weight).solve()
                    weight = pd.DataFrame(weight, columns=[date]).T
                    reason = '{0}：模型当期无优化解！'.format(date) if status == 'infeasible' else np.nan
                    status = pd.DataFrame(index=[date], columns=['优化状态', '原因'], data=[[status, reason]])
                elif self.method == 'max_utility':
                    self.ret = period_data['ret_df']
                    self.cov = period_data['cov_df']
                    logger.debug('OPT Parameters In')
                    for p in [date, self.method, self.asset_type, self.asset_list, self.ret, self.cov, self.risk_aversion, self.lb_list, self.ub_list, self.asset_category_df, self.category_lb_list, self.category_ub_list, self.total_weight]:
                        logger.debug(p)
                    weight, status = MaxUtility(self.asset_type, self.asset_list, self.ret, self.cov, self.risk_aversion, self.lb_list, self.ub_list, self.asset_category_df, self.category_lb_list, self.category_ub_list, self.total_weight).solve()
                    weight = pd.DataFrame(weight, columns=[date]).T
                    reason = '{0}：模型当期无优化解！'.format(date) if status == 'infeasible' else np.nan
                    status = pd.DataFrame(index=[date], columns=['优化状态', '原因'], data=[[status, reason]])
                else:
                    self.ret = period_data['ret_df']
                    self.cov = period_data['cov_df']
                    logger.debug('OPT Parameters In')
                    for p in [date, self.method, self.asset_type, self.asset_list, self.ret, self.cov, self.lb_list, self.ub_list, self.asset_category_df, self.category_lb_list, self.category_ub_list, self.total_weight]:
                        logger.debug(p)
                    weight, status = MSR(self.asset_type, self.asset_list, self.ret, self.cov, self.lb_list, self.ub_list, self.asset_category_df, self.category_lb_list, self.category_ub_list, self.total_weight).solve()
                    weight = pd.DataFrame(weight, columns=[date]).T
                    reason = '{0}：模型当期无优化解！'.format(date) if status == 'infeasible' else np.nan
                    status = pd.DataFrame(index=[date], columns=['优化状态', '原因'], data=[[status, reason]])
            except:
                weight = pd.DataFrame(index=[date], columns=self.asset_list + ['cash'])
                status = pd.DataFrame(index=[date], columns=['优化状态', '原因'], data=[['infeasible', '{0}：模型当期无优化解！'.format(date)]])
            try:
                self.ret_ori = period_data['ret_df_ori']
                self.cov_ori = period_data['cov_df_ori']
                logger.debug('EF Parameters In')
                for p in [date, self.method, self.asset_type, self.asset_list, self.ret_ori, self.cov_ori, self.lb_list, self.ub_list, self.asset_category_df, self.total_weight, weight]:
                    logger.debug(p)
                ef_weight = EF(self.asset_type, self.asset_list, self.ret_ori, self.cov_ori, self.lb_list, self.ub_list, self.asset_category_df, self.total_weight, weight).solve()
                ef_weight['date'] = date
                ef_weight = ef_weight[['date', 'group'] + self.asset_list + ['cash', 'sigma', 'r']]
            except:
                self.ret_ori = period_data['ret_df_ori']
                self.cov_ori = period_data['cov_df_ori']
                ef_weight = pd.DataFrame(index=range(22), columns=['date', 'group'] + self.asset_list + ['cash', 'sigma', 'r'])
                ef_weight['date'] = date
                ef_weight['group'] = list(range(21)) + ['result']
                w_star = weight[self.asset_list].T if len(weight[self.asset_list].dropna()) > 0 else None
                if w_star is not None:
                    sigma2_star = (np.matrix(w_star).T * np.matrix(self.cov_ori) * np.matrix(w_star))[0, 0]
                    sigma_star = np.sqrt(sigma2_star)
                    r_star = (np.matrix(w_star).T * np.matrix(self.ret_ori))[0, 0]
                else:
                    sigma_star = np.nan
                    r_star = np.nan
                ef_weight.iloc[-1, 2:-2] = weight.iloc[0]
                ef_weight.iloc[-1, -2] = sigma_star
                ef_weight.iloc[-1, -1] = r_star
                ef_weight = pd.concat([ef_weight.iloc[:-1].dropna(), ef_weight.iloc[-1:]])
        print('[{0}]/[{1}] done'.format(date, self.method))

        logger.debug('date')
        logger.debug(date)
        logger.debug('weight')
        logger.debug(weight.to_json())
        logger.debug('status')
        logger.debug(status.to_json())
        logger.debug('ef_weight')
        logger.debug(ef_weight.to_json())
        return weight, status, ef_weight

    def get_all(self):
        result_list = []
        p = Pool(processes=self.processes)
        for date, period_data in self.preprocessed_data.items():
            result = p.apply_async(self.get_optimal_one_process, args=(date, period_data))
            result_list.append(result)
        p.close()
        p.join()
        print('processes done.')
        weight_list, status_list, ef_weight_list = [], [], []
        for result in result_list:
            weight, status, ef_weight = result.get()
            weight_list.append(weight)
            status_list.append(status)
            ef_weight_list.append(ef_weight)
        weight_df = pd.concat(weight_list).sort_index()
        status_df = pd.concat(status_list).sort_index()
        ef_weight_df = pd.concat(ef_weight_list).sort_values(['date', 'group'])
        # 权重归一化（本版本不支持有现金配置）
        weight_df = weight_df[self.asset_list]
        weight_df['TOTAL'] = weight_df.sum(axis=1)
        weight_df['TOTAL'] = weight_df['TOTAL'].replace(0.0, np.nan)
        weight_df = weight_df.apply(lambda x: x.iloc[:len(self.asset_list)] / x[-1], axis=1)
        if self.reblance_type == 'init_weight' and len(weight_df.dropna()) != 0:
            start_index = weight_df.dropna().index[0]
            weight_df.loc[weight_df.index > start_index, :] = np.nan
            weight_df = weight_df.fillna(method='ffill')
            status_df.loc[status_df.index > start_index, :] = np.nan
            status_df = status_df.fillna(method='ffill')
        # 权重归一化（本版本不支持有现金配置）
        ef_weight_df['TOTAL'] = ef_weight_df[self.asset_list].sum(axis=1)
        ef_weight_df['TOTAL'] = ef_weight_df['TOTAL'].replace(0.0, np.nan)
        ef_weight_df[self.asset_list] = ef_weight_df[self.asset_list + ['TOTAL']].apply(lambda x: x.iloc[:len(self.asset_list)] / x[-1], axis=1)
        ef_weight_df = ef_weight_df[['date', 'group'] + self.asset_list + ['sigma', 'r']]
        # if len(weight_df.dropna()) == 0:
        #     print('no optimal results!')
        return weight_df, status_df, ef_weight_df


if __name__ == '__main__':
    # mutual_index: ['HM0001', 'HM0024', 'HM0095']
    # private_index: ['HB0011', 'HB0016', 'HB1001']
    # market_index: ['000300', '000906', 'CBA00301']
    # mutual_fund: ['002943', '688888', '000729']
    # private_fund: ['SGK768', 'SX8958', 'SR4480']

    weight_df, status_df, ef_weight_df = MeanVariance(asset_type='fund',  # index, fund
                                                      asset_list=['002943', '688888', '000729'],
                                                      asset_type_dict={'002943': 'MUTUAL_FUND', '688888': 'MUTUAL_FUND', '000729': 'MUTUAL_FUND'},  # MUTUAL_INDEX, PRIVATE_INDEX, MARKET_INDEX, MUTUAL_FUND, PRIVATE_FUND
                                                      method='max_return',  # max_return, min_risk, max_utility, max_sr, max_ir
                                                      start_date='20181231',
                                                      end_date='20220704',
                                                      is_reblance=True,   # True, False
                                                      reblance_type='init_target',  # init_weight, init_target
                                                      n=3,
                                                      frequency='month',  # day, week, month, quarter, year
                                                      compute_return_days=120,  # 交易日
                                                      compute_risk_days=120,  # 交易日
                                                      asset_category_dict={'002943': 'EQUITY', '688888': 'EQUITY', '000729': 'BOND'}, # EQUITY, BOND, COMMODITY, CURRENCY
                                                      category_lb_list=[0.0, 0.0, 0.0, 0.0],
                                                      category_ub_list=[0.5, 0.5, 1.0, 1.0],
                                                      target_risk=0.03,
                                                      processes=4
                                                      ).get_all()
    print(weight_df, status_df, ef_weight_df)