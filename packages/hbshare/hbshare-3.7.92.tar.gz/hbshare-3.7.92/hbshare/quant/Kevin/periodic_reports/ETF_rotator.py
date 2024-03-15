"""
ETF轮动策略尝试
回测区间： 2016.1.1 - 2023.3.1
"""
import datetime
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from WindPy import w

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

w.start()


def save_data_to_csv(start_date, end_date):
    pool_dict = {
                "沪深300ETF": "510300.SH",
                "中证1000ETF": "512100.SH",
                "红利ETF": "510880.SH",
                "创业板ETF": "159915.SZ",
                "纳指ETF": "513100.SH",
                "黄金ETF": "518880.SH"
            }
    # 数据
    save_path = "D:\\etf_strategy_base\\market_info"
    all_data = []
    for key, value in pool_dict.items():
        res = w.wsd(value, "open,high,low,close", start_date, end_date, "PriceAdj=B")
        data = pd.DataFrame(index=res.Fields, columns=res.Times, data=res.Data).T
        data['trade_date'] = data.index
        data['trade_date'] = data['trade_date'].apply(lambda x: x.strftime("%Y%m%d"))
        data.reset_index(drop=True, inplace=True)
        data['etf_name'] = key
        all_data.append(data)
    all_data = pd.concat(all_data).sort_values(by=['trade_date', 'etf_name'])
    dates = sorted(all_data['trade_date'].unique())
    for date in dates:
        all_data.query("trade_date == @date").to_csv(
            os.path.join(save_path, '{}.csv'.format(date)), index=False, encoding="gbk")

def nav_ploter(df, name_list):
    act_df = df.copy()
    act_df['trade_date'] = act_df.index
    act_df['trade_date'] = act_df['trade_date'].apply(lambda x: datetime.datetime.strptime(x, "%Y%m%d"))
    act_df = act_df.set_index('trade_date')
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.set_xlabel('日期')
    ax.set_ylabel('净值')
    for name in name_list + ['轮动策略']:
        if name in name_list:
            act_df[name + '净值'] = act_df[name] / act_df[name].iloc[0]
            ax.plot(act_df[name + '净值'].index, act_df[name + '净值'].values, linestyle='--')
        else:
            ax.plot(act_df[name + '净值'].index, act_df[name + '净值'].values, linestyle='-', color='#FF8124')

    ax.legend(name_list + ['轮动策略'])
    ax.set_title("轮动策略净值曲线对比")
    plt.show()


def calculate_score(srs, N=25):
    if srs.shape[0] < N:
        return np.NaN
    x = np.arange(1, N + 1)
    y = srs.values / srs.values[0]
    lr = LinearRegression().fit(x.reshape(-1, 1), y)
    slope = lr.coef_[0]
    r_squared = lr.score(x.reshape(-1, 1), y)
    score = 10000 * slope * r_squared
    return score


class EtfRotator:
    def __init__(self, start_date, end_date, method="common"):
        self.start_date = start_date
        self.end_date = end_date
        self.method = method

    def run(self):
        # 备选池：沪深300、中证1000、红利、创业板、纳指、黄金
        save_path = "D:\\etf_strategy_base\\market_info"
        listdir = os.listdir(save_path)
        data_list = []
        for filename in listdir:
            data = pd.read_csv(os.path.join(save_path, filename), encoding="gbk", dtype={"trade_date": str})
            data_list.append(data)
        all_data = pd.concat(data_list)
        c2c = pd.pivot_table(all_data, index='trade_date', columns='etf_name', values='CLOSE').sort_index()
        # 动量长度
        N = 20
        s_date = datetime.datetime.strptime(self.start_date, "%Y-%m-%d").strftime("%Y%m%d")
        # name_list = c2c.columns.tolist()
        name_list = ['创业板ETF', '红利ETF', '纳指ETF', '黄金ETF']
        if self.method == "common":
            # 最普通的组合
            for name in name_list:
                c2c['日收益率_' + name] = c2c[name] / c2c[name].shift(1) - 1
                c2c['涨幅_' + name] = c2c[name] / c2c[name].shift(N + 1) - 1
            df = c2c.dropna().loc[s_date:]
            df['信号'] = df[['涨幅_' + v for v in name_list]].idxmax(axis=1).str.replace('涨幅_', '')
            df['信号'] = df['信号'].shift(1)
            df = df.iloc[1:]
            df['轮动策略日收益率'] = df.apply(lambda x: x['日收益率_' + x['信号']], axis=1)
            df.loc[df.index[0], '轮动策略日收益率'] = 0.0
            df['轮动策略净值'] = (1.0 + df['轮动策略日收益率']).cumprod()
            nav_ploter(df, name_list)
        elif self.method == "strength_opt":
            # 强弱排序：RSRS
            N = 25
            for name in name_list:
                c2c['日收益率_' + name] = c2c[name] / c2c[name].shift(1) - 1
                c2c['得分_' + name] = c2c[name].rolling(N).apply(lambda x: calculate_score(x, N))
            # 去掉缺失值
            df = c2c.dropna().loc[s_date:]
            df['信号'] = df[['得分_' + v for v in name_list]].idxmax(axis=1).str.replace('得分_', '')
            df['信号'] = df['信号'].shift(1)
            df = df.iloc[1:]
            df['轮动策略日收益率'] = df.apply(lambda x: x['日收益率_' + x['信号']], axis=1)
            df.loc[df.index[0], '轮动策略日收益率'] = 0.0
            df['轮动策略净值'] = (1.0 + df['轮动策略日收益率']).cumprod()
            nav_ploter(df, name_list)


if __name__ == '__main__':
    # save_data_to_csv("2016-11-08", "2023-03-01")
    EtfRotator("2016-12-30", "2023-03-01", method="common").run()