"""
可投池多策略构建 vs 多策略
"""
import pandas as pd
import numpy as np
from datetime import datetime
import hbshare as hbs
from hbshare.quant.Kevin.quant_room.MyUtil.data_loader import get_fund_nav_from_sql, get_trading_day_list
from Arbitrage_backtest import cal_annual_return, cal_annual_volatility, cal_sharpe_ratio, cal_max_drawdown


def get_fund_nav(sub_pool, name):
    fund_dict = sub_pool.set_index('代表产品')['基金代码'].to_dict()
    start_date, end_date = sub_pool['入池时间'].min(), '20230928'

    trading_day_list = get_trading_day_list(start_date, end_date, frequency="week")
    nav_df = get_fund_nav_from_sql(start_date, end_date, fund_dict).reindex(trading_day_list)

    adj_nav = []
    for fund_name in fund_dict.keys():
        s_date = sub_pool[sub_pool['代表产品'] == fund_name]['入池时间'].values[0]
        e_date = sub_pool[sub_pool['代表产品'] == fund_name]['出池时间'].values[0]
        e_date = end_date if e_date >= end_date else e_date
        tmp = nav_df[[fund_name]].loc[s_date: e_date]
        adj_nav.append(tmp)
    adj_nav = pd.concat(adj_nav, axis=1).sort_index()
    return_df = adj_nav.pct_change(limit=1).dropna(how='all', axis=1)
    mean_df = return_df.mean(axis=1).dropna().to_frame(name)

    return mean_df


def multi_strategy_portfolio():
    # 存续池
    pool_exist = pd.read_excel('D:\\研究基地\\私募量化基金池\\量化基金池202309.xlsx', sheet_name="量化池列表", header=1)
    include_cols = ['基金代码', '代表产品', '超一级/一级策略', '二级策略', '入池时间']
    pool_exist = pool_exist.dropna(subset=["二级策略"])[include_cols]
    pool_exist['入池时间'] = pool_exist['入池时间'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
    # 已出池
    pool_out = pd.read_excel('D:\\研究基地\\私募量化基金池\\量化基金池202309.xlsx', sheet_name="出池记录", header=1)
    include_cols = ['基金代码', '基金简称', '超一级/一级策略', '二级策略', '入池时间', '出池时间']
    pool_out = pool_out.dropna(subset=["二级策略"])[include_cols].rename(columns={"基金简称": "代表产品"})
    pool_out['入池时间'] = pool_out['入池时间'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
    pool_out['出池时间'] = pool_out['出池时间'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
    # 整合
    pool = pd.concat([pool_exist, pool_out]).sort_values(by='基金代码')
    pool['出池时间'] = pool['出池时间'].fillna('20301231')

    # 500指增
    sub_pool = pool[pool['超一级/一级策略'] == '股票 - 指数增强']
    sub_pool = sub_pool[sub_pool['二级策略'] == '500指数增强']
    mean_df_alpha = get_fund_nav(sub_pool, '500指增')
    # CTA
    sub_pool = pool[pool['超一级/一级策略'] == '管理期货']
    sub_pool = sub_pool[sub_pool['二级策略'] != '趋势CTA（美元）']
    sub_pool.loc[sub_pool['代表产品'].str.contains('黑翼'), '出池时间'] = '20201231'
    exclude_list = ['道合东哥2号', '展弘稳进1号1期', '德劭锐哲中国', '腾胜中国聚量宏观策略1号', '涵德盈冲量化CTA2号', 'Millburn ResOP']
    sub_pool = sub_pool[~sub_pool['代表产品'].isin(exclude_list)]
    sub_pool.loc[sub_pool['代表产品'] == '华宝兴业元盛七号A', '基金代码'] = '246039'

    # 手动剔除
    not_available = ['黑翼CTA二号', '黑翼CTA-T2', '九坤量化CTA1号', '正定成长CTA1号', '正定稳健CTA1号']
    sub_pool = sub_pool[~sub_pool['代表产品'].isin(not_available)]

    mean_df_cta = get_fund_nav(sub_pool, 'CTA')
    # 套利
    # sub_pool1 = pool[(pool['超一级/一级策略'] == '另类策略') | (pool['二级策略'] == '套利CTA')]
    # sub_pool2 = pool[pool['代表产品'].isin(['蒙玺分形3号', '稳博中睿6号'])]
    # sub_pool = pd.concat([sub_pool1, sub_pool2])
    # mean_df_arb = get_fund_nav(sub_pool, '套利')
    # 市场中性
    sub_pool = pool[pool['二级策略'] == '500市场中性']
    exclude_list = ['希格斯招享1号', '量派睿核10号']
    sub_pool = sub_pool[~sub_pool['代表产品'].isin(exclude_list)]
    mean_df_neu = get_fund_nav(sub_pool, '市场中性')

    # mean_df = mean_df_alpha.merge(mean_df_cta, left_index=True, right_index=True, how='outer').merge(
    #     mean_df_arb, left_index=True, right_index=True, how='outer').merge(
    #     mean_df_neu, left_index=True, right_index=True, how='outer').sort_index().loc["20190215":]
    mean_df = mean_df_alpha.merge(mean_df_cta, left_index=True, right_index=True, how='outer').merge(
        mean_df_neu, left_index=True, right_index=True, how='outer').sort_index().loc["20190215":]

    # 组合构建
    # weight = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0.25, 0.2, 0, 0.55],
    #           [0.5, 0.5, 0, 0], [0.2, 0.05, 0.05, 0.7], [0.8, 0.2, 0, 0], [0, 0.1, 0.1, 0.8], [1./3, 1./3, 0, 1./3]]
    # weight_df = pd.DataFrame(index=['500指增', 'CTA', '套利', '市场中性',
    #                                 '25%指增+55%市场中性+20%CTA',
    #                                 '50%指增+50%CTA', '20%指增+70%中性+5%CTA+5%套利',
    #                                 '80%指增+20%CTA', '80%中性+10%CTA+10%套利', '指增/CTA/市场中性各1/3'], columns=mean_df.columns, data=weight)
    # port_return = mean_df.dot(weight_df.T)
    # port_nav = (1 + port_return).cumprod()
    port_nav = (1 + mean_df.mean(axis=1)).cumprod().to_frame('模拟组合费前')
    # trading_day_list = get_trading_day_list("20190215", "20230928", frequency="week")
    # fund_dict = {"对冲精选N1": "SCS026", "新方程大类配置": "SK1216"}
    # nav_df = get_fund_nav_from_sql("20190215", "20230928", fund_dict).reindex(trading_day_list)

    portfolio_index_df = pd.DataFrame(
        index=port_nav.columns, columns=['年化收益', '年化波动', '最大回撤', 'Sharpe', '胜率', '平均损益比'])
    portfolio_index_df.loc[:, '年化收益'] = port_nav.pct_change().dropna(how='all').apply(cal_annual_return, axis=0)
    portfolio_index_df.loc[:, '年化波动'] = \
        port_nav.pct_change().dropna(how='all').apply(cal_annual_volatility, axis=0)
    portfolio_index_df.loc[:, '最大回撤'] = port_nav.apply(cal_max_drawdown, axis=0)
    portfolio_index_df.loc[:, 'Sharpe'] = \
        port_nav.pct_change().dropna(how='all').apply(lambda x: cal_sharpe_ratio(x, 0.015), axis=0)
    portfolio_index_df.loc[:, '胜率'] = \
        port_nav.pct_change().dropna(how='all').apply(lambda x: x.gt(0).sum() / len(x), axis=0)
    portfolio_index_df.loc[:, '平均损益比'] = \
        port_nav.pct_change().dropna(how='all').apply(lambda x: x[x > 0].mean() / x[x < 0].abs().mean(), axis=0)
    portfolio_index_df.index.name = '产品名称'
    portfolio_index_df.reset_index(inplace=True)
    # 格式处理
    portfolio_index_df['年化收益'] = portfolio_index_df['年化收益'].apply(lambda x: format(x, '.2%'))
    portfolio_index_df['年化波动'] = portfolio_index_df['年化波动'].apply(lambda x: format(x, '.2%'))
    portfolio_index_df['最大回撤'] = portfolio_index_df['最大回撤'].apply(lambda x: format(x, '.2%'))
    portfolio_index_df['Sharpe'] = portfolio_index_df['Sharpe'].round(2)
    portfolio_index_df['胜率'] = portfolio_index_df['胜率'].apply(lambda x: format(x, '.1%'))
    portfolio_index_df['平均损益比'] = portfolio_index_df['平均损益比'].round(2)

    return portfolio_index_df


def single_pm_portfolio():
    config_df = pd.read_excel(
        "D:\\研究基地\\Z-数据整理\\一次性数据统计\\管理人信息数据for多策略.xlsx", sheet_name=0, dtype={"净值起始": str})
    # 中性无业绩
    config_df = config_df[config_df['管理人'] != '九坤']
    fund_dict = config_df.set_index('基金名称')['基金代码'].to_dict()
    start_date, end_date = "20190215", '20230928'

    trading_day_list = get_trading_day_list(start_date, end_date, frequency="week")
    nav_df = get_fund_nav_from_sql(start_date, end_date, fund_dict).reindex(trading_day_list)

    adj_nav = []
    for fund_name in fund_dict.keys():
        s_date = config_df[config_df['基金名称'] == fund_name]['净值起始'].values[0]
        tmp = nav_df[[fund_name]].loc[s_date:]
        adj_nav.append(tmp)
    adj_nav = pd.concat(adj_nav, axis=1).sort_index()
    # 添加黑翼的中性
    hy_neu = pd.read_excel(
        "D:\\研究基地\\Z-数据整理\\一次性数据统计\\管理人信息数据for多策略.xlsx", sheet_name=1, dtype={"日期": str})
    hy_neu = hy_neu.set_index('日期')['单位净值'].to_frame('黑翼市场中性5号')
    adj_nav = adj_nav.merge(hy_neu, left_index=True, right_index=True, how='left')
    # 更新config
    new_row = {"管理人": "黑翼", "策略类型": "中性", "基金代码": "SGW463", "基金名称": "黑翼市场中性5号", "净值起始": "20190912"}
    config_df = config_df.append(new_row, ignore_index=True)
    config_df.sort_values(by=['管理人', '策略类型'], inplace=True)
    # 计算
    inc = list(config_df['管理人'].unique())
    return_df = pd.DataFrame(index=adj_nav.index, columns=inc)
    for name in inc:
        idx = config_df[config_df['管理人'] == name]['基金名称'].tolist()
        tmp = adj_nav[idx].pct_change(limit=1).dropna(how='all')
        return_df.loc[:, name] = tmp.mean(axis=1, skipna=False)

    return_df = return_df.dropna(how='all')
    nav_df = (1 + return_df).cumprod()
    year_return = nav_df.reindex(["20191227", "20201231", "20211231", "20221230", "20230928"]).pct_change()

    return year_return


if __name__ == '__main__':
    multi_strategy_portfolio()
    # single_pm_portfolio()