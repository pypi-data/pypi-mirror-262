"""
线上和本地的风险模型结果校验程序
"""
import pandas as pd
import hbshare as hbs
import matplotlib.pyplot as plt
import numpy as np
import os
from hbshare.quant.Kevin.quant_room.MyUtil.data_loader import fetch_data_batch_hbs
from hbshare.quant.Kevin.rm_associated.config import style_names

path = r'D:\kevin\risk_model_jy\RiskModel\data'
style_name_list = [
    "size", "beta", "momentum", "earnyield", "resvol", "growth", "btop", "leverage", "liquidity", "sizenl"]


def style_factor_check(date, factor_name):
    sql_script = "SELECT * FROM st_ashare.r_st_barra_style_factor where TRADE_DATE = '{}'".format(date)
    style_factor_ol = fetch_data_batch_hbs(sql_script, "alluser")[['ticker'] + style_name_list].set_index('ticker')
    print("线上风格暴露数目：{}".format(style_factor_ol.shape[0]))

    data_path = os.path.join(path, r'zzqz_sw\style_factor')
    style_factor_local = pd.read_csv(
        os.path.join(data_path, '{0}.csv'.format(date)), dtype={"ticker": str}).set_index('ticker')
    print("本地风格暴露数目：{}".format(style_factor_local.shape[0]))

    factor_compare = pd.merge(style_factor_ol[factor_name].to_frame(name=factor_name + '_ol'),
                              style_factor_local[factor_name].to_frame(name=factor_name + '_local'),
                              left_index=True, right_index=True)
    print(factor_compare)


def factor_return_check(date):
    sql_script = "SELECT * FROM st_ashare.r_st_barra_factor_return where TRADE_DATE = '{}'".format(date)
    factor_return_ol = fetch_data_batch_hbs(sql_script, "alluser").set_index('factor_name')['factor_ret']

    data_path = os.path.join(path, r'zzqz_sw\factor_return')
    factor_return_local = pd.read_csv(
        os.path.join(data_path, '{0}.csv'.format(date)), dtype={"ticker": str}).set_index('factor_name')['factor_ret']

    return_compare = pd.merge(factor_return_ol.to_frame('f_ret_ol'), factor_return_local.to_frame('f_ret_local'),
                              left_index=True, right_index=True)
    print(return_compare)


def specific_return_check(date):
    sql_script = "SELECT * FROM st_ashare.r_st_barra_specific_return where TRADE_DATE = '{}'".format(date)
    s_ret_ol = fetch_data_batch_hbs(sql_script, "alluser")
    s_ret_ol['ticker'] = s_ret_ol['ticker'].apply(lambda x: x.zfill(6))
    s_ret_ol = s_ret_ol.set_index('ticker')['s_ret']

    data_path = os.path.join(path, r'zzqz_sw\specific_return')
    s_ret_local = pd.read_csv(
        os.path.join(data_path, '{0}.csv'.format(date)), dtype={"ticker": str}).set_index('ticker')['s_ret']

    s_ret_compare = pd.merge(s_ret_ol.to_frame('s_ret_ol'), s_ret_local.to_frame('s_ret_local'),
                             left_index=True, right_index=True)
    print(s_ret_compare)


def factor_cov_check(date):
    data_path = os.path.join(path, r'zzqz_sw\factor_return')
    factor_return_local = pd.read_csv(
        os.path.join(data_path, '{0}.csv'.format(date)), dtype={"ticker": str}).set_index('factor_name')['factor_ret']
    name_list = [x.lower() for x in factor_return_local.index.tolist()]

    sql_script = "SELECT * FROM st_ashare.r_st_barra_factor_cov where TRADE_DATE = '{}'".format(date)
    factor_cov_ol = fetch_data_batch_hbs(sql_script, "alluser").set_index(
        'factor_name').reindex(factor_return_local.index)[name_list]

    data_path = os.path.join(path, r'zzqz_sw\factor_cov\short')
    factor_cov_local = pd.read_csv(os.path.join(data_path, '{0}.csv'.format(date))).set_index('factor_name')
    factor_cov_local = factor_cov_local.reindex(factor_return_local.index)[factor_return_local.index]

    dm, um = np.linalg.eig(factor_cov_ol)
    dm1, um1 = np.linalg.eig(factor_cov_local)
    dm_df = pd.DataFrame({"dm_ol": dm, "dm_local": dm1})
    dm_df.plot.bar()
    plt.show()


def srisk_check(date):
    sql_script = "SELECT * FROM st_ashare.r_st_barra_s_risk where TRADE_DATE = '{}'".format(date)
    srisk_ol = fetch_data_batch_hbs(sql_script, "alluser").set_index('ticker')['s_ret']

    data_path = os.path.join(path, r'zzqz_sw\srisk\short')
    srisk_local = pd.read_csv(
        os.path.join(data_path, '{0}.csv'.format(date)), dtype={"ticker": str}).set_index('ticker')

    srisk_compare = pd.merge(srisk_ol.to_frame('srisk_ol'), srisk_local, left_index=True, right_index=True)
    print(srisk_compare)


if __name__ == '__main__':
    trade_date = '20231215'
    style_factor_check(trade_date, 'momentum')
    # factor_return_check(trade_date)
    # specific_return_check(trade_date)
    # factor_cov_check(trade_date)
    # srisk_check(trade_date)