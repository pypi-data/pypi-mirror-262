#!/usr/bin/python
# coding:utf-8
# 统计基金表现的def

import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine
import pymysql
from hbshare.quant.CChen.data.data import load_funds_data, load_funds_alpha, load_calendar_extra

pymysql.install_as_MySQLdb()


# 计算每只产品的年化收益，年华波动，夏普，最大回撤等指标
def performance_analysis(
        data_df,
        risk_free=0.015,
        start_date=datetime(2010, 1, 1).date(),
        end_date=datetime.now().date(),
        ret_num_per_year=52,
        monthly_funds=None,
        print_info=True
):
    """
    用于计算基金各项净值表现指标

    Parameters
    ----------
    data_df : DataFrame。
        净值序列，需要包括日期列，日期列的列名为“日期”或者“t_date”。
    risk_free : float, default: 0.015
        年化无风险收益率，用于计算夏普等指标。
    start_date : datetime.date, default: 2010/1/1
        用于对data_df切片.
        data_df中，日期小于start_date的行会被切除。
    end_date : datetime.date, default: 2010/1/1
        用于对data_df切片.
        data_df中，日期大于end_date的行会被切除。
    ret_num_per_year : int, default: 52
        data_df中净值的每年频数。
        输入周净值则以参数52进行年化
        输入日净值可以将此参数设置为250进行年化
    monthly_funds : list, default: None
        部分产品只披露月净值，不针对这部分产品进行部分收益统计
    print_info : bool, default: True
        计算时是否打印信息

    Returns
    -------
    DataFrame

    """
    if monthly_funds is None:
        monthly_funds = []
    funds = data_df.columns.tolist()
    date_col = 't_date'
    if 't_date' in funds:
        funds.remove(date_col)
    elif '日期' in funds:
        date_col = '日期'
        funds.remove('日期')
    # data_df['ret'] = data_df['nav'] / data_df['nav'].shift(1)

    result_all = pd.DataFrame()
    dd_all = data_df[[date_col]].copy()
    for i in funds:
        single_df = data_df[[date_col, i]]
        # data_before = single_df[single_df[date_col] < start_date][date_col].tolist()
        # if len(data_before) > 0:
        #     start_date_lag1 = data_before[-1]
        # else:
        #     start_date_lag1 = start_date
        single_df = single_df[
            np.array(single_df[date_col] >= start_date) & np.array(single_df[date_col] <= end_date)
            ].reset_index(drop=True)

        single_data = single_df[single_df[i] > 0]
        if len(single_data) > 1:
            if print_info:
                print('\t计算 ' + str(i) + ' 指标')
            start_index = single_data.index[0]
            single_df = single_df.iloc[start_index:].reset_index(drop=True)

            # 剔除最新净值之后的空值（若产品最新净值未按时更新）
            single_df = single_df[single_df[i] > 0].reset_index(drop=True)

            single_df['ret'] = single_df[i] / single_df[i].shift(1) - 1
            single_df['highest'] = single_df[i].cummax()
            single_df['dd'] = (single_df[i] - single_df['highest']) / single_df['highest']
            single_df['ddd'] = single_df['dd'].apply(lambda x: 1 if x < 0 else 0)
            single_df['ddds'] = single_df['ddd'].cumsum()
            single_df['dddg'] = (single_df.index - single_df['ddds']) * single_df['ddd']
            max_dd = min(single_df['dd'])

            dd_days = single_df['dddg'].value_counts().reset_index().sort_values(by='dddg')
            if len(dd_days) > 1:
                dd_days_hist = max(dd_days['dddg'].tolist()[1:])
                if single_df['ddd'].tolist()[-1] == 0:
                    dd_days_now = 0
                else:
                    dd_days_now = dd_days['dddg'].tolist()[-1]
            else:
                dd_days_hist = np.nan
                dd_days_now = np.nan

            fund_last_days = single_df[date_col][len(single_df) - 1] - single_df[date_col][0]
            cum_return = single_df[i][len(single_df) - 1] / single_df[i][0] - 1
            annualized_return = (single_df[i][len(single_df) - 1] / single_df[i][0]) ** (365 / fund_last_days.days) - 1
            annualized_return_mean = np.mean(single_df['ret'][1:] + 1) ** ret_num_per_year - 1  # 复利年化
            annualized_return_mean_simple = np.mean(single_df['ret'][1:]) * ret_num_per_year
            annualized_vol = np.std(single_df['ret'][1:], ddof=1) * np.sqrt(ret_num_per_year)

            single_df['downside_risk'] = single_df['ret']  #- risk_free
            single_df.loc[
                single_df['downside_risk'] > ((1 + risk_free) ** (1 / ret_num_per_year) - 1),
                'downside_risk'
            ] = 0
            downside_vol = np.std(single_df['downside_risk'][1:], ddof=1) * np.sqrt(ret_num_per_year)
            if annualized_vol == 0:
                sharpe = np.nan
            else:
                sharpe = (annualized_return - risk_free) / annualized_vol
            if downside_vol != 0:
                sortino = (annualized_return - risk_free) / downside_vol
            else:
                sortino = np.nan

            if max_dd < 0:
                calmar = annualized_return / -max_dd
            else:
                calmar = None

            win_rate = sum(single_df['ret'] > 0) / (len(single_df) - 1)

            if len(single_df[single_df['ret'] < 0]['ret']) > 0:
                win_loss = (
                        np.average(single_df[single_df['ret'] > 0]['ret'])
                        / np.average(-single_df[single_df['ret'] < 0]['ret'])
                )
            else:
                win_loss = np.nan

            if i in monthly_funds:
                annualized_return_mean = np.nan
                annualized_vol = np.nan
                sharpe = np.nan
                sortino = np.nan
                win_rate = np.nan
                win_loss = np.nan
        else:
            cum_return = np.nan
            annualized_return = np.nan
            annualized_return_mean = np.nan
            annualized_return_mean_simple = np.nan
            annualized_vol = np.nan
            max_dd = np.nan
            sharpe = np.nan
            sortino = np.nan
            calmar = np.nan
            win_rate = np.nan
            win_loss = np.nan
            dd_days_hist = np.nan
            dd_days_now = np.nan

        result_single = pd.DataFrame(
            {
                start_date.strftime('%Y%m%d') + '以来累计': cum_return,
                start_date.strftime('%Y%m%d') + '以来年化': annualized_return,
                '平均周收益年化': annualized_return_mean,
                # '平均年化收益(单利)': annualized_return_mean_simple,
                '年化波动率': annualized_vol,
                '最大回撤': max_dd,
                '历史最长回撤周': dd_days_hist,
                '已回撤周': dd_days_now,
                'Sharpe': sharpe,
                'Sortino': sortino,
                # '收益峰度': single_df['ret'][1:].kurt(),
                # '收益偏度': single_df['ret'][1:].skew(),
                'Calmar': calmar,
                '投资胜率': win_rate,
                '平均损益比': win_loss

            }, index=[i]
        ).T.reset_index()
        if len(result_all) == 0:
            result_all = result_single
        else:
            result_all = result_all.merge(result_single, on='index')

        # if len(dd_all) == 0:
        #     dd_all = single_df[['t_date', 'dd']].rename(columns={'dd': i})
        # else:
        if 'dd' in single_df.columns:
            dd_all = dd_all.merge(single_df[[date_col, 'dd']].rename(columns={'dd': i}), on=date_col, how='left')
        else:
            dd_all[i] = None

    return result_all, dd_all, data_df.set_index(date_col).ffill().pct_change().reset_index()


def ret(data_df):
    funds = data_df.columns.tolist()
    date_col = 't_date'
    if 't_date' in funds:
        funds.remove(date_col)
    elif '日期' in funds:
        date_col = '日期'
        funds.remove('日期')
    result_all = data_df[funds].ffill().pct_change()
    result_all['t_date'] = data_df[date_col]
    return result_all


# 计算每只产品每月收益
def performance_monthly_ret(data_df):
    result_all = ret(data_df=data_df)
    return result_all[1:].iloc[::-1]


# 按类型计算产品平均收益率
def performance_ret_per_type(start_date, end_date, keyword='type', freq='w', db_work=''):
    fund_list = pd.read_sql_query(
        'select * from fund_list where class=="cta"', create_engine(db_work)
    )
    type_list = fund_list[keyword].drop_duplicates().tolist()
    type_ret = pd.DataFrame()
    for i in type_list:
        funds = fund_list[fund_list[keyword] == i].reset_index(drop=True)
        funds_data = load_funds_data(
            fund_list=funds,
            first_date=start_date,
            end_date=end_date,
            freq=freq
        )
        funds_ret = performance_monthly_ret(data_df=funds_data)
        funds_ret.to_excel('rwewe.xlsx')
        funds_ret[i] = funds_ret[funds['name'].tolist()].mean(axis=1)
        if len(type_ret) == 0:
            type_ret = funds_ret[['t_date', i]]
        else:
            type_ret = pd.merge(type_ret, funds_ret[['t_date', i]], on='t_date', how='left')

    return type_ret.iloc[::-1]


# 每只产品固定数据
# 收益（本周，近四周，近八周，2020年度，2019年度）
# data_df传入产品净值升序序列
def performance_specific_ret(data_df, form=True, monthly_funds=None, yearly_ret_0=datetime(2017, 12, 29).date()):
    if monthly_funds is None:
        monthly_funds = []
    funds = data_df.columns.tolist()
    date_col = 't_date'
    if 't_date' in funds:
        funds.remove(date_col)
    elif '日期' in funds:
        date_col = '日期'
        funds.remove('日期')

    ret_this_week = []
    ret_last_week = []
    ret_this_4 = []
    ret_this_8 = []
    ret_3_months = []
    ret_6_months = []
    ret_2021 = []
    ret_2020 = []  # 年化
    ret_2019 = []  # 年化
    ret_2018 = []  # 年化

    yearly_return = {}

    for i in funds:
        print('\t computing specific index: ' + str(i))
        single_df = data_df[[date_col, i]].copy()
        # single_df['ret'] = data_df[i] / data_df[i].shift(1)
        if i not in monthly_funds:
            ret_this_week.append(single_df[i][len(single_df) - 1] / single_df[i][len(single_df) - 2] - 1)
            ret_last_week.append(single_df[i][len(single_df) - 2] / single_df[i][len(single_df) - 3] - 1)
            ret_this_4.append(single_df[i][len(single_df) - 1] / single_df[i][len(single_df) - 5] - 1)
            try:
                ret_this_8.append(single_df[i][len(single_df) - 1] / single_df[i][len(single_df) - 9] - 1)
            except KeyError:
                ret_this_8.append(None)

            try:
                ret_3_months.append(single_df[i][len(single_df) - 1] / single_df[i][len(single_df) - 13] - 1)
            except KeyError:
                ret_3_months.append(None)

            try:
                ret_6_months.append(single_df[i][len(single_df) - 1] / single_df[i][len(single_df) - 25] - 1)
            except KeyError:
                ret_6_months.append(None)
        else:
            ret_this_week.append(None)
            ret_last_week.append(None)
            ret_this_4.append(None)
            ret_this_8.append(None)
            ret_3_months.append(None)
            ret_6_months.append(None)

        single_df['year'] = single_df[date_col].apply(lambda x: x.year)
        range_dates = [max(yearly_ret_0, single_df[date_col][0])]
        year_slice = single_df.drop_duplicates(subset=['year'], keep='last')
        if len(year_slice) > 0:
            range_dates += year_slice[year_slice[date_col] > range_dates[0]][date_col].tolist()

        yearly_return[i] = {}
        for t in range(1, len(range_dates)):
            yearly_data = single_df[
                np.array(single_df[date_col] >= range_dates[t - 1])
                & np.array(single_df[date_col] <= range_dates[t])
            ][i]
            yearly_data = yearly_data[yearly_data > 0].tolist()
            if len(yearly_data) == 0:
                continue
            yearly_return[i][str(range_dates[t].year)] = yearly_data[-1] / yearly_data[0] - 1

    if form:
        result_df = pd.DataFrame(
            {
                '本周': ret_this_week,
                '上周': ret_last_week,
                '近四周': ret_this_4,
                '近八周': ret_this_8,
                '近三月': ret_3_months,
                '近六月': ret_6_months,
                # '2021': ret_2021,
                # '2020': ret_2020,
                # '2019': ret_2019,
                # '2018': ret_2018
            }, index=funds
        ).T.reset_index()

        return pd.concat([result_df, pd.DataFrame(yearly_return).reset_index().sort_values('index', ascending=False)])

    else:
        result_df = pd.DataFrame(
            {
                '本周收益': ret_this_week,
                '上周收益': ret_last_week,
                '近四周收益': ret_this_4
            }, index=funds
        ).sort_values(by='本周收益', ascending=True)

        return result_df.T.reset_index()


# 统计汇总
def update_performance(
        start_d,
        end_d,
        funds,
        db_path,
        # cal_db_path,
        month_release,
        data_type='',
        # avg=True
):
    fund_list = pd.read_sql_query(
        'select * from fund_list where `name` in ' + str(tuple(funds)), create_engine(db_path)
    )

    nav_origin = None

    if data_type.lower() != 'alpha':
        funds_data = load_funds_data(
            fund_list=fund_list,
            first_date=datetime(2000, 1, 1).date(),
            end_date=end_d,
            db_path=db_path,
            # cal_db_path=cal_db_path,
            print_info=True
        )
        funds_data_monthly = load_funds_data(
            fund_list=fund_list,
            first_date=start_d,
            end_date=end_d,
            freq='month',
            db_path=db_path,
            # cal_db_path=cal_db_path,
            print_info=True
        )

    else:
        funds_data = load_funds_alpha(
            fund_list=fund_list,
            first_date=datetime(2000, 1, 1).date(),
            end_date=end_d,
            db_path=db_path,
            # cal_db_path=cal_db_path,
            print_info=True
        )
        nav_origin = funds_data['nav']
        funds_data = funds_data['eav']

        cal_daily = load_calendar_extra(freq='', end_date=end_d)
        cal_daily = pd.merge(cal_daily, funds_data, on='t_date', how='left')
        cal_daily = cal_daily.fillna(method='ffill')

        funds_data_monthly = pd.merge(
            load_calendar_extra(freq='month', end_date=end_d),
            cal_daily,
            on='t_date', how='left'
        )
        funds_data_monthly = funds_data_monthly[funds_data_monthly['t_date'] >= start_d]

    result_monthly_ret = ret(funds_data_monthly)[1:].iloc[::-1]

    funds_date = funds_data[['t_date']].copy()
    funds_date.loc[:, 'year'] = pd.to_datetime(funds_data['t_date']).dt.year
    funds_date = funds_date.drop_duplicates(subset=['year'], keep='last')
    funds_date = funds_date[funds_date['year'] >= 2018].sort_values(by='year', ascending=False).reset_index(drop=True)
    funds_date.loc[:, 'year1'] = funds_date['year'].shift(1)
    funds_date = funds_date[1:5].reset_index(drop=True)

    result_key = []
    result_dd = []
    result_ret = []
    for d in range(len(funds_date)):
        rrr = performance_analysis(
            funds_data[funds_data['t_date'] >= start_d].reset_index(drop=True),
            monthly_funds=month_release,
            start_date=funds_date['t_date'][d],
        )
        result_key.append(rrr[0])
        result_dd.append(rrr[1])
        result_ret.append(rrr[2])

    result_key0, _, _ = performance_analysis(
        funds_data[funds_data['t_date'] >= start_d].reset_index(drop=True), monthly_funds=month_release,
        start_date=funds_data['t_date'].tolist()[-52]
    )

    result_specific = performance_specific_ret(
        funds_data[funds_data['t_date'] >= start_d].reset_index(drop=True), monthly_funds=month_release
    )

    fund_name_list = []
    fund_date_list = []
    fund_start_date = []
    for n in fund_list['name']:
        fund_name_list.append(n)
        try:
            fund_date_list.append(funds_data[funds_data[n] > 0]['t_date'].tolist()[-1].strftime('%Y-%m-%d'))
        except IndexError:
            fund_date_list.append(None)

        try:
            fund_start_date.append(funds_data[funds_data[n] > 0]['t_date'].tolist()[0].strftime('%Y/%m/%d'))
        except IndexError:
            fund_start_date.append(None)

    result_date = pd.DataFrame(
        {
            '起始日期': fund_start_date,
            '最新日期': fund_date_list
        }, index=fund_name_list
    ).T.reset_index()

    results_all = pd.concat([result_date, result_specific, result_key0])
    for i in result_key:
        results_all = pd.concat([results_all, i])

    nav_all = funds_data

    dd_all = result_dd[-1]

    weekly_ret_all = result_ret[-1]

    monthly_ret_all = result_monthly_ret

    nav_all_origin = nav_origin

    nav_2019 = nav_all[np.array(nav_all['t_date'] >= datetime(2018, 12, 28).date())].copy()
    nav_2020 = nav_all[np.array(nav_all['t_date'] >= datetime(2019, 12, 27).date())].copy()

    funds = nav_all.columns.tolist()
    funds.remove('t_date')

    for i in funds:
        try:
            nav_2019.loc[:, i] = nav_2019[i] / nav_2019[nav_2019[i] > 0][i].tolist()[0]
        except IndexError:
            nav_2019.loc[:, i] = None

        try:
            nav_2020.loc[:, i] = nav_2020[i] / nav_2020[nav_2020[i] > 0][i].tolist()[0]
        except IndexError:
            nav_2020.loc[:, i] = None

    result = {
        'main': results_all.reset_index(drop=True),
        'nav2020': nav_2020.sort_values(by='t_date', ascending=False).reset_index(drop=True),
        'nav2019': nav_2019.sort_values(by='t_date', ascending=False).reset_index(drop=True),
        'nav': nav_all.sort_values(by='t_date', ascending=False).reset_index(drop=True),
        'dd': dd_all.sort_values(by='t_date', ascending=False).reset_index(drop=True),
        'weekly_ret': weekly_ret_all.sort_values(by='t_date', ascending=False).reset_index(drop=True),
        'monthly_ret': monthly_ret_all
    }
    if data_type == 'alpha':
        result['nav_o'] = nav_all_origin.sort_values(by='t_date', ascending=False).reset_index(drop=True)
    return result

