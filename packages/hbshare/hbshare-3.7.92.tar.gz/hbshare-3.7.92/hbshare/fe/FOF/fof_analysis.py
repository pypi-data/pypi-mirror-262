import datetime
import pandas as pd
import numpy as np
from hbshare.fe.XZ import db_engine
from hbshare.fe.XZ import functionality
from scipy import interpolate
import  os

util=functionality.Untils()
hbdb=db_engine.HBDB()
plot=functionality.Plot(1000,600)
localdb=db_engine.PrvFunDB().engine


def rolling_rank(array):
    s = pd.Series(array)
    return s.rank(ascending=True).iloc[-1] / len(array)

def monotonic(L):
        return all(x > y for x, y in zip(L, L[1:])) or all(x < y for x, y in zip(L, L[1:]))

def find_weight_change_point(weight_history,col_list,index_list,monotonic_lenght=20):

    weight_target_df = []

    def trade_stat(q_line_date, weight_history):

        tempdf = pd.DataFrame()

        if (len(q_line_date) > 0):
            q_line_date = \
                [weight_history['日期'].iloc[0]] \
                + q_line_date['日期'].tolist() \
                + [weight_history['日期'].iloc[-1]]

            sql = """select zqdm,jyrq,spjg from st_market.t_st_zs_hqql 
            where jyrq in ({0}) and zqdm in ({1})""" \
                .format(util.list_sql_condition(q_line_date),util.list_sql_condition(index_list))

            mu_index_ret = hbdb.db2df(sql, db='alluser').pivot_table('spjg', 'jyrq', 'zqdm')
            mu_index_ret.index = mu_index_ret.index.astype(str)

            for i in range(len(q_line_date) - 1):
                remove_data = int(monotonic_lenght / 2)

                tempdf.loc[q_line_date[i] + " to " + q_line_date[i + 1], '权重均值'] = \
                    weight_history[(weight_history['日期'] >= q_line_date[i])
                                   & (weight_history['日期'] <= q_line_date[i + 1])][col][remove_data:-remove_data].mean()
                tempdf.loc[q_line_date[i] + " to " + q_line_date[i + 1], '权重中值'] = \
                    weight_history[(weight_history['日期'] >= q_line_date[i])
                                   & (weight_history['日期'] <= q_line_date[i + 1])][col][
                    remove_data:-remove_data].median()
                tempdf.loc[q_line_date[i] + " to " + q_line_date[i + 1], '偏离均值'] = \
                    weight_history[(weight_history['日期'] >= q_line_date[i])
                                   & (weight_history['日期'] <= q_line_date[i + 1])][col + "_30div"][
                    remove_data:-remove_data].mean()
                tempdf.loc[q_line_date[i] + " to " + q_line_date[i + 1], '偏离最大'] = \
                    weight_history[(weight_history['日期'] >= q_line_date[i])
                                   & (weight_history['日期'] <= q_line_date[i + 1])][col + "_30div"][
                    remove_data:-remove_data].max()

                if(q_line_date[i] in mu_index_ret.index and q_line_date[i+1] in mu_index_ret.index ):

                    for index_name in index_list:
                        tempdf.loc[q_line_date[i] + " to " + q_line_date[i + 1], index_name] = \
                            (mu_index_ret.loc[q_line_date[i + 1]][index_name] /
                             mu_index_ret.loc[q_line_date[i]][index_name] - 1)


        else:

            tempdf.loc['全期', '权重均值'] = weight_history[col].mean()
            tempdf.loc['全期', '权重中值'] = weight_history[col].median()

            tempdf.loc['全期', '偏离均值'] = weight_history[col + "_30div"][30:-30].mean()
            tempdf.loc['全期', '偏离最大'] = weight_history[col + "_30div"][30:-30].max()

        return tempdf

    for col in col_list:

        weight_history[col + "_30MA"] = weight_history[col].rolling(30).mean()
        weight_history[col + "_30div"] = abs(weight_history[col] - weight_history[col + "_30MA"])
        weight_history[col + 'Ndays_monotonic'] =\
            weight_history[col + "_30div"].rolling(monotonic_lenght).apply(
            monotonic)
        weight_history[col + 'Ndays_monotonic_T-1'] = \
            [np.nan] + weight_history[col + 'Ndays_monotonic'][0:-1].tolist()
        weight_history.loc[(weight_history[col + 'Ndays_monotonic'] == 1) & (
                weight_history[col + 'Ndays_monotonic_T-1'] == 0), col + '_q_line'] = True

        weight_history[col + '_q_line'] = weight_history[col + '_q_line'].iloc[monotonic_lenght:].tolist() + [
            np.nan] * monotonic_lenght

        q_line_date = weight_history[weight_history[col + '_q_line'] == True]

        tempdf = trade_stat(q_line_date, weight_history)
        less_than1_diff = tempdf[tempdf['权重中值'].diff().abs() <= 0.02].index
        while len(less_than1_diff) > 0:
            for date_line in less_than1_diff:
                q_line_date = q_line_date[q_line_date['日期'] != date_line[0:8]]
            tempdf = trade_stat(q_line_date, weight_history)
            less_than1_diff = tempdf[tempdf['权重中值'].diff().abs() <= 0.02].index

        tempdf = tempdf.reset_index(drop=False).rename(columns={'index': '持续日期'})
        tempdf.index = len(tempdf) * [col]
        weight_target_df.append(tempdf)

    weight_target_df = pd.concat(weight_target_df, axis=0)

    return  weight_target_df

def temp_valuation_table_analysis(product,end_date,start_date=None,get_nav_from_gzb=False):


    if (start_date is None):
        start_date = '0'

    file_name_list = os.listdir(r"E:\FOF分析\{0}\估值表"
                            .format(product))



    for name in file_name_list:
        solved_gzb = []
        exist_date_list = []
        jjjzc = []
        ljjz = []
        solved_gzb_gl = []
        print(name) #S21582_新方程对冲精选H1号基金20210604.xls
        gzb = pd.read_excel(r"E:\FOF分析\{0}\估值表\{1}"
                            .format(product, name))

        # deal with H1 special valuation table
        if (len((gzb.iloc[1][0]).split('估值日期')) > 1):
            gzb = gzb.iloc[1:-3]
            data = (gzb.iloc[0][0]).split('估值日期')[1].replace('-', '').replace(':', '').replace('：', '').replace(' ',
                                                                                                                    '').replace(
                '_', '')
            gzb = gzb.iloc[1:]
            gzb.columns = gzb.iloc[0]
        else:
            data = gzb.columns[0].split('_')[2].replace('-', '').replace(':', '').replace('：', '').replace(' ',
                                                                                                           '').replace(
                '_', '')
            gzb.columns = gzb.iloc[0]

        if (data < start_date):
            continue
        if (data > end_date):
            continue

        gzb.columns = [str(x).replace(' ', '') for x in gzb.columns.tolist()]
        gzb.rename(columns={'行情收市价': '市价'}, inplace=True)
        if (get_nav_from_gzb):
            temp_jjjzc = gzb[gzb['科目代码'] == '基金资产净值:']['市值'].iloc[0]
            temp_ljjz = gzb[gzb['科目代码'] == '累计单位净值:']['市值'].iloc[0]
        else:
            temp_ljjz = []
            temp_jjjzc = []

        gzb_gl = gzb.copy()

        gzb = gzb[((gzb['科目代码'].astype(str).str.startswith('11090501'))
                   | (gzb['科目代码'].astype(str).str.startswith('11090201'))
                   | (gzb['科目代码'].astype(str).str.startswith('11050201'))
                   | (gzb['科目代码'].astype(str).str.startswith('11050301')) | (
                       gzb['科目代码'].astype(str).str.startswith('11050401')) |
                   (gzb['科目代码'].astype(str).str.startswith('11090601'))
                   | (gzb['科目代码'].astype(str) == '1203') | (gzb['科目代码'].astype(str).str.startswith('11090101'))
                   | (gzb['科目代码'].astype(str) == '1002'))
                  &
                  ((gzb['科目代码'].astype(str) != '11090201')
                   & (gzb['科目代码'].astype(str) != '11090501')
                   & (gzb['科目代码'].astype(str) != '11050201')
                   & (gzb['科目代码'].astype(str) != '11050301')
                   & (gzb['科目代码'].astype(str) != '11050401')
                   & (gzb['科目代码'].astype(str) != '11090601')
                   & (gzb['科目代码'].astype(str) != '11090101'))][['科目代码', '科目名称', '数量'
            , '单位成本', '成本占净值%', '市价', '市值', '市值占净值%', '估值增值']]

        if (len(gzb_gl[((gzb_gl['科目代码'].astype(str).str.startswith('12032006'))
                        | (gzb_gl['科目代码'].astype(str).str.startswith('12030508')))
                       &
                       ((gzb_gl['科目代码'].astype(str) != '12032006')
                        & (gzb_gl['科目代码'].astype(str) != '12030508'))]) > 0):

            gzb_gl = gzb_gl[((gzb_gl['科目代码'].astype(str).str.startswith('12032006'))
                             | (gzb_gl['科目代码'].astype(str).str.startswith('12030508')))
                            &
                            ((gzb_gl['科目代码'].astype(str) != '12032006')
                             & (gzb_gl['科目代码'].astype(str) != '12030508'))][['科目代码', '科目名称', '数量'
                , '单位成本', '成本占净值%', '市价', '市值', '市值占净值%', '估值增值']]

        else:

            gzb_gl = gzb_gl[((gzb_gl['科目代码'].astype(str).str.startswith('12032006'))
                             | (gzb_gl['科目代码'].astype(str).str.startswith('12030508')))
            ][['科目代码', '科目名称', '数量'
                , '单位成本', '成本占净值%', '市价', '市值', '市值占净值%', '估值增值']]

        if ('1203' not in gzb['科目代码'].tolist()):
            gzb.loc[gzb.index[-1] + 1] = ['1203', '应收股利'] + [0] * 7

        gzb['科目代码'] = gzb['科目代码'].str[-6:]
        gzb['date'] = data
        gzb_gl['date'] = data
        if (data not in exist_date_list):
            exist_date_list.append(data)
            solved_gzb.append(gzb)
            solved_gzb_gl.append(gzb_gl)
            jjjzc.append(temp_jjjzc)
            ljjz.append(temp_ljjz)

        hold_df = pd.concat(solved_gzb, axis=0)
        # solved_gzb_gl = pd.concat(solved_gzb_gl, axis=0)

        # transfor wrong jjdm to right jjdm 和聚平台证券投资基金

        orginal_code = ['1ZLZG3', '1BYTZ2', '1AAAA7', '1BXZG2', '1BLKS1', '2QHGH1', '1HYZG5', '1HFL32', '2HFLH1',
                        '2JZTZ1', '1JZTZ4', '1LPTZ2', '2LPTZ4', '1LSTZ9', '3MXTZ1', '1MXTZ8', '3MHTZ3', '1MHTZC', '1MHTZJ',
                        '1MHTZB', '1MHTZE', '1QLTZ3', '1QLTZ5', '1QLT11', '2RQZG1', '3RPTZ2', '1SGD12', '1XMZC2', '1XMZC1',
                        '1XKTZA', '1XKTZ5', '3XKTZ2', '1YFT12', '3ZHTZ1', 'SH3322', '1GYZC1', 'JZ510B', '2CQRY1',
                        'GT498A', '2SGDZ1', 'NT762C', 'QS592B', 'NY736C', '4XLZC2', 'S9649B', '3LRZG1', '2CQZG1', 'LS0002',
                        'LS0003',
                        'LS0004', 'LS0013', 'LS0017', 'LS0007', 'LS0008', 'LS0009', 'LS0010', 'LS0014', 'LS0012', 'LC078A',
                        'QB109B',
                        'X5605B', '1WKTZ2', 'ET353B', 'GH832B', 'TY576A', 'VZ894A', 'B1666A', '2YZTZ1', '2WDZG1', '270004',
                        '519019',
                        'FLWJN1', 'xfcxf2', 'GYLW1A', 'SFCHCA', 'YTCZN7', 'GFJZ12', '1HCHF1', '66391B', '246040', '23582A',
                        'HBCT2A',
                        'HXQJ1F', 'Y4405C', '1AADH2', '3HYZG1', '1AAPP8', 'ABE53B', 'XX346B', 'ACM31B', 'NP315B', 'XB480B',
                        'R0001B']
        maped_code = ['SLP211', 'SNZ338', 'SQS281', 'STR792', 'SED697', 'SY0256', 'S83614', 'SNX384', 'SLK497',
                      'SNE372', 'SJD015', 'SNP300', 'SQJ816', 'SER492', 'SJA462', 'SGP290', 'SR0001', 'SM8148', 'SLF242',
                      'SEF092', 'SCY785', 'SGC224', 'SGY379', 'SNL641', 'SJZ021', 'SX5605', 'SGU946', 'SEU546', 'SEZ550',
                      'SSE288', 'SNV206', 'SSM840', 'SNP647', 'SQS592', 'P20830', 'SY8350', 'T04393', 'SNR623',
                      'SGT498', 'SGT498', 'SNT762', 'SQS592', 'SNY736', 'SNY736', 'SS9649', 'SS9649', 'SQK761', 'SJZ510',
                      'SQK761',
                      'SQA948', 'SQF770', 'SNY736', 'SK6332', 'SVZ894', 'STY576', 'SEM863', 'SCL316', 'SXD663', 'SLC078',
                      'SQB109',
                      'SX5605', 'S33474', 'SET353', 'SGH832', 'STY576', 'SVZ894', 'SB1666', 'SGT338', 'SNT164', '270014',
                      '017772',
                      'P02494', 'P12095', 'SJ5324', 'S63506', 'SS0299', 'S62866', 'SQG573', 'S66391', 'M06228', 'S23582',
                      'M06228',
                      'SH5035', 'SY4405', 'SQB109', 'T04393', 'SQL839', 'P51276', 'P51276', 'SQF770', 'SNP315', 'SXB480',
                      'SR0001']
        jjdm_map = pd.DataFrame()
        jjdm_map['科目代码'] = orginal_code
        jjdm_map['映射代码'] = maped_code
        hold_df = pd.merge(hold_df, jjdm_map, how='left', on='科目代码')
        hold_df.loc[hold_df['映射代码'].notnull(), '科目代码'] = hold_df[hold_df['映射代码'].notnull()]['映射代码']
        hold_df.drop('映射代码', axis=1, inplace=True)

        jjdm_list = hold_df['科目代码'].unique()
        # get prv list and mutual list
        sql = "select jjdm,cpfl,jjfl,ejfl from st_fund.t_st_gm_jjxx where jjdm in ({}) and cpfl='2'" \
            .format(util.list_sql_condition(jjdm_list))
        mutual_fund = hbdb.db2df(sql, db='funduser')

        sql = "select jjdm,cpfl,jjfl,ejfl from st_hedge.t_st_jjxx where jjdm in ({}) and cpfl='4'" \
            .format(util.list_sql_condition(jjdm_list))
        prv_fund = hbdb.db2df(sql, db='highuser')

        fund_features = pd.concat([mutual_fund, prv_fund], axis=0)
        hold_df = pd.merge(hold_df, fund_features, how='left',
                           left_on='科目代码', right_on='jjdm').drop('jjdm', axis=1).rename(columns={'科目代码': 'jjdm',
                                                                                                     '科目名称': 'jjjc',
                                                                                                     '数量': 'quant',
                                                                                                     '单位成本': 'cbprice',
                                                                                                     '市价': 'jjjz',
                                                                                                     '市值': 'mv',
                                                                                                     '成本占净值%': 'cb_w',
                                                                                                     '市值占净值%': 'weight',
                                                                                                     '估值增值': 'value_increased', })

        # get the wrong jjdm list
        know_jjdm=hold_df[['jjdm','jjjc']].drop_duplicates('jjdm')
        wrong_jjdm = hold_df[hold_df['cpfl'].isnull()][['jjdm','jjjc']].drop_duplicates('jjdm')
        wrong_jjdm = wrong_jjdm[ (wrong_jjdm['jjdm'] != '1203') & (wrong_jjdm['jjdm'] != '1002')]
        if (len(wrong_jjdm) > 0):
            wrong_jjdm['科目名称_t'] = wrong_jjdm['jjjc']
            wrong_jjdm['科目名称_t'] = wrong_jjdm['科目名称_t'].str.replace('A类', 'A')
            wrong_jjdm['科目名称_t'] = wrong_jjdm['科目名称_t'].str.replace('B类', 'B')
            wrong_jjdm['科目名称_t'] = wrong_jjdm['科目名称_t'].str.replace('C类', 'C')
            wrong_jjdm['科目名称_t'] = wrong_jjdm['科目名称_t'].str.replace('A级', 'A')
            wrong_jjdm['科目名称_t'] = wrong_jjdm['科目名称_t'].str.replace('B级', 'B')
            wrong_jjdm['科目名称_t'] = wrong_jjdm['科目名称_t'].str.replace('C级', 'C')
            if (len(wrong_jjdm) == 1):
                sql = "select jjjc,jjmc from st_hedge.t_st_jjxx where jjmc in ('{}')" \
                    .format(wrong_jjdm['科目名称_t'].tolist()[0])
            else:
                sql = "select jjjc,jjmc,jjdm as new_jjdm from st_hedge.t_st_jjxx where jjmc in {}".format(
                    tuple(wrong_jjdm['科目名称_t'].tolist()))
            right_jjdm = hbdb.db2df(sql, db='highuser').drop_duplicates()
            wrong_jjdm = pd.merge(wrong_jjdm.drop(['jjdm', 'jjjc'], axis=1), right_jjdm,
                                  left_on='科目名称_t', right_on='jjmc', how='left')
            wrong_jjdm = \
                pd.merge(wrong_jjdm, know_jjdm, how='left',
                         left_on='jjmc',right_on='jjjc').drop('jjjc_y',axis=1).rename(columns={'jjjc_x':'jjjc'})



            if('new_jjdm' in wrong_jjdm.columns.tolist()):

                if (len(wrong_jjdm[wrong_jjdm['new_jjdm'].isnull()]) > 0):
                    wrong_jjdm['jjjc'] = wrong_jjdm['jjjc'].str.replace('A', '')
                    wrong_jjdm['jjjc'] = wrong_jjdm['jjjc'].str.replace('B', '')
                    wrong_jjdm['jjjc'] = wrong_jjdm['jjjc'].str.replace('C', '')
                    wrong_jjdm['jjjc'] = wrong_jjdm['jjjc'].str.replace('级', '')
                    wrong_jjdm['jjjc'] = wrong_jjdm['jjjc'].str.replace('类', '')
                    wrong_jjdm = pd.merge(wrong_jjdm, know_jjdm, how='left', left_on='jjjc', right_on='投资基金简称')
                    wrong_jjdm.loc[wrong_jjdm['投资基金代码_x'].isnull(), '投资基金代码_x'] = \
                        wrong_jjdm.loc[wrong_jjdm['投资基金代码_x'].isnull()]['投资基金代码_y']
                    wrong_jjdm.rename(columns={'投资基金代码_x': '投资基金代码'}, inplace=True)

                hold_df = pd.merge(hold_df, wrong_jjdm[['jjdm', 'new_jjdm']], how='left', on='jjdm')
                hold_df.loc[hold_df['new_jjdm'].notnull(), 'jjdm'] = hold_df[hold_df['new_jjdm'].notnull()][
                    'new_jjdm']
                hold_df.drop('new_jjdm', axis=1, inplace=True)

            jjdm_list = hold_df['jjdm'].unique()
            # get prv list and mutual list
            sql = "select jjdm,cpfl,jjfl,ejfl from st_fund.t_st_gm_jjxx where jjdm in ({}) and cpfl='2'" \
                .format(util.list_sql_condition(jjdm_list))
            mutual_fund = hbdb.db2df(sql, db='funduser')

            sql = "select jjdm,cpfl,jjfl,ejfl from st_hedge.t_st_jjxx where jjdm in ({}) and cpfl='4'" \
                .format(util.list_sql_condition(jjdm_list))
            prv_fund = hbdb.db2df(sql, db='highuser')

            fund_features = pd.concat([mutual_fund, prv_fund], axis=0)
            hold_df = pd.merge(hold_df.drop(['ejfl','jjfl','cpfl'],axis=1), fund_features, how='left',
                               on='jjdm').rename(
                columns={'科目代码': 'jjdm',
                         '科目名称': 'jjjc',
                         '数量': 'quant',
                         '单位成本': 'cbprice',
                         '市价': 'jjjz',
                         '市值': 'mv',
                         '成本占净值%': 'cb_w',
                         '市值占净值%': 'weight',
                         '估值增值': 'value_increased', })


        # if (len(wrong_jjdm) > 0):
        #     print("the following jjdm need to be mapped mannually ")
        #     print(wrong_jjdm[['科目代码', '科目名称', 'jjjc']])
        #     raise Exception

        # deal with two recoreds for one ticker at certain date
        def remvoe_duplicate_ticker(hold_df):
            error_list = hold_df.groupby(['jjdm', 'date'])['jjjc'].count()[
                hold_df.groupby(['jjdm', 'date'])['jjjc'].count() >= 2].reset_index()['jjdm'].unique().tolist()
            if (len(error_list) > 0):
                error_list = hold_df[hold_df['jjdm'].isin(error_list)]
                error_list[['quant_x', 'value_increased_x', 'mv_x']] = error_list[['quant', 'value_increased', 'mv']].fillna(0)
                error_list = error_list.groupby(['jjdm', 'date']).sum()[['quant_x', 'value_increased_x', 'mv_x']].reset_index()

                hold_df = hold_df.drop_duplicates(['jjdm', 'date'])

                hold_df = pd.merge(hold_df, error_list, how='left', on=['jjdm', 'date'])
                hold_df.loc[hold_df['quant_x'].notnull(), 'quant'] = hold_df.loc[hold_df['quant_x'].notnull()]['quant_x']
                hold_df.loc[hold_df['value_increased_x'].notnull(), 'value_increased'] = \
                hold_df.loc[hold_df['value_increased_x'].notnull()]['value_increased_x']
                hold_df.loc[hold_df['quant_x'].notnull(), 'quant'] = hold_df.loc[hold_df['quant_x'].notnull()]['quant_x']
                hold_df.loc[hold_df['mv_x'].notnull(), 'mv'] = hold_df.loc[hold_df['mv_x'].notnull()]['mv_x']
                hold_df.drop(['quant_x', 'value_increased_x', 'mv_x'], axis=1, inplace=True)

            return hold_df


        hold_df = remvoe_duplicate_ticker(hold_df)



        hold_df.loc[(hold_df['cpfl'].isnull()) & (hold_df['jjdm'] != '000nan'), 'cpfl'] = 4
        hold_df.loc[hold_df['cpfl']==4,'cpfl']='私募基金'
        hold_df.loc[hold_df['cpfl'] == 2, 'cpfl'] = '公募基金'

        quant_pool_in = \
        pd.read_excel(r"E:\FOF分析\量化二级映射表.xlsx"
                      )[[ '基金代码', '二级策略']].drop_duplicates('基金代码')
        hold_df=pd.merge(hold_df,quant_pool_in[['基金代码','二级策略']]
                         ,how='left',left_on='jjdm',right_on='基金代码')

        hold_df['jjdm'] = ["'" + str(x) for x in hold_df['jjdm']]
        hold_df.sort_values(['date', 'jjdm']).to_excel(r"E:\FOF分析\{0}\基金持仓数据_{1}.xlsx".format(product,name.split(".")[0]), index=False)

        print(name + ' Done ')

def temp_holding_file_analysis():

    file_name_list = os.listdir(r"E:\FOF分析\一堆量化\持仓解析文件")

    all_hold=[]

    for name in file_name_list:
        print(name) #S21582_新方程对冲精选H1号基金20210604.xls
        hold = pd.read_excel(r"E:\FOF分析\一堆量化\持仓解析文件\{0}"
                            .format(name))
        hold['FOF名称']=name
        all_hold.append(hold)

    pd.concat(all_hold,axis=0).to_excel(r"E:\FOF分析\一堆量化\持仓解析文件\全部持仓文件.xlsx")


def stress_test(end_date, fof_ret,fof_ej_ret):
    sql = "select zqdm,tjyf,hb1y from st_market.t_st_zs_yhb where zqdm in ('881001','H11001') and tjyf<='{}' and tjyf>='201001'".format(
        str(end_date)[0:6])
    month_ret = hbdb.db2df(sql, db='alluser').pivot_table('hb1y', 'tjyf', 'zqdm')

    quarter_ret = month_ret.copy()
    quarter_ret = (quarter_ret / 100 + 1).cumprod()
    quarter_ret['month'] = quarter_ret.index.astype(str).str[4:6]
    quarter_ret.loc[quarter_ret['month'] == '03', 'quarter'] = 'Q1'
    quarter_ret.loc[quarter_ret['month'] == '06', 'quarter'] = 'Q2'
    quarter_ret.loc[quarter_ret['month'] == '09', 'quarter'] = 'Q3'
    quarter_ret.loc[quarter_ret['month'] == '12', 'quarter'] = 'Q4'
    quarter_ret = quarter_ret[quarter_ret['quarter'].notnull()]
    quarter_ret.drop(['month', 'quarter'], axis=1, inplace=True)
    quarter_ret = quarter_ret.pct_change()

    def get_month_quarter_for_ret(fof_ret):
        fof_ret=(fof_ret+1).cumprod()
        fof_ret['ym'] = fof_ret.index.astype(str).str[0:6]
        fof_ret_month=fof_ret.drop_duplicates('ym',keep='last')


        fof_ret_month['month']=fof_ret_month['ym'].astype(str).str[4:6]
        fof_ret_month.loc[fof_ret_month['month'] == '03', 'quarter'] = 'Q1'
        fof_ret_month.loc[fof_ret_month['month'] == '06', 'quarter'] = 'Q2'
        fof_ret_month.loc[fof_ret_month['month'] == '09', 'quarter'] = 'Q3'
        fof_ret_month.loc[fof_ret_month['month'] == '12', 'quarter'] = 'Q4'
        fof_ret_q=fof_ret_month[fof_ret_month['quarter'].notnull()]

        fof_ret_month=fof_ret_month.set_index('ym').drop(['quarter','month'],axis=1).pct_change()
        fof_ret_q=fof_ret_q.set_index('ym').drop(['quarter','month'],axis=1).pct_change()

        return fof_ret_month,fof_ret_q

    fof_ret_month, fof_ret_q=get_month_quarter_for_ret(fof_ret)
    fof_ej_ret_month, fof_ej_ret_q=get_month_quarter_for_ret(fof_ej_ret)

    fof_ret_month=pd.merge(fof_ret_month,fof_ej_ret_month,how='left',on='ym')
    fof_ret_q=pd.merge(fof_ret_q,fof_ej_ret_q,how='left',on='ym')


    month_ret.index=month_ret.index.astype(str)
    quarter_ret.index = quarter_ret.index.astype(str)


    #find stress month

    month_threshield=month_ret.quantile(0.1)
    quarter_threshield = quarter_ret.quantile(0.1)
    month_ret=month_ret.loc[fof_ret_month.index.min():]
    quarter_ret=quarter_ret.loc[fof_ret_q.index.min():]


    month_stock_stress_perfromance=fof_ret_month.loc[month_ret[month_ret['881001']<=month_threshield['881001']].index].mean()
    month_bond_stress_perfromance=fof_ret_month.loc[month_ret[month_ret['H11001']<=month_threshield['H11001']].index].mean()
    quarter_stock_stress_perfromance=fof_ret_q.loc[quarter_ret[quarter_ret['881001']<=quarter_threshield['881001']].index].mean()
    quarter_bond_stress_perfromance=fof_ret_q.loc[quarter_ret[quarter_ret['H11001']<=quarter_threshield['H11001']].index].mean()


    FOF_stress_test=pd.concat([month_stock_stress_perfromance.to_frame('权益压力月资产平均收益'),
                               month_bond_stress_perfromance.to_frame('债券压力月资产平均收益'),
                               quarter_stock_stress_perfromance.to_frame('权益压力季资产平均收益'),
                               quarter_bond_stress_perfromance.to_frame('债券压力季资产平均收益')],axis=1)

    return  FOF_stress_test


def get_super_asset_index_stats(latest_holding,latest_date):

    sql="select jyrq,spjg,zsdm from st_hedge.t_st_sm_zhmzs where zsdm in ('HB0011','HB0018','HB1001','HB1002') and jyrq <='{}'".format(latest_date)
    data=hbdb.db2df(sql,db='highuser').pivot_table('spjg','jyrq','zsdm')


    sql="select spjg ,jyrq,zqdm from st_market.t_st_zs_hq where zqdm in ('H11001','930950') and jyrq>='20070101' and jyrq<='{}' ".format(latest_date)
    mutual_index=hbdb.db2df(sql,db='alluser').pivot_table('spjg','jyrq','zqdm')
    mutual_index.index=mutual_index.index.astype(str)
    data=pd.merge(data,mutual_index,how='left',on='jyrq')


    sql=("select jjdm,hb1z,tjrq from st_fund.t_st_gm_zhb where jjdm in {0} and tjrq<='{1}' and hb1z!=99999"
         .format(tuple(latest_holding[latest_holding['cpfl']=='公募基金']['jjdm'].tolist()),latest_date))
    mutual_nav=hbdb.db2df(sql,db='funduser')
    if(len(mutual_nav)>0):
        mutual_nav['tjrq']=mutual_nav['tjrq'].astype(str)
        mutual_nav =mutual_nav.pivot_table('hb1z', 'tjrq', 'jjdm')
    else:
        mutual_nav=pd.DataFrame(columns=['tjrq'])

    sql=("select jjdm,hb1z,tjrq from st_hedge.t_st_sm_zhb where jjdm in {0} and tjrq<='{1}' and hb1z!=99999"
         .format(tuple(latest_holding[latest_holding['cpfl']=='私募基金']['jjdm'].tolist()),latest_date))
    prv_nav=hbdb.db2df(sql,db='highuser')
    if(len(prv_nav)>0):
        prv_nav =prv_nav.pivot_table('hb1z','tjrq','jjdm')
    else:
        prv_nav=pd.DataFrame(columns=['tjrq'])

    sql=("select jjdm,hb1z,tjrq from st_fixed.t_st_gs_zhb where jjdm in {0} and tjrq<='{1}' and hb1z!=99999 "
         .format(tuple(latest_holding[latest_holding['cpfl']=='私募基金']['jjdm'].tolist()),latest_date))
    fix_income_nav=hbdb.db2df(sql,db='highuser')
    if(len(fix_income_nav)>0):
        fix_income_nav =fix_income_nav.pivot_table('hb1z','tjrq','jjdm')
    else:
        fix_income_nav=pd.DataFrame(columns=['tjrq'])

    hold_nav=pd.merge(prv_nav,mutual_nav,how='left'
                      ,on='tjrq')
    hold_nav=pd.merge(hold_nav,fix_income_nav,how='left'
                      ,on='tjrq')
    hold_nav=hold_nav.iloc[-156:].set_index('tjrq')

    latest_holding=pd.merge(latest_holding,
                            latest_holding.groupby('yjcl')['weight'].sum().to_frame('total_w'),
                            how='left',on='yjcl')
    latest_holding['w']=latest_holding['weight']/latest_holding['total_w']
    latest_holding=pd.merge(latest_holding,
                            latest_holding.groupby('ejfl')['weight'].sum().to_frame('total_w2'),
                            how='left',on='ejfl')
    latest_holding['w2']=latest_holding['weight']/latest_holding['total_w2']

    latest_holding.set_index('jjdm',inplace=True)

    hold_asset_data=pd.DataFrame()
    hold_ef_asset_data=pd.DataFrame()
    for asset_type in latest_holding['yjcl'].unique().tolist():

        jjdm_list=latest_holding[(latest_holding['yjcl'] == asset_type)
                       &(latest_holding.index.isin(hold_nav.columns.tolist()))].index.tolist()
        hold_asset_data[asset_type]=(
            hold_nav[jjdm_list].fillna(0).dot(latest_holding.loc[jjdm_list]['w'].fillna(0)))

    for asset_type in ['公募偏股', '量化多头', '主观多头']:

        jjdm_list=latest_holding[(latest_holding['ejfl'] == asset_type)
                       &(latest_holding.index.isin(hold_nav.columns.tolist()))].index.tolist()
        if(len(jjdm_list)>0):
            hold_ef_asset_data[asset_type]=(
                hold_nav[jjdm_list].fillna(0).dot(latest_holding.loc[jjdm_list]['w2'].fillna(0)))

    hold_asset_data=hold_asset_data / 100
    hold_ef_asset_data=hold_ef_asset_data / 100
    data.columns=['进攻性资产', 'CTA','主观多头','量化多头','公募偏股','稳健性资产']

    fof_stress_test=stress_test(latest_date, hold_asset_data,hold_ef_asset_data)

    def rolling_pct_change(array):
        s = pd.Series(array)
        return s.iloc[-1] / s.iloc[0] - 1
    def calculate_necessary_stats(data):

        #calculate var

        rolling_156_ret=data.rolling(52).apply(rolling_pct_change)
        rolling_156_ret=rolling_156_ret[rolling_156_ret['CTA'].notnull()]
        asset_VAR=rolling_156_ret.rolling(156).quantile(0.05)
        asset_VAR=asset_VAR[asset_VAR['CTA'].notnull()]

        #calculate corr
        data=data.pct_change()
        data = data[data['CTA'].notnull()]

        tempdata=data.rolling(156).corr().reset_index()
        tempdata=tempdata.iloc[156 * 3:]

        corr=pd.DataFrame()
        corr['date']=tempdata['jyrq'].unique().tolist()
        corr['进攻性资产-CTA']=tempdata[tempdata['level_1']=='CTA']['进攻性资产'].tolist()
        corr['进攻性资产-稳健性资产']=tempdata[tempdata['level_1']=='稳健性资产']['进攻性资产'].tolist()
        corr['CTA-稳健性资产']=tempdata[tempdata['level_1']=='稳健性资产']['CTA'].tolist()
        corr['公募偏股-主观多头']=tempdata[tempdata['level_1']=='公募偏股']['主观多头'].tolist()
        corr['主观多头-量化多头']=tempdata[tempdata['level_1']=='主观多头']['量化多头'].tolist()
        corr['公募偏股-量化多头']=tempdata[tempdata['level_1']=='公募偏股']['量化多头'].tolist()


        #calculate_vol
        tempdata=data.rolling(156).std()*np.sqrt(52)
        asset_vol=tempdata.iloc[156 :]

        #calculate_annually_ret

        def rolling_cumprod(arr):

            return np.power(arr.cumprod().iloc[-1],52/len(arr))-1

        tempdata=(data + 1).rolling(52*3).apply(rolling_cumprod)
        asset_annually_ret=tempdata.iloc[156 :]
        corr.set_index('date',inplace=True)

        return asset_annually_ret,asset_vol,corr,asset_VAR

    asset_annually_ret, asset_vol, asset_corr, asset_VAR=calculate_necessary_stats(data)

    hold_asset_data=pd.merge(hold_asset_data,hold_ef_asset_data,how='left',on='tjrq')

    fof_annually_ret=(
            np.power( (hold_asset_data + 1).cumprod().iloc[-1] ,52/len(hold_asset_data))- 1)

    fof_vol=hold_asset_data.std()*np.sqrt(52)

    fof_corr=pd.DataFrame()
    fof_corr['进攻性资产-CTA']=[hold_asset_data.corr()['进攻性资产'].loc['CTA']]
    fof_corr['进攻性资产-稳健性资产']=[hold_asset_data.corr()['进攻性资产'].loc['稳健性资产']]
    fof_corr['CTA-稳健性资产']=[hold_asset_data.corr()['CTA'].loc['稳健性资产']]
    fof_corr['公募偏股-主观多头']=[hold_asset_data.corr()['公募偏股'].loc['主观多头']]
    fof_corr['主观多头-量化多头']=[hold_asset_data.corr()['主观多头'].loc['量化多头']]
    fof_corr['公募偏股-量化多头']=[hold_asset_data.corr()['公募偏股'].loc['量化多头']]

    rolling_156_ret = (hold_asset_data+1).cumprod().rolling(52).apply(rolling_pct_change)
    rolling_156_ret = rolling_156_ret[rolling_156_ret['CTA'].notnull()]
    fof_VAR = rolling_156_ret.quantile(0.05)

    asset_annually_ret.columns = ["基准：" + x for x in asset_annually_ret.columns]
    asset_vol.columns = ["基准：" + x for x in asset_vol.columns]
    asset_corr.columns = ["基准：" + x for x in asset_corr.columns]
    asset_VAR.columns = ["基准：" + x for x in asset_VAR.columns]

    asset_annually_ret.loc[asset_annually_ret.index[-1],
    ['FOF：进攻性资产', 'FOF：稳健性资产','FOF：CTA', 'FOF：公募偏股','FOF：量化多头','FOF：主观多头']] = fof_annually_ret.values.tolist()
    asset_corr.loc[asset_corr.index[-1],
    ['FOF：进攻性资产-CTA', 'FOF：进攻性资产-稳健性资产', 'FOF：CTA-稳健性资产'
        ,'FOF：公募偏股-主观多头','FOF：主观多头-量化多头','FOF：公募偏股-量化多头']] = fof_corr.values.tolist()[0]
    asset_vol.loc[asset_vol.index[-1],
    ['FOF：进攻性资产', 'FOF：稳健性资产', 'FOF：CTA','FOF：公募偏股','FOF：量化多头','FOF：主观多头']] = fof_vol.values.tolist()
    asset_VAR.loc[asset_VAR.index[-1],
    ['FOF：进攻性资产', 'FOF：稳健性资产', 'FOF：CTA','FOF：公募偏股','FOF：量化多头','FOF：主观多头']] = fof_VAR.values.tolist()


    return  asset_annually_ret.iloc[-365:], asset_vol.iloc[-365:], asset_corr.iloc[-365:], asset_VAR.iloc[-365:],fof_stress_test


class FOF_analysis:

    def __init__(self,dir,end_date):

        raw_df=pd.read_excel(dir,sheet_name='数据')
        # remove '未定义',keep 审核通过 take
        raw_df = raw_df[(raw_df['审核状态'] == '审核通过') & (raw_df['投资类型'] != '未定义')]
        raw_df = raw_df[(raw_df['投资类型'] == '认购') |
                        (raw_df['投资类型'] == '申购')|
                        (raw_df['投资类型'] == '赎回')|
                        (raw_df['投资类型'] == '份额转入')|
                        (raw_df['投资类型'] == '份额转出')]

        raw_df['交易日期'] = raw_df['交易日期'].astype(str).str.replace('-', '')
        raw_df = raw_df[raw_df['交易日期'] <= end_date]
        raw_df['交易日期']=[x[0:8] for x in raw_df['交易日期']]
        raw_df['投资基金代码'] = [ str(x).replace('.OF','') for x in raw_df['投资基金代码']]
        raw_df['投资基金代码'] = [("000000"+str(x))[-6:] for x in raw_df['投资基金代码']]

        #add the nav price for mutual fund
        #deal with multi trades that happend at the same day for same ticker
        raw_df=pd.merge(raw_df.groupby(['交易日期','投资基金代码','投资类型','审核状态'])[['认申购金额','申请份额', '赎回份额', '赎回费']].sum().reset_index()
                        ,raw_df[['指令ID', '交易日期', '产品名称', '产品代码', '投资类型', '投资基金代码', '投资基金简称', '确认净值', '审核状态']].drop_duplicates(['交易日期','投资基金代码','投资类型','审核状态']),how='left',on=['交易日期','投资基金代码','投资类型','审核状态'])




        self.trading_flow=raw_df
        self.prv_jjflmap= dict(zip(['c','d','b','Z','1','2','3','4','5','7','8','0'], ['其他','多策略','多空仓型','组合型','股票型'
                                    ,'债券型','货币型','宏观策略','市场中性','套利型','管理期货','其他']))
        self.prv_ejflmap =dict(zip(['Z001','Z002','c005','c006','c007','1001','1002','2001','2002','2003','2004','8003','8004','8005','8006','0'
                     ],['MOM','FOF','其他策略','期权策略','其他衍生品','主观多头','量化多头','纯债策略','强债策略','转债策略','债券其他','量化趋势','量化套利','管理期货复合','主观CTA','其他'
                     ]))
        self.mu_jjflmap= dict(zip(['1', '2', '3','0','7','9'], ['股票型', '债券型', '混合型','其他','货币型','QDII']))
        self.mu_ejflmap =dict(zip(['13', '14', '15', '16', '21', '22', '23', '24', '25', '26', '27', '28', '34', '35', '36', '37',
                     '38',
                     '41', '42','0','91'
                     ],['普通股票型', '股票型', '增强指数型', '被动指数型', '被动指数型债券', '短期纯债型', '混合债券型一级', '混合债券型二级', '增强指数型债券', '债券型',
                     '中长期纯债型',
                     '可转换债券型', '平衡混合型', '灵活配置型', '混合型', '偏股混合型', '偏债混合型', '股票多空', '商品型','其他','股票型QDII'
                     ]))

        self.index_enhance_manual_map=dict(zip(['SJH866'],['500zz']))

    @staticmethod
    def get_fund_lable(trading_detail):

        # merge mu fund style label
        max_date = \
            pd.read_sql("select max(asofdate) as max_date from jjpic_value_p_hbs ", con=localdb)['max_date'].iloc[0]
        sql = "SELECT jjdm,`风格偏好`,`风格类型`,`成长绝对暴露(持仓)`,`价值绝对暴露(持仓)` from jjpic_value_p_hbs where asofdate='{0}' and jjdm in ({1})" \
            .format(max_date, util.list_sql_condition(trading_detail['jjdm'].unique().tolist()))
        mu_style_lable = pd.read_sql(sql, con=localdb)

        # get the A share label for C share fund
        miss_mu_jjdm = set(trading_detail[(trading_detail['cpfl'] == '2')
                                          & (trading_detail['ejfl'].isin(['13', '35', '37']))][
                               'jjdm']).difference(set(mu_style_lable['jjdm']))

        if(len(miss_mu_jjdm)>0):
            # get fund name
            sql = "select jjdm,jjjc,jjmc from st_fund.t_st_gm_jjxx where jjdm in ({})" \
                .format(util.list_sql_condition(list(miss_mu_jjdm)))
            fund_name = hbdb.db2df(sql, db='funduser')
            fund_name['jjjc'] = [x.replace('C', 'A') for x in fund_name['jjjc'].tolist()]
            fund_name = pd.merge(fund_name, hbdb.db2df(sql="select jjdm,jjjc,jjmc from st_fund.t_st_gm_jjxx where jjmc in ({}) "
                                                       .format(util.list_sql_condition(fund_name['jjmc'].tolist())),
                                                       db='funduser')
                                 , how='left', on='jjmc')
            name_map = dict(zip(fund_name[fund_name['jjdm_y'].isin(miss_mu_jjdm)].sort_values('jjmc')['jjdm_x'].tolist(),
                                fund_name[~fund_name['jjdm_y'].isin(miss_mu_jjdm)].sort_values('jjmc')['jjdm_y'].tolist()))
            name_map_inverse=dict(zip(fund_name[~fund_name['jjdm_y'].isin(miss_mu_jjdm)].sort_values('jjmc')['jjdm_y'].tolist()
                                      ,fund_name[fund_name['jjdm_y'].isin(miss_mu_jjdm)].sort_values('jjmc')['jjdm_x'].tolist()))

            trading_detail.loc[trading_detail['jjdm'].isin(fund_name['jjdm_x'].tolist())
            , 'jjdm'] = [name_map[x] for x in
                         trading_detail[trading_detail['jjdm'].isin(fund_name['jjdm_x'].tolist())]['jjdm'].tolist()]

            sql = "SELECT jjdm,`风格偏好`,`风格类型`,`成长绝对暴露(持仓)`,`价值绝对暴露(持仓)` from jjpic_value_p_hbs where asofdate='{0}' and jjdm in ({1})" \
                .format(max_date, util.list_sql_condition(trading_detail['jjdm'].unique().tolist()))
            mu_style_lable = pd.read_sql(sql, con=localdb)

        mu_style_lable.loc[(mu_style_lable['风格偏好'] == '均衡')
                           & (mu_style_lable['价值绝对暴露(持仓)'] > mu_style_lable['成长绝对暴露(持仓)'])
                           & (mu_style_lable['风格类型'] == '配置')
        , '风格偏好'] = '价值'
        mu_style_lable.drop_duplicates('jjdm',inplace=True)


        trading_detail = pd.merge(trading_detail, mu_style_lable[['jjdm', '风格偏好']]
                                  , how='left', on='jjdm')
        sql = "SELECT jjdm,`规模偏好` from jjpic_size_p_hbs where asofdate='{0}' and jjdm in ({1})" \
            .format(max_date, util.list_sql_condition(trading_detail['jjdm'].unique().tolist()))
        mu_size_lable = pd.read_sql(sql, con=localdb)
        mu_size_lable.drop_duplicates('jjdm',inplace=True)

        trading_detail = pd.merge(trading_detail, mu_size_lable[['jjdm', '规模偏好']]
                                  , how='left', on='jjdm')

        missed_mu_jjdm = trading_detail[(trading_detail['风格偏好'].isnull())
                                        & (trading_detail['cpfl'] == '2')
                                        & (trading_detail['ejfl'] != '38')][['jjdm', 'jjjc']]
        missed_prv_jjdm = trading_detail[(trading_detail['风格偏好'].isnull())
                                         & (trading_detail['cpfl'] == '4')
                                         ][['jjdm', 'jjjc']]

        file_list = pd.DataFrame(data=os.listdir(r"E:\GitFolder\docs\净值标签"), columns=['name'])

        nav_mu_label = pd.read_excel(r"E:\GitFolder\docs\净值标签\{}"
                                     .format(file_list[file_list['name'].str.startswith('公募基于净值标签')].iloc[-1]['name']))[
            ['jjdm', '规模标签', '风格标签']]

        nav_mu_label['jjdm'] = [("000000" + str(x))[-6:] for x in nav_mu_label['jjdm']]
        missed_mu_jjdm = pd.merge(missed_mu_jjdm, nav_mu_label, how='left', on='jjdm').drop_duplicates(
            'jjdm').set_index('jjdm')

        for jjdm in missed_mu_jjdm.index.tolist():
            trading_detail.loc[trading_detail['jjdm'] == jjdm, '风格偏好'] = missed_mu_jjdm.loc[jjdm]['风格标签']
            trading_detail.loc[trading_detail['jjdm'] == jjdm, '规模偏好'] = missed_mu_jjdm.loc[jjdm]['规模标签']

        nav_prv_label = pd.read_excel(r"E:\GitFolder\docs\净值标签\{}"
            .format(
            file_list[file_list['name'].str.startswith('全部私募打标结果')].iloc[-1]['name']))[['jjdm', '基金简称', '大小盘', '成长价值']]
        missed_prv_jjdm = pd.merge(missed_prv_jjdm, nav_prv_label, how='left', on='jjdm')
        nav_prv_label['company'] = nav_prv_label['基金简称'].str[0:2]
        missed_prv_jjdm['company'] = missed_prv_jjdm['jjjc'].str[0:2]
        nav_prv_label = nav_prv_label.groupby(['company', '大小盘', '成长价值']).count()['jjdm'].reset_index().sort_values(
            ['company', 'jjdm']).drop_duplicates('company', keep='last').drop('jjdm', axis=1)
        missed_prv_jjdm = pd.merge(missed_prv_jjdm, nav_prv_label, how='left', on='company')
        missed_prv_jjdm.loc[missed_prv_jjdm['大小盘_x'].isnull(), '大小盘_x'] = \
            missed_prv_jjdm[missed_prv_jjdm['大小盘_x'].isnull()]['大小盘_y']
        missed_prv_jjdm.loc[missed_prv_jjdm['成长价值_x'].isnull(), '成长价值_x'] = \
            missed_prv_jjdm[missed_prv_jjdm['成长价值_x'].isnull()]['成长价值_y']
        missed_prv_jjdm = missed_prv_jjdm.rename(columns={'大小盘_x': '大小盘'
            , '成长价值_x': '成长价值'}).drop(['大小盘_y',
                                       '成长价值_y'], axis=1).drop_duplicates('jjdm').set_index('jjdm')

        for jjdm in missed_prv_jjdm.index.tolist():
            trading_detail.loc[trading_detail['jjdm'] == jjdm, '风格偏好'] = missed_prv_jjdm.loc[jjdm]['成长价值']
            trading_detail.loc[trading_detail['jjdm'] == jjdm, '规模偏好'] = missed_prv_jjdm.loc[jjdm]['大小盘']

        if(len(miss_mu_jjdm)>0):
            trading_detail.loc[trading_detail['jjdm'].isin(list(name_map_inverse.keys()))
            , 'jjdm'] = [name_map_inverse[x] for x in
                         trading_detail[trading_detail['jjdm'].isin(list(name_map_inverse.keys()))]['jjdm'].tolist()]


        return trading_detail

    def fromtrading2holding(self,end_date,start_date=None):

        if(start_date is None):
            start_date='0'

        # read trading details

        raw_df = self.trading_flow


        raw_df=pd.merge(raw_df.drop_duplicates(['产品名称','投资基金代码','交易日期','指令类型'])[['产品名称', '投资基金'
            , '投资基金代码', '指令类型', '投资类型', '交易日期', '确认净值','审核状态']]
                        ,raw_df.groupby(['产品名称','投资基金代码','交易日期','指令类型']).sum()[['认申购金额','赎回份额','赎回费']].reset_index()
                        ,how='inner',on=['产品名称','投资基金代码','交易日期','指令类型'])

        #combine the same action happend in one day


        for product in raw_df['产品名称'].unique():
            df = raw_df[raw_df['产品名称'] == product]
            df = df.sort_values('交易日期')
            nav_df = pd.read_excel(r"E:\FOF分析\{}\基金净值数据.xls".format(product))
            nav_df['日期'] = nav_df['日期'].astype(str).str.replace('-', '')
            nav_df = nav_df.sort_values('日期')
            nav_df=nav_df[nav_df['日期']<=end_date]
            date_list = nav_df['日期'].tolist()
            date_list = date_list + df['交易日期'].unique().tolist()
            date_list=list(set(date_list))
            date_list.sort()
            hold_df = []

            for i in range(len(date_list)):

                date = date_list[i]


                buy = df[((df['投资类型'] == '申购')|(df['投资类型'] == '认购')|(df['投资类型'] == '份额转入'))
                         & (df['交易日期'] == date)][['投资基金代码', '认申购金额', '确认净值']]
                sell = df[((df['投资类型'] == '赎回')|(df['投资类型'] == '份额转出'))
                          & (df['交易日期'] == date)][['投资基金代码', '赎回份额', '确认净值', '赎回费']]

                if (i == 0):
                    tempdf = pd.DataFrame(columns=['date', 'jjdm', 'quant', 'cbprice','buyprice', 'sellprice'])
                    tempdf['date'] = [date]
                else:
                    tempdf = hold_df[i - 1].copy()

                # buy
                if (len(buy) > 0):
                    buy['buy_quant'] = buy['认申购金额'] / buy['确认净值']

                    tempdf = pd.merge(tempdf, buy[['投资基金代码', 'buy_quant', '确认净值']]
                                      , how='outer', left_on='jjdm', right_on='投资基金代码')

                    tempdf.loc[tempdf['buy_quant'].notnull(), 'cbprice'] = ((tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'cbprice']*tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'quant']).fillna(0)+tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             '确认净值']*tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'buy_quant'])/\
                                                                           (tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'quant'].fillna(0)+tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'buy_quant'])

                    # tempdf.loc[tempdf['buy_quant'].notnull(), 'money_price'] = ((tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'cbprice']*tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'quant']*tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'money_price']).fillna(0)+tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          '确认净值']*tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'buy_quant']*nav_df[nav_df['日期']==date]['单位净值'].values[0])/\
                    #                                                        ((tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'cbprice']*tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'quant']).fillna(0)+tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          '确认净值']*tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'buy_quant'])


                    tempdf['cbprice']=tempdf['cbprice'].astype(float)

                    tempdf.loc[tempdf['buy_quant'].notnull(), 'quant'] = tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'quant'].fillna(0) \
                                                                         + tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'buy_quant']
                    tempdf.loc[tempdf['buy_quant'].notnull(), 'jjdm'] = tempdf.loc[tempdf['buy_quant'].notnull()][
                        '投资基金代码']
                    tempdf.loc[tempdf['buy_quant'].notnull(), 'buyprice'] = tempdf.loc[tempdf['buy_quant'].notnull()][
                        '确认净值']

                    tempdf.drop(['buy_quant', '投资基金代码', '确认净值'], axis=1, inplace=True)
                    tempdf = tempdf[tempdf['jjdm'].notnull()]
                # sell
                if (len(sell) > 0):
                    tempdf = pd.merge(tempdf, sell[['投资基金代码', '赎回份额', '确认净值']]
                                      , how='left', left_on='jjdm', right_on='投资基金代码')

                    tempdf.loc[tempdf['赎回份额'].notnull(), 'cbprice'] = ((tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             'cbprice']*tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             'quant']).fillna(0)-tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             '确认净值']*tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             '赎回份额'])/\
                                                                           (tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             'quant'].fillna(0)-tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             '赎回份额'])




                    tempdf.loc[tempdf['赎回份额'].notnull(), 'quant'] = tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                        'quant'].fillna(0) \
                                                                    - tempdf.loc[tempdf['赎回份额'].notnull()]['赎回份额']
                    #if left quant<100,make it 0
                    tempdf.loc[(tempdf['赎回份额'].notnull())&(tempdf['quant']<=100), 'quant']=0

                    tempdf.loc[tempdf['赎回份额'].notnull(), 'sellprice'] = tempdf.loc[tempdf['赎回份额'].notnull()]['确认净值']
                    tempdf.drop(['赎回份额', '投资基金代码', '确认净值'], axis=1, inplace=True)

                tempdf['date'] = date

                if(date==start_date ):
                    file_name_list =pd.DataFrame(data=os.listdir(r"E:\FOF分析\{0}\估值表\{1}"
                                                .format(product,start_date[0:6])),columns=['name'])
                    file_name_list['name_new'] = [x.replace("-", '') for x in file_name_list['name']]
                    fold_name = \
                    file_name_list[file_name_list['name_new'].str.contains(start_date)]['name'].iloc[0]
                    gzb = pd.read_excel(r"E:\FOF分析\{0}\估值表\{1}\{2}"
                                        .format(product, start_date[0:6], fold_name)).iloc[2:-3]
                    gzb.columns = gzb.iloc[0]
                    gzb = gzb[((gzb['科目代码'].astype(str).str.startswith('11090501'))
                               | (gzb['科目代码'].astype(str).str.startswith('11090201'))
                               | (gzb['科目代码'].astype(str).str.startswith('11050201'))
                               | (gzb['科目代码'].astype(str).str.startswith('11050301')) |
                               (gzb['科目代码'].astype(str).str.startswith('11090601')))
                              &
                              ((gzb['科目代码'].astype(str) != '11090201')
                               & (gzb['科目代码'].astype(str) != '11090501')
                               & (gzb['科目代码'].astype(str) != '11050201')
                               & (gzb['科目代码'].astype(str) != '11050301')
                               & (gzb['科目代码'].astype(str) != '11090601'))][['科目代码', '科目名称', '市价']]

                    gzb.loc[(gzb['科目代码'].str.startswith('11090201'))
                            & (~gzb['科目代码'].str.startswith('11090201S'))
                            & (~gzb['科目代码'].str.startswith('11090201P')), '科目代码'] = "S" + \
                                                                                    gzb[(gzb['科目代码'].str.startswith(
                                                                                        '11090201'))
                                                                                        & (~gzb['科目代码'].str.startswith(
                                                                                        '11090201S'))]['科目代码'].str[
                                                                                    -6:-1]
                    gzb.loc[(gzb['科目代码'].str.startswith('11090601'))
                            & (~gzb['科目代码'].str.startswith('11090601S'))
                            & (~gzb['科目代码'].str.startswith('11090601P')), '科目代码'] = "S" + \
                                                                                    gzb[(gzb['科目代码'].str.startswith(
                                                                                        '11090601'))
                                                                                        & (~gzb['科目代码'].str.startswith(
                                                                                        '11090601S'))]['科目代码'].str[
                                                                                    -6:-1]

                    gzb['科目代码']=gzb['科目代码'].str[-6:-1]
                    tempdf['科目代码']=tempdf['jjdm'].astype(str).str[-6:-1]
                    tempdf=pd.merge(tempdf,gzb,how='left',on='科目代码')
                    tempdf['cbprice']=tempdf['市价']
                    tempdf=tempdf[tempdf['市价'].notnull()]
                    tempdf.drop(['科目名称','市价','科目代码'],axis=1,inplace=True)
                    tempdf=tempdf[tempdf['quant']!=0]

                hold_df.append(tempdf)

            hold_df = pd.concat(hold_df, axis=0)
            hold_df = pd.merge(hold_df, nav_df[['日期', '资产净值', '资产份额', '单位净值','累计单位净值']]
                               , how='left', left_on='date', right_on='日期')
            hold_df['jjdm']=[("000000"+x)[-6:] for x in hold_df['jjdm'].astype(str).tolist()]
            jjdm_list = hold_df['jjdm'].unique().tolist()

            # get prv list and mutual list
            sql = "select jjdm,jjjc,cpfl,jjfl,ejfl from st_fund.t_st_gm_jjxx where jjdm in ({}) and cpfl='2'" \
                .format(util.list_sql_condition([("000000" + x)[-6:] for x in jjdm_list]))
            mutual_fund = hbdb.db2df(sql, db='funduser')

            sql = "select jjdm,jjjc,cpfl,jjfl,ejfl from st_hedge.t_st_jjxx where jjdm in ({}) and cpfl='4'" \
                .format(util.list_sql_condition(jjdm_list))
            prv_fund = hbdb.db2df(sql, db='highuser')
            #
            # sql="select jjdm,jjjc,cpfl,jjfl,ejfl from st_fixed.t_st_jjxx where jjdm in ({0}) "\
            #     .format(util.list_sql_condition(jjdm_list))
            # fix_fund=hbdb.db2df(sql, db='fixeduser')

            # read fund nav from DB

            # for prv fund
            if(len(prv_fund)>0):
                sql = "select jjdm,jzrq,jjjz from st_hedge.t_st_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'" \
                    .format(util.list_sql_condition(prv_fund['jjdm'].tolist()), date_list[0], date_list[-1])
                prv_nav = hbdb.db2df(sql, db='highuser')
            else:
                prv_nav=pd.DataFrame(columns=['jjdm','jzrq','jjjz'])

            prv_nav_new=[]

            for date in hold_df['date'].unique().tolist():
                tempdf=\
                    prv_nav[(prv_nav['jzrq']<=date)&(prv_nav['jjjz'].notnull())][['jjjz','jjdm']].drop_duplicates('jjdm',keep='last')
                tempdf['jzrq']=date
                prv_nav_new.append(tempdf)

            prv_nav=pd.concat(prv_nav_new,axis=0).reset_index(drop=True)

            # for mutual fund
            if(len(mutual_fund[mutual_fund['jjfl']!='7'])>0):
                sql = "select jjdm,jzrq,jjjz from st_fund.t_st_gm_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'" \
                    .format(util.list_sql_condition(mutual_fund['jjdm'].tolist()), date_list[0], date_list[-1])
                mutual_nav = hbdb.db2df(sql, db='funduser')
                mutual_nav['jzrq'] = mutual_nav['jzrq'].astype(str)
            else:
                mutual_nav=pd.DataFrame(columns=['jjdm','jzrq','jjjz'])

            mu_nav_new=[]

            for date in hold_df['date'].unique().tolist():
                tempdf=\
                    mutual_nav[(mutual_nav['jzrq']<=date)&(mutual_nav['jjjz'].notnull())][['jjjz','jjdm']].drop_duplicates('jjdm',keep='last')
                tempdf['jzrq']=date
                mu_nav_new.append(tempdf)

            mutual_nav=pd.concat(mu_nav_new,axis=0).reset_index(drop=True)


            hold_nan = hold_df[hold_df['jjdm'].isin(list((set(hold_df['jjdm'].unique()).difference(set(mutual_fund['jjdm'].tolist()))).difference(set(prv_fund['jjdm'].tolist()))))]

            hold_df_mu = pd.merge(hold_df[hold_df['jjdm'].isin(mutual_fund['jjdm'].tolist())], mutual_nav
                                  , how='left', left_on=['jjdm', 'date'], right_on=['jjdm', 'jzrq'])
            hold_df_mu=pd.merge(hold_df_mu,mutual_fund,how='left',on='jjdm')

            hold_df_prv = pd.merge(hold_df[hold_df['jjdm'].isin(prv_fund['jjdm'].tolist())], prv_nav
                                   , how='left', left_on=['jjdm', 'date'], right_on=['jjdm', 'jzrq'])
            hold_df_prv=pd.merge(hold_df_prv,prv_fund,how='left',on='jjdm')

            hold_df = pd.concat([hold_nan, hold_df_prv], axis=0)
            hold_df = pd.concat([hold_df, hold_df_mu], axis=0).sort_values('date').drop(['jzrq', '日期'], axis=1)

            hold_df=self.get_fund_lable(hold_df)


            #make sure that every fund has jjjz at the last day
            file_name_list = pd.DataFrame(data=os.listdir(r"E:\FOF分析\{0}\估值表\{1}"
                                                          .format(product, hold_df['date'].max()[0:6])),
                                          columns=['name'])
            file_name_list['name_new']=[x.replace("-",'') for x in file_name_list['name']]
            fold_name = file_name_list[file_name_list['name_new'].str.contains(hold_df['date'].max())]['name'].iloc[0]
            gzb = pd.read_excel(r"E:\FOF分析\{0}\估值表\{1}\{2}"
                                .format(product, hold_df['date'].max()[0:6], fold_name)).iloc[2:-3]
            gzb.columns = gzb.iloc[0]
            gzb = gzb[((gzb['科目代码'].astype(str).str.startswith('11090501'))
                       | (gzb['科目代码'].astype(str).str.startswith('11090201'))
                       |(gzb['科目代码'].astype(str).str.startswith('11050201'))
                       |(gzb['科目代码'].astype(str).str.startswith('11050301'))|
                       (gzb['科目代码'].astype(str).str.startswith('11090601')))
                      &
                      ((gzb['科目代码'].astype(str) != '11090201')
                       & (gzb['科目代码'].astype(str) != '11090501')
                       &(gzb['科目代码'].astype(str) != '11050201')
                       &(gzb['科目代码'].astype(str) != '11050301')
                       &(gzb['科目代码'].astype(str) != '11090601'))][['科目代码', '科目名称', '市价']]

            gzb.loc[(gzb['科目代码'].str.startswith('11090201'))
                    & (~gzb['科目代码'].str.startswith('11090201S'))
                    & (~gzb['科目代码'].str.startswith('11090201P')), '科目代码'] = "S" + \
                                                                            gzb[(gzb['科目代码'].str.startswith('11090201'))
                                                                                & (~gzb['科目代码'].str.startswith(
                                                                                '11090201S'))]['科目代码'].str[-6:-1]
            gzb.loc[(gzb['科目代码'].str.startswith('11090601'))
               & (~gzb['科目代码'].str.startswith('11090601S'))
               & (~gzb['科目代码'].str.startswith('11090601P')), '科目代码'] = "S" + \
                                                                            gzb[(gzb['科目代码'].str.startswith('11090601'))
               & (~gzb['科目代码'].str.startswith('11090601S'))]['科目代码'].str[-6:-1]

            gzb['科目代码'] = gzb['科目代码'].str[-6:]
            hold_df['科目代码'] = hold_df['jjdm'].astype(str).str[-6:]
            hold_df = pd.merge(hold_df, gzb, how='left', on='科目代码')
            hold_df.loc[hold_df['jjjz'].isnull(),'jjjz']=hold_df[hold_df['jjjz'].isnull()]['市价']
            hold_df.drop(['科目名称', '市价', '科目代码'], axis=1, inplace=True)

            hold_df.to_excel(r"E:\FOF分析\{}\基金持仓数据.xlsx".format(product), index=False)

            print(product + ' Done ')

    def valuation_table_analysis(self,product,end_date,start_date=None,get_nav_from_gzb=False):

        if(start_date is None):
            start_date='0'

        month_list=os.listdir(r"E:\FOF分析\{0}\估值表"
                                    .format(product))

        solved_gzb=[]
        exist_date_list=[]
        jjjzc=[]
        ljjz=[]
        solved_gzb_gl=[]
        for month in month_list:
            file_name_list =pd.DataFrame(data=os.listdir(r"E:\FOF分析\{0}\估值表\{1}"
                                        .format(product,month)),columns=['name'])

            for name in file_name_list['name']:
                #print(name) #S21582_新方程对冲精选H1号基金20210604.xls
                gzb = pd.read_excel(r"E:\FOF分析\{0}\估值表\{1}\{2}"
                                    .format(product, month, name))

                #deal with H1 special valuation table
                if(len((gzb.iloc[1][0]).split('估值日期'))>1):
                    gzb=gzb.iloc[1:-3]
                    data=(gzb.iloc[0][0]).split('估值日期')[1].replace('-','').replace(':','').replace('：','').replace(' ','').replace('_','')
                    gzb = gzb.iloc[1:]
                    gzb.columns = gzb.iloc[0]
                else:
                    data=gzb.columns[0].split('_')[2].replace('-','').replace(':','').replace('：','').replace(' ','').replace('_','')
                    gzb.columns = gzb.iloc[0]

                if(data<start_date):
                    continue
                if(data>end_date):
                    continue


                gzb.columns = [str(x).replace(' ', '') for x in gzb.columns.tolist()]
                gzb.rename(columns={'行情收市价':'市价'},inplace=True)
                if(get_nav_from_gzb):
                    temp_jjjzc=gzb[gzb['科目代码'] == '基金资产净值:']['市值'].iloc[0]
                    temp_ljjz=gzb[gzb['科目代码'] == '累计单位净值:']['市值'].iloc[0]
                else:
                    temp_ljjz=[]
                    temp_jjjzc=[]

                gzb_gl=gzb.copy()

                gzb = gzb[((gzb['科目代码'].astype(str).str.startswith('11090501'))
                           | (gzb['科目代码'].astype(str).str.startswith('11090201'))
                           | (gzb['科目代码'].astype(str).str.startswith('11050201'))
                           | (gzb['科目代码'].astype(str).str.startswith('11050301')) |(gzb['科目代码'].astype(str).str.startswith('11050401')) |
                           (gzb['科目代码'].astype(str).str.startswith('11090601'))
                           |(gzb['科目代码'].astype(str)=='1203')|(gzb['科目代码'].astype(str).str.startswith('11090101'))
                           |(gzb['科目代码'].astype(str)=='1002'))
                          &
                          ((gzb['科目代码'].astype(str) != '11090201')
                           & (gzb['科目代码'].astype(str) != '11090501')
                           & (gzb['科目代码'].astype(str) != '11050201')
                           & (gzb['科目代码'].astype(str) != '11050301')
                           & (gzb['科目代码'].astype(str) != '11050401')
                           & (gzb['科目代码'].astype(str) != '11090601')
                           &(gzb['科目代码'].astype(str) != '11090101'))][['科目代码', '科目名称','数量'
                    ,'单位成本','成本占净值%','市价','市值','市值占净值%','估值增值']]

                if (len(gzb_gl[((gzb_gl['科目代码'].astype(str).str.startswith('12032006'))
                                 |(gzb_gl['科目代码'].astype(str).str.startswith('12030508')))
                          &
                          ((gzb_gl['科目代码'].astype(str) != '12032006')
                           &(gzb_gl['科目代码'].astype(str) != '12030508'))]) > 0):

                    gzb_gl = gzb_gl[((gzb_gl['科目代码'].astype(str).str.startswith('12032006'))
                                     |(gzb_gl['科目代码'].astype(str).str.startswith('12030508')))
                              &
                              ((gzb_gl['科目代码'].astype(str) != '12032006')
                               &(gzb_gl['科目代码'].astype(str) != '12030508'))][['科目代码', '科目名称','数量'
                        ,'单位成本','成本占净值%','市价','市值','市值占净值%','估值增值']]

                else:

                    gzb_gl = gzb_gl[((gzb_gl['科目代码'].astype(str).str.startswith('12032006'))
                                     | (gzb_gl['科目代码'].astype(str).str.startswith('12030508')))
                                    ][['科目代码', '科目名称', '数量'
                        , '单位成本', '成本占净值%', '市价', '市值', '市值占净值%', '估值增值']]


                if('1203' not in gzb['科目代码'].tolist()):
                    gzb.loc[gzb.index[-1]+1]=['1203','应收股利']+[0]*7


                gzb['科目代码']=gzb['科目代码'].str[-6:]
                gzb['date']=data
                gzb_gl['date']=data
                if(data not  in exist_date_list):
                    exist_date_list.append(data)
                    solved_gzb.append(gzb)
                    solved_gzb_gl.append(gzb_gl)
                    jjjzc.append(temp_jjjzc)
                    ljjz.append(temp_ljjz)

        hold_df=pd.concat(solved_gzb,axis=0)
        solved_gzb_gl=pd.concat(solved_gzb_gl,axis=0)

        #transfor wrong jjdm to right jjdm 和聚平台证券投资基金


        orginal_code=['1ZLZG3', '1BYTZ2', '1AAAA7', '1BXZG2', '1BLKS1', '2QHGH1', '1HYZG5', '1HFL32', '2HFLH1',
                      '2JZTZ1', '1JZTZ4', '1LPTZ2', '2LPTZ4', '1LSTZ9', '3MXTZ1', '1MXTZ8', '3MHTZ3', '1MHTZC', '1MHTZJ',
                      '1MHTZB', '1MHTZE', '1QLTZ3', '1QLTZ5', '1QLT11', '2RQZG1', '3RPTZ2', '1SGD12', '1XMZC2', '1XMZC1',
                       '1XKTZA', '1XKTZ5', '3XKTZ2', '1YFT12', '3ZHTZ1','SH3322','1GYZC1','JZ510B','2CQRY1',
                      'GT498A','2SGDZ1','NT762C','QS592B','NY736C','4XLZC2','S9649B','3LRZG1','2CQZG1','LS0002','LS0003',
                      'LS0004','LS0013','LS0017','LS0007','LS0008','LS0009','LS0010','LS0014','LS0012','LC078A','QB109B',
                      'X5605B','1WKTZ2','ET353B','GH832B','TY576A','VZ894A','B1666A','2YZTZ1','2WDZG1','270004','519019',
                      'FLWJN1','xfcxf2','GYLW1A','SFCHCA','YTCZN7','GFJZ12','1HCHF1','66391B','246040','23582A','HBCT2A',
                      'HXQJ1F','Y4405C','1AADH2','3HYZG1','1AAPP8','ABE53B','XX346B','ACM31B','NP315B','XB480B','R0001B']
        maped_code=['SLP211', 'SNZ338', 'SQS281', 'STR792', 'SED697', 'SY0256', 'S83614', 'SNX384', 'SLK497',
                    'SNE372', 'SJD015', 'SNP300', 'SQJ816', 'SER492', 'SJA462', 'SGP290', 'SR0001', 'SM8148', 'SLF242',
                    'SEF092', 'SCY785', 'SGC224', 'SGY379', 'SNL641', 'SJZ021', 'SX5605', 'SGU946', 'SEU546', 'SEZ550',
                    'SSE288', 'SNV206', 'SSM840', 'SNP647', 'SQS592','P20830','SY8350','T04393','SNR623',
                    'SGT498','SGT498','SNT762','SQS592','SNY736','SNY736','SS9649','SS9649','SQK761','SJZ510','SQK761',
                    'SQA948','SQF770','SNY736','SK6332','SVZ894','STY576','SEM863','SCL316','SXD663','SLC078','SQB109',
                    'SX5605','S33474','SET353','SGH832','STY576','SVZ894','SB1666','SGT338','SNT164','270014','017772',
                    'P02494','P12095','SJ5324','S63506','SS0299','S62866','SQG573','S66391','M06228','S23582','M06228',
                    'SH5035','SY4405','SQB109','T04393','SQL839','P51276','P51276','SQF770','SNP315','SXB480','SR0001']
        jjdm_map=pd.DataFrame()
        jjdm_map['科目代码']=orginal_code
        jjdm_map['映射代码'] = maped_code
        hold_df=pd.merge(hold_df,jjdm_map,how='left',on='科目代码')
        hold_df.loc[hold_df['映射代码'].notnull(),'科目代码']=hold_df[hold_df['映射代码'].notnull()]['映射代码']
        hold_df.drop('映射代码',axis=1,inplace=True)


        #get the wrong jjdm list
        know_jjdm=self.trading_flow[['投资基金简称','投资基金代码']].drop_duplicates()
        wrong_jjdm=pd.merge(hold_df[['科目代码','科目名称']],know_jjdm,
                            how='left',left_on='科目代码',
        right_on='投资基金代码').drop_duplicates('科目代码')
        wrong_jjdm=wrong_jjdm[(wrong_jjdm['投资基金简称'].isnull())&(wrong_jjdm['科目代码']!='1203')&(wrong_jjdm['科目代码']!='1002')]
        if(len(wrong_jjdm)>0):
            wrong_jjdm['科目名称_t']=wrong_jjdm['科目名称']
            wrong_jjdm['科目名称_t']=wrong_jjdm['科目名称_t'].str.replace('A类','A')
            wrong_jjdm['科目名称_t']=wrong_jjdm['科目名称_t'].str.replace('B类','B')
            wrong_jjdm['科目名称_t']=wrong_jjdm['科目名称_t'].str.replace('C类','C')
            wrong_jjdm['科目名称_t']=wrong_jjdm['科目名称_t'].str.replace('A级','A')
            wrong_jjdm['科目名称_t']=wrong_jjdm['科目名称_t'].str.replace('B级','B')
            wrong_jjdm['科目名称_t']=wrong_jjdm['科目名称_t'].str.replace('C级','C')
            if(len(wrong_jjdm)==1):
                sql = "select jjjc,jjmc from st_hedge.t_st_jjxx where jjmc in ('{}')"\
                    .format(wrong_jjdm['科目名称_t'].tolist()[0])
            else:
                sql = "select jjjc,jjmc from st_hedge.t_st_jjxx where jjmc in {}".format(
                    tuple(wrong_jjdm['科目名称_t'].tolist()))
            right_jjdm=hbdb.db2df(sql,db='highuser').drop_duplicates()
            wrong_jjdm=pd.merge(wrong_jjdm,right_jjdm,
                                left_on='科目名称_t',right_on='jjmc',how='left').drop(['投资基金简称','投资基金代码'],axis=1)
            wrong_jjdm = pd.merge(wrong_jjdm, know_jjdm, how='left', left_on='jjjc', right_on='投资基金简称')

            if(len(wrong_jjdm[wrong_jjdm['投资基金代码'].isnull()])>0):
                wrong_jjdm['jjjc']=wrong_jjdm['jjjc'].str.replace('A','')
                wrong_jjdm['jjjc']=wrong_jjdm['jjjc'].str.replace('B','')
                wrong_jjdm['jjjc']=wrong_jjdm['jjjc'].str.replace('C','')
                wrong_jjdm['jjjc']=wrong_jjdm['jjjc'].str.replace('级','')
                wrong_jjdm['jjjc']=wrong_jjdm['jjjc'].str.replace('类','')
                wrong_jjdm = pd.merge(wrong_jjdm, know_jjdm, how='left', left_on='jjjc', right_on='投资基金简称')
                wrong_jjdm.loc[wrong_jjdm['投资基金代码_x'].isnull(),'投资基金代码_x']=\
                    wrong_jjdm.loc[wrong_jjdm['投资基金代码_x'].isnull()]['投资基金代码_y']
                wrong_jjdm.rename(columns={'投资基金代码_x':'投资基金代码'},inplace=True)


            hold_df=pd.merge(hold_df,wrong_jjdm[['科目代码','投资基金代码']],how='left',on='科目代码')
            hold_df.loc[hold_df['投资基金代码'].notnull(),'科目代码']=hold_df[hold_df['投资基金代码'].notnull()]['投资基金代码']
            hold_df.drop('投资基金代码',axis=1,inplace=True)

            wrong_jjdm=wrong_jjdm[wrong_jjdm['投资基金代码'].isnull()]
        if(len(wrong_jjdm)>0):
            print("the following jjdm need to be mapped mannually ")
            print(wrong_jjdm[['科目代码','科目名称','jjjc']])
            raise Exception


        jjdm_list=hold_df['科目代码'].unique()
        # get prv list and mutual list
        sql = "select jjdm,cpfl,jjfl,ejfl from st_fund.t_st_gm_jjxx where jjdm in ({}) and cpfl='2'" \
            .format(util.list_sql_condition(jjdm_list))
        mutual_fund = hbdb.db2df(sql, db='funduser')

        sql = "select jjdm,cpfl,jjfl,ejfl from st_hedge.t_st_jjxx where jjdm in ({}) and cpfl='4'" \
            .format(util.list_sql_condition(jjdm_list))
        prv_fund = hbdb.db2df(sql, db='highuser')

        fund_features=pd.concat([mutual_fund,prv_fund],axis=0)
        hold_df=pd.merge(hold_df,fund_features,how='left',
                         left_on='科目代码',right_on='jjdm').drop('jjdm',axis=1).rename(columns={'科目代码':'jjdm',
                                                                                             '科目名称':'jjjc',
                                                                                             '数量':'quant',
                                                                                             '单位成本':'cbprice',
                                                                                             '市价':'jjjz',
                                                                                             '市值':'mv',
                                                                                             '成本占净值%':'cb_w',
                                                                                             '市值占净值%':'weight',
                                                                                             '估值增值':'value_increased',})

        # hold_nan = hold_df[hold_df['jjdm'].isin(list((set(hold_df['jjdm'].unique()).difference(set(mutual_fund['jjdm'].tolist()))).difference(set(prv_fund['jjdm'].tolist()))))]
        #
        # hold_df_mu = pd.merge(hold_df[hold_df['jjdm'].isin(mutual_fund['jjdm'].tolist())], mutual_nav
        #                       , how='left', left_on=['jjdm', 'date'], right_on=['jjdm', 'jzrq'])
        # hold_df_mu=pd.merge(hold_df_mu,mutual_fund,how='left',on='jjdm')
        #
        # hold_df_prv = pd.merge(hold_df[hold_df['jjdm'].isin(prv_fund['jjdm'].tolist())], prv_nav
        #                        , how='left', left_on=['jjdm', 'date'], right_on=['jjdm', 'jzrq'])
        # hold_df_prv=pd.merge(hold_df_prv,prv_fund,how='left',on='jjdm')
        #
        # hold_df = pd.concat([hold_nan, hold_df_prv], axis=0)
        # hold_df = pd.concat([hold_df, hold_df_mu], axis=0).sort_values('date').drop(['jzrq', '日期'], axis=1)

        if(get_nav_from_gzb):
            jjjzc=pd.DataFrame(data=jjjzc,columns=['资产净值'])
            jjjzc['日期']=exist_date_list
            jjjzc['累计单位净值']=ljjz
            jjjzc.sort_values(['日期']).to_excel(r"E:\FOF分析\{}\基金净值解析数据.xlsx".format(product), index=False)


        nav_df = pd.read_excel(r"E:\FOF分析\{}\基金净值数据.xlsx".format(product))
        nav_df['日期'] = nav_df['日期'].astype(str).str.replace('-', '')
        nav_df = nav_df.sort_values('日期')

        hold_df=pd.merge(hold_df,nav_df[['日期', '资产净值', '资产份额', '单位净值', '累计单位净值']]
                         ,how='left',left_on='date',right_on='日期').drop('日期',axis=1)
        for col in ['quant','value_increased','mv']:
            hold_df[col] = hold_df[col].astype(str).str.replace(',', '').astype(float)
        for col in ['市值','数量','估值增值']:
            solved_gzb_gl[col] = solved_gzb_gl[col].astype(str).str.replace(',', '').astype(float)



        #deal with two recoreds for one ticker at certain date
        def remvoe_duplicate_ticker(hold_df):
            error_list = hold_df.groupby(['jjdm', 'date'])['jjjc'].count()[
                hold_df.groupby(['jjdm', 'date'])['jjjc'].count() >= 2].reset_index()['jjdm'].unique().tolist()
            if(len(error_list)>0):
                error_list=hold_df[hold_df['jjdm'].isin(error_list)]
                error_list[['quant_x', 'value_increased_x','mv_x']] = error_list[['quant', 'value_increased','mv']].fillna(0)
                error_list=error_list.groupby(['jjdm', 'date']).sum()[['quant_x','value_increased_x','mv_x']].reset_index()

                hold_df=hold_df.drop_duplicates(['jjdm', 'date'])

                hold_df=pd.merge(hold_df,error_list,how='left',on=['jjdm', 'date'])
                hold_df.loc[hold_df['quant_x'].notnull(),'quant']=hold_df.loc[hold_df['quant_x'].notnull()]['quant_x']
                hold_df.loc[hold_df['value_increased_x'].notnull(),'value_increased']=hold_df.loc[hold_df['value_increased_x'].notnull()]['value_increased_x']
                hold_df.loc[hold_df['quant_x'].notnull(),'quant']=hold_df.loc[hold_df['quant_x'].notnull()]['quant_x']
                hold_df.loc[hold_df['mv_x'].notnull(),'mv']=hold_df.loc[hold_df['mv_x'].notnull()]['mv_x']
                hold_df.drop(['quant_x', 'value_increased_x','mv_x'],axis=1,inplace=True)

            return  hold_df

        hold_df=remvoe_duplicate_ticker(hold_df)
        hold_df=self.get_fund_lable(hold_df)

        hold_df['jjdm']=["'"+str(x) for x in hold_df['jjdm']]
        hold_df.sort_values(['date','jjdm']).to_excel(r"E:\FOF分析\{}\基金持仓数据.xlsx".format(product), index=False)
        solved_gzb_gl.sort_values(['date']).to_excel(r"E:\FOF分析\{}\基金股利数据.xlsx".format(product), index=False)


        print(product + ' Done ')


    def fund_attribution_new(self,hold_df,gl_df):

        hold_df['ejfl'] = hold_df['ejfl'].fillna(0).astype(str).str.replace("\.0", '')
        hold_df['jjfl'] = hold_df['jjfl'].fillna(0).astype(str).str.replace("\.0", '')


        for index in self.mu_jjflmap.keys():
            hold_df.loc[(hold_df['jjfl'] == index)
                        &(hold_df['cpfl'] == '公募基金'), 'jjfl'] = self.mu_jjflmap[index]
        for index in self.prv_jjflmap.keys():
            hold_df.loc[(hold_df['jjfl'] == index)
                        &(hold_df['cpfl'] == '私募基金'), 'jjfl'] = self.prv_jjflmap[index]

        for index in self.mu_ejflmap.keys():
            hold_df.loc[(hold_df['ejfl'] == index)
                        &(hold_df['cpfl'] == '公募基金'), 'ejfl'] = self.mu_ejflmap[index]
        for index in self.prv_ejflmap.keys():
            hold_df.loc[(hold_df['ejfl'] == index)
                        &(hold_df['cpfl'] == '私募基金'), 'ejfl'] = self.prv_ejflmap[index]

        trade_data=self.trading_flow

        cont=[]
        hold_df['ret'] = hold_df[['jjdm', 'jjjz']].groupby('jjdm').diff().fillna(0)
        for jjdm in hold_df['jjdm'].unique():

            # print(jjdm)

            # tempdf=hold_df[hold_df['jjdm']==jjdm] SEU546 B6071

            tempdf=pd.merge(pd.DataFrame(data=hold_df['date'].unique(),columns=['date']),
                            hold_df[hold_df['jjdm']==jjdm],how='left',on='date').fillna(0)


            tempdf['revenue']=tempdf['value_increased'].diff()
            tempdf['revenue_2'] = tempdf['mv'].diff().to_list()
            # tempdf['资产份额变动']=(tempdf['资产份额'].pct_change()+1)

            tempdf['quant_change']=tempdf['quant'].diff().fillna(0)

            tempdf_trade=trade_data[trade_data['投资基金代码'] == jjdm]
            tempdf_trade['交易日期'] = [datetime.datetime.strptime(x, '%Y%m%d') for x in tempdf_trade['交易日期']]

            buy=tempdf[tempdf['quant_change'] >0]['date']
            sell=tempdf[tempdf['quant_change'] <0]['date']
            last_used_trade_date = []
            for buydate in buy:
                day_delta = \
                    datetime.datetime.strptime(str(buydate), '%Y%m%d') - \
                    tempdf_trade[(tempdf_trade['认申购金额'] > 0)&(~tempdf_trade['交易日期'].isin(last_used_trade_date))][
                    '交易日期'].to_frame('day_delta')
                day_delta['day_delta'] = [x.days for x in day_delta['day_delta']]

                #condition=day_delta[(day_delta['day_delta']>0)&(day_delta['day_delta']<7)]
                condition=day_delta[(day_delta['day_delta']>0)&((day_delta['day_delta']<=30))]
                condition=( tempdf[tempdf['quant_change'] > 0].set_index('date').loc[buydate][
                      'quant_change']/tempdf_trade.loc[condition.index.tolist()]['申请份额']-1>=-0.15).sum()

                if(condition==0 or len(day_delta)==0):

                    #处理产品分红产生的mv变动
                    tempdf.loc[tempdf['date']==buydate,'revenue']=\
                        tempdf.loc[tempdf['date']==buydate]['revenue_2']
                else:
                    last_used_trade_date.append(tempdf_trade.loc[day_delta[(day_delta['day_delta']>0)].index.tolist()]['交易日期'].iloc[0])


            last_sell_day=19000101
            for selldate in sell:
                day_delta = \
                    datetime.datetime.strptime(str(selldate), '%Y%m%d') - \
                    tempdf_trade[tempdf_trade['投资类型'] =='赎回'][
                    '交易日期'].to_frame('day_delta')
                day_delta['day_delta'] = [x.days for x in day_delta['day_delta']]


                if(((day_delta['day_delta']>0)&(day_delta['day_delta']<30)).sum()==0 or len(day_delta)==0):
                    tempdf.loc[tempdf['date']==selldate,'revenue']=\
                        tempdf.loc[tempdf['date']==selldate]['revenue_2']
                else:

                    tempdf_trade['date_delta']=\
                        [x.days for x in (datetime.datetime.strptime(str(selldate), '%Y%m%d')-tempdf_trade['交易日期'])]

                    #match the right trading &(tempdf_trade['date_delta']<last_sell_day_delta)
                    qrjz=tempdf_trade[(tempdf_trade['赎回份额']>0)
                                      &(tempdf_trade['date_delta']>0)
                                      &(tempdf_trade['赎回份额']/tempdf[tempdf['date']==selldate]['quant_change'].abs().iloc[0]>=0.5)
                                      &(tempdf_trade['赎回份额']/tempdf[tempdf['date']==selldate]['quant_change'].abs().iloc[0]<=1.5)
                                      &(tempdf_trade['date_delta']<=30)].sort_values('date_delta')
                    if(len(qrjz)>0):
                        qrjz=qrjz.loc[(qrjz['赎回份额']+tempdf[tempdf['date']==selldate]['quant_change'].iloc[0]).abs().sort_values().index[0]]['确认净值']
                        tempdf.loc[tempdf['date']==selldate,'revenue']=\
                            tempdf.loc[tempdf['date']==selldate]['revenue_2']+\
                           qrjz*tempdf[tempdf['date']==selldate]['quant_change'].abs()-\
                            tempdf_trade[tempdf_trade['date_delta']>0].fillna(0).sort_values('date_delta').iloc[0]['赎回费']
                    else:
                        tempdf.loc[tempdf['date'] == selldate, 'revenue'] = \
                            tempdf.loc[tempdf['date'] == selldate]['revenue_2']

            tempdf['资产净值_上期'] = [np.nan] + tempdf['资产净值'].iloc[0:-1].tolist()
            tempdf.loc[tempdf['资产净值_上期']==0,'资产净值_上期']=np.nan
            if(jjdm!='1203' and jjdm!='1202' ):
                tempdf['contr'] = tempdf['revenue'] / tempdf['资产净值_上期']
                # tempdf.loc[(tempdf['quant_change'] != 0) & (tempdf['jjdm'] == 0), 'jjdm'] = jjdm
                cont.append(tempdf[['jjdm','date','contr','revenue','revenue_2']])
            elif(jjdm=='1203'):

                tempdf2 = pd.merge(pd.DataFrame(data=hold_df['date'].unique(), columns=['date']),
                                  hold_df[hold_df['jjdm'] == '1002'], how='left', on='date').fillna(0)

                tempdf2['revenue_2_y'] = tempdf2['mv'].diff().to_list()

                tempdf=pd.merge(tempdf,tempdf2[['date','revenue_2_y']],how='left',on='date')

                waiting_edite_df=\
                    tempdf.loc[(tempdf['revenue_2']<0)]
                last_gl_date=19900921
                # to make the contribution of divided from certain product to re assign to the correct asset type
                for gl_date2 in waiting_edite_df['date']:
                    #20201207
                    # print(gl_date2)
                    gl_date = hold_df[hold_df['date'] < gl_date2]['date'].unique()[-1]
                    a = gl_df[(gl_df['date'] == gl_date)]
                    b = gl_df[(gl_df['date'] == gl_date2)]
                    c=pd.merge(a,b,how='left',on='科目代码').fillna(0)
                    c['diff'] = c['市值_x'] - c['市值_y']
                    c=c[c['diff']>0]
                    # gl_target['diff'] = gl_target['市值'] - \
                    #                     waiting_edite_df[waiting_edite_df['date'] == gl_date2]['mv'].iloc[0]
                    # gl_target = gl_target.sort_values('diff').iloc[0]['科目名称']
                    gl_target=c['科目名称_x'].tolist()
                    gl_target=hold_df[(hold_df['jjjc'].isin(gl_target))][['jjdm','jjjc']].drop_duplicates()

                    #to deal with situation that no specific product dividen information is provided and divdend become cash
                    if(len(c)==1 and c['科目代码'].iloc[0]==12032006):

                        quant_change=hold_df.groupby('date')['quant'].sum().diff().to_frame('quant_change')
                        if(quant_change.loc[gl_date2]['quant_change']-
                                trade_data[trade_data['交易日期']==str(gl_date2)]['申请份额'].sum()-trade_data[trade_data['交易日期']==str(gl_date2)]['赎回份额'].sum()):
                            tempdf.loc[(tempdf['date'] == gl_date2), 'revenue_2'] = 0



                    #check if the dividen transfrom to cash

                    for i in range(len(gl_target)):
                        jjjc=gl_target['jjjc'].iloc[i]
                        jjdm = gl_target['jjdm'].iloc[i]

                        if(len(hold_df[(hold_df['date'] == gl_date2)&(hold_df['jjjc']==jjjc)])==0):
                            condition=True
                        elif(hold_df[(hold_df['date'] == gl_date2)&(hold_df['jjjc']==jjjc)]['quant'].iloc[0]-
                                hold_df.loc[(hold_df['date'] == gl_date)&(hold_df['jjjc']==jjjc)]['quant'].iloc[0]==0):
                            condition=True
                        else:
                            condition=False
                        if(condition):

                            tempdf.loc[(tempdf['date'] == gl_date2), 'revenue_2'] = 0

                            real_gl_date=gl_df[(gl_df['科目名称']==jjjc)
                                               &(gl_df['date']<gl_date2)&
                                               (gl_df['date']>last_gl_date)].iloc[0]['date']

                            for info in ['风格偏好', '规模偏好','ejfl', 'jjfl', 'cpfl','二级策略']:
                                hold_df.loc[(hold_df['date'] == real_gl_date)&(hold_df['jjdm'] =='1203'), info] =\
                                    hold_df[(hold_df['date']<=real_gl_date)&(hold_df['jjdm']==jjdm)][info].iloc[-1]

                    last_gl_date=gl_date2
                #tempdf.loc[(tempdf['revenue_2']<0)&((tempdf['revenue_2'].fillna(0).astype(int)+tempdf['revenue_2_y'].fillna(0).astype(int)).abs()<=1000), 'revenue_2'] = 0
                tempdf['contr'] = tempdf['revenue_2'] / tempdf['资产净值_上期']

                cont.append(tempdf[['jjdm','date','contr','revenue','revenue_2']])
        cont =pd.concat(cont,axis=0).sort_values('date')
        hold_df['weight']=hold_df['weight'].astype(str).str.replace('%', '').astype(float) / 100

        hold_df=pd.merge(hold_df,cont,how='left',on=['date','jjdm'])

        # cont=pd.merge(cont,hold_df[['jjdm','jjjc','ejfl','jjfl','cpfl','风格偏好','规模偏好','二级策略']].drop_duplicates('jjdm'),how='left',on=['jjdm'])
        # cont = pd.merge(cont, hold_df[['jjdm',  'weight','date']],how='left', on=['jjdm','date'])
        # cont=cont[cont['jjdm']!=0]

        cont = hold_df[['date', 'jjdm','jjjc', 'contr', 'weight','ejfl','jjfl','cpfl','风格偏好','规模偏好','二级策略']]
        mimic_nav = (cont.groupby('date').sum()['contr'] + 1).cumprod().to_frame('mimic_ret')\
                    * hold_df['累计单位净值'].iloc[0]
        mimic_nav['mimic_ret'] = [np.nan] + mimic_nav['mimic_ret'].iloc[0:-1].tolist()
        cont=pd.merge(cont,mimic_nav,how='left',on=['date'])
        cont['contribute_ret']=cont['contr']*cont['mimic_ret']/hold_df['累计单位净值'].iloc[0]
        cont['contribute_ret'] = cont['contr'] * cont['mimic_ret'] / hold_df['累计单位净值'].iloc[0]

        cont['year']=cont['date'].astype(str).str[0:4]
        year_nav=\
            cont.drop_duplicates('year',keep='last')[['year','mimic_ret']].set_index('year')
        for year in cont['year'].unique()[1:]:
            cont[year] = cont['contr'] * cont['mimic_ret'] / year_nav.loc[str(int(year)-1)]['mimic_ret']

        cont.drop('year',axis=1,inplace=True)

        return hold_df,cont

    def fund_attribution(self,hold_df,holding_time,if_prv):

        total_time= \
            (datetime.datetime.strptime(str(hold_df['date'].iloc[-1]),"%Y%m%d")-\
            datetime.datetime.strptime(str(hold_df['date'].iloc[0]),"%Y%m%d")).days

        total_trade_days=len(hold_df['date'].unique())

        if(if_prv):
            # prv ret
            mu_df = hold_df[hold_df['cpfl'] == '私募基金']
            mu_df['ejfl'] = mu_df['ejfl'].fillna(0).astype(str).str.replace("\.0", '')
            mu_df['jjfl'] = mu_df['jjfl'].fillna(0).astype(str).str.replace("\.0", '')
            jjfl_map = self.prv_jjflmap
            for index in jjfl_map.keys():
                mu_df.loc[mu_df['jjfl'] == index, 'jjfl'] = jjfl_map[index]
            ejfl_map = self.prv_ejflmap
            for index in ejfl_map.keys():
                mu_df.loc[mu_df['ejfl'] == index, 'ejfl'] = ejfl_map[index]

            #get jj ret from start to end
            # sql="select jjdm,jjjz,jzrq from st_hedge.t_st_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'"\
            #     .format(util.list_sql_condition(mu_df['jjdm'].unique().tolist()),
            #             hold_df['date'].iloc[0],hold_df['date'].iloc[-1])
            # nav=hbdb.db2df(sql,db='highuser').sort_values('jzrq')
            # nav=pd.merge(nav.drop_duplicates('jjdm',keep='last')[['jjdm','jjjz']]
            #              ,nav.drop_duplicates('jjdm',keep='first')[['jjdm','jjjz']]
            #              ,how='left',on='jjdm')

        else:

            # mutual ret
            mu_df = hold_df[hold_df['cpfl'] == '公募基金']
            mu_df['ejfl'] = mu_df['ejfl'].fillna(0).astype(str).str.replace("\.0", '')
            mu_df['jjfl'] = mu_df['jjfl'].fillna(0).astype(str).str.replace("\.0", '')
            jjfl_map = self.mu_jjflmap
            for index in jjfl_map.keys():
                mu_df.loc[mu_df['jjfl'] == index, 'jjfl'] = jjfl_map[index]
            ejfl_map = self.mu_ejflmap
            for index in ejfl_map.keys():
                mu_df.loc[mu_df['ejfl'] == index, 'ejfl'] = ejfl_map[index]

            # sql="select jjdm,jjjz,jzrq from st_fund.t_st_gm_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'"\
            #     .format(util.list_sql_condition(mu_df['jjdm'].unique().tolist()),
            #             hold_df['date'].iloc[0],hold_df['date'].iloc[-1])
            # nav=hbdb.db2df(sql,db='funduser').sort_values('jzrq')
            # nav=pd.merge(nav.drop_duplicates('jjdm',keep='last')[['jjdm','jjjz']]
            #              ,nav.drop_duplicates('jjdm',keep='first')[['jjdm','jjjz']]
            #              ,how='left',on='jjdm')

        mu_df['资产净值']=mu_df['资产净值'].astype(str).str.replace(',','').astype(float)
        mu_df['累计份额'] = mu_df['资产净值'] / mu_df['累计单位净值']

        out_df=[]

        for jjdm in mu_df['jjdm'].unique().tolist():

            tempdf=mu_df[mu_df['jjdm']==jjdm]
            tempdf['share_changed']=tempdf['累计份额'].diff()

            tempdf=pd.merge(mu_df[['date']].drop_duplicates('date').sort_values('date')
                            ,tempdf,how='left',on='date')
            tempdf=tempdf[tempdf['jjdm'].notnull()]
            tempdf.reset_index(inplace=True)
            tempdf.loc[0,'first_buy_price']=tempdf.loc[0]['jjjz']
            tempdf['index_diff'] = tempdf['index'].diff()

            for i in range(1,len(tempdf)):

                if(tempdf.loc[i]['index_diff']==1):
                    tempdf.loc[i,'first_buy_price']=tempdf.loc[i-1]['first_buy_price']
                else:
                    tempdf.loc[i, 'first_buy_price'] = tempdf.loc[i]['jjjz']

            for group in tempdf['first_buy_price'].unique().tolist():

                tempdf2=tempdf[tempdf['first_buy_price']==group]
                holding_days=len(tempdf2)
                # tempdf2=tempdf2[(tempdf2['share_changed'].abs()>=500000)
                #                 |(tempdf2['date']==tempdf2['date'].iloc[0])
                #                 |(tempdf2['date']==tempdf2['date'].iloc[-1])]
                # tempdf2['revenue']=tempdf2['value_increased']
                # tempdf2['revenue']=(tempdf2['revenue'].fillna(0).diff()).iloc[1:].tolist()+[np.nan]
                tempdf2['revenue'] = tempdf2['value_increased']
                tempdf2['contribute_ret'] = tempdf2['revenue'] / (tempdf2['累计单位净值'].iloc[0]*tempdf2['累计份额'])

                out_df.append(tempdf2)

                # mu_df.loc[(mu_df['jjdm']==jjdm)&
                #           (mu_df['date']>=tempdf2['date'].min())&
                #           (mu_df['date']<=tempdf2['date'].max()),'revenue'] = tempdf2['revenue'].sum()
                #
                # mu_df.loc[(mu_df['jjdm']==jjdm)&
                #           (mu_df['date']>=tempdf2['date'].min())&
                #           (mu_df['date']<=tempdf2['date'].max()),'contribute_ret'] = tempdf2['contribute_ret'].sum()
                #
                # mu_df.loc[(mu_df['jjdm']==jjdm)&
                #           (mu_df['date']>=tempdf2['date'].min())&
                #           (mu_df['date']<=tempdf2['date'].max()),'holding_days'] = holding_days/total_trade_days
                #
                # mu_df.loc[(mu_df['jjdm']==jjdm)&
                #           (mu_df['date']>=tempdf2['date'].min())&
                #           (mu_df['date']<=tempdf2['date'].max()),'ret'] = \
                #     (tempdf2['jjjz']/tempdf2['first_buy_price']-1).iloc[-1]

        #mu_df.drop_duplicates(['jjdm', 'contribute_ret'])
        out_df=pd.concat(out_df,axis=0)
        return out_df

    @staticmethod
    def attribution_by_class(fund_attribution,index_type_map):

        def attributon_classification(fund_attribution,class_col,class_name):

            statrage_att = fund_attribution.groupby(['date', class_col]).sum()[
                ['contribute_ret', 'weight', 'contr']].reset_index()
            statrage_att['ret'] = (statrage_att['contr'] / statrage_att['weight'] + 1)
            statrage_att['ret'] = statrage_att.groupby(class_col).cumprod()['ret']
            statrage_att = pd.merge(statrage_att.groupby(class_col).sum()[['contribute_ret', 'weight']]
                                    , statrage_att.drop_duplicates(class_col, keep='last')[['ret', class_col]], how='inner',
                                    on=class_col)
            statrage_att['weight'] = statrage_att['weight'] / statrage_att['weight'].sum()
            statrage_att['ret'] = statrage_att['ret'] - 1

            statrage_att.set_index(class_col, inplace=True)
            # plot.plotly_jjpic_bar(statrage_att[['contribute_ret']], class_name+'收益贡献分布')
            # plot.plotly_jjpic_bar(statrage_att[['ret']], class_name+'收益率分布')

            return statrage_att


        statrage_att=attributon_classification(fund_attribution,'yjcl','超一级策略')


        fund_attribution['ejfl'] = [x.replace('灵活配置型', '公募偏股') for x in fund_attribution['ejfl']]
        fund_attribution['ejfl'] = [x.replace('偏股混合型', '公募偏股') for x in fund_attribution['ejfl']]
        fund_attribution['ejfl'] = [x.replace('普通股票型', '公募偏股') for x in fund_attribution['ejfl']]
        stock_asset_jjfl = ['主观多头', '量化多头', '公募偏股']

        plot.plotly_jjpic_bar((fund_attribution[fund_attribution['ejfl'].isin(stock_asset_jjfl
                                                                   )].drop_duplicates('jjdm')).groupby('ejfl').count()['jjdm'].to_frame('持仓数量').sort_values('持仓数量',ascending=False)
                        , '进攻性资产数量分布')

        stock_att = fund_attribution[fund_attribution['ejfl'].isin(stock_asset_jjfl
                                                                   )]
        stock_att=attributon_classification(stock_att, 'ejfl', '进攻性资产')

        index_enhance_att = fund_attribution[fund_attribution['二级策略'].astype(str).str.contains('指数增强')]

        if(len(index_enhance_att)>0):

            plot.plotly_jjpic_bar((index_enhance_att.drop_duplicates('jjdm')).groupby(
                '二级策略').count()['jjdm'].to_frame('持仓数量').sort_values('持仓数量', ascending=False)
                                  , '量化多头资产数量分布')

            index_enhance_att=attributon_classification(index_enhance_att, '二级策略', '量化多头资产')


        style_att=fund_attribution[fund_attribution['ejfl'].isin(['公募偏股','主观多头'])]

        style_att=attributon_classification(style_att, '风格偏好', '成长价值风格')

        size_att = fund_attribution[fund_attribution['ejfl'].isin(['公募偏股', '主观多头'])]
        size_att.loc[size_att['规模偏好'].astype(str).str.contains('大'),'规模偏好']='大'
        size_att.loc[size_att['规模偏好'].astype(str).str.contains('中'),'规模偏好']='中小'
        size_att.loc[size_att['规模偏好'].astype(str).str.contains('小'),'规模偏好']='中小'

        size_att=attributon_classification(size_att, '规模偏好', '市值风格')


        attribution_by_class=[statrage_att,stock_att,index_enhance_att,style_att,size_att]
        attribution_by_class = pd.concat(attribution_by_class, axis=0)


        return  attribution_by_class

    @staticmethod
    def generate_index_enhance_index(start_date,end_date):

        quant_pool_in = \
        pd.read_excel(r"E:\GitFolder\docs\To虚怀\业绩统计(fof&池）\基金池\数据源\量化基金池20231130.xlsx"
                      , sheet_name='量化池列表')[['入池时间', '基金代码', '二级策略']]
        quant_pool_out = \
        pd.read_excel(r"E:\GitFolder\docs\To虚怀\业绩统计(fof&池）\基金池\数据源\量化基金池20231130.xlsx"
                      , sheet_name='出池记录')[['入池时间', '基金代码', '出池时间', '二级策略']]
        quant_pool = pd.concat([quant_pool_out, quant_pool_in], axis=0)
        quant_pool = quant_pool[(quant_pool['二级策略'].isin(['500指数增强', '1000指数增强', '300指数增强']))]
        quant_pool['入池时间'] = quant_pool['入池时间'].astype(str).str.replace('-', '').str[0:6]
        quant_pool['出池时间'] = quant_pool['出池时间'].astype(str).str.replace('-', '').str[0:6]
        quant_pool.drop_duplicates('基金代码', inplace=True)

        sql = "select jjdm,hb1y,tjyf from st_hedge.t_st_sm_yhb where jjdm in ({0}) and tjyf>='{1}' and tjyf<='{2}' and hb1y!=99999" \
            .format(util.list_sql_condition(quant_pool['基金代码'].tolist())
                    ,start_date,end_date)
        quant_pool_nav = hbdb.db2df(sql, db='highuser')
        quant_pool_nav = pd.merge(quant_pool_nav, quant_pool, how='left'
                                  , left_on='jjdm', right_on='基金代码')
        quant_pool_nav = quant_pool_nav[(quant_pool_nav['入池时间'] < quant_pool_nav['tjyf'])
                                        & (quant_pool_nav['出池时间'] >= quant_pool_nav['tjyf'])]
        quant_pool_nav = quant_pool_nav.groupby(['二级策略', 'tjyf']).mean()['hb1y'].to_frame('量化池') / 100

        quant_pool_nav=quant_pool_nav.reset_index().pivot_table('量化池', 'tjyf', '二级策略')

        return (quant_pool_nav+1).cumprod()

    def get_bmk_return(self,start_date,end_date,from_local_db=False):


        # get market mutual index return

        sql = """select zqdm,jyrq,spjg from st_market.t_st_zs_hqql 
        where jyrq>='{0}' and jyrq<='{1}' and zqdm in ('885001','399370','399371','399314','399315','399316','881001','399311','CI0077','H11001')""" \
            .format(str(int(start_date[0:4])-3)+start_date[4:], end_date)

        mu_index_ret = hbdb.db2df(sql, db='alluser').pivot_table('spjg', 'jyrq', 'zqdm')

        mu_index_ret.rename(columns={
                                     '885001':'公募偏股',
                                     '399370':'国证成长',
                                     '399371':'国证价值',
                                     '399314':'国证大盘',
                                     '399315':'国证中盘',
                                     '399316':'国证小盘',
                                     'H11001':'中证全债'},inplace=True)


        for col in mu_index_ret.columns:
            mu_index_ret[col]=mu_index_ret[col]/mu_index_ret[col].iloc[0]

        for col in ['国证大盘', '国证中盘', '国证小盘', '国证成长', '国证价值']:
            mu_index_ret[col+'_累计超额'] = mu_index_ret[col]-mu_index_ret['399311']

        for col in ['公募偏股']:
            mu_index_ret[col+'_累计超额'] = mu_index_ret[col]-mu_index_ret['881001']

        for col in ['国证大盘', '国证中盘', '国证小盘', '国证成长', '国证价值','公募偏股']:
            mu_index_ret[col+'_rank']=mu_index_ret[col+'_累计超额'].rolling(500,1).apply(rolling_rank)
            mu_index_ret.drop(col+'_累计超额',axis=1,inplace=True)


        sql = """select zsdm,jyrq,spjg from st_hedge.t_st_sm_zhmzs 
        where jyrq>='{0}' and jyrq<='{1}' and zsdm in ('HB0018','HB1001','HB1002','HB0011')""" \
            .format(str(int(start_date[0:4])-3)+start_date[4:], end_date)

        # howbuy_index_ret = hbdb.db2df(sql, db='highuser').pivot_table('spjg', 'jyrq', 'zsdm').fillna(1000)
        howbuy_index_ret=pd.read_excel(r"E:\FOF分析\bmk所用指数_扣完业绩报酬周净值.xlsx")
        howbuy_index_ret['jyrq']=howbuy_index_ret['Unnamed: 0'].astype(str)
        howbuy_index_ret=(howbuy_index_ret[(howbuy_index_ret['jyrq']>=str(int(start_date[0:4])-3)+start_date[4:])
                                          &(howbuy_index_ret['jyrq']<=end_date)]).set_index('jyrq').drop('Unnamed: 0',axis=1)



        howbuy_index_ret.rename(columns={'5亿CTA指数':'CTA',
                                     'HB1001':'主观多头',
                                     'HB1002':'量化多头',
                                     'HB0011':'好买股票'},inplace=True)
        mu_index_ret.index=mu_index_ret.index.astype(str)
        for col in howbuy_index_ret.columns:
            howbuy_index_ret[col]=howbuy_index_ret[col]/howbuy_index_ret[col].iloc[0]

        # howbuy_index_ret=pd.merge(howbuy_index_ret,mu_index_ret[['881001']],how='left',
        #                           left_index=True,right_index=True)

        for col in howbuy_index_ret.columns:
            howbuy_index_ret[col]=howbuy_index_ret[col]/howbuy_index_ret[col].iloc[0]

        for col in ['CTA', '主观多头', '量化多头']:
            howbuy_index_ret[col+'_累计超额'] = howbuy_index_ret[col]-howbuy_index_ret['好买股票']

        for col in ['CTA', '主观多头', '量化多头']:
            howbuy_index_ret[col+'_rank']=howbuy_index_ret[col+'_累计超额'].rolling(100,1).apply(rolling_rank)
            howbuy_index_ret.drop(col+'_累计超额',axis=1,inplace=True)

        # howbuy_index_ret.drop('881001', axis=1, inplace=True)
        howbuy_index_ret=howbuy_index_ret.loc[start_date:]

        mu_index_ret=mu_index_ret.loc[start_date:]


        index_enhance_index = \
            self.generate_index_enhance_index(str(int(start_date[0:4])-3)+start_date[4:6]
                                              , str(end_date)[0:6])
        for col in index_enhance_index.columns.tolist():
            index_enhance_index[col+'_rank']=index_enhance_index[col].rolling(24,1).apply(rolling_rank)

        index_enhance_index=index_enhance_index.loc[str(start_date)[0:4]:]


        return  howbuy_index_ret,mu_index_ret,index_enhance_index


    @staticmethod
    def brinson_wise_analysis(fund_attribution,dir,howbuy_index_ret
                              , mu_index_ret, index_enhance_index
                              ,stock_bmk_w=None,bond_bmk_w=None,CTA_bmk_w=None):

        ret_cont_his_table=[]
        ret_his_table=[]

        def get_vol_contribution(weight_by_year, std_by_year, std_summary, corrbyyear, corr):

            vol_cont = weight_by_year.copy()
            for col in vol_cont.columns.tolist():
                for year in weight_by_year[weight_by_year[col].notnull()].index.tolist():
                    temp_value = np.power(weight_by_year.loc[year][col], 2) * \
                                 np.power(std_by_year.loc[year][col + 'FOF收益率'], 2)
                    asset_list = vol_cont.loc[year][vol_cont.loc[year].notnull()].index.tolist()
                    asset_list.remove(col)
                    for asset in asset_list:
                        temp_value += weight_by_year.loc[year][col] * \
                                      weight_by_year.loc[year][asset] * \
                                      corrbyyear.loc[year, asset + 'FOF收益率'][col + 'FOF收益率'] * \
                                      std_by_year.loc[year][col + 'FOF收益率'] * \
                                      std_by_year.loc[year][asset + 'FOF收益率']

                    vol_cont.loc[year, col] = temp_value
                year = '全时期'
                temp_value = np.power(weight_by_year.mean(axis=0)[col], 2) * \
                             np.power(std_summary.loc[col + 'FOF']['年化波动率'], 2)
                for asset in asset_list:
                    temp_value += weight_by_year.mean(axis=0)[col] * \
                                  weight_by_year.mean(axis=0)[asset] * \
                                  corr.loc[asset + 'FOF收益率'][col + 'FOF收益率'] * \
                                  std_summary.loc[col + 'FOF']['年化波动率'] * \
                                  std_summary.loc[asset + 'FOF']['年化波动率']
                vol_cont.loc[year, col] = temp_value

            return vol_cont

        #calculate ideal asset weight by BLM assumption that all asset allocation submit to mean variance model


        prv_stock_ret= \
            (np.power((howbuy_index_ret['主观多头'].iloc[-1]/ howbuy_index_ret['主观多头'].iloc[0])
                     ,52/len(howbuy_index_ret))-1)

        mu_stock_ret= \
            (np.power((mu_index_ret['公募偏股'].iloc[-1]/ mu_index_ret['公募偏股'].iloc[0])
                     ,250/len(mu_index_ret))-1)

        prv_quant_ret= \
            (np.power((howbuy_index_ret['量化多头'].iloc[-1]/ howbuy_index_ret['量化多头'].iloc[0])
                     ,52/len(howbuy_index_ret))-1)

        if (prv_stock_ret < 0 or mu_stock_ret < 0 or prv_quant_ret < 0):

            min_ret=np.min([prv_stock_ret,mu_stock_ret,prv_quant_ret])
            prv_stock_ret=prv_stock_ret-min_ret+0.03
            mu_stock_ret = mu_stock_ret - min_ret+0.03
            prv_quant_ret = prv_quant_ret - min_ret+0.03

        if(stock_bmk_w is None):
            stock_ret = \
                (np.power((howbuy_index_ret['HB0011'].iloc[-1] / howbuy_index_ret['HB0011'].iloc[0])
                          , 52 / len(howbuy_index_ret)) - 1)
            CTA_ret = \
                (np.power((howbuy_index_ret['CTA'].iloc[-1] / howbuy_index_ret['CTA'].iloc[0])
                          , 52 / len(howbuy_index_ret)) - 1)
            bond_ret = \
                (np.power((mu_index_ret['CBA00301'].iloc[-1] / mu_index_ret['CBA00301'].iloc[0])
                          , 250 / len(mu_index_ret)) - 1)

            if (stock_ret < 0 or CTA_ret < 0 or bond_ret < 0):
                min_ret = np.min([stock_ret, CTA_ret, bond_ret])
                stock_ret = stock_ret - min_ret + 0.03
                CTA_ret = CTA_ret - min_ret + 0.03
                bond_ret = bond_ret - min_ret + 0.03

            stock_sharp= \
                stock_ret/\
                (howbuy_index_ret['好买股票'].pct_change().std()*np.sqrt(52))

            CTA_sharp= \
                CTA_ret/\
                (howbuy_index_ret['CTA'].pct_change().std()*np.sqrt(52))

            bond_sharp= \
                bond_ret/\
                (mu_index_ret['CBA00301'].pct_change().std()*np.sqrt(250))

            total_sharp = stock_sharp + CTA_sharp + bond_sharp
            stock_bmk_w = stock_sharp / total_sharp
            bond_bmk_w = bond_sharp / total_sharp
            CTA_bmk_w = CTA_sharp / total_sharp

        prv_stock_sharp= \
            prv_stock_ret/\
            (howbuy_index_ret['主观多头'].pct_change().std()*np.sqrt(52))

        mu_stock_sharp= \
            mu_stock_ret/\
            (mu_index_ret['公募偏股'].pct_change().std()*np.sqrt(250))

        prv_quant_sharp= \
            prv_quant_ret/\
            (howbuy_index_ret['量化多头'].pct_change().std()*np.sqrt(52))


        total_sharp=prv_stock_sharp+mu_stock_sharp+prv_quant_sharp
        prv_stock_bmk_w=prv_stock_sharp/total_sharp
        mu_stock_bmk_w = mu_stock_sharp / total_sharp
        prv_quant_bmk_w = prv_quant_sharp / total_sharp



        #make all index monthly
        #
        # index_std=pd.concat([howbuy_index_ret[['HB0011', 'CTA', '主观多头', '量化多头']].pct_change().std()*np.sqrt(52),
        #                      mu_index_ret[['公募偏股',
        #                                    'CBA00301']].pct_change().std() * np.sqrt(365),
        #                      index_enhance_index[['1000指数增强', '300指数增强', '500指数增强']].pct_change().std()*np.sqrt(12)
        #                      ],axis=0).to_frame('波动率')
        # index_std.index=['进攻性资产市场','CTA资产市场','主观多头市场','量化多头市场','公募偏股市场',
        #                  '稳健性资产市场','1000指数增强市场','300指数增强市场','500指数增强市场']

        mu_index_ret = pd.merge(mu_index_ret[['399311', '国证大盘', '国证中盘', '国证小盘', '国证成长', '国证价值', '中证全债', '公募偏股',
        'CI0077']], howbuy_index_ret[['好买股票', 'CTA', '主观多头', '量化多头']],
                                how='left', on='jyrq')
        mu_index_ret['tjyf']=mu_index_ret.index.astype(str).str[0:6]
        index_enhance_index=pd.merge(mu_index_ret.reset_index(drop=False)[['jyrq', 'tjyf']].drop_duplicates('tjyf', keep='last'),
                 index_enhance_index[['1000指数增强', '300指数增强', '500指数增强']], how='left', on='tjyf')
        mu_index_ret = pd.merge(mu_index_ret, index_enhance_index[['1000指数增强', '300指数增强', '500指数增强','jyrq']],
                                how='left', on='jyrq')

        index_std = mu_index_ret[['公募偏股',
                                  '中证全债', '好买股票', 'CTA', '主观多头', '量化多头', '1000指数增强', '300指数增强',
                                  '500指数增强']].pct_change().fillna(0)+1
        index_std['tjyf'] = mu_index_ret['tjyf']
        index_std = index_std.groupby('tjyf').cumprod()
        index_std['tjyf'] = mu_index_ret['tjyf']
        index_std_by_year=(index_std.drop_duplicates('tjyf', keep='last').set_index('tjyf')-1)
        index_std=\
            (index_std_by_year.std()*np.sqrt(12)).to_frame('年化波动率')
        index_std.index=['公募偏股市场', '稳健性资产市场','进攻性资产市场','CTA资产市场','主观多头市场','量化多头市场',
                        '1000指数增强市场','300指数增强市场','500指数增强市场']
        index_std_by_year['year']=index_std_by_year.index.str[0:4]
        index_std_by_year=index_std_by_year.groupby('year').std()*np.sqrt(12)
        index_std_by_year.columns=['公募偏股市场', '稳健性资产市场','进攻性资产市场','CTA资产市场','主观多头市场','量化多头市场',
                        '1000指数增强市场','300指数增强市场','500指数增强市场']

        index_std_by_year.to_excel(dir.replace('基金持仓数据', '市场年度波动率'))


        # interpolation for all index
        for indexname in ['好买股票', 'CTA',
       '主观多头', '量化多头','1000指数增强', '300指数增强', '500指数增强',]:
            # print(indexname)
            temp = mu_index_ret[indexname].reset_index(drop=True)
            tempnotnull=temp[temp.notnull()]
            f = interpolate.interp1d(tempnotnull.index.values, tempnotnull.values, kind='cubic')
            ynew = f(temp.iloc[tempnotnull.index[0]:tempnotnull.index[-1]].index.values)
            temp.loc[tempnotnull.index[0]:tempnotnull.index[-1]-1]=ynew
            temp.loc[0:tempnotnull.index[0]]=tempnotnull.iloc[0]
            temp.loc[tempnotnull.index[-1]:] = tempnotnull.iloc[-1]
            mu_index_ret[indexname]=temp.values

        for col in ['CTA','主观多头','量化多头','公募偏股','好买股票','中证全债'
            ,'1000指数增强', '300指数增强', '500指数增强']:

            mu_index_ret[col]=mu_index_ret[col].pct_change().fillna(0)

        index_ret_monthly=mu_index_ret[['jyrq','CTA','主观多头','量化多头'
            ,'公募偏股','好买股票','中证全债','1000指数增强', '300指数增强', '500指数增强']].rename(columns={'jyrq':'date'})

        # big asset return reasoning
        day_len=len(fund_attribution['date'].unique())

        equit_att = \
            fund_attribution.groupby(
                ['date', 'yjcl']).sum().reset_index()

        cont_his=equit_att.pivot_table('contribute_ret','date', 'yjcl').cumsum()
        cont_his.index=cont_his.index.astype(str)
        ret_cont_his_table.append(cont_his)
        # plot.plotly_line_style(cont_his, '超一级资产贡献时序')
        equit_att['year']=equit_att['date'].astype(str).str[0:4]
        year_list=equit_att['year'].unique().tolist()[1:]
        cont_his_byyear=equit_att.groupby(['year','yjcl']).sum()[['contribute_ret']+year_list].reset_index()
        for year in  year_list:
            cont_his_byyear.loc[cont_his_byyear['year']==year,'contribute_ret']=\
                cont_his_byyear[cont_his_byyear['year']==year][year]
        cont_his_byyear=cont_his_byyear.pivot_table('contribute_ret', 'year', 'yjcl').rename(
            columns={'CTA': 'CTA资产'})
        cont_his_byyear['合计']=cont_his_byyear.sum(axis=1)
        equit_att=equit_att.drop('year',axis=1)

        #using weight of last valuation day instead of the same day as contr
        # weight_2=[]
        # for yjfl in equit_att['yjcl'].unique():
        #     temp_w=equit_att[equit_att['yjcl']==yjfl]
        #     temp_w['weight_2'] =[temp_w['weight'].iloc[0]]+temp_w['weight'].iloc[0:-1].tolist()
        #     weight_2.append(temp_w[['date','yjcl','weight_2']])
        # weight_2=pd.concat(weight_2,axis=0)
        # equit_att=pd.merge(equit_att,weight_2,how='left',on=['date','yjcl'])
        #
        # equit_att['ret'] = equit_att['contr'] / equit_att['weight_2']
        equit_att['ret'] = equit_att['contr'] / equit_att['weight']
        equit_att = equit_att.reset_index()
        equit_att = pd.merge(equit_att,
                             equit_att.groupby('date').sum()[['weight']].rename(columns={'weight': 'total_weight'}),
                             how='left', on='date')
        equit_att['weight'] = equit_att['weight'] / equit_att['total_weight']

        missing_asset_type=list(set(['进攻性资产', 'CTA', '稳健性资产']).difference(equit_att['yjcl'].unique()))
        equit_att = pd.merge(equit_att.pivot_table('ret', 'date', 'yjcl')
                             , equit_att.pivot_table('weight', 'date', 'yjcl')
                             , how='left', on='date')

        for asset_type in missing_asset_type:
            equit_att[asset_type+'_x']=np.nan
            equit_att[asset_type + '_y'] = np.nan

        equit_att.index=equit_att.index.astype(str)
        equit_att = pd.merge(equit_att, index_ret_monthly, how='left', on='date')

        # arrange the bmk weight
        equit_att['进攻性资产bmk_w'] = stock_bmk_w
        equit_att['CTAbmk_w'] = CTA_bmk_w
        equit_att['稳健性资产bmk_w'] = bond_bmk_w

        # return allocation
        total_extra_ret = (equit_att[['进攻性资产_x', 'CTA_x', '稳健性资产_x']].fillna(0).values * equit_att[
            ['进攻性资产_y', 'CTA_y', '稳健性资产_y']].fillna(0).values \
                           - equit_att[['好买股票', 'CTA', '中证全债']].fillna(0).values * equit_att[
                               ['进攻性资产bmk_w', 'CTAbmk_w', '稳健性资产bmk_w']].values).sum(axis=1)
        allocation_extraret = ((equit_att[['进攻性资产_y', 'CTA_y', '稳健性资产_y']].fillna(0).values - \
                                equit_att[['进攻性资产bmk_w', 'CTAbmk_w', '稳健性资产bmk_w']].values) * equit_att[
                                   ['好买股票', 'CTA', '中证全债']].fillna(0).values).sum(axis=1)
        selection_extraret = pd.DataFrame(data=(equit_att[['进攻性资产bmk_w', 'CTAbmk_w', '稳健性资产bmk_w']].values * (
                    equit_att[['进攻性资产_x', 'CTA_x', '稳健性资产_x']].values -
                    equit_att[['好买股票', 'CTA', '中证全债']].fillna(0).values))).fillna(0).sum(axis=1)
        brinson_his = pd.DataFrame()
        brinson_his['date'] = equit_att['date'].tolist()
        brinson_his['总超额'] = total_extra_ret
        brinson_his['配置收益'] = allocation_extraret
        brinson_his['择基收益'] = selection_extraret.values.tolist()
        brinson_his['其他收益'] = brinson_his['总超额'] - brinson_his['配置收益'] - brinson_his['择基收益']
        brinson_his.set_index('date', inplace=True)
        brinson_his = (brinson_his+1).cumprod()-1

        # plot.plotly_line_style(brinson_his, '超一级资产收益拆解')
        equit_att.rename(columns={'进攻性资产_y': '进攻性资产FOF配置权重',
                                  'CTA_y': 'CTA资产FOF配置权重',
                                  '稳健性资产_y': '稳健性资产FOF配置权重',
                                  '进攻性资产bmk_w': '进攻性资产市场隐含权重',
                                  '稳健性资产bmk_w': '稳健性资产市场隐含权重',
                                  'CTAbmk_w': 'CTA资产市场隐含权重',
                                  '好买股票': '进攻性资产指数收益率',
                                  '中证全债': '稳健性资产指数收益率',
                                  'CTA': 'CTA资产指数收益率',
                                  '进攻性资产_x': '进攻性资产FOF收益率',
                                  '稳健性资产_x': '稳健性资产FOF收益率',
                                  'CTA_x': 'CTA资产FOF收益率',
                                  }, inplace=True)

        brinson_his.to_excel(dir.replace('基金持仓数据', '超一级资产brinsion数据'), index=True)
        equit_att = equit_att.set_index('date')
        # plot.plotly_line_style(equit_att[['进攻性资产FOF配置权重',
        #                                   'CTA资产FOF配置权重', '稳健性资产FOF配置权重', '进攻性资产市场隐含权重',
        #                                   '稳健性资产市场隐含权重', 'CTA资产市场隐含权重']], '超一级资产配置权重对比')

        #make sure that bmk return is consitent with product return date
        for col in cont_his_byyear.columns[:-1].tolist():
            equit_att.loc[equit_att[col + 'FOF收益率'].isnull(), col + '指数收益率'] = np.nan
            cont_his_byyear[col]=cont_his_byyear[col].map("{:.2%}".format)
        cont_his_byyear['合计'] = cont_his_byyear['合计'].map("{:.2%}".format)

        weight_summary=(equit_att[['CTA资产FOF配置权重',
       '稳健性资产FOF配置权重', '进攻性资产FOF配置权重','进攻性资产市场隐含权重', 'CTA资产市场隐含权重',
       '稳健性资产市场隐含权重']].mean()).to_frame('平均配置权重').sort_index()
        weight_summary.index=[x.replace('配置权重','') for x in weight_summary.index]
        weight_summary.index = [x.replace('隐含权重', '') for x in weight_summary.index]
        cont_summary=cont_his.iloc[-1].to_frame('收益贡献')
        cont_summary.index=[x.replace('CTA','CTA资产') for x in cont_summary.index]
        cont_summary.index = [x+'FOF' for x in cont_summary.index]

        equit_att[['进攻性资产FOF收益率', '稳健性资产FOF收益率',
                   'CTA资产FOF收益率', '进攻性资产指数收益率', 'CTA资产指数收益率', '稳健性资产指数收益率']] = \
            (equit_att[['进攻性资产FOF收益率', '稳健性资产FOF收益率',
                        'CTA资产FOF收益率', '进攻性资产指数收益率', 'CTA资产指数收益率', '稳健性资产指数收益率']].fillna(0) + 1).cumprod()

        ret_his_table.append(equit_att[['进攻性资产FOF收益率', '稳健性资产FOF收益率',
                   'CTA资产FOF收益率', '进攻性资产指数收益率', 'CTA资产指数收益率', '稳健性资产指数收益率']])

        # equit_att[['进攻性资产FOF收益率', '稳健性资产FOF收益率',
        #            'CTA资产FOF收益率', '进攻性资产指数收益率', 'CTA资产指数收益率', '稳健性资产指数收益率']]\
        #     .to_excel(dir.replace('基金持仓数据', '超一级资产收益率对比'),index=True)
        # plot.plotly_line_style(equit_att[['进攻性资产FOF收益率', '稳健性资产FOF收益率',
        #                                   'CTA资产FOF收益率', '进攻性资产指数收益率', 'CTA资产指数收益率', '稳健性资产指数收益率']], '超一级资产收益率对比')

        ret_summary = equit_att[['进攻性资产FOF收益率', '稳健性资产FOF收益率',
                                 'CTA资产FOF收益率', '进攻性资产指数收益率',
                                 'CTA资产指数收益率', '稳健性资产指数收益率']]

        ret_summary['year']=ret_summary.index.astype(str).str[0:4]
        corrbyyear=(ret_summary[['进攻性资产FOF收益率', '稳健性资产FOF收益率',
                                 'CTA资产FOF收益率','year']].set_index('year').pct_change()).groupby('year').corr()
        corr=(ret_summary[['进攻性资产FOF收益率', '稳健性资产FOF收益率',
                                 'CTA资产FOF收益率']].pct_change()).corr()

        ret_byyear=ret_summary.drop_duplicates('year',keep='last').drop('year',axis=1)
        ret_byyear=pd.concat([ret_byyear.iloc[[0]]-1,ret_byyear.pct_change().iloc[1:]],axis=0)
        ret_byyear.columns = [x.replace('收益率', '') for x in ret_byyear.columns]
        ret_byyear.columns = [x.replace('指数', '市场') for x in ret_byyear.columns]
        ret_byyear=ret_byyear[ret_byyear.columns.sort_values().tolist()]

        ret_summary.drop('year',axis=1,inplace=True)
        ret_summary=ret_summary.iloc[-1].to_frame('年化收益率').sort_index()-1
        ret_summary.index=[x.replace('收益率','') for x in ret_summary.index]
        ret_summary.index = [x.replace('指数', '市场') for x in ret_summary.index]
        ret_summary=np.power((ret_summary['年化收益率'] + 1), 250 / day_len) - 1

        equit_att=\
            equit_att[['CTA资产FOF收益率', '稳健性资产FOF收益率', '进攻性资产FOF收益率']].pct_change().fillna(0)+1
        equit_att['tjyf']=equit_att.index.astype(str).str[0:6]

        std_by_year=(equit_att.set_index('tjyf').groupby('tjyf').cumprod())\
            .reset_index().drop_duplicates('tjyf',keep='last')
        std_summary=((std_by_year.drop('tjyf',axis=1)-1).std()
                     * np.sqrt(12)).to_frame('年化波动率')

        std_by_year['year'] = std_by_year['tjyf'].str[0:4]
        std_by_year=\
            (std_by_year.drop('tjyf', axis=1).set_index('year')-1).groupby('year').std()*np.sqrt(12)
        std_summary.index = [x.replace('收益率', '') for x in std_summary.index]
        std_summary = pd.concat([std_summary, index_std.loc[['进攻性资产市场', 'CTA资产市场', '稳健性资产市场']]], axis=0)

        weight_by_year = \
            (fund_attribution.groupby(['date', 'yjcl']).sum()[['weight']].reset_index())
        weight_by_year['year'] = weight_by_year['date'].astype(str).str[0:4]
        weight_by_year=\
            (weight_by_year.groupby(['year', 'yjcl']).mean()[['weight']].reset_index()).pivot_table('weight', 'year',
                                                                                        'yjcl')

        weight_by_year.rename(columns={'CTA':'CTA资产'},inplace=True)
        vol_cont=get_vol_contribution(weight_by_year,std_by_year,std_summary,corrbyyear,corr)


        summary=pd.concat([ret_summary,std_summary,weight_summary,cont_summary],axis=1)
        summary['夏普比率'] = summary['年化收益率'] / summary['年化波动率']
        for col in summary.columns:
            summary[col]=summary[col].map("{:.2%}".format)
        for col in ret_byyear.columns:
            ret_byyear[col] = ret_byyear[col].map("{:.2%}".format)

        # pd.concat([summary.sort_index().reset_index(drop=False)
        #               ,cont_his_byyear.sort_index().reset_index(drop=False).rename(columns={'year':'年份'}),
        #            ret_byyear.sort_index().reset_index(drop=False).rename(columns={'date':'日期'})
        #               ,vol_cont.reset_index(drop=False),std_by_year.reset_index(drop=False)],axis=1)\
        #     .to_excel(dir.replace('基金持仓数据', '超一级策略数据汇总'))


        # equit asset return reasoning

        equit_att = \
            (fund_attribution[fund_attribution['ejfl'].isin(['主观多头'
                                                               , '量化多头', '公募偏股'])].groupby(['date','ejfl']).sum()).reset_index()

        if(len(equit_att)>0):
            cont_his=equit_att.pivot_table('contribute_ret','date', 'ejfl').cumsum()
            cont_his.index=cont_his.index.astype(str)
            ret_cont_his_table.append(cont_his)
            # cont_his.to_excel(dir.replace('基金持仓数据', '超一级资产收益贡献时序'),index=True)
            # plot.plotly_line_style(cont_his, '进攻资产贡献时序')
            equit_att['year']=equit_att['date'].astype(str).str[0:4]
            year_list=equit_att['year'].unique().tolist()[1:]
            cont_his_byyear=equit_att.groupby(['year','ejfl']).sum()[['contribute_ret']+year_list].reset_index()
            for year in  year_list:
                cont_his_byyear.loc[cont_his_byyear['year']==year,'contribute_ret']=\
                    cont_his_byyear[cont_his_byyear['year']==year][year]
            cont_his_byyear=cont_his_byyear.pivot_table('contribute_ret', 'year', 'ejfl')
            cont_his_byyear['合计']=cont_his_byyear.sum(axis=1)
            equit_att=equit_att.drop('year',axis=1)

            #using weight of last valuation day instead of the same day as contr
            # weight_2=[]
            # for yjfl in equit_att['ejfl'].unique():
            #     temp_w=equit_att[equit_att['ejfl']==yjfl]
            #     temp_w['weight_2'] =[temp_w['weight'].iloc[0]]+temp_w['weight'].iloc[0:-1].tolist()
            #     weight_2.append(temp_w[['date','ejfl','weight_2']])
            # weight_2=pd.concat(weight_2,axis=0)
            # equit_att=pd.merge(equit_att,weight_2,how='left',on=['date','ejfl'])
            #equit_att['ret']=equit_att['contr']/equit_att['weight_2']

            equit_att['ret'] = equit_att['contr'] / equit_att['weight']
            equit_att=equit_att.reset_index()
            equit_att=pd.merge(equit_att,
                               equit_att.groupby('date').sum()[['weight']].rename(columns={'weight':'total_weight'}),
                               how='left',on='date')
            equit_att['weight'] = equit_att['weight'] / equit_att['total_weight']

            missing_asset_type = list(set(['主观多头', '量化多头','公募偏股']).difference(equit_att['ejfl'].unique()))
            equit_att=pd.merge(equit_att.pivot_table('ret','date','ejfl')
                     ,equit_att.pivot_table('weight','date','ejfl')
                     ,how='left',on='date')
            for asset_type in missing_asset_type:
                equit_att[asset_type+'_x']=np.nan
                equit_att[asset_type + '_y'] = np.nan


            equit_att.index = equit_att.index.astype(str)
            equit_att=pd.merge(equit_att,index_ret_monthly,how='left',on='date')

            # arrange the bmk weight
            equit_att['主观多头bmk_w'] = prv_stock_bmk_w
            equit_att['量化股票bmk_w'] = prv_quant_bmk_w
            equit_att['公募偏股bmk_w'] = mu_stock_bmk_w

            for col in cont_his_byyear.columns[:-1]:
                equit_att.loc[equit_att[col+'_x'].isnull(),col+'_x']=equit_att[equit_att[col+'_x'].isnull()][col]
                cont_his_byyear[col] = cont_his_byyear[col].map("{:.2%}".format)
            cont_his_byyear['合计'] = cont_his_byyear['合计'].map("{:.2%}".format)

            # return allocation
            total_extra_ret=(equit_att[['主观多头_x', '量化多头_x', '公募偏股_x']].fillna(0).values * equit_att[['主观多头_y', '量化多头_y', '公募偏股_y']].fillna(0).values \
            -equit_att[['主观多头', '量化多头', '公募偏股']].fillna(0).values * equit_att[['主观多头bmk_w', '量化股票bmk_w', '公募偏股bmk_w']].values).sum(axis=1)
            allocation_extraret = ((equit_att[['主观多头_y', '量化多头_y','公募偏股_y']].fillna(0).values-\
                                  equit_att[['主观多头bmk_w', '量化股票bmk_w', '公募偏股bmk_w']].values)*equit_att[['主观多头', '量化多头', '公募偏股']].fillna(0).values).sum(axis=1)
            selection_extraret=pd.DataFrame(data=(equit_att[['主观多头bmk_w', '量化股票bmk_w', '公募偏股bmk_w']].values * (equit_att[['主观多头_x','量化多头_x', '公募偏股_x' ]].values-
                                                                                              equit_att[['主观多头', '量化多头', '公募偏股']].fillna(0).values))).fillna(0).sum(axis=1)
            brinson_his=pd.DataFrame()
            brinson_his['date']=equit_att['date'].tolist()
            brinson_his['总超额'] =total_extra_ret
            brinson_his['配置收益'] =allocation_extraret
            brinson_his['择基收益'] = selection_extraret.values.tolist()
            brinson_his['其他收益'] =brinson_his['总超额']-brinson_his['配置收益']-brinson_his['择基收益']
            brinson_his.set_index('date',inplace=True)
            brinson_his = (brinson_his + 1).cumprod() - 1

            # plot.plotly_line_style(brinson_his,'进攻性资产收益拆解')
            equit_att.rename(columns={'主观多头_y':'主观多头FOF配置权重',
                                      '公募偏股_y':'公募偏股FOF配置权重',
                                      '量化多头_y':'量化多头FOF配置权重',
                                      '主观多头bmk_w':'主观多头市场隐含权重',
                                      '量化股票bmk_w':'量化多头市场隐含权重',
                                      '公募偏股bmk_w':'公募偏股市场隐含权重',
                                      '主观多头':'主观多头指数收益率',
                                      '量化多头':'量化多头指数收益率',
                                      '公募偏股':'公募偏股指数收益率',
                                      '主观多头_x':'主观多头FOF收益率',
                                      '量化多头_x':'量化多头FOF收益率',
                                      '公募偏股_x':'公募偏股FOF收益率',
                                      },inplace=True)

            brinson_his.to_excel(dir.replace('基金持仓数据', '进攻性资产brinsion数据'),index=True)
            equit_att=equit_att.set_index('date')
           #  plot.plotly_line_style(equit_att[['主观多头FOF配置权重',
           # '公募偏股FOF配置权重', '量化多头FOF配置权重','主观多头市场隐含权重',
           #                                    '量化多头市场隐含权重', '公募偏股市场隐含权重']], '进攻性资产配置权重对比')


            weight_summary = (equit_att[['量化多头FOF配置权重',
                                         '公募偏股FOF配置权重', '主观多头FOF配置权重', '量化多头市场隐含权重', '公募偏股市场隐含权重',
                                         '主观多头市场隐含权重']].mean()).to_frame('平均配置权重').sort_index()
            weight_summary.index = [x.replace('配置权重', '') for x in weight_summary.index]
            weight_summary.index = [x.replace('隐含权重', '') for x in weight_summary.index]
            cont_summary = cont_his.iloc[-1].to_frame('收益贡献')

            cont_summary.index = [x + 'FOF' for x in cont_summary.index]

            equit_att[['主观多头FOF收益率', '量化多头FOF收益率',
                       '公募偏股FOF收益率', '主观多头指数收益率', '公募偏股指数收益率', '量化多头指数收益率']]=\
                (equit_att[['主观多头FOF收益率', '量化多头FOF收益率',
                       '公募偏股FOF收益率', '主观多头指数收益率', '公募偏股指数收益率', '量化多头指数收益率']].fillna(0) + 1).cumprod()

            ret_his_table.append(equit_att[['主观多头FOF收益率', '量化多头FOF收益率',
           '公募偏股FOF收益率','主观多头指数收益率', '公募偏股指数收益率', '量化多头指数收益率']])
           #  equit_att[['主观多头FOF收益率', '量化多头FOF收益率',
           # '公募偏股FOF收益率','主观多头指数收益率', '公募偏股指数收益率', '量化多头指数收益率']]\
           #      .to_excel(dir.replace('基金持仓数据', '进攻性资产收益率对比'),index=True)
           #  plot.plotly_line_style(equit_att[['主观多头FOF收益率', '量化多头FOF收益率',
           # '公募偏股FOF收益率','主观多头指数收益率', '公募偏股指数收益率', '量化多头指数收益率']], '进攻性资产收益率对比')

            ret_summary=equit_att[['量化多头FOF收益率', '公募偏股FOF收益率',
                       '主观多头FOF收益率', '量化多头指数收益率',
                                   '主观多头指数收益率', '公募偏股指数收益率']]
            ret_summary['year']=ret_summary.index.astype(str).str[0:4]

            corrbyyear=(ret_summary[['主观多头FOF收益率', '公募偏股FOF收益率', '量化多头FOF收益率','year']].set_index('year').pct_change()).groupby('year').corr()
            corr=(ret_summary[['主观多头FOF收益率', '公募偏股FOF收益率', '量化多头FOF收益率']].pct_change()).corr()

            ret_byyear=ret_summary.drop_duplicates('year',keep='last').drop('year',axis=1)
            ret_byyear=pd.concat([ret_byyear.iloc[[0]]-1,ret_byyear.pct_change().iloc[1:]],axis=0)
            ret_byyear.columns = [x.replace('收益率', '') for x in ret_byyear.columns]
            ret_byyear.columns = [x.replace('指数', '市场') for x in ret_byyear.columns]
            ret_byyear = ret_byyear[ret_byyear.columns.sort_values().tolist()]

            ret_summary.drop('year',axis=1,inplace=True)
            ret_summary=ret_summary.iloc[-1].to_frame('年化收益率').sort_index()-1
            ret_summary.index=[x.replace('收益率','') for x in ret_summary.index]
            ret_summary.index = [x.replace('指数', '市场') for x in ret_summary.index]
            ret_summary = np.power((ret_summary['年化收益率'] + 1), 250 / day_len) - 1

            equit_att=\
                equit_att[['主观多头FOF收益率', '公募偏股FOF收益率', '量化多头FOF收益率']].pct_change().fillna(0)+1
            equit_att['tjyf']=equit_att.index.astype(str).str[0:6]

            std_by_year = (equit_att.set_index('tjyf').groupby('tjyf').cumprod()) \
                .reset_index().drop_duplicates('tjyf', keep='last')
            std_summary = ((std_by_year.drop('tjyf', axis=1) - 1).std()
                           * np.sqrt(12)).to_frame('年化波动率')

            std_by_year['year'] = std_by_year['tjyf'].str[0:4]
            std_by_year = \
                (std_by_year.drop('tjyf', axis=1).set_index('year') - 1).groupby('year').std() * np.sqrt(12)
            std_summary.index = [x.replace('收益率', '') for x in std_summary.index]
            std_summary=pd.concat([std_summary,index_std.loc[['主观多头市场', '公募偏股市场',
                                      '量化多头市场']]],axis=0)

            weight_by_year = \
                (fund_attribution[fund_attribution['ejfl'].isin(['主观多头', '量化多头', '公募偏股'])].
                 groupby(['date', 'ejfl']).sum()[['weight']].reset_index())
            weight_by_year['year'] = weight_by_year['date'].astype(str).str[0:4]
            weight_by_year=\
                (weight_by_year.groupby(['year', 'ejfl']).mean()[['weight']].reset_index()).pivot_table('weight', 'year',
                                                                                            'ejfl')
            vol_cont=\
                get_vol_contribution(weight_by_year,std_by_year,std_summary,corrbyyear,corr)

            summary=pd.concat([ret_summary,std_summary,weight_summary,cont_summary],axis=1)
            summary['夏普比率'] = summary['年化收益率'] / summary['年化波动率']
            for col in summary.columns:
                summary[col]=summary[col].map("{:.2%}".format)
            for col in ret_byyear.columns:
                ret_byyear[col] = ret_byyear[col].map("{:.2%}".format)

            pd.concat([summary.sort_index().reset_index(drop=False)
                          ,cont_his_byyear.sort_index().reset_index(drop=False).rename(columns={'year':'年份'}),
                       ret_byyear.sort_index().reset_index(drop=False).rename(columns={'date':'日期'})
                          ,vol_cont.reset_index(drop=False),std_by_year.reset_index(drop=False)],axis=1)\
                .to_excel(dir.replace('基金持仓数据', '进攻资产数据汇总'))
            # plot.plotly_table(summary.sort_index().reset_index(drop=False),500,'')
            # plot.plotly_table(cont_his_byyear.sort_index().reset_index(drop=False).rename(columns={'year':'年份'}), 500, '')
            # plot.plotly_table(ret_byyear.sort_index().reset_index(drop=False).rename(columns={'date':'日期'}), 1000, '')

            index_enhance_att = \
                (fund_attribution[fund_attribution['二级策略'].astype(str).str.contains('指数增强')].groupby(['date','二级策略']).sum()).reset_index()

            if(len(index_enhance_att)>0):

                cont_his = index_enhance_att.groupby(['date', '二级策略']).sum()[['contribute_ret']].reset_index().pivot_table(
                    'contribute_ret',
                    'date', '二级策略').cumsum()
                cont_his.index=cont_his.index.astype(str)
                ret_cont_his_table.append(cont_his)
                # plot.plotly_line_style(cont_his, '量化多头资产贡献时序')
                index_enhance_att['year'] = index_enhance_att['date'].astype(str).str[0:4]

                cont_his_byyear = index_enhance_att.groupby(['year', '二级策略']).sum()[['contribute_ret'] + year_list].reset_index()
                for year in year_list:
                    cont_his_byyear.loc[cont_his_byyear['year'] == year, 'contribute_ret'] = \
                        cont_his_byyear[cont_his_byyear['year'] == year][year]
                cont_his_byyear = cont_his_byyear.pivot_table('contribute_ret', 'year', '二级策略')
                cont_his_byyear['合计'] = cont_his_byyear.sum(axis=1)

                index_enhance_att = index_enhance_att.drop('year', axis=1)
                index_enhance_att['ret'] = index_enhance_att['contr'] / index_enhance_att['weight']
                index_enhance_att = index_enhance_att.reset_index()
                index_enhance_att = pd.merge(index_enhance_att,
                                     index_enhance_att.groupby('date').sum()[['weight']].rename(columns={'weight': 'total_weight'}),
                                     how='left', on='date')
                index_enhance_att['weight'] = index_enhance_att['weight'] / index_enhance_att['total_weight']

                index_enhance_att = pd.merge(index_enhance_att.pivot_table('ret', 'date', '二级策略')
                                     , index_enhance_att.pivot_table('weight', 'date', '二级策略')
                                     , how='left', on='date')
                index_enhance_att.index = index_enhance_att.index.astype(str)
                index_enhance_att = pd.merge(index_enhance_att,
                                             index_ret_monthly[['date','1000指数增强','500指数增强','300指数增强']],
                                             how='left', on='date')

                index_enhance_att.reset_index(inplace=True)
                # arrange the bmk weight
                index_enhance_att['1000指数增强bmk_w'] = 0.1
                index_enhance_att['500指数增强bmk_w'] = 0.8
                index_enhance_att['300指数增强bmk_w'] = 0.1

                for asset in ['1000指数增强', '500指数增强', '300指数增强']:

                    if(asset+'_x' not in index_enhance_att.columns):
                        index_enhance_att[asset+'_x']=np.nan
                        index_enhance_att[asset + '_y'] = np.nan
                        cont_his_byyear[asset]=np.nan

                    index_enhance_att.loc[index_enhance_att[asset + '_x'].isnull(), asset + '_x'] = \
                        index_enhance_att[index_enhance_att[asset + '_x'].isnull()][
                        asset]

                    cont_his_byyear[asset] = cont_his_byyear[asset].map("{:.2%}".format)

                cont_his_byyear['合计'] = cont_his_byyear['合计'].map("{:.2%}".format)

                # return allocation
                total_extra_ret = (index_enhance_att[['1000指数增强_x', '500指数增强_x', '300指数增强_x']].fillna(0).values * index_enhance_att[
                    ['1000指数增强_y', '500指数增强_y', '300指数增强_y']].fillna(0).values \
                                   - index_enhance_att[['1000指数增强', '500指数增强', '300指数增强']].fillna(0).values * index_enhance_att[
                                       ['1000指数增强bmk_w', '500指数增强bmk_w', '300指数增强bmk_w']].values).sum(axis=1)
                allocation_extraret = ((index_enhance_att[['1000指数增强_y', '500指数增强_y', '300指数增强_y']].fillna(0).values - \
                                        index_enhance_att[['1000指数增强bmk_w', '500指数增强bmk_w', '300指数增强bmk_w']].values) * index_enhance_att[
                                           ['1000指数增强', '500指数增强', '300指数增强']].fillna(0).values).sum(axis=1)
                selection_extraret = pd.DataFrame(data=(index_enhance_att[['1000指数增强bmk_w', '500指数增强bmk_w', '300指数增强bmk_w']].values * (
                            index_enhance_att[['1000指数增强_x', '500指数增强_x', '300指数增强_x']].values -
                            index_enhance_att[['1000指数增强', '500指数增强', '300指数增强']].fillna(0).values))).fillna(0).sum(axis=1)
                brinson_his = pd.DataFrame()
                brinson_his['date'] = index_enhance_att['date'].tolist()
                brinson_his['总超额'] = total_extra_ret
                brinson_his['配置收益'] = allocation_extraret
                brinson_his['择基收益'] = selection_extraret.values.tolist()
                brinson_his['其他收益'] = brinson_his['总超额'] - brinson_his['配置收益'] - brinson_his['择基收益']
                brinson_his.set_index('date', inplace=True)
                brinson_his = (brinson_his + 1).cumprod() - 1

                # plot.plotly_line_style(brinson_his, '指数增强收益拆解')

                index_enhance_att.rename(columns={'1000指数增强_y': '1000指数增强FOF配置权重',
                                          '500指数增强_y': '500指数增强FOF配置权重',
                                          '300指数增强_y': '300指数增强FOF配置权重',
                                          '1000指数增强bmk_w': '1000指数增强市场隐含权重',
                                          '300指数增强bmk_w': '300指数增强市场隐含权重',
                                          '500指数增强bmk_w': '500指数增强市场隐含权重',
                                          '1000指数增强': '1000指数增强指数收益率',
                                          '300指数增强': '300指数增强指数收益率',
                                          '500指数增强': '500指数增强指数收益率',
                                          '1000指数增强_x': '1000指数增强FOF收益率',
                                          '300指数增强_x': '300指数增强FOF收益率',
                                          '500指数增强_x': '500指数增强FOF收益率',
                                          }, inplace=True)
                brinson_his.to_excel(dir.replace('基金持仓数据', '指数增强资产brinsion数据'), index=True)
                index_enhance_att = index_enhance_att.set_index('date')
               #  plot.plotly_line_style(index_enhance_att[['500指数增强FOF配置权重',
               # '1000指数增强FOF配置权重', '300指数增强FOF配置权重','500指数增强市场隐含权重',
               #                                    '1000指数增强市场隐含权重', '300指数增强市场隐含权重']], '指增资产配置权重对比')


                index_enhance_att['tjyf']=[str(x)[0:6] for x in index_enhance_att.index]

                index_enhance_att[['500指数增强FOF收益率', '1000指数增强FOF收益率',
                           '300指数增强FOF收益率', '500指数增强指数收益率', '300指数增强指数收益率', '1000指数增强指数收益率']]=\
                    index_enhance_att[['500指数增强FOF收益率', '1000指数增强FOF收益率',
                           '300指数增强FOF收益率', '500指数增强指数收益率', '300指数增强指数收益率', '1000指数增强指数收益率']].fillna(0)+1

                std_by_year = (index_enhance_att.set_index('tjyf').groupby('tjyf')[['1000指数增强FOF收益率', '500指数增强FOF收益率', '300指数增强FOF收益率']].cumprod()) \
                    .reset_index().drop_duplicates('tjyf', keep='last')
                std_summary = ((std_by_year.drop('tjyf', axis=1) - 1).std()
                               * np.sqrt(12)).to_frame('年化波动率')

                std_by_year['year'] = std_by_year['tjyf'].str[0:4]
                std_by_year = \
                    (std_by_year.drop('tjyf', axis=1).set_index('year') - 1).groupby('year').std() * np.sqrt(12)

                # std_summary = \
                #     ((index_enhance_att.groupby('tjyf')[['1000指数增强FOF收益率', '500指数增强FOF收益率', '300指数增强FOF收益率']].cumprod()-1).std() * np.sqrt(12)).to_frame('年化波动率')
                std_summary.index = [x.replace('FOF收益率', 'FOF') for x in std_summary.index]
                std_summary = pd.concat([std_summary,
                                         index_std.loc[['1000指数增强市场', '500指数增强市场', '300指数增强市场']]], axis=0)

                weight_summary = (index_enhance_att[['1000指数增强FOF配置权重',
                                             '500指数增强FOF配置权重', '300指数增强FOF配置权重', '1000指数增强市场隐含权重', '500指数增强市场隐含权重',
                                             '300指数增强市场隐含权重']].mean()).to_frame('平均配置权重').sort_index()
                weight_summary.index = [x.replace('配置权重', '') for x in weight_summary.index]
                weight_summary.index = [x.replace('隐含权重', '') for x in weight_summary.index]
                cont_summary = cont_his.iloc[-1].to_frame('收益贡献')
                cont_summary.index = [x.replace('CTA', 'CTA资产') for x in cont_summary.index]
                cont_summary.index = [x + 'FOF' for x in cont_summary.index]


                index_enhance_att[['500指数增强FOF收益率', '1000指数增强FOF收益率',
                           '300指数增强FOF收益率', '500指数增强指数收益率', '300指数增强指数收益率', '1000指数增强指数收益率']] = \
                    (index_enhance_att[['500指数增强FOF收益率', '1000指数增强FOF收益率',
                           '300指数增强FOF收益率', '500指数增强指数收益率', '300指数增强指数收益率', '1000指数增强指数收益率']]).cumprod()

                ret_his_table.append(index_enhance_att[['500指数增强FOF收益率', '1000指数增强FOF收益率',
                                   '300指数增强FOF收益率', '500指数增强指数收益率', '300指数增强指数收益率', '1000指数增强指数收益率']])

                # index_enhance_att[['500指数增强FOF收益率', '1000指数增强FOF收益率',
                #                    '300指数增强FOF收益率', '500指数增强指数收益率', '300指数增强指数收益率', '1000指数增强指数收益率']] \
                #     .to_excel(dir.replace('基金持仓数据', '指增资产收益率对比'), index=True)

                # plot.plotly_line_style(index_enhance_att[['500指数增强FOF收益率', '1000指数增强FOF收益率',
                #                                           '300指数增强FOF收益率', '500指数增强指数收益率', '300指数增强指数收益率', '1000指数增强指数收益率']], '指增资产收益率对比')

                ret_summary = index_enhance_att[['1000指数增强FOF收益率', '500指数增强FOF收益率',
                                         '300指数增强FOF收益率', '1000指数增强指数收益率',
                                         '300指数增强指数收益率', '500指数增强指数收益率']]

                ret_summary['year'] = ret_summary.index.astype(str).str[0:4]

                corrbyyear = (
                    ret_summary[['1000指数增强FOF收益率', '500指数增强FOF收益率', '300指数增强FOF收益率', 'year']].set_index('year').pct_change()).groupby(
                    'year').corr()
                corr = (ret_summary[['1000指数增强FOF收益率', '500指数增强FOF收益率', '300指数增强FOF收益率']].pct_change()).corr()

                ret_byyear = ret_summary.drop_duplicates('year', keep='last').drop('year', axis=1)
                ret_byyear = pd.concat([ret_byyear.iloc[[0]] - 1, ret_byyear.pct_change().iloc[1:]], axis=0)
                ret_byyear.columns = [x.replace('FOF收益率', 'FOF') for x in ret_byyear.columns]
                ret_byyear.columns = [x.replace('指数收益率', '市场') for x in ret_byyear.columns]
                ret_byyear = ret_byyear[ret_byyear.columns.sort_values().tolist()]

                ret_summary.drop('year', axis=1, inplace=True)
                ret_summary = ret_summary.iloc[-1].to_frame('年化收益率').sort_index() - 1
                ret_summary.index = [x.replace('FOF收益率', 'FOF') for x in ret_summary.index]
                ret_summary.index = [x.replace('指数收益率', '市场') for x in ret_summary.index]
                ret_summary = np.power((ret_summary['年化收益率'] + 1), 250 / day_len) - 1

                weight_by_year = \
                    (fund_attribution[fund_attribution['二级策略'].isin(['1000指数增强', '500指数增强', '300指数增强'])].
                     groupby(['date', '二级策略']).sum()[['weight']].reset_index())
                weight_by_year['year'] = weight_by_year['date'].astype(str).str[0:4]
                weight_by_year = \
                    (weight_by_year.groupby(['year', '二级策略']).mean()[['weight']].reset_index()).pivot_table('weight',
                                                                                                            'year',
                                                                                                            '二级策略')
                vol_cont =  \
                    get_vol_contribution(weight_by_year, std_by_year, std_summary, corrbyyear, corr)


                summary = pd.concat([ret_summary,std_summary,  weight_summary, cont_summary], axis=1)
                summary['夏普比率'] = summary['年化收益率'] / summary['年化波动率']
                for col in summary.columns:
                    summary[col] = summary[col].map("{:.2%}".format)
                for col in ret_byyear.columns:
                    ret_byyear[col] = ret_byyear[col].map("{:.2%}".format)

                pd.concat([summary.sort_index().reset_index(drop=False)
                              , cont_his_byyear.sort_index().reset_index(drop=False).rename(columns={'year': '年份'}),
                           ret_byyear.sort_index().reset_index(drop=False).rename(columns={'date': '日期'}),
                           vol_cont.reset_index(drop=False),std_by_year.reset_index(drop=False)], axis=1) \
                    .to_excel(dir.replace('基金持仓数据', '量化多头资产数据汇总'))
                # plot.plotly_table(summary.sort_index().reset_index(drop=False), 700, '')
                # plot.plotly_table(cont_his_byyear.sort_index().reset_index(drop=False).rename(columns={'year': '年份'}), 500,
                #                   '')
                # plot.plotly_table(ret_byyear.sort_index().reset_index(drop=False).rename(columns={'date': '日期'}), 1000, '')

        ret_cont_his_table=pd.concat(ret_cont_his_table,axis=1)
        ret_his_table=pd.concat(ret_his_table, axis=1)


        return ret_his_table,ret_cont_his_table

    @staticmethod
    def fund_lable_analysis(hold_df):

        hold_df['资产净值']=hold_df['资产净值'].astype(str).str.replace(',','').astype(float)


        def mutual_lable_analysis(hold_df):

            mu_lable=hold_df[(hold_df['cpfl']=='公募基金')
                             &(hold_df['ejfl'].isin([13,35,37]))][['date'
                ,'jjdm','jjjc','jjjz','quant','资产净值']]

            #read style lable from local db

            max_asofdate=pd.read_sql("select max(asofdate) as date from jjpic_value_p_hbs"
                                     ,con=localdb)['date'][0]
            sql="SELECT jjdm,`风格偏好`,`成长绝对暴露(持仓)`,`价值绝对暴露(持仓)` from jjpic_value_p_hbs where jjdm in ({0}) and  asofdate='{1}'"\
                .format(util.list_sql_condition(mu_lable['jjdm'].unique().tolist()),max_asofdate)
            value_pic=pd.read_sql(sql,con=localdb)

            sql="SELECT jjdm,`规模偏好`,`大盘绝对暴露(持仓)`,`中盘绝对暴露(持仓)`,`小盘绝对暴露(持仓)` from jjpic_size_p_hbs where jjdm in ({0}) and  asofdate='{1}'"\
                .format(util.list_sql_condition(mu_lable['jjdm'].unique().tolist()),max_asofdate)
            size_pic=pd.read_sql(sql,con=localdb)


            #read industry type lable from local db
            max_asofdate=pd.read_sql("select max(asofdate) as date from jjpic_industry_p"
                                     ,con=localdb)['date'][0]
            sql="SELECT jjdm,`一级行业类型` from jjpic_industry_p where jjdm in ({0}) and  asofdate='{1}'"\
                .format(util.list_sql_condition(mu_lable['jjdm'].unique().tolist()),max_asofdate)
            industry_pic=pd.read_sql(sql,con=localdb)

            mu_lable=pd.merge(mu_lable,value_pic,how='left',on='jjdm')
            mu_lable = pd.merge(mu_lable, size_pic, how='left', on='jjdm')
            mu_lable = pd.merge(mu_lable, industry_pic, how='left', on='jjdm')

            mu_lable['持仓权重']=mu_lable['quant']*mu_lable['jjjz']/mu_lable['资产净值']

            for col in ['成长绝对暴露(持仓)','价值绝对暴露(持仓)','大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)']:
                mu_lable[col]=mu_lable[col]*mu_lable['持仓权重']

            value_pic=mu_lable.groupby(['date',
                                        '风格偏好']).sum()[['持仓权重']].reset_index().pivot_table('持仓权重','date','风格偏好').fillna(0)

            value_pic2=mu_lable.groupby('date').sum()[['成长绝对暴露(持仓)','价值绝对暴露(持仓)']]
            size_pic = mu_lable.groupby(['date'
                                            , '规模偏好']).sum()[['持仓权重']].reset_index().pivot_table('持仓权重','date','规模偏好').fillna(0)

            size_pic2 = mu_lable.groupby('date').sum()[['大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)']]
            industry_pic = mu_lable.groupby(['date'
                                                , '一级行业类型']).sum()[['持仓权重']].reset_index().pivot_table('持仓权重','date','一级行业类型').fillna(0)


            return  value_pic,value_pic2,size_pic,size_pic2,industry_pic

        def prv_lable_analysis(hold_df):

            prv_lable = hold_df[(hold_df['cpfl'] == '私募基金')
                                & (hold_df['ejfl'].isin([1001]))][['date'
                , 'jjdm', 'jjjc', 'jjjz', 'quant', '资产净值']]

            file_name_list = os.listdir(r"E:\GitFolder\docs\净值标签")
            file_name_list.sort()
            fold_name = ''
            for name in file_name_list:
                if (name.startswith('全部私募打标结果')):
                    fold_name = name
                    break
            prv_pic = pd.read_excel(r"E:\GitFolder\docs\净值标签\{}".format(fold_name), sheet_name='数据')
            prv_lable = pd.merge(prv_lable, prv_pic[['jjdm', '大小盘', '成长价值']]
                                 , how='left', on='jjdm')
            return  prv_lable

        value_pic,value_pic2,size_pic,size_pic2,industry_pic=mutual_lable_analysis(hold_df)

        data, layout=plot.plotly_area(value_pic.T*100,'公募风格类型分布时序'
                                      ,range_upper=value_pic.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

        data, layout=plot.plotly_area(value_pic2.T*100,'公募持仓打穿后成长价值分布'
                                      ,range_upper=value_pic2.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

        data, layout=plot.plotly_area(size_pic.T*100, '公募市值类型分布时序'
                                      ,range_upper=size_pic.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

        data, layout=plot.plotly_area(size_pic2.T*100,'公募持仓打穿后大中小盘分布'
                                      ,range_upper=size_pic2.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

        data, layout=plot.plotly_area(industry_pic.T*100, '公募行业类型分布时序',
                                      range_upper=industry_pic.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

    @staticmethod
    def calculate_holding_time(inputdf):

        hold_df=inputdf.copy()

        #calculate the max tolarance
        hold_df['current_ret']=hold_df['jjjz']/hold_df['cbprice']-1
        hold_df['year'] = hold_df['date'].astype(str).str[0:4]
        max_tolarance=hold_df.groupby(['yjcl']).min('current_ret')['current_ret'].reset_index()

        #calculate the ret at sold

        still_holding_jjdm=hold_df[hold_df['date']==hold_df['date'].max()]['jjdm'].tolist()
        sold_moment=\
            hold_df[~hold_df['jjdm'].isin(still_holding_jjdm)].drop_duplicates('jjdm',keep='last')
        sold_moment['sold_ret'] = sold_moment['jjjz'] / sold_moment['cbprice'] - 1
        sold_moment=sold_moment.groupby('yjcl').describe()['sold_ret']

        yjcl_weight_his=hold_df.groupby(['yjcl','date']).sum()['weight'].reset_index()

        for asset in yjcl_weight_his['yjcl'].unique():
            tempdf=hold_df[hold_df['yjcl']==asset].set_index('date')
            for date in yjcl_weight_his[yjcl_weight_his['yjcl']==asset]['date'].unique():
                yjcl_weight_his.loc[(yjcl_weight_his['yjcl']==asset)&
                                    (yjcl_weight_his['date']==date),'cent']=\
                    tempdf.loc[[date]].sort_values('weight', ascending=False)['weight'].iloc[0:3].sum()

        yjcl_weight_his['cent']=yjcl_weight_his['cent']/yjcl_weight_his['weight']
        yjcl_weight_his['year']=yjcl_weight_his['date'].astype(str).str[0:4]
        cent_by_asset=yjcl_weight_his.groupby(['year','yjcl']).mean()['cent'].reset_index()



        return max_tolarance,sold_moment,cent_by_asset

    @staticmethod
    def style_analysis(hold_df,cb_w=False):

        if(cb_w):
            style_df = hold_df.groupby(['date', '风格偏好']).sum()[['cb_w']].reset_index().rename(columns={'cb_w':'weight'})
        else:
            style_df=hold_df.groupby(['date', '风格偏好']).sum()[['weight']].reset_index()

        style_df=\
            pd.merge(style_df,style_df.groupby('date').sum()['weight'].to_frame('total_w'),how='left',on='date')
        style_df['weight']=style_df['weight']/style_df['total_w']
        style_df=style_df.pivot_table('weight','date',
                                      '风格偏好')

        data, layout=plot.plotly_area(style_df.T*100,'',range_upper=100)
        plot.plot_render(data, layout)

        style_df=style_df.reset_index(drop=False).rename(columns={'date': '日期'})
        style_df['日期']=style_df['日期'].astype(str)
        weight_col=style_df.columns.tolist()
        weight_col.remove('日期')
        style_summary=find_weight_change_point(style_df, weight_col,index_list=['399370','399371'])
        for col in style_summary.drop('持续日期',axis=1).columns.to_list():
            style_summary[col]=style_summary[col].map("{:.2%}".format)
        plot.plotly_table(style_summary.reset_index(),1200,'')

        return  style_df

    def holding_analysis(self,dir,stock_bmk_w=1/3,bond_bmk_w=1/3,CTA_bmk_w=1/3,start_date=None,end_date=None):

        hold_df=pd.read_excel(dir)
        hold_df['jjdm']=hold_df['jjdm'].str.replace("'", "")
        hold_df['资产份额']=hold_df['资产份额'].astype(str).str.replace(',','').astype(float)
        hold_df['资产净值'] = hold_df['资产净值'].astype(str).str.replace(',', '').astype(float)
        if(start_date is not None):
            hold_df=hold_df[hold_df['date']>=int(start_date)]
        if(end_date is not None):
            hold_df=hold_df[hold_df['date']<=int(end_date)]


        #remove the money asset

        #read trade info



        #mark prv fix income fund as prv
        hold_df.loc[(hold_df['cpfl'].isnull()) & (hold_df['jjdm'] != '000nan'), 'cpfl'] = 4
        hold_df.loc[hold_df['cpfl']==4,'cpfl']='私募基金'
        hold_df.loc[hold_df['cpfl'] == 2, 'cpfl'] = '公募基金'

        quant_pool_in = \
        pd.read_excel(r"E:\FOF分析\量化二级映射表.xlsx"
                      )[[ '基金代码', '二级策略']].drop_duplicates('基金代码')
        hold_df=pd.merge(hold_df,quant_pool_in[['基金代码','二级策略']]
                         ,how='left',left_on='jjdm',right_on='基金代码')

        gl_df=pd.read_excel(dir.replace('基金持仓数据','基金股利数据'))
        hold_df,fund_attribution=self.fund_attribution_new(hold_df,gl_df)
        jjfl2stratage_map=dict(zip(['管理期货','股票型','混合型','其他','债券型','市场中性','套利型','多策略','QDII','货币型','多空仓型','宏观策略']
                                   ,['CTA','进攻性资产','进攻性资产','稳健性资产','稳健性资产','稳健性资产','稳健性资产','进攻性资产','进攻性资产','稳健性资产','进攻性资产','进攻性资产']))
        fund_attribution['yjcl']=[jjfl2stratage_map[x] for x in fund_attribution['jjfl']]
        hold_df['yjcl'] = [jjfl2stratage_map[x] for x in hold_df['jjfl']]

        max_tolarance,sold_moment,cent_by_asset=self.calculate_holding_time(hold_df)
        pd.concat([max_tolarance,sold_moment.reset_index(),
                   cent_by_asset],axis=1).to_excel(dir.replace('基金持仓数据','个股特征统计'))
        # plot.plotly_table(holding_time_table,1000,'')
        #


        #for tempary use : since we can not get the specific ret contribution, we can only add the trade ret on each asset based on it weight
        rel_ret=hold_df['累计单位净值'].iloc[-1]/hold_df['累计单位净值'].iloc[0]-1
        explained_ret=fund_attribution['contribute_ret'].sum()
        trade_ret=rel_ret-explained_ret


        style_weight_his=self.style_analysis(hold_df,cb_w=False)
        style_weight_his.to_excel(dir.replace('基金持仓数据','风格权重时序'))
        #self.style_analysis(hold_df, fund_attribution, cb_w=True)

        hold_df['ym']=hold_df['date'].astype(str).str[0:6]
        hold_df['month']=hold_df['date'].astype(str).str[4:6]

        first_st_his=(hold_df.groupby(['date','ejfl']).sum()[['weight']]*100).reset_index().pivot_table('weight','ejfl','date').fillna(0)
        data, layout=plot.plotly_area(first_st_his,'test')
        plot.plot_render(data, layout)

        hold_by_jj=\
            hold_df[(hold_df['date'].isin(hold_df.drop_duplicates('ym', keep='last')['date'].tolist()))
                &(hold_df['month'].isin(['03','06','09','12']))].pivot_table('weight','jjjc','date').fillna(0)
        for col in hold_by_jj.columns.tolist():
            hold_by_jj[col]=hold_by_jj[col].map("{:.2%}".format)

        pd.merge(hold_by_jj,hold_df[['jjjc','yjcl','jjfl','ejfl','二级策略']].drop_duplicates('jjjc'),how='left',on='jjjc').to_excel(dir.replace('基金持仓数据','季度持仓by基金'))
        plot.plotly_table(hold_by_jj.reset_index(),200*len(hold_by_jj.columns),'')

        tempdf_hold=hold_df[(hold_df['date'].isin(hold_df.drop_duplicates('ym', keep='last')['date'].tolist()))
                &(hold_df['month'].isin(['03','06','09','12']))]
        tempdf_hold['name_weight']=tempdf_hold['jjjc']+"("+tempdf_hold['weight'].fillna(0).map("{:.2%}".format)+")"

        tempdf_con=fund_attribution.copy()
        tempdf_con['month'] = tempdf_con['date'].astype(str).str[4:6]
        tempdf_con.loc[tempdf_con['month'].isin(['01','02','03']),'month']='Q1'
        tempdf_con.loc[tempdf_con['month'].isin(['04', '05', '06']), 'month'] = 'Q2'
        tempdf_con.loc[tempdf_con['month'].isin(['07', '08', '09']), 'month'] = 'Q3'
        tempdf_con.loc[tempdf_con['month'].isin(['10', '11', '12']), 'month'] = 'Q4'
        tempdf_con['yq'] = tempdf_con['date'].astype(str).str[0:4]+tempdf_con['month']

        tempdf_con=\
            tempdf_con.groupby(['jjjc', 'yq']).sum()[['contribute_ret']].reset_index().fillna(0)
        tempdf_con['contribute_ret']=tempdf_con.groupby('jjjc').cumsum(axis=0)['contribute_ret']
        tempdf_con=tempdf_con.pivot_table('contribute_ret', 'jjjc','yq')
        pd.merge(tempdf_con, hold_df[['jjjc', 'yjcl', 'jjfl', 'ejfl', '二级策略']].drop_duplicates('jjjc'), how='left',
                 on='jjjc').to_excel(dir.replace('基金持仓数据','基金季度贡献'))

        hold_by_date=[]
        for ym in tempdf_hold['ym'].unique():
            hold_by_date.append(pd.DataFrame(data=tempdf_hold[(tempdf_hold['ym']==ym)
                                                              &(tempdf_hold['weight']>0)].sort_values('weight',ascending=False)['name_weight'].tolist(),columns=[ym]))
        hold_by_date=pd.concat(hold_by_date,axis=1)
        hold_by_date.to_excel(dir.replace('基金持仓数据','季度持仓by日期'))
        plot.plotly_table(hold_by_date,200*len(hold_by_jj.columns),'')


        attribution_by_class=self.attribution_by_class(fund_attribution,self.index_enhance_manual_map)

        howbuy_index_ret, mu_index_ret, index_enhance_index=self.get_bmk_return(str(hold_df['date'].iloc[0])
                                                                                ,str(hold_df['date'].iloc[-1]))

        fund_attribution.to_excel(dir.replace('基金持仓数据','个基收益贡献'),index=False)
        attribution_by_class.to_excel(dir.replace('基金持仓数据','各级资产收益贡献'))

        ret_his_table,ret_cont_his_table=self.brinson_wise_analysis(fund_attribution,dir,howbuy_index_ret
                              , mu_index_ret, index_enhance_index,stock_bmk_w=stock_bmk_w,bond_bmk_w=bond_bmk_w,CTA_bmk_w=CTA_bmk_w)


        ret_cont_his_table.to_excel(dir.replace('基金持仓数据', '资产收益贡献时序'), index=True)
        ret_his_table.to_excel(dir.replace('基金持仓数据', '资产收益率对比'), index=True)

        (hold_df.groupby(['date', 'ejfl'])[['weight']].sum().reset_index().pivot_table('weight', 'date',
                                                                                       'ejfl') * 100).reset_index().to_excel(dir.replace('基金持仓数据','一级策略时序图')
                                                                                                                             ,index=False)
        (hold_df.groupby(['date', 'yjcl'])[['weight']].sum().reset_index().pivot_table('weight', 'date',
                                                                                       'yjcl') * 100).reset_index().to_excel(dir.replace('基金持仓数据','超一级策略时序图')
                                                                                                                             ,index=False)
        #self.fund_lable_analysis(hold_df)

    def holding_analysis_for_weekly_tracking(self,dir,stock_bmk_w=1/3,bond_bmk_w=1/3,CTA_bmk_w=1/3,start_date=None,end_date=None):

        hold_df=pd.read_excel(dir)
        hold_df['jjdm']=hold_df['jjdm'].str.replace("'", "")
        hold_df['资产份额']=hold_df['资产份额'].astype(str).str.replace(',','').astype(float)
        hold_df['资产净值'] = hold_df['资产净值'].astype(str).str.replace(',', '').astype(float)
        if(start_date is not None):
            hold_df=hold_df[hold_df['date']>=int(start_date)]
        if(end_date is not None):
            hold_df=hold_df[hold_df['date']<=int(end_date)]


        #remove the money asset

        #read trade info



        #mark prv fix income fund as prv
        hold_df.loc[(hold_df['cpfl'].isnull()) & (hold_df['jjdm'] != '000nan'), 'cpfl'] = 4
        hold_df.loc[hold_df['cpfl']==4,'cpfl']='私募基金'
        hold_df.loc[hold_df['cpfl'] == 2, 'cpfl'] = '公募基金'

        quant_pool_in = \
        pd.read_excel(r"E:\FOF分析\量化二级映射表.xlsx"
                      )[[ '基金代码', '二级策略']].drop_duplicates('基金代码')
        hold_df=pd.merge(hold_df,quant_pool_in[['基金代码','二级策略']]
                         ,how='left',left_on='jjdm',right_on='基金代码')

        gl_df=pd.read_excel(dir.replace('基金持仓数据','基金股利数据'))
        hold_df,fund_attribution=self.fund_attribution_new(hold_df,gl_df)
        jjfl2stratage_map=dict(zip(['管理期货','股票型','混合型','其他','债券型','市场中性','套利型','多策略','QDII','货币型','多空仓型','宏观策略']
                                   ,['CTA','进攻性资产','进攻性资产','稳健性资产','稳健性资产','稳健性资产','稳健性资产','进攻性资产','进攻性资产','稳健性资产','进攻性资产','进攻性资产']))
        fund_attribution['yjcl']=[jjfl2stratage_map[x] for x in fund_attribution['jjfl']]
        hold_df['yjcl'] = [jjfl2stratage_map[x] for x in hold_df['jjfl']]

        max_tolarance,sold_moment,cent_by_asset=self.calculate_holding_time(hold_df)
        pd.concat([max_tolarance,sold_moment.reset_index(),
                   cent_by_asset],axis=1).to_excel(dir.replace('基金持仓数据','个股特征统计'))


        #self.style_analysis(hold_df, fund_attribution, cb_w=True)

        hold_df['ym']=hold_df['date'].astype(str).str[0:6]
        hold_df['month']=hold_df['date'].astype(str).str[4:6]

        first_st_his=(hold_df.groupby(['date','ejfl']).sum()[['weight']]*100).reset_index().pivot_table('weight','ejfl','date').fillna(0)

        hold_by_jj=\
            hold_df[(hold_df['date'].isin(hold_df.drop_duplicates('ym', keep='last')['date'].tolist()))
                &(hold_df['month'].isin(['03','06','09','12']))].pivot_table('weight','jjjc','date').fillna(0)
        for col in hold_by_jj.columns.tolist():
            hold_by_jj[col]=hold_by_jj[col].map("{:.2%}".format)

        pd.merge(hold_by_jj,hold_df[['jjjc','yjcl','jjfl','ejfl','二级策略']].drop_duplicates('jjjc'),how='left',on='jjjc').to_excel(dir.replace('基金持仓数据','季度持仓by基金'))


        tempdf_hold=hold_df[(hold_df['date'].isin(hold_df.drop_duplicates('ym', keep='last')['date'].tolist()))
                &(hold_df['month'].isin(['03','06','09','12']))]
        tempdf_hold['name_weight']=tempdf_hold['jjjc']+"("+tempdf_hold['weight'].fillna(0).map("{:.2%}".format)+")"

        tempdf_con=fund_attribution.copy()
        tempdf_con['month'] = tempdf_con['date'].astype(str).str[4:6]
        tempdf_con.loc[tempdf_con['month'].isin(['01','02','03']),'month']='Q1'
        tempdf_con.loc[tempdf_con['month'].isin(['04', '05', '06']), 'month'] = 'Q2'
        tempdf_con.loc[tempdf_con['month'].isin(['07', '08', '09']), 'month'] = 'Q3'
        tempdf_con.loc[tempdf_con['month'].isin(['10', '11', '12']), 'month'] = 'Q4'
        tempdf_con['yq'] = tempdf_con['date'].astype(str).str[0:4]+tempdf_con['month']

        tempdf_con=\
            tempdf_con.groupby(['jjjc', 'yq']).sum()[['contribute_ret']].reset_index().fillna(0)
        tempdf_con['contribute_ret']=tempdf_con.groupby('jjjc').cumsum(axis=0)['contribute_ret']
        tempdf_con=tempdf_con.pivot_table('contribute_ret', 'jjjc','yq')
        pd.merge(tempdf_con, hold_df[['jjjc', 'yjcl', 'jjfl', 'ejfl', '二级策略']].drop_duplicates('jjjc'), how='left',
                 on='jjjc').to_excel(dir.replace('基金持仓数据','基金季度贡献'))

        hold_by_date=[]
        for ym in tempdf_hold['ym'].unique():
            hold_by_date.append(pd.DataFrame(data=tempdf_hold[(tempdf_hold['ym']==ym)
                                                              &(tempdf_hold['weight']>0)].sort_values('weight',ascending=False)['name_weight'].tolist(),columns=[ym]))
        hold_by_date=pd.concat(hold_by_date,axis=1)
        hold_by_date.to_excel(dir.replace('基金持仓数据','季度持仓by日期'))



        attribution_by_class=self.attribution_by_class(fund_attribution,self.index_enhance_manual_map)

        howbuy_index_ret, mu_index_ret, index_enhance_index=self.get_bmk_return(str(hold_df['date'].iloc[0])
                                                                                ,str(hold_df['date'].iloc[-1]))


        ret_his_table,ret_cont_his_table=self.brinson_wise_analysis(fund_attribution,dir,howbuy_index_ret
                              , mu_index_ret, index_enhance_index,stock_bmk_w=stock_bmk_w,bond_bmk_w=bond_bmk_w,CTA_bmk_w=CTA_bmk_w)

        yj_weight_his=(hold_df.groupby(['date', 'ejfl'])[['weight']].sum().reset_index().pivot_table('weight', 'date',
                                                                                       'ejfl') * 100).reset_index()
        cyj_weight_his=(hold_df.groupby(['date', 'yjcl'])[['weight']].sum().reset_index().pivot_table('weight', 'date',
                                                                                       'yjcl') * 100).reset_index()

        return attribution_by_class,ret_cont_his_table,ret_his_table,yj_weight_his,cyj_weight_his,fund_attribution

    def trade_date_preprocessing(self,weight_his_dir,hold_data_dir,start_date):

        #read stratage weight history data from local file

        stratage_weight_his=pd.read_excel(weight_his_dir)
        stratage_weight_his['date']=stratage_weight_his['date'].astype(str)
        stratage_weight_his=stratage_weight_his[stratage_weight_his['date']>=start_date]
        # stratage_weight_his.columns=[x.replace('(%)','占比') for x in stratage_weight_his.columns]
        # stratage_weight_his['沪深300']=(stratage_weight_his['沪深300占比']+100)/100

        #get bmk index ret
        howbuy_index_ret,mu_index_ret,index_enhance_index=\
            self.get_bmk_return( stratage_weight_his['date'].iloc[0]
                             ,stratage_weight_his['date'].iloc[-1])
        mu_index_ret.index=mu_index_ret.index.astype(str)

        for col in howbuy_index_ret.columns:
            if('rank' not in col):
                howbuy_index_ret[col]=howbuy_index_ret[col]/howbuy_index_ret[col].iloc[0]
        for col in mu_index_ret.columns:
            if ('rank' not in col):
                mu_index_ret[col]=mu_index_ret[col]/mu_index_ret[col].iloc[0]


        #read fund class info and FOF nav info
        hold_df = pd.read_excel(hold_data_dir)[['jjdm','cpfl','jjfl','ejfl','风格偏好', '规模偏好']].drop_duplicates('jjdm',keep='last')
        hold_df.loc[hold_df['cpfl'].isnull(),'cpfl']=4
        fof_nav= pd.read_excel(hold_data_dir)[['date','资产净值','资产份额','单位净值']].drop_duplicates('date',keep='last')
        fof_nav['date']=fof_nav['date'].astype(str)
        for col in ['资产净值','资产份额','单位净值']:
            fof_nav[col]=\
                fof_nav[col].astype(str).str.replace(',','').astype(float)


        #read trading flow
        trading_detail=self.trading_flow[self.trading_flow['产品名称']==product]
        trading_detail=trading_detail[trading_detail['交易日期']>=start_date]
        trading_detail['投资基金代码']=trading_detail['投资基金代码'].astype(str)
        hold_df['jjdm']=hold_df['jjdm'].str.replace("'","")
        trading_detail=pd.merge(trading_detail,hold_df
                                ,how='left',left_on='投资基金代码',right_on='jjdm').drop('投资基金代码',axis=1)
        trading_detail=pd.merge(trading_detail,fof_nav
                                ,how='left',left_on='交易日期',right_on='date').drop('交易日期',axis=1)

        #remove money asset
        trading_detail=trading_detail[(trading_detail['jjfl']!=7)
                                      &(trading_detail['jjfl'].notnull())]

        #data cleaning
        trading_detail.loc[(trading_detail['cpfl'].isnull())
                           &(trading_detail['投资基金简称'].str.startswith('CTA')),'jjfl']='8'
        trading_detail.loc[(trading_detail['cpfl'].isnull())
                           &(trading_detail['投资基金简称'].str.startswith('CTA')),'cpfl']=4
        trading_detail['ejfl']=trading_detail['ejfl'].fillna(0).astype(str).str.replace("\.0", '')
        trading_detail['jjfl'] = trading_detail['jjfl'].fillna(0).astype(str).str.replace("\.0", '')
        trading_detail[['认申购金额','赎回份额','确认净值','单位净值']]=\
            trading_detail[['认申购金额','赎回份额','确认净值','单位净值']].astype(float)
        trading_detail['资产净值']=trading_detail['资产净值'].astype(str).str.replace(',', '').astype(float)
        trading_detail['资产份额']=trading_detail['资产份额'].astype(str).str.replace(',', '').astype(float)

        #rename the fund class name by chinese
        trading_detail.loc[trading_detail['cpfl']==4,'jjfl']\
            =[self.prv_jjflmap[x] for x in trading_detail[trading_detail['cpfl']==4]['jjfl']]
        trading_detail.loc[trading_detail['cpfl']==4,'ejfl']\
            =[self.prv_ejflmap[x] for x in trading_detail[trading_detail['cpfl']==4]['ejfl']]

        trading_detail.loc[trading_detail['cpfl']==2,'jjfl']\
            =[self.mu_jjflmap[x] for x in trading_detail[trading_detail['cpfl']==2]['jjfl']]
        trading_detail.loc[trading_detail['cpfl']==2,'ejfl']\
            =[self.mu_ejflmap[x] for x in trading_detail[trading_detail['cpfl']==2]['ejfl']]

        trading_detail.loc[trading_detail['投资类型']=='申购','change_w']\
            =trading_detail[trading_detail['投资类型']=='申购']['认申购金额']/\
             trading_detail[trading_detail['投资类型']=='申购']['资产净值']*100
        trading_detail.loc[trading_detail['投资类型']=='赎回','change_w']\
            =trading_detail[trading_detail['投资类型']=='赎回']['赎回份额']\
             /trading_detail[trading_detail['投资类型']=='赎回']['确认净值']/\
             trading_detail[trading_detail['投资类型']=='赎回']['资产净值']*-100

        hsl=self.calculate_hsl(trading_detail)
        hsl.to_excel(hold_data_dir.replace('基金持仓数据','FOF换手率统计'),index=False)
        plot.plotly_table(hsl,1000,'')

        #trading analysis
        #merge index ret data
        trading_data=pd.merge(stratage_weight_his[['date']]
                             ,howbuy_index_ret,how='left',left_on='date',right_index=True)
        trading_data=pd.merge(trading_data
                             ,mu_index_ret,how='left',left_on='date',right_index=True)
        trading_data['ym']=trading_data['date'].str[0:6]
        trading_data=pd.merge(trading_data
                             ,index_enhance_index,how='left',left_on='ym',right_index=True)

        #using liner interpolation to make up missed data
        for indexname in howbuy_index_ret.columns.tolist()\
                         +index_enhance_index.columns.tolist()+mu_index_ret.columns.tolist():

            temp = trading_data[indexname].reset_index(drop=True)
            tempnotnull=temp[temp.notnull()]
            f = interpolate.interp1d(tempnotnull.index.values, tempnotnull.values, kind='cubic')
            ynew = f(temp.iloc[tempnotnull.index[0]:tempnotnull.index[-1]].index.values)
            temp.loc[tempnotnull.index[0]:tempnotnull.index[-1]-1]=ynew
            trading_data[indexname]=temp.values

        for col in [ 'CTA', '主观多头', '量化多头', '国证大盘', '国证中盘', '国证小盘',
       '国证成长', '国证价值', '公募偏股','1000指数增强','500指数增强','300指数增强']:
            if(col in ['CTA', '主观多头', '量化多头',  '公募偏股']):
                trading_data[col] = trading_data[col] - trading_data['881001']
            elif(col in ['国证大盘', '国证中盘', '国证小盘','国证成长', '国证价值']):
                trading_data[col]=trading_data[col]-trading_data['399311']
            else:
                trading_data[col] = trading_data[col]-trading_data['量化多头']
            trading_data["ma10"]=trading_data[col].rolling(10).mean()
            trading_data["ma60"] = trading_data[col].rolling(60).mean()
            trading_data.loc[trading_data['ma60']>=trading_data['ma10'],col+'trend']=-1
            trading_data.loc[trading_data['ma60'] <= trading_data['ma10'], col + 'trend'] = 1
            trading_data.drop(['ma10','ma60'],axis=1,inplace=True)

        #sum the weight_change for one fund at one day
        trading_detail=pd.merge(trading_detail
                                ,trading_detail.groupby(['date','jjdm']).sum('change_w')['change_w'].reset_index()
                                ,how='left'
                                ,on=['date','jjdm']).rename(columns={'change_w_y':'change_w'}).drop('change_w_x',axis=1)

        trading_detail=trading_detail.drop_duplicates(['date','jjdm'])


        jjfl2stratage_map=dict(zip(['管理期货','股票型','混合型','其他','债券型','市场中性','套利型','多策略','QDII','货币型','多空仓型']
                                   ,['CTA','进攻性资产','进攻性资产','稳健性资产','稳健性资产','稳健性资产','稳健性资产','进攻性资产','进攻性资产','稳健性资产','进攻性资产']))

        trading_detail['cyjcl']=[jjfl2stratage_map[x] for x in trading_detail['jjfl']]
        #merge weight change by class
        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['jjfl'] == '管理期货'].groupby('date').sum()['change_w'].to_frame('CTA_weight_change')
                             ,how='left',left_on='date',right_index=True)

        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['ejfl'] == '量化多头'].groupby('date').sum()['change_w'].to_frame('量化多头_weight_change')
                             ,how='left',left_on='date',right_index=True)

        for type in ['300','500','1000']:
            trading_detail.loc[(trading_detail['jjdm'].str.contains(type))
                             &(trading_detail['ejfl']=='量化多头'),'sjfl']=type+'指增'
            trading_data = pd.merge(trading_data
                                    , trading_detail[trading_detail['sjfl']==type+'指增'].groupby(
                    'date').sum()['change_w'].to_frame(type+'指增_weight_change')
                                    , how='left', left_on='date', right_index=True)

        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['ejfl'] == '主观多头'].groupby('date').sum()['change_w'].to_frame('主观多头_weight_change')
                             ,how='left',left_on='date',right_index=True)

        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['ejfl'].isin(['偏股混合型','灵活配置型','普通股票型'])].groupby('date').sum()['change_w'].to_frame('公募偏股_weight_change')
                             ,how='left',left_on='date',right_index=True)

        trading_data=pd.merge(trading_data
                             ,trading_detail[~trading_detail['jjfl'].isin(['混合型',
        '股票型','管理期货'])].groupby('date').sum()['change_w'].to_frame('其他_weight_change')
                             ,how='left',left_on='date',right_index=True)

        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['cyjcl'] == 'CTA'].groupby('date').sum()['change_w'].to_frame('CTA资产_weight_change')
                             ,how='left',left_on='date',right_index=True)
        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['cyjcl'] == '进攻性资产'].groupby('date').sum()['change_w'].to_frame('进攻性资产_weight_change')
                             ,how='left',left_on='date',right_index=True)
        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['cyjcl'] == '稳健性资产'].groupby('date').sum()['change_w'].to_frame('稳健性资产_weight_change')
                             ,how='left',left_on='date',right_index=True)

        fof_nav['FOF净申赎'] = fof_nav['资产份额'].diff(1) * fof_nav['单位净值']
        trading_data=pd.merge(trading_data,fof_nav[['date','资产份额','资产净值']]
                              ,how='left',left_on='date',right_on='date').set_index('date')



        return  trading_data,trading_detail,fof_nav

    @staticmethod
    def define_trading_type(trading_data):

        # lable negative trading
        #add two columns 资产净值T+14 and 资产净值T-14
        trading_data['资产份额T+14']=trading_data['资产份额'].iloc[14:].tolist() + 14 * [np.nan]
        trading_data['资产份额T-14'] = 14 * [np.nan]+trading_data['资产份额'].iloc[0:-14].tolist()
        trading_data['调仓类型']=''
        trading_data.loc[((trading_data['CTA_weight_change']>0)
                         |(trading_data['量化多头_weight_change']>0)
                         |(trading_data['主观多头_weight_change']>0)
                         |(trading_data['公募偏股_weight_change']>0)
                         |(trading_data['其他_weight_change']>0))
                         &((trading_data['资产份额T-14']<trading_data['资产份额'])
                           |(trading_data.index<=trading_data.index[60])),'调仓类型']='被动增仓'

        trading_data.loc[((trading_data['CTA_weight_change']<0)
                         |(trading_data['量化多头_weight_change']<0)
                         |(trading_data['主观多头_weight_change']<0)
                         |(trading_data['公募偏股_weight_change']<0)
                         |(trading_data['其他_weight_change']<0))
                         &((trading_data['资产份额T+14']<trading_data['资产份额'])|
                           (trading_data.index<=trading_data.index[60])),'调仓类型']='被动减仓'

        trading_data.loc[((trading_data['CTA_weight_change'].notnull())
                         |(trading_data['量化多头_weight_change'].notnull())
                         |(trading_data['主观多头_weight_change'].notnull())
                         |(trading_data['公募偏股_weight_change'].notnull())
                         |(trading_data['其他_weight_change'].notnull())
                         )
                         &(trading_data['调仓类型']==''),'调仓类型']='主动'


        return  trading_data

    @staticmethod
    def calculate_hsl(inputdf):

        positive_trade=inputdf.copy()
        positive_trade=positive_trade[positive_trade['change_w'].notnull()]
        positive_trade['change_w']=abs(positive_trade['change_w'])
        positive_trade['year']=positive_trade['date'].astype(str).str[0:4]

        jjfl2stratage_map=dict(zip(['管理期货','股票型','混合型','其他','债券型','市场中性','套利型','多策略','QDII','货币型','多空仓型']
                                   ,['CTA','进攻性资产','进攻性资产','稳健性资产','稳健性资产','稳健性资产','稳健性资产','进攻性资产','进攻性资产','稳健性资产','进攻性资产']))
        positive_trade['cyjce']=[jjfl2stratage_map[x] for x in positive_trade['jjfl']]
        hsl=(positive_trade.groupby(['year','cyjce']).sum()['change_w']/100).to_frame('双边换手率').reset_index()

        print('avg hsl is '+str(hsl['双边换手率'].mean()))

        return hsl

    def fof_trading_analysis(self,weight_his_dir,hold_data_dir,start_date,product):


        #trade data pre processing
        trading_data,trading_detail,fof_nav=\
            self.trade_date_preprocessing(weight_his_dir,hold_data_dir,start_date)

        #temparory use
        first_class_asset_weight_his=pd.read_excel(weight_his_dir)
        # first_class_asset_weight_his['公募偏股(%)']=\
        #     first_class_asset_weight_his['股票型(公募)(%)']+first_class_asset_weight_his['混合型(公募)(%)']
        first_class_asset_weight_his['date']=first_class_asset_weight_his['date'].astype(str)
        # temparory use

        #*******define trading type : positive or negative *******
        trading_data=self.define_trading_type(trading_data)

        trading_data[[ 'CTA','CTA资产_weight_change',
                        '进攻性资产_weight_change', '稳健性资产_weight_change']].to_excel(hold_data_dir.replace('基金持仓数据','超一级策略交易时序'))

        negative_trade=trading_data[trading_data['调仓类型'].str.contains('被动')]
        negative_trade_summary=pd.DataFrame(index=negative_trade['调仓类型'].unique().tolist())
        for type in negative_trade['调仓类型'].unique().tolist():
            for asset in ['CTA','量化多头','主观多头','公募偏股','其他']:
                negative_trade_summary.loc[type,asset]= \
                    len(negative_trade[(negative_trade['调仓类型'] == type)
                                       & (negative_trade[asset + "_weight_change"].notnull())])

        #positive_trade=trading_data[(trading_data['调仓类型']=='主动')]
        positive_trade=trading_data[(trading_data['调仓类型']!='')]


        positive_trade=positive_trade.reset_index(drop=False)
        positive_trade_block=[]

        jjfl2stratage_map = dict(zip(['管理期货', '股票型', '混合型', '其他', '债券型', '市场中性', '套利型', '多策略', 'QDII', '货币型', '多空仓型']
                                     , ['CTA', '进攻性资产', '进攻性资产', '稳健性资产', '稳健性资产', '稳健性资产', '稳健性资产', '进攻性资产', '进攻性资产',
                                        '稳健性资产', '进攻性资产']))
        def define_trade_type(inputdf):


            block_detail=inputdf.copy()
            block_detail['操作类型']=[jjfl2stratage_map[x] for x in block_detail['jjfl']]

            style_detail=block_detail.groupby('风格偏好').sum()['change_w']
            size_detail = block_detail.groupby('规模偏好').sum()['change_w']
            ej_detail=block_detail.groupby('ejfl').sum()['change_w']
            # cyjfl_detail=block_detail.groupby('操作类型').sum()['change_w']
            weight_change=[np.nan]*12


            trade_type2=''
            trade_type3=''
            for style in style_detail.index.tolist():

                if(style_detail.loc[style]>0):
                    action='买'
                else:
                    action='卖'

                if(style=='价值'):
                    weight_change[8]=style_detail.loc[style]
                elif(style=='成长'):
                    weight_change[7] = style_detail.loc[style]

                trade_type2+=action+"%.2f%%" % abs(style_detail.loc[style])+style+","

            for style in size_detail.index.tolist():

                if (size_detail.loc[style] > 0):
                    action = '买'
                else:
                    action = '卖'

                if('大' in  style):
                    weight_change[9]=size_detail.loc[style]
                elif('中' in  style):
                    weight_change[10] = size_detail.loc[style]
                elif ('小' in  style):
                    weight_change[11] = size_detail.loc[style]

                trade_type3 += action + "%.2f%%" % abs(size_detail.loc[style])+style+","

            for ejfl in ej_detail.index.tolist():

                if('管理期货' in  ejfl):
                    weight_change[0]=ej_detail.loc[ejfl]
                elif('量化多头' in  ejfl  ):
                    weight_change[1] = ej_detail.loc[ejfl]
                elif ('300指增' in  ejfl):
                    weight_change[2] = ej_detail.loc[ejfl]
                elif ('500指增' in  ejfl):
                    weight_change[3] = ej_detail.loc[ejfl]
                elif ('1000指增' in  ejfl):
                    weight_change[4] = ej_detail.loc[ejfl]
                elif ('主观多头' in  ejfl):
                    weight_change[5] = ej_detail.loc[ejfl]
                elif ('偏股混合型' in  ejfl or '普通股票型' in  ejfl or '灵活配置型' in  ejfl ):
                    weight_change[6] = ej_detail.loc[ejfl]



            if(len(block_detail[block_detail['change_w']>0])>0
                    and len(block_detail[block_detail['change_w'] < 0])>0):

                block_detail['YTM'] = abs(block_detail['YTM'] * block_detail['change_w'])
                buy_ytm=block_detail[block_detail['change_w']>0].sum()['YTM']
                sell_ytm = block_detail[block_detail['change_w'] < 0].sum()['YTM']

                if (buy_ytm>sell_ytm ):
                    if_win = '胜'
                else:
                    if_win = '败'
            else:
                if_win=''

            if(len(block_detail['操作类型'].unique())>1):

                block_detail=block_detail.groupby('操作类型').sum()[['change_w']]
                trade_type = ''
            else:
                if(len(block_detail['ejfl'].unique())>1):
                    block_detail = block_detail.groupby('ejfl').sum()[['change_w']]
                    trade_type = ''

                else:
                    if(if_win!=''):
                        trade_type = '置换{}资产'.format(block_detail['ejfl'].unique()[0])
                    else:
                        if(block_detail['change_w'].sum()>0):
                            trade_type = '购买{}资产'.format("%.2f%%" %abs(block_detail['change_w'].sum())+block_detail['ejfl'].unique()[0])
                        else:
                            trade_type = '卖出{}资产'.format("%.2f%%" %abs(block_detail['change_w'].sum())+block_detail['ejfl'].unique()[0])


            if(trade_type==''):
                for index in block_detail.index.tolist():

                    if(block_detail.loc[index]['change_w']>0):
                        trade_dir='买'
                    else:
                        trade_dir='卖'
                    trade_type+=trade_dir+"%.2f%%" % block_detail.loc[index]['change_w']+index+";"

            return  trade_type,trade_type2,trade_type3,if_win,weight_change


        i=0
        while (i<len(positive_trade)):

            t0=datetime.datetime.strptime(positive_trade.iloc[i]['date']
                                          , '%Y%m%d')
            t_14=(t0+datetime.timedelta(days=14)).strftime('%Y%m%d')
            tempdf=positive_trade[(positive_trade['date']>=positive_trade.iloc[i]['date'])
                           &(positive_trade['date']<=t_14)]

            increase_asset=0
            decrease_asset=0
            for col in ['CTA','量化多头','主观多头','公募偏股','其他']:
                increase_asset+=len(tempdf[tempdf[col+'_weight_change']>0])
                decrease_asset+=len(tempdf[tempdf[col+'_weight_change']<0])
            if(len(tempdf)>1):
            # if(increase_asset>0 and decrease_asset>0):
                i = tempdf.index[-1]
                t0 = datetime.datetime.strptime(positive_trade.iloc[i]['date']
                                                , '%Y%m%d')
                if((t0-datetime.datetime.strptime(tempdf['date'].max(),'%Y%m%d')).days<=7):
                    tempdf=pd.concat([tempdf,positive_trade[(
                            positive_trade['date']==positive_trade.iloc[i]['date'] )]],axis=0)
                    i = tempdf.index[-1] + 1

                positive_trade_block.append(tempdf)

            else:
                if(len(tempdf)==1):
                    positive_trade_block.append(tempdf)
                i += 1

        wc_name = ['CTA_weight_change', '量化多头_weight_change', '300指增_weight_change', '500指增_weight_change',
                   '1000指增_weight_change', '主观多头_weight_change', '公募偏股_weight_change', '国证成长_weight_change'
            , '国证价值_weight_change', '国证大盘_weight_change', '国证中盘_weight_change', '国证小盘_weight_change']
        for i in range(len(positive_trade_block)):
            block=positive_trade_block[i]
            block_detail=\
                trading_detail[trading_detail['date'].isin(block['date'].unique())][['jjdm','cpfl','jjfl','ejfl','风格偏好', '规模偏好','date','change_w','投资基金简称']]


            sql = "select jjdm,jzrq,jjjz from st_fund.t_st_gm_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'" \
                .format(util.list_sql_condition(block_detail[block_detail['cpfl']==2]['jjdm'].tolist())
                        , block_detail['date'].iloc[0], fof_nav['date'].iloc[-1])
            mutual_nav = hbdb.db2df(sql, db='funduser')
            if(len(mutual_nav)>0):
                mutual_nav=mutual_nav.pivot_table('jjjz','jzrq','jjdm')
                for col in mutual_nav.columns:
                    block_detail.loc[block_detail['jjdm']==col,'YTM']=\
                        mutual_nav[mutual_nav[col].notnull()][col].iloc[-1]\
                        /mutual_nav[mutual_nav[col].notnull()][col].iloc[0]-1

            sql = "select jjdm,jzrq,jjjz from st_hedge.t_st_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'" \
                .format(util.list_sql_condition(block_detail[block_detail['cpfl']==4]['jjdm'].tolist())
                        , block_detail['date'].iloc[0], fof_nav['date'].iloc[-1])
            prv_nav = hbdb.db2df(sql, db='highuser')
            if(len(prv_nav)>0):
                prv_nav=prv_nav.pivot_table('jjjz','jzrq','jjdm')
                for col in prv_nav.columns:
                    block_detail.loc[block_detail['jjdm']==col,'YTM']=\
                        prv_nav[prv_nav[col].notnull()][col].iloc[-1]\
                        /prv_nav[prv_nav[col].notnull()][col].iloc[0]-1

            block_detail['trade_group']=i+1

            trade_type,trade_type2,trade_type3,if_win,weight_change=\
                define_trade_type(block_detail)
            block_detail['资产操作类型']=trade_type
            block_detail['风格操作类型'] = trade_type2
            block_detail['市值风格操作类型'] = trade_type3
            block_detail['操作结果'] = if_win

            for j in range(12):
                block_detail[wc_name[j]]=weight_change[j]

            positive_trade_block[i]=block_detail

        positive_trade_block=pd.concat(positive_trade_block,axis=0)
        positive_trade_block['change_w']=positive_trade_block['change_w']/100
        for col in ['change_w','YTM']:
            positive_trade_block[col] = \
                positive_trade_block[col].map("{:.2%}".format)

        positive_trade_block=\
            positive_trade_block.sort_values(['trade_group', 'date'])[['trade_group', 'date', '投资基金简称', 'YTM', 'change_w'
            , 'jjfl', 'ejfl', '资产操作类型', '操作结果', '风格操作类型', '市值风格操作类型']+wc_name]
        silme_positive_trade=positive_trade_block.drop_duplicates('trade_group',keep='last')[['date'
            ,'资产操作类型', '风格操作类型', '市值风格操作类型']+wc_name].set_index('date')
        silme_trade_data=pd.merge(trading_data[['CTA', '主观多头', '量化多头', 'CTA_rank', '主观多头_rank', '量化多头_rank',
       '国证大盘', '国证中盘', '国证小盘', '国证成长', '国证价值', '881001','中证全债', 'CI0077', '公募偏股', '国证大盘_rank',
       '国证中盘_rank', '国证小盘_rank', '国证成长_rank', '国证价值_rank',
       '公募偏股_rank', 'ym', '1000指数增强', '300指数增强', '500指数增强', '1000指数增强_rank',
       '300指数增强_rank', '500指数增强_rank', 'CTAtrend', '主观多头trend', '量化多头trend',
       '国证大盘trend', '国证中盘trend', '国证小盘trend', '国证成长trend', '国证价值trend',
       '公募偏股trend', '1000指数增强trend', '500指数增强trend', '300指数增强trend']],silme_positive_trade,how='left',left_index=True,right_index=True)


        silme_trade_summary=pd.DataFrame(index=wc_name,columns=['买入时点','卖出时点','买入左侧比例','卖出左侧比例'])
        for name in wc_name:
            if(sum(silme_trade_data[name].notnull())>0):
                short_name=name.split('_')[0]
                silme_trade_summary.loc[name,'买入时点']= \
                    sum(silme_trade_data[silme_trade_data[name] > 0][short_name + '_rank'] *
                        silme_trade_data[silme_trade_data[name] > 0][short_name + '_weight_change']) / \
                    silme_trade_data[silme_trade_data[name] > 0][short_name + '_weight_change'].sum()
                silme_trade_summary.loc[name,'卖出时点']= \
                    sum(silme_trade_data[silme_trade_data[name] < 0][short_name + '_rank'] *
                        silme_trade_data[silme_trade_data[name] < 0][short_name + '_weight_change']) / \
                    silme_trade_data[silme_trade_data[name] < 0][short_name + '_weight_change'].sum()

                silme_trade_summary.loc[name,'买入左侧比例']= \
                    sum((silme_trade_data[silme_trade_data[name] > 0][short_name + 'trend'] == -1) * (
                    silme_trade_data[silme_trade_data[name] > 0][short_name + '_weight_change'])) / (
                    silme_trade_data[silme_trade_data[name] > 0][short_name + '_weight_change']).sum()
                silme_trade_summary.loc[name,'卖出左侧比例']= \
                    sum((silme_trade_data[silme_trade_data[name] < 0][short_name + 'trend'] == 1) * (
                    silme_trade_data[silme_trade_data[name] < 0][short_name + '_weight_change'])) / (
                    silme_trade_data[silme_trade_data[name] < 0][short_name + '_weight_change']).sum()

        for col in silme_trade_summary:
            silme_trade_summary[col]=silme_trade_summary[col].map("{:.2%}".format)

        # plot.plotly_table(silme_trade_summary.reset_index(drop=False), 1000, '')
        # plot.plotly_table(negative_trade_summary.reset_index(drop=False), 1000, '')
        # plot.plotly_table(positive_trade_block[['trade_group', 'date', '投资基金', 'YTM', 'change_w'
        #     , 'jjfl', 'ejfl', '资产操作类型', '风格操作类型', '市值风格操作类型']],1500,'')
        positive_trade_block=pd.merge(positive_trade_block,trading_detail[['投资基金简称','风格偏好','规模偏好']].drop_duplicates('投资基金简称')
                                      ,how='left',on='投资基金简称').rename(columns={'trade_group':'交易组',
                                                                             'date':'交易日期',
                                                                             'change_w':'权重变动',
                                                                             'jjfl':'基金分类',
                                                                             'ejfl':'二级分类'})
        positive_trade_block[['交易组', '交易日期','资产操作类型',
                              '风格操作类型', '市值风格操作类型','投资基金简称',
                              '权重变动', '基金分类', '二级分类','风格偏好', '规模偏好']].to_excel(hold_data_dir.replace('基金持仓数据','交易细节'))
        silme_trade_summary.to_excel(hold_data_dir.replace('基金持仓数据', '资产配置交易细节'))

        first_class_asset_weight_his=pd.merge(first_class_asset_weight_his
                                              ,silme_trade_data[['CTA', '主观多头', '量化多头','公募偏股','881001','中证全债', 'CI0077', '国证成长', '国证价值']]
                                              ,how='left',on='date')
        first_class_asset_weight_his.to_excel(hold_data_dir.replace('基金持仓数据', '一级策略权重与指数'))



        data, layout=plot.plotly_line_and_bar(silme_trade_data[['CTA']]
                                                  ,silme_trade_data[['CTA_weight_change']]
                                              ,product+'CTA交易时序')
        plot.plot_render(data, layout)

        data, layout=plot.plotly_line_and_bar(silme_trade_data[['主观多头']]
                                                  ,silme_trade_data[['主观多头_weight_change']]
                                              ,product+'私募股多交易时序')
        plot.plot_render(data, layout)

        data, layout=plot.plotly_line_and_bar(silme_trade_data[['量化多头']]
                                                  ,silme_trade_data[['量化多头_weight_change']]
                                              ,product+'量化多头交易时序')
        plot.plot_render(data, layout)

        data, layout=plot.plotly_line_and_bar(silme_trade_data[['公募偏股']]
                                                  ,silme_trade_data[['公募偏股_weight_change']]
                                              ,product+'公募偏股交易时序')
        plot.plot_render(data, layout)

        data, layout=plot.plotly_line_and_bar(silme_trade_data[['国证成长']]
                                                  ,silme_trade_data[['国证成长_weight_change']]
                                              ,product+'国证成长交易时序')
        plot.plot_render(data, layout)
        data, layout=plot.plotly_line_and_bar(silme_trade_data[['国证价值']]
                                                  ,silme_trade_data[['国证价值_weight_change']]
                                              ,product+'国证价值交易时序')
        plot.plot_render(data, layout)
        data, layout=plot.plotly_line_and_bar(silme_trade_data[['国证大盘']]
                                                  ,silme_trade_data[['国证大盘_weight_change']]
                                              ,product+'国证大盘交易时序')
        plot.plot_render(data, layout)
        data, layout=plot.plotly_line_and_bar(silme_trade_data[['国证中盘']]
                                                  ,silme_trade_data[['国证中盘_weight_change']]
                                              ,product+'国证中盘交易时序')
        plot.plot_render(data, layout)
        data, layout=plot.plotly_line_and_bar(silme_trade_data[['国证小盘']]
                                                  ,silme_trade_data[['国证小盘_weight_change']]
                                              ,product+'国证小盘交易时序')
        plot.plot_render(data, layout)

class FOF_ams_data_analysis:


    def __init__(self,dir1,dir2,product_list):

        for product in product_list:

            self.year_ret_analysis(dir2.replace('@@',product))
            self.define_weight_target(dir1.replace('@@',product))

    @staticmethod
    def define_weight_target(dir,monotonic_lenght=20):

        weight_history=pd.read_excel(dir)
        weight_history.columns=[x.replace('(%)','') for x in weight_history.columns]
        weight_history['日期']=weight_history['日期'].astype(str)
        weight_history['total']=weight_history.sum(axis=1)

        equity_asset=['股票型(私募)', '股票型(公募)', '混合型(公募)']

        weight_history['进攻性资产仓位'] =\
            weight_history[equity_asset].sum(axis=1)

        for col in equity_asset:
            weight_history[col]=\
                weight_history[col]/weight_history['进攻性资产仓位']
        weight_history['进攻性资产仓位']=weight_history['进攻性资产仓位']/100

        weight_target_df=[]

        def trade_stat(q_line_date,weight_history):

            tempdf = pd.DataFrame()

            if(len(q_line_date)>0):
                q_line_date = \
                    [weight_history['日期'].iloc[0]]\
                    +q_line_date['日期'].tolist()\
                    +[weight_history['日期'].iloc[-1]]

                sql = """select zqdm,jyrq,spjg from st_market.t_st_zs_hqql 
                where jyrq in ({0}) and zqdm in ('881001','885001')""" \
                    .format(util.list_sql_condition(q_line_date))

                mu_index_ret = hbdb.db2df(sql, db='alluser').pivot_table('spjg', 'jyrq', 'zqdm')
                mu_index_ret.index = mu_index_ret.index.astype(str)


                for i in range(len(q_line_date)-1):

                    remove_data=int(monotonic_lenght/2)

                    tempdf.loc[q_line_date[i]+" to "+q_line_date[i+1],'权重均值']= \
                        weight_history[(weight_history['日期']>= q_line_date[i])
                                   &(weight_history['日期']<= q_line_date[i+1])][col][remove_data:-remove_data].mean()
                    tempdf.loc[q_line_date[i]+" to "+q_line_date[i+1],'权重中值']=\
                        weight_history[(weight_history['日期']>= q_line_date[i])
                                   &(weight_history['日期']<= q_line_date[i+1])][col][remove_data:-remove_data].median()
                    tempdf.loc[q_line_date[i]+" to "+q_line_date[i+1],'偏离均值']= \
                        weight_history[(weight_history['日期']>= q_line_date[i])
                                   &(weight_history['日期']<= q_line_date[i+1])][col+"_30div"][remove_data:-remove_data].mean()
                    tempdf.loc[q_line_date[i]+" to "+q_line_date[i+1],'偏离最大']= \
                        weight_history[(weight_history['日期']>= q_line_date[i])
                                   &(weight_history['日期']<= q_line_date[i+1])][col+"_30div"][remove_data:-remove_data].max()


                    tempdf.loc[q_line_date[i]+" to "+q_line_date[i+1],'全A涨幅']=\
                        (mu_index_ret.loc[q_line_date[i+1]]['881001']/
                         mu_index_ret.loc[q_line_date[i]]['881001']-1)
                    tempdf.loc[q_line_date[i]+" to "+q_line_date[i+1],'偏股混涨幅']=\
                        (mu_index_ret.loc[q_line_date[i+1]]['885001']/
                         mu_index_ret.loc[q_line_date[i]]['885001']-1)

            else:

                tempdf.loc['全期', '权重均值'] =weight_history[col].mean()
                tempdf.loc['全期', '权重中值'] = weight_history[col].median()

                tempdf.loc['全期', '偏离均值'] =weight_history[col + "_30div"][30:-30].mean()
                tempdf.loc['全期', '偏离最大'] =weight_history[col + "_30div"][30:-30].max()

            return  tempdf

        for col in ['进攻性资产仓位']+equity_asset:

            weight_history[col+"_30MA"]=weight_history[col].rolling(30).mean()
            weight_history[col+"_30div"]=abs(weight_history[col]-weight_history[col+"_30MA"])
            weight_history[col+'Ndays_monotonic']=weight_history[col+"_30div"].rolling(monotonic_lenght).apply(monotonic)
            weight_history[col + 'Ndays_monotonic_T-1']=\
                [np.nan]+weight_history[col+'Ndays_monotonic'][0:-1].tolist()
            weight_history.loc[(weight_history[col+'Ndays_monotonic'] == 1) & (
                        weight_history[col + 'Ndays_monotonic_T-1'] == 0), col+'_q_line'] = True

            weight_history[col+'_q_line']=weight_history[col+'_q_line'].iloc[monotonic_lenght:].tolist()+[np.nan]*monotonic_lenght


            q_line_date=weight_history[weight_history[col+'_q_line']==True]


            tempdf=trade_stat(q_line_date, weight_history)
            less_than1_diff=tempdf[tempdf['权重中值'].diff().abs()<=0.02].index
            while len(less_than1_diff)>0:
                for date_line in less_than1_diff:
                    q_line_date=q_line_date[q_line_date['日期']!=date_line[0:8]]
                tempdf = trade_stat(q_line_date, weight_history)
                less_than1_diff = tempdf[tempdf['权重中值'].diff().abs() <= 0.02].index

            tempdf = tempdf.reset_index(drop=False).rename(columns={'index': '持续日期'})
            tempdf.index = len(tempdf) * [col]
            weight_target_df.append(tempdf)

        weight_target_df=pd.concat(weight_target_df,axis=0)

        for col in ['权重均值','权重中值','偏离均值','偏离最大','全A涨幅','偏股混涨幅']:

            weight_target_df[col]=weight_target_df[col].map("{:.2%}".format)


        plot.plotly_table(weight_target_df.reset_index(),1200,'资产仓位中枢与变动')

    @staticmethod
    def year_ret_analysis(dir):
        nav_history=pd.read_excel(dir)[['日期','累计单位净值']]

        nav_history['日期']=nav_history['日期'].astype(str).str.replace('-','')
        nav_history=nav_history.sort_values('日期')
        nav_history['year']=nav_history['日期'].str[0:4]

        summary=pd.DataFrame(index=nav_history['year'].unique()
                             ,columns=['收益率','波动率'])
        for date in nav_history['year'].unique():
            summary.loc[date,'收益率']=\
                nav_history[nav_history['year']==date]['累计单位净值'].iloc[-1]\
                /nav_history[nav_history['year']==date]['累计单位净值'].iloc[0]-1
            summary.loc[date, '波动率']=\
                nav_history[nav_history['year']==date]['累计单位净值'].pct_change().std()*np.sqrt(250)

        for col in summary.columns:

            summary[col]=summary[col].map("{:.2%}".format)

        plot.plotly_table(summary.reset_index(drop=False),500,'')



        print('')


if __name__ == '__main__':
    #
    # temp_holding_file_analysis()
    #temp_valuation_table_analysis('一堆量化',start_date='20240130',end_date='20240201')

    # fada=FOF_ams_data_analysis("E:\FOF分析\@@\一级策略时序图.xlsx"
    #                            ,"E:\FOF分析\@@\基金净值数据.xls"
    #                            ,product_list=['新方程星动力S7号基金','新方程-北大价值精选FOF1号'])

    # data=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WeChat Files\wxid_xvk2piiub53y12\FileStorage\MsgAttach\9e20f478899dc29eb19741386f9343c8\File\2022-11\881304.WI-成分进出记录-20221123.xlsx")
    # data['日期']=[str(x).replace('-','') for x in data['日期']]
    # data=data.sort_values('日期')



    # sql="select jsrq,zqdm,zqmc,zjbl,zgbl from st_fund.t_st_gm_gpzh where jjdm='001714' and jsrq>='20160101'"
    # data=hbdb.db2df(sql,db='funduser')
    #
    # prv_hold = pd.read_excel(r"E:\GitFolder\docs\私募股多持仓分析\刘泽龙\新方程泓澄精选_S63505_20221122.xls"
    #                          , sheet_name='持仓时序')
    # prv_hold.drop_duplicates('股票简称', inplace=True)
    # mu_hold = pd.read_excel(r"E:\GitFolder\hbshare\fe\FOF\工银zjbl.xlsx")
    # 
    # date_list=mu_hold.columns.tolist()
    # prv_date_list=prv_hold.columns.tolist()[2:]
    # 
    # prv_hold = prv_hold.drop('股票代码',axis=1).set_index('股票简称').T
    # prv_hold=prv_hold.iloc[5:]
    # prv_hold.drop(prv_hold.sum(axis=0)[prv_hold.sum(axis=0) == 0].index.tolist(),axis=1,inplace=True)
    # prv_buy_time=pd.DataFrame(columns=prv_hold.columns.tolist())
    # for zq in prv_hold.columns.unique().tolist():
    #     prv_buy_time.loc['0',zq]=prv_hold[prv_hold[zq].notnull()].index[0]
    # 
    # prv_buy_time=prv_buy_time.T.rename(columns={'0': '泓澄买入时点'})
    # 
    # 
    # mu_hold = mu_hold.set_index('zqmc').T
    # mu_buy_time = pd.DataFrame(columns=mu_hold.columns.tolist())
    # for zq in mu_hold.columns.unique().tolist():
    #     mu_buy_time.loc['0', zq] = mu_hold[mu_hold[zq].notnull()].index[0]
    # 
    # mu_buy_time=mu_buy_time.T.rename(columns={'0': '工银买入时点'})
    # 
    # buy_time=pd.merge(mu_buy_time,prv_buy_time,how='inner',left_index=True,right_index=True)
    # buy_time['泓澄买入时点']=[datetime.datetime.strptime(str(x),
    #                                                '%Y%m%d') for x in buy_time['泓澄买入时点']]
    # buy_time['工银买入时点']=[datetime.datetime.strptime(str(x),
    #                                                '%Y%m%d') for x in buy_time['工银买入时点']]
    # buy_time['diff']=buy_time['泓澄买入时点']-buy_time['工银买入时点']
    # buy_time['diff']=[x.days for x in buy_time['diff']]
    # buy_time.to_excel('买入时点比较.xlsx')

    # #
    # summary_df=pd.DataFrame(index=['工银 交集占持仓数量比','泓澄_交集占持仓数量比','工银 交集占持仓数量比（过去三月）','泓澄_交集占持仓数量比（过去三月）'
    #     ,'工银_交集占股票比例','泓澄_交集占股票比例','工银_交集占股票比例（过去三月）','泓澄_交集占股票比例（过去三月）','当月交集持仓比例差别和'])
    #
    # summary_df_top10 = pd.DataFrame(index=['工银 交集占持仓数量比', '泓澄_交集占持仓数量比',
    #     '工银_交集占股票比例', '泓澄_交集占股票比例', '当月交集持仓比例差别和'])
    #
    # for i in range(1,len(date_list)):
    #
    #     mu_con_hold=mu_hold[mu_hold[date_list[i]].notnull()][['zqmc',date_list[i]]]
    #     mu_zqjc=mu_con_hold['zqmc'].tolist()
    #
    #     mu_con_hold_top10=mu_con_hold.sort_values(date_list[i], ascending=False)[0:10]
    #
    #     prv_con_hold=prv_hold[(prv_hold[prv_date_list[i * 3 + 2]].notnull())
    #     |(prv_hold[prv_date_list[i * 3 + 3]].notnull())
    #     |(prv_hold[prv_date_list[i * 3 + 4]].notnull())][['股票简称']
    #                                                                          +prv_date_list[i * 3 + 2:i * 3 + 5]]
    #     prv_con_hold[prv_date_list[i * 3 + 2:i * 3 + 5]].astype(float)
    #
    #
    #     prv_con_hold2=prv_hold[prv_hold[prv_date_list[i * 3 + 4]].notnull()][['股票简称']+[prv_date_list[i * 3 + 4]]]
    #     prv_con_hold_top10=prv_con_hold2.sort_values(prv_date_list[i * 3 + 4], ascending=False)[0:10]
    #
    #
    #     prv_zqjc=prv_con_hold['股票简称'].unique().tolist()
    #
    #     prv_zqjc2=prv_con_hold2['股票简称'].unique().tolist()
    #
    #     covered_zqjc=list(set(mu_zqjc).intersection(set(prv_zqjc)))
    #
    #     covered_zqjc2=list(set(mu_zqjc).intersection(set(prv_zqjc2)))
    #
    #     joint_holding=pd.merge(mu_con_hold,prv_con_hold2,how='inner',left_on='zqmc',right_on='股票简称').drop('zqmc',axis=1)
    #     joint_holding['diff']=joint_holding[joint_holding.columns[0]]-joint_holding[joint_holding.columns[2]]
    #
    #     value_list=[len(covered_zqjc2)/len(mu_zqjc),len(covered_zqjc2)/len(prv_zqjc2)
    #         ,len(covered_zqjc)/len(mu_zqjc),len(covered_zqjc)/len(prv_zqjc),
    #                 mu_con_hold[mu_con_hold['zqmc'].isin(covered_zqjc2)].sum().iloc[1] / mu_con_hold.sum().iloc[1],
    #                 prv_con_hold2[prv_con_hold2['股票简称'].isin(covered_zqjc2)].sum().iloc[1] / prv_con_hold2.sum().iloc[
    #                     1],
    #                 mu_con_hold[mu_con_hold['zqmc'].isin(covered_zqjc)].sum().iloc[1]/mu_con_hold.sum().iloc[1],
    #                 prv_con_hold[prv_con_hold['股票简称'].isin(covered_zqjc)].sum().iloc[1:].sum()/prv_con_hold.sum().iloc[1:].sum(),
    #                 joint_holding['diff'].abs().sum()]
    #
    #     summary_df[date_list[i]]=value_list
    #
    #     joint_holding_top10=pd.merge(mu_con_hold_top10,prv_con_hold_top10,
    #              how='inner',left_on='zqmc',right_on='股票简称').drop('zqmc',axis=1)
    #     joint_holding_top10['diff'] = joint_holding_top10[joint_holding_top10.columns[0]] - joint_holding_top10[joint_holding_top10.columns[2]]
    #
    #     top_10_joint=list(set(mu_con_hold_top10['zqmc']).intersection(set(prv_con_hold_top10['股票简称'])))
    #
    #     summary_df_top10[date_list[i]]=[len(top_10_joint)/len(mu_con_hold_top10),
    #                                     len(top_10_joint)/len(prv_con_hold_top10),
    #                                     mu_con_hold_top10[mu_con_hold_top10['zqmc'].isin(top_10_joint)].sum().iloc[1]/mu_con_hold_top10.sum().iloc[1],
    #                                     prv_con_hold_top10[prv_con_hold_top10['股票简称'].isin(top_10_joint)].sum().iloc[1]/prv_con_hold_top10.sum().iloc[1],
    #                                     joint_holding_top10['diff'].abs().sum()/100]
    #
    #
    # summary_df.to_excel('持仓对比总结.xlsx',index=True)
    # summary_df_top10.to_excel('top10持仓对比总结.xlsx',index=True)

    # jjdm_list=util.get_bmk_funds_list_20220824('20220630',)
    # sql="select jjdm,min(jzrq) from st_fund.t_st_gm_jjjz where jzrq>='20160331' and jjdm in ({}) group by jjdm "\
    #     .format(util.list_sql_condition(jjdm_list))
    # mu_nav_all=hbdb.db2df(sql,db='funduser')
    # jjdm_list = mu_nav_all[mu_nav_all['min(jzrq)'] <= 20160331]['jjdm'].tolist()
    #
    # sql="select jjdm,min(jzrq) from st_fund.t_st_gm_jjjz where jzrq>='20160331' and jjdm in ({}) group by jjdm "\
    #     .format(util.list_sql_condition(jjdm_list))
    # mu_nav_all=hbdb.db2df(sql,db='funduser')

    # nav_compare = pd.read_excel(r"E:\GitFolder\hbshare\fe\FOF\nav_compare.xlsx")[['日期','泓澄净值日涨跌幅']]
    # sql="select jjdm,jzrq,ljjz from st_fund.t_st_gm_jjjz where jzrq>='20160331' and jjdm in ({})"\
    #     .format(util.list_sql_condition(['001910','161005','000761','660006','519069']))
    # mu_nav_all=hbdb.db2df(sql,db='funduser').pivot_table('ljjz','jzrq','jjdm').pct_change()

    # for i in range(6):
    #
    #     sql="select jjdm,jzrq,ljjz from st_fund.t_st_gm_jjjz where jzrq>='20160331' and jjdm in ({})"\
    #         .format(util.list_sql_condition(jjdm_list[200*i:200*(i+1)]))
    #     mu_nav_all=hbdb.db2df(sql,db='funduser').pivot_table('ljjz','jzrq','jjdm').pct_change()
    #
    #     mu_nav_all=pd.merge(mu_nav_all,nav_compare,
    #                         how='right',left_on='jzrq',right_on='日期').drop('日期',axis=1).corr()[['泓澄净值日涨跌幅']]
    #     mu_nav_all.to_excel('全公募相关性_{}.xlsx'.format(i))

    #mu_nav_all=pd.merge(mu_nav_all,nav_compare[])

    # nav_compare['ym']=nav_compare['日期'].astype(str).str[0:6]
    # nav_compare['year'] = nav_compare['日期'].astype(str).str[0:4]
    #
    # jzcor=nav_compare[['工银净值', '华安逆向策略混合', '华安安信消费', '泓澄净值',  '万得全A',
    #    '万得偏股混合型基金指数','万得金仓200']].corr()
    # retcor=nav_compare[['工银净值日涨跌幅', '华安逆向策略混合涨跌幅', '华安安信消费涨跌幅', '泓澄净值日涨跌幅',
    #    '万得全A涨跌幅', '万得偏股混合型基金指数涨跌幅', '万得金仓200日涨跌幅']].corr()
    #
    # pd.concat([jzcor,retcor],axis=1).to_excel('全期像关系.xlsx')
    #
    # yearjz_cor=[]
    # yearret_cor = []
    # for year in nav_compare['year'].unique().tolist():
    #     yearjz_cor.append(nav_compare[nav_compare['year']==year][['工银净值', '华安逆向策略混合', '华安安信消费', '泓澄净值',  '万得全A',
    #    '万得偏股混合型基金指数','万得金仓200']].corr())
    #     yearret_cor.append(nav_compare[nav_compare['year'] == year][['工银净值日涨跌幅', '华安逆向策略混合涨跌幅', '华安安信消费涨跌幅', '泓澄净值日涨跌幅',
    #    '万得全A涨跌幅', '万得偏股混合型基金指数涨跌幅', '万得金仓200日涨跌幅']].corr())
    #
    # for ym in nav_compare['ym'].unique().tolist():
    #     nav_compare[nav_compare['ym'] == ym][['工银净值', '泓澄净值', '万得金仓200', '万得金仓100', '万得金仓50', '万得金仓30']].corr()
    #     nav_compare[nav_compare['ym'] == ym][['工银净值日涨跌幅', '泓澄净值日涨跌幅', '万得金仓200日涨跌幅', '万得金仓100日涨跌幅', '万得金仓50日涨跌幅',
    #                                               '万得金仓30日涨跌幅']].corr()


    # sql="select jzrq,ljjz from st_fund.t_st_gm_jjjz where jjdm ='519002' and jzrq>='20160331' "
    # mu_nav=hbdb.db2df(sql,db='funduser')
    # mu_nav['jzrq'] = mu_nav['jzrq'].astype(str)
    #
    # prv2=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-11\泓澄16-18年净值(1).xlsx")[['估值日期','单位净值']]
    # prv_3=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-11\净值份额单位净值查询_7118_新方程泓澄精选证券投资基金_20190101_20221118(1).xls")[['日期','累计单位净值']]
    # prv2['日期'] = ["20" + x.split('/')[2] + x.split('/')[1] + x.split('/')[0] for x in prv2['估值日期']]
    # prv_3['日期'] = [str(x)[0:10].replace('-','') for x in prv_3['日期']]
    # prv_3.rename(columns={'累计单位净值':'单位净值'},inplace=True)
    # prv=pd.concat([prv2[prv2['日期']<'20190101'][['日期','单位净值']],prv_3],axis=0)
    #
    # nav_compare = pd.merge(mu_nav, prv, how='inner', left_on='jzrq',right_on='日期').drop('jzrq',axis=1)
    #
    # jincang_index=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WeChat Files\wxid_xvk2piiub53y12\FileStorage\MsgAttach\9e20f478899dc29eb19741386f9343c8\File\2022-11\金仓指数行情序列.xlsx")
    # jincang_index['日期']=[str(x)[0:10].replace('-','') for x in jincang_index['时间']]
    #
    # nav_compare = pd.merge(nav_compare, jincang_index, how='inner', on='日期').drop('时间', axis=1)
    # nav_compare.to_excel('净值比较.xlsx')

    # fa=FOF_analysis(dir=r"E:\FOF分析\{}\交易流水.xlsx"
    #                 .format('大类配置进取型'),end_date='20230630')
    # fa.valuation_table_analysis(product='大类配置进取型',start_date='20221104',end_date='20230630')
    # fa.fromtrading2holding(start_date='20190510',end_date='20221031')

    #['大类配置','易米大类配置','冲精选N1']7
    for product in ['一堆量化']:


        fa = FOF_analysis(dir=r"E:\FOF分析\{}\交易流水.xlsx"
                           .format(product), end_date='20240130')
        fa.valuation_table_analysis(product=product,start_date='20240130',end_date='20240130')
        fa.holding_analysis(dir=r"E:\FOF分析\{}\基金持仓数据.xlsx".format(product),
                             start_date='20230630',end_date='20230930',CTA_bmk_w=1/3,stock_bmk_w=1/3,bond_bmk_w=1/3)
        # fa.fof_trading_analysis(weight_his_dir=r"E:\FOF分析\{}\一级策略时序图.xlsx".format(product)
        #                         ,hold_data_dir=r"E:\FOF分析\{}\基金持仓数据.xlsx".format(product)
        #                         ,start_date='20230930',product=product)



        # fa.fof_trading_analysis(weight_his_dir=r"E:\FOF分析\{}\一级策略时序图.xlsx".format(product)
        #                         ,hold_data_dir=r"E:\FOF分析\{}\基金持仓数据.xlsx".format(product)
        #                         ,start_date='20210119',product=product)

