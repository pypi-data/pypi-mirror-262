# -*- coding:utf-8 -*-
import pandas as pd
from hbshare.fe.XZ import db_engine
from hbshare.fe.XZ import functionality
from hbshare.fe.mutual_analysis import  holdind_based as hb
import numpy as np
import datetime
from hbshare.fe.return_analysis import pool_return_analysis as pra
import time
import  hbshare

util=functionality.Untils()
hbdb=db_engine.HBDB()
localdb=db_engine.PrvFunDB().engine
ia=hb.Industry_analysis()
plot=functionality.Plot(700,350)
ind_map=dict(zip(['股份制银行',
 '房地产开发',
 '软件开发',
 '环境治理',
 '一般零售',
 '轨交设备',
 '电池',
 '基础建设',
 '玻璃玻纤',
 '黑色家电',
 '摩托车及其他',
 '农产品加工',
 '光学光电子',
 '消费电子',
 '水泥',
 '汽车服务',
 '饰品',
 '电力',
 '医药商业',
 '汽车零部件',
 '通信设备',
 'IT服务',
 '综合',
 '通用设备',
 '装修建材',
 '房地产服务',
 '炼化及贸易',
 '工业金属',
 '其他电子',
 '专业工程',
 '计算机设备',
 '航运港口',
 '航空机场',
 '医疗服务',
 '贸易',
 '化学制药',
 '电视广播',
 '工程机械',
 '证券',
 '白色家电',
 '电网设备',
 '生物制品',
 '家电零部件',
 '燃气',
 '农化制品',
 '多元金融',
 '化学纤维',
 '化学原料',
 '中药',
 '酒店餐饮',
 '铁路公路',
 '旅游及景区',
 '造纸',
 '地面兵装',
 '个护用品',
 '教育',
 '出版',
 '照明设备',
 '军工电子',
 '商用车',
 '环保设备',
 '煤炭开采',
 '航空装备',
 '化学制品',
 '白酒',
 '乘用车',
 '自动化设备',
 '林业',
 '广告营销',
 '医疗美容',
 '物流',
 '保险',
 '房屋建设',
 '冶钢原料',
 '金属新材料',
 '元件',
 '小金属',
 '包装印刷',
 '家居用品',
 '影视院线',
 '数字媒体',
 '饲料',
 '特钢',
 '普钢',
 '医疗器械',
 '种植业',
 '休闲食品',
 '焦炭',
 '纺织制造',
 '非白酒',
 '养殖业',
 '能源金属',
 '工程咨询服务',
 '渔业',
 '专用设备',
 '专业连锁',
 '饮料乳品',
 '塑料',
 '通信服务',
 '食品加工',
 '电机',
 '油气开采',
 '贵金属',
 '橡胶',
 '服装家纺',
 '城商行',
 '非金属材料',
 '小家电',
 '互联网电商',
 '厨卫电器',
 '装修装饰',
 '半导体',
 '化妆品',
 '游戏',
 '光伏设备',
 '风电设备',
 '油服工程',
 '其他电源设备',
 '文娱用品',
 '调味发酵品',
 '农业综合',
 '电子化学品',
 '其他家电',
 '动物保健',
 '专业服务',
 '农商行',
 '航天装备',
 '体育',
 '航海装备',
 '网络服务',
 '有色金属冶炼与加工',
 '电气设备',
 '环保工程及服务',
 '家用轻工',
 '建筑装饰',
 '建筑材料',
 '金属制品',
 '计算机应用',
 '石油化工',
 '其他采掘',
 '传媒',
 '铁路运输',
 '酒店',
 '电源设备',
 '稀有金属',
 '金属非金属新材料',
 '互联网传媒',
 '畜禽养殖',
 '国有大型银行',
 '旅游零售',
 '本地生活服务','社交','其他银行'],['银行',
 '房地产',
 '计算机',
 '环保',
 '商贸零售',
 '机械设备',
 '电力设备',
 '建筑装饰',
 '建筑材料',
 '家用电器',
 '汽车',
 '农林牧渔',
 '电子',
 '电子',
 '建筑材料',
 '汽车',
 '纺织服饰',
 '公用事业',
 '医药生物',
 '汽车',
 '通信',
 '计算机',
 '综合',
 '机械设备',
 '建筑材料',
 '房地产',
 '石油石化',
 '有色金属',
 '电子',
 '建筑装饰',
 '计算机',
 '交通运输',
 '交通运输',
 '医药生物',
 '商贸零售',
 '医药生物',
 '传媒',
 '机械设备',
 '非银金融',
 '家用电器',
 '电力设备',
 '医药生物',
 '家用电器',
 '公用事业',
 '基础化工',
 '非银金融',
 '基础化工',
 '基础化工',
 '医药生物',
 '社会服务',
 '交通运输',
 '社会服务',
 '轻工制造',
 '国防军工',
 '美容护理',
 '社会服务',
 '传媒',
 '家用电器',
 '国防军工',
 '汽车',
 '环保',
 '煤炭',
 '国防军工',
 '基础化工',
 '食品饮料',
 '汽车',
 '机械设备',
 '农林牧渔',
 '传媒',
 '美容护理',
 '交通运输',
 '非银金融',
 '建筑装饰',
 '钢铁',
 '有色金属',
 '电子',
 '有色金属',
 '轻工制造',
 '轻工制造',
 '传媒',
 '传媒',
 '农林牧渔',
 '钢铁',
 '钢铁',
 '医药生物',
 '农林牧渔',
 '食品饮料',
 '煤炭',
 '纺织服饰',
 '食品饮料',
 '农林牧渔',
 '有色金属',
 '建筑装饰',
 '农林牧渔',
 '机械设备',
 '商贸零售',
 '食品饮料',
 '基础化工',
 '通信',
 '食品饮料',
 '电力设备',
 '石油石化',
 '有色金属',
 '基础化工',
 '纺织服饰',
 '银行',
 '基础化工',
 '家用电器',
 '商贸零售',
 '家用电器',
 '建筑装饰',
 '电子',
 '美容护理',
 '传媒',
 '电力设备',
 '电力设备',
 '石油石化',
 '电力设备',
 '轻工制造',
 '食品饮料',
 '农林牧渔',
 '电子',
 '家用电器',
 '农林牧渔',
 '社会服务',
 '银行',
 '国防军工',
 '社会服务',
 '国防军工',
 '信息服务',
 '有色金属',
 '机械设备',
 '公用事业',
 '轻工制造',
 '建筑建材',
 '建筑建材',
 '钢铁',
 '信息服务',
 '化工',
 '采掘',
 '信息服务',
 '交通运输',
 '休闲服务',
 '电气设备',
 '有色金属',
 '有色金属',
 '传媒',
 '农林牧渔',
 '银行',
 '商贸零售',
 '社会服务','传媒','银行']))


class old_version:
    @staticmethod
    def industry_pic(jjdm,jjjc,th1=0.5,th2=0.5,show_num=20,if_percentage=True):

        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_industry_property_new",con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_industry_property_new where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        industry_p=pd.read_sql(sql,con=localdb).rename(columns={'cen_ind_1':'一级行业集中度',
                                                                'ratio_ind_1':'一级行业换手率',
                                                                'cen_ind_2': '二级行业集中度',
                                                                'ratio_ind_2': '二级行业换手率',
                                                                'cen_ind_3': '三级行业集中度',
                                                                'ratio_ind_3': '三级行业换手率',
                                                                'industry_num':'行业暴露数',
                                                                'top5': '前五大行业',
                                                                'longtou_med':'龙头占比(时序中位数)',
                                                                'longtou_mean': '龙头占比(时序均值)',
                                                                'longtou_med_rank': '龙头占比(时序中位数)排名',
                                                                'longtou_mean_rank': '龙头占比(时序均值)排名',
                                                                'cen_theme':'主题集中度',
                                                                'ratio_theme':'主题换手率'
                                                                })
        industry_p[['龙头占比(时序均值)','龙头占比(时序中位数)']]=industry_p[['龙头占比(时序均值)','龙头占比(时序中位数)']]/100
        float_col_list=industry_p.columns.tolist()
        float_col_list.remove('jjdm')
        float_col_list.remove('asofdate')
        float_col_list.remove('前五大行业')


        industry_detail_df_list=[]
        class_name_list=['yjxymc','ejxymc','sjxymc']
        name_map=dict(zip([ 'zsbl_mean', 'ROE_mean', 'NETASSETPS_mean',
           'DIVIDENDRATIO_mean', 'OPERCASHFLOWPS_mean', 'TOTALMV_mean', 'PE_mean',
           'PB_mean', 'PEG_mean', 'EPS_mean', 'NETPROFITGROWRATE_mean',
           'OPERATINGREVENUEYOY_mean', 'longtou_zjbl_for_ind_mean', 'zsbl_med',
           'ROE_med', 'NETASSETPS_med', 'DIVIDENDRATIO_med', 'OPERCASHFLOWPS_med',
           'TOTALMV_med', 'PE_med', 'PB_med', 'PEG_med', 'EPS_med',
           'NETPROFITGROWRATE_med', 'OPERATINGREVENUEYOY_med',
           'longtou_zjbl_for_ind_med', 'jjdm', 'zsbl_mean_rank', 'ROE_mean_rank',
           'NETASSETPS_mean_rank', 'DIVIDENDRATIO_mean_rank',
           'OPERCASHFLOWPS_mean_rank', 'TOTALMV_mean_rank', 'PE_mean_rank',
           'PB_mean_rank', 'PEG_mean_rank', 'EPS_mean_rank',
           'NETPROFITGROWRATE_mean_rank', 'OPERATINGREVENUEYOY_mean_rank',
           'longtou_zjbl_for_ind_mean_rank', 'zsbl_med_rank', 'ROE_med_rank',
           'NETASSETPS_med_rank', 'DIVIDENDRATIO_med_rank',
           'OPERCASHFLOWPS_med_rank', 'TOTALMV_med_rank', 'PE_med_rank',
           'PB_med_rank', 'PEG_med_rank', 'EPS_med_rank',
           'NETPROFITGROWRATE_med_rank', 'OPERATINGREVENUEYOY_med_rank',
           'longtou_zjbl_for_ind_med_rank', 'growth_mean_rank', 'value_mean_rank',
           'growth_med_rank', 'value_med_rank'],['占持仓比例(时序均值)','净资产收益率(时序均值)',
                                                 '每股净资产与价格比率(时序均值)','股息率(时序均值)',
                                                 '经营现金流与价格比率(时序均值)','总市值(时序均值)',
                                                 'PE(时序均值)','PB(时序均值)','PEG(时序均值)',
                                                 '每股收益与价格比率(时序均值)','净利润增长率(时序均值)',
                                                 '主营业务增长率(时序均值)','行业龙头占比(时序均值)',
                                                 '占持仓比例(时序中位数)','净资产收益率(时序中位数)',
                                                 '每股净资产与价格比率(时序中位数)','股息率(时序中位数)',
                                                 '经营现金流与价格比率(时序中位数)','总市值(时序中位数)',
                                                 'PE(时序中位数)','PB(时序中位数)','PEG(时序中位数)',
                                                 '每股收益与价格比率(时序中位数)','净利润增长率(时序中位数)',
                                                 '主营业务增长率(时序中位数)','行业龙头占比(时序中位数)',
                                                 'jjdm','占持仓比例(时序均值)排名','净资产收益率(时序均值)排名',
                                                 '每股净资产与价格比率(时序均值)排名','股息率(时序均值)排名',
                                                 '经营现金流与价格比率(时序均值)排名','总市值(时序均值)排名',
                                                 'PE(时序均值)排名','PB(时序均值)排名','PEG(时序均值)排名',
                                                 '每股收益与价格比率(时序均值)排名','净利润增长率(时序均值)排名',
                                                 '主营业务增长率(时序均值)排名','行业龙头占比(时序均值)排名',
                                                 '占持仓比例(时序中位数)排名','净资产收益率(时序中位数)排名',
                                                 '每股净资产与价格比率(时序中位数)排名','股息率(时序中位数)排名',
                                                 '经营现金流与价格比率(时序中位数)排名','总市值(时序中位数)排名',
                                                 'PE(时序中位数)排名','PB(时序中位数)排名','PEG(时序中位数)排名',
                                                 '每股收益与价格比率(时序中位数)排名','净利润增长率(时序中位数)排名',
                                                 '主营业务增长率(时序中位数)排名','行业龙头占比(时序中位数)排名',
                                                 '综合成长属性(时序均值)排名','综合价值属性(时序均值)排名','综合成长属性(时序中位数)排名',
                                                 '综合价值属性(时序中位数)排名','asofdate']))

        sql=" select * from hbs_industry_financial_stats where ENDDATE>='{0}' and ENDDATE<='{1}'"\
            .format(str(int(latest_date[0:4])-3)+latest_date[4:6],latest_date[0:6])
        industry_financial_info=pd.read_sql(sql,con=localdb)

        industry_financial_info[['ROE','NETPROFITGROWRATE',
                                 'OPERATINGREVENUEYOY','DIVIDENDRATIO']]=industry_financial_info[['ROE','NETPROFITGROWRATE',
                                 'OPERATINGREVENUEYOY','DIVIDENDRATIO']]/100

        industry_financial_info_mean=industry_financial_info\
            .groupby('industry_name').median().rename(columns={
            "ROE":"行业净资产收益率","EPS":"行业每股收益比股价","OPERCASHFLOWPS":"行业经营现金流与价格比率",
            "NETPROFITGROWRATE":"行业净利润增长率","OPERATINGREVENUEYOY":"行业主营业务增长率",
            "NETASSETPS":"行业每股净资产与价格比率","DIVIDENDRATIO":"行业股息率","AVERAGEMV":"行业平均市值","TOTALMV":"行业总市值",
            "PE":"行业PE","PB":"行业PB","PEG":"行业PEG"})
        industry_financial_info_med=industry_financial_info\
            .groupby('industry_name').median().rename(columns={
            "ROE":"行业净资产收益率","EPS":"行业每股收益比股价","OPERCASHFLOWPS":"行业经营现金流与价格比率",
            "NETPROFITGROWRATE":"行业净利润增长率","OPERATINGREVENUEYOY":"行业主营业务增长率",
            "NETASSETPS":"行业每股净资产与价格比率","DIVIDENDRATIO":"行业股息率","AVERAGEMV":"行业平均市值","TOTALMV":"行业总市值",
            "PE":"行业PE","PB":"行业PB","PEG":"行业PEG"})

        industry_financial_info=pd.merge(industry_financial_info_mean,industry_financial_info_med,
                                         how='inner',left_index=True,right_index=True)

        industry_financial_info.columns=industry_financial_info.columns.str.replace('TOP',"")
        industry_financial_info.columns = industry_financial_info.columns.str.replace('TOP', "")
        industry_financial_info.columns = industry_financial_info.columns.str.replace('MV', "市值")
        industry_financial_info.columns = industry_financial_info.columns.str.replace('%', "分位数")
        industry_financial_info.columns = industry_financial_info.columns.str.replace('_x', "(时序均值)")
        industry_financial_info.columns = industry_financial_info.columns.str.replace('_y', "(时序中位数)")
        industry_financial_info.reset_index(inplace=True)

        theme_weight=pd.DataFrame()
        for i in range(3):
            latest_date = pd.read_sql(
                "select max(asofdate) as asofdate from hbs_industry_property_{0}_industry_level".format(i+1), con=localdb)['asofdate'][0]

            sql = "SELECT * from hbs_industry_property_{2}_industry_level where jjdm='{0}' and asofdate='{1}' " \
                .format(jjdm, latest_date,i+1)
            temp_ind_detail=pd.read_sql(sql, con=localdb).rename(columns=name_map)
            temp_ind_detail.rename(columns={class_name_list[i]:'行业名称'},inplace=True)
            temp_ind_detail=temp_ind_detail.sort_values('占持仓比例(时序均值)', ascending=False).iloc[0:show_num]
            temp_ind_detail[['行业龙头占比(时序均值)', '行业龙头占比(时序中位数)',
                             '净资产收益率(时序均值)','股息率(时序均值)','净利润增长率(时序均值)',
                             '主营业务增长率(时序均值)','净资产收益率(时序中位数)','股息率(时序中位数)',
                             '净利润增长率(时序中位数)', '主营业务增长率(时序中位数)']] = temp_ind_detail[['行业龙头占比(时序均值)', '行业龙头占比(时序中位数)',
                             '净资产收益率(时序均值)','股息率(时序均值)','净利润增长率(时序均值)',
                             '主营业务增长率(时序均值)','净资产收益率(时序中位数)','股息率(时序中位数)',
                             '净利润增长率(时序中位数)', '主营业务增长率(时序中位数)']] / 100

            temp_ind_detail=pd.merge(temp_ind_detail,industry_financial_info,
                                     how='left',left_on='行业名称',right_on='industry_name')

            temp_ind_detail=temp_ind_detail[['行业名称', '占持仓比例(时序均值)',
           '占持仓比例(时序均值)排名',
            '综合价值属性(时序均值)排名','综合成长属性(时序均值)排名',
            '行业龙头占比(时序均值)', '行业龙头占比(时序均值)排名',
           '主营业务增长率(时序均值)','主营业务增长率(时序均值)排名','行业主营业务增长率(时序均值)',
            '净利润增长率(时序均值)','净利润增长率(时序均值)排名','行业净利润增长率(时序均值)',
           '净资产收益率(时序均值)','净资产收益率(时序均值)排名','行业净资产收益率(时序均值)',
           '每股净资产与价格比率(时序均值)', '每股净资产与价格比率(时序均值)排名','行业每股净资产与价格比率(时序均值)',
          '每股收益与价格比率(时序均值)', '每股收益与价格比率(时序均值)排名','行业每股收益比股价(时序均值)',
           '经营现金流与价格比率(时序均值)','经营现金流与价格比率(时序均值)排名','行业经营现金流与价格比率(时序均值)',
           '股息率(时序均值)', '股息率(时序均值)排名','行业股息率(时序均值)',
            'PE(时序均值)', 'PE(时序均值)排名','行业PE(时序均值)',
            'PB(时序均值)', 'PB(时序均值)排名','行业PB(时序均值)',
            'PEG(时序均值)', 'PEG(时序均值)排名','行业PEG(时序均值)',
     '总市值(时序均值)','总市值(时序均值)排名', '行业平均市值(时序均值)','25分位数市值(时序均值)','50分位数市值(时序均值)', '75分位数市值(时序均值)',
                                             '90分位数市值(时序均值)','asofdate',
                                             '占持仓比例(时序中位数)', '占持仓比例(时序中位数)排名','综合价值属性(时序中位数)排名',
                                             '综合成长属性(时序中位数)排名','行业龙头占比(时序中位数)', '行业龙头占比(时序中位数)排名',
                                             '主营业务增长率(时序中位数)', '主营业务增长率(时序中位数)排名',
                                             '净利润增长率(时序中位数)', '净利润增长率(时序中位数)排名','行业净利润增长率(时序中位数)',
                                             '净资产收益率(时序中位数)', '净资产收益率(时序中位数)排名','行业净资产收益率(时序中位数)',
                                             '每股净资产与价格比率(时序中位数)', '每股净资产与价格比率(时序中位数)排名','行业每股净资产与价格比率(时序中位数)',
                                             '每股收益与价格比率(时序中位数)','每股收益与价格比率(时序中位数)排名','行业每股收益比股价(时序中位数)',
                                             '经营现金流与价格比率(时序中位数)', '经营现金流与价格比率(时序中位数)排名','行业经营现金流与价格比率(时序中位数)',
                                             '股息率(时序中位数)', '股息率(时序中位数)排名','行业股息率(时序中位数)',
                                             'PE(时序中位数)','PE(时序中位数)排名','行业PE(时序中位数)',
                                             'PB(时序中位数)','PB(时序中位数)排名','行业PB(时序中位数)',
                                             'PEG(时序中位数)','PEG(时序中位数)排名','行业PEG(时序中位数)',
                                             '总市值(时序中位数)', '总市值(时序中位数)排名',
                                             '行业平均市值(时序中位数)', '25分位数市值(时序中位数)', '50分位数市值(时序中位数)', '75分位数市值(时序中位数)',
                                             '90分位数市值(时序中位数)'
                                             ]]

            ind_detial_float_col=temp_ind_detail.columns.tolist()
            ind_detial_float_col.sort()
            for col in ['总市值(时序中位数)','总市值(时序中位数)排名',
     '总市值(时序均值)','总市值(时序均值)排名', '行业平均市值(时序中位数)','25分位数市值(时序中位数)',
                        '50分位数市值(时序中位数)', '75分位数市值(时序中位数)', '90分位数市值(时序中位数)','行业平均市值(时序均值)','25分位数市值(时序均值)',
                        '50分位数市值(时序均值)', '75分位数市值(时序均值)', '90分位数市值(时序均值)','asofdate','行业名称',
                        'PE(时序中位数)','PE(时序均值)','PEG(时序中位数)','PEG(时序均值)',
                        'PB(时序中位数)','PB(时序均值)','行业PE(时序中位数)','行业PB(时序中位数)','行业PEG(时序中位数)','行业PE(时序均值)','行业PB(时序均值)','行业PEG(时序均值)']:
                ind_detial_float_col.remove(col)
            if(i==0):
                theme_weight=temp_ind_detail[['行业名称', '占持仓比例(时序均值)']]
            if(if_percentage):
                for col in ind_detial_float_col:
                    temp_ind_detail[col]=temp_ind_detail[col].map("{:.2%}".format)
            industry_detail_df_list.append(temp_ind_detail )


        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_industry_shift_property_new",con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_industry_shift_property_new where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        industry_sp=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
        ind_sp_float_col_list=industry_sp.columns.tolist()
        ind_sp_float_col_list.remove('jjdm')
        ind_sp_float_col_list.remove('asofdate')


        #generate the label:
        if(industry_p['一级行业集中度'][0]>th1 and industry_p['一级行业换手率'][0]>th2):
            industry_p['一级行业类型']='博弈'
        elif(industry_p['一级行业集中度'][0]>th1 and industry_p['一级行业换手率'][0]<th2):
            industry_p['一级行业类型'] = '专注'
        elif(industry_p['一级行业集中度'][0]<th1 and industry_p['一级行业换手率'][0]>th2):
            industry_p['一级行业类型'] = '轮动'
        elif(industry_p['一级行业集中度'][0]<th1 and industry_p['一级行业换手率'][0]<th2):
            industry_p['一级行业类型'] = '配置'


        if(industry_p['二级行业集中度'][0]>th1 and industry_p['二级行业换手率'][0]>th2):
            industry_p['二级行业类型']='博弈'
        elif(industry_p['二级行业集中度'][0]>th1 and industry_p['二级行业换手率'][0]<th2):
            industry_p['二级行业类型'] = '专注'
        elif(industry_p['二级行业集中度'][0]<th1 and industry_p['二级行业换手率'][0]>th2):
            industry_p['二级行业类型'] = '轮动'
        elif(industry_p['二级行业集中度'][0]<th1 and industry_p['二级行业换手率'][0]<th2):
            industry_p['二级行业类型'] = '配置'

        if(industry_p['三级行业集中度'][0]>th1 and industry_p['三级行业换手率'][0]>th2):
            industry_p['三级行业类型']='博弈'
        elif(industry_p['三级行业集中度'][0]>th1 and industry_p['三级行业换手率'][0]<th2):
            industry_p['三级行业类型'] = '专注'
        elif(industry_p['三级行业集中度'][0]<th1 and industry_p['三级行业换手率'][0]>th2):
            industry_p['三级行业类型'] = '轮动'
        elif(industry_p['三级行业集中度'][0]<th1 and industry_p['三级行业换手率'][0]<th2):
            industry_p['三级行业类型'] = '配置'

        if (industry_p['主题集中度'][0] > th1 and industry_p['主题换手率'][0] > th2):
            industry_p['主题类型'] = '博弈'
        elif (industry_p['主题集中度'][0] > th1 and industry_p['主题换手率'][0] < th2):
            industry_p['主题类型'] = '专注'
        elif (industry_p['主题集中度'][0] < th1 and industry_p['主题换手率'][0] > th2):
            industry_p['主题类型'] = '轮动'
        elif (industry_p['主题集中度'][0] < th1 and industry_p['主题换手率'][0] < th2):
            industry_p['主题类型'] = '配置'
        if(if_percentage):
            for col in float_col_list:
                industry_p[col]=industry_p[col].map("{:.2%}".format)
            for col in ind_sp_float_col_list[0:int(len(ind_sp_float_col_list)/2)]:
                industry_sp.loc[industry_sp.index!='切换次数',col]=\
                    industry_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
            for col in ind_sp_float_col_list[int(len(ind_sp_float_col_list)/2):]:
                industry_sp[col]=\
                    industry_sp[col].astype(float).map("{:.2%}".format)

        industry_p['基金简称']=[jjjc]
        # industry_p_old['基金简称']=[jjjc]

        #theme picture
        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from hbs_theme_shift_property_new", con=localdb)['asofdate'][0]

        sql = "SELECT * from hbs_theme_shift_property_new where jjdm='{0}' and asofdate='{1}' " \
            .format(jjdm, latest_date)
        theme_sp = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)

        theme_sp_float_col_list = theme_sp.columns.tolist()
        theme_sp_float_col_list.remove('jjdm')
        theme_sp_float_col_list.remove('asofdate')

        if (if_percentage):
            for col in theme_sp_float_col_list[0:int(len(theme_sp_float_col_list) / 2)]:
                theme_sp.loc[theme_sp.index != '切换次数', col] = \
                    theme_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
            for col in theme_sp_float_col_list[int(len(theme_sp_float_col_list) / 2):]:
                theme_sp[col] = \
                    theme_sp[col].astype(float).map("{:.2%}".format)

        theme_weight=pd.merge(theme_weight,ia.ind2thememap,
                              how='left',left_on='行业名称',right_on='industry_name').drop('industry_name',axis=1)
        theme_weight=theme_weight.groupby('theme').sum().T.reset_index(drop=True)
        for col in theme_weight.columns:
            theme_weight[col] = \
                theme_weight[col].astype(float).map("{:.2%}".format)

        industry_p=pd.concat([industry_p,theme_weight],axis=1)
        theme_p=industry_p[['jjdm','基金简称','主题类型','主题集中度', '主题换手率','大金融', '消费', 'TMT',
           '周期', '制造', 'asofdate']]
        theme_sp = theme_sp[['Total_rank',
                             '大金融_rank', '消费_rank', 'TMT_rank', '周期_rank', '制造_rank',
                             'Total', '大金融', '消费', 'TMT', '周期', '制造', 'asofdate']]
        theme_sp.reset_index(inplace=True)


        industry_p=industry_p[['jjdm','基金简称','一级行业类型','一级行业集中度', '一级行业换手率','前五大行业','龙头占比(时序均值)',
           '龙头占比(时序中位数)', '龙头占比(时序均值)排名', '龙头占比(时序中位数)排名','二级行业类型','二级行业集中度', '二级行业换手率',
                               '三级行业类型','三级行业集中度', '三级行业换手率','asofdate']]

        industry_sp=industry_sp[['Total_rank', '农林牧渔_rank',
           '基础化工_rank', '钢铁_rank', '有色金属_rank', '电子_rank', '家用电器_rank',
           '食品饮料_rank', '纺织服饰_rank', '轻工制造_rank', '医药生物_rank', '公用事业_rank',
           '交通运输_rank', '房地产_rank', '商贸零售_rank', '社会服务_rank', '综合_rank',
           '建筑材料_rank', '建筑装饰_rank', '电力设备_rank', '国防军工_rank', '计算机_rank',
           '传媒_rank', '通信_rank', '银行_rank', '非银金融_rank', '汽车_rank', '机械设备_rank',
           '煤炭_rank', '石油石化_rank', '环保_rank', '美容护理_rank','Total', '农林牧渔', '基础化工', '钢铁', '有色金属', '电子', '家用电器', '食品饮料', '纺织服饰',
           '轻工制造', '医药生物', '公用事业', '交通运输', '房地产', '商贸零售', '社会服务', '综合', '建筑材料',
           '建筑装饰', '电力设备', '国防军工', '计算机', '传媒', '通信', '银行', '非银金融', '汽车', '机械设备',
           '煤炭', '石油石化', '环保', '美容护理','asofdate']]
        industry_sp.reset_index(inplace=True)

        return industry_p,industry_sp,theme_p,theme_sp,industry_detail_df_list

    @staticmethod
    def style_pic(jjdm,jjjc,fre,th1=0.5,th2=0.5,if_percentage=True):

        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from nav_style_property_value where fre='{0}'"
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from nav_style_property_value where jjdm='{0}' and fre='{1}' and asofdate='{2}' "\
            .format(jjdm,fre,latest_date)
        value_p=pd.read_sql(sql,con=localdb).rename(columns={'shift_ratio_rank':'换手率排名',
                                                             'centralization_rank':'集中度排名',
                                                             '成长_mean':'成长暴露排名',
                                                             '价值_mean':'价值暴露排名',
                                                             '成长_abs_mean': '成长绝对暴露',
                                                             '价值_abs_mean': '价值绝对暴露',
                                                             'manager_change':'经理是否未变更',
                                                             'shift_ratio':'换手率',
                                                             'centralization':'集中度',
                                                             'fre':'回归周期',
                                                             })


        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_style_property "
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_style_property where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        value_p_hbs=pd.read_sql(sql,con=localdb).rename(columns={'cen_lv':'集中度(持仓)',
                                                                 'shift_lv':'换手率(持仓)',
                                                                 '成长':'成长绝对暴露(持仓)',
                                                                 '价值':'价值绝对暴露(持仓)',
                                                                 'cen_lv_rank':'集中度排名(持仓)',
                                                                 'shift_lv_rank':'换手率排名(持仓)',
                                                                 '成长_rank':'成长暴露排名(持仓)',
                                                                 '价值_rank':'价值暴露排名(持仓)',})


        # generate the label for nav based :
        winning_value=value_p[['成长暴露排名','价值暴露排名']].T[value_p[['成长暴露排名','价值暴露排名']].T[0]
                                                     ==value_p[['成长暴露排名','价值暴露排名']].T.max()[0]].index[0]
        if(value_p['集中度排名'][0]>th1 and value_p['换手率排名'][0]>th2 ):
            value_p['风格类型']='博弈'
            value_p['风格偏好']=winning_value[0:2]
        elif(value_p['集中度排名'][0]>th1 and value_p['换手率排名'][0]<th2 ):
            value_p['风格类型'] = '专注'
            value_p['风格偏好'] = winning_value[0:2]
        elif(value_p['集中度排名'][0]<th1 and value_p['换手率排名'][0]>th2 ):
            value_p['风格类型'] = '轮动'
            value_p['风格偏好'] = '均衡'
        elif(value_p['集中度排名'][0]<th1 and value_p['换手率排名'][0]<th2 ):
            value_p['风格类型'] = '配置'
            value_p['风格偏好'] =  '均衡'

        value_p['基金简称']=jjjc
        value_p=value_p[['jjdm','基金简称','风格类型','风格偏好','换手率排名','集中度排名',
                         '成长暴露排名', '价值暴露排名','成长绝对暴露','价值绝对暴露' ,'经理是否未变更',
                         '换手率', '集中度','回归周期','asofdate']]

        # generate the label for hbs based :
        winning_value=value_p_hbs[['成长暴露排名(持仓)','价值暴露排名(持仓)']].T[value_p_hbs[['成长暴露排名(持仓)','价值暴露排名(持仓)']].T[0]
                                                     ==value_p_hbs[['成长暴露排名(持仓)','价值暴露排名(持仓)']].T.max()[0]].index[0]
        if(value_p_hbs['集中度排名(持仓)'][0]>th1 and value_p_hbs['换手率排名(持仓)'][0]>th2 ):
            value_p_hbs['风格类型']='博弈'
            value_p_hbs['风格偏好']=winning_value[0:2]
        elif(value_p_hbs['集中度排名(持仓)'][0]>th1 and value_p_hbs['换手率排名(持仓)'][0]<th2 ):
            value_p_hbs['风格类型'] = '专注'
            value_p_hbs['风格偏好'] = winning_value[0:2]
        elif(value_p_hbs['集中度排名(持仓)'][0]<th1 and value_p_hbs['换手率排名(持仓)'][0]>th2 ):
            value_p_hbs['风格类型'] = '轮动'
            value_p_hbs['风格偏好'] = '均衡'
        elif(value_p_hbs['集中度排名(持仓)'][0]<th1 and value_p_hbs['换手率排名(持仓)'][0]<th2 ):
            value_p_hbs['风格类型'] = '配置'
            value_p_hbs['风格偏好'] =  '均衡'

        value_p_hbs['基金简称']=jjjc
        value_p_hbs=value_p_hbs[['jjdm','基金简称','风格类型','风格偏好','集中度(持仓)', '换手率(持仓)',
                                 '成长绝对暴露(持仓)', '价值绝对暴露(持仓)', '集中度排名(持仓)',
           '换手率排名(持仓)', '成长暴露排名(持仓)', '价值暴露排名(持仓)', 'asofdate']]

        if(if_percentage):
            for col in ['集中度(持仓)', '换手率(持仓)', '成长绝对暴露(持仓)', '价值绝对暴露(持仓)', '集中度排名(持仓)',
               '换手率排名(持仓)', '成长暴露排名(持仓)', '价值暴露排名(持仓)']:
                value_p_hbs[col]=value_p_hbs[col].map("{:.2%}".format)

        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from nav_style_property_size where fre='{0}'"
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from nav_style_property_size where jjdm='{0}' and fre='{1}' and asofdate='{2}' "\
            .format(jjdm,fre,latest_date)
        size_p=pd.read_sql(sql,con=localdb).rename(columns={'shift_ratio_rank':'换手率排名',
                                                             'centralization_rank':'集中度排名',
                                                             '大盘_mean':'大盘暴露排名',
                                                             '中盘_mean':'中盘暴露排名',
                                                            '小盘_mean':'小盘暴露排名',
                                                            '大盘_abs_mean': '大盘绝对暴露',
                                                            '中盘_abs_mean': '中盘绝对暴露',
                                                            '小盘_abs_mean': '小盘绝对暴露',
                                                             'manager_change':'经理是否未变更',
                                                             'shift_ratio':'换手率',
                                                             'centralization':'集中度',
                                                             'fre':'回归周期',
                                                             })

        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_size_property "
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_size_property where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        size_p_hbs=pd.read_sql(sql,con=localdb).rename(columns={'cen_lv':'集中度(持仓)',
                                                                 'shift_lv':'换手率(持仓)',
                                                                 '大盘':'大盘绝对暴露(持仓)',
                                                                 '中盘':'中盘绝对暴露(持仓)',
                                                                 '小盘': '小盘绝对暴露(持仓)',
                                                                 'cen_lv_rank':'集中度排名(持仓)',
                                                                 'shift_lv_rank':'换手率排名(持仓)',
                                                                 '大盘_rank':'大盘暴露排名(持仓)',
                                                                 '中盘_rank':'中盘暴露排名(持仓)',
                                                                 '小盘_rank': '小盘暴露排名(持仓)',
                                                                })



        # generate the label for nav based :
        winning_size=[x[0] for x in size_p[['大盘暴露排名','中盘暴露排名','小盘暴露排名']].T[size_p[['大盘暴露排名','中盘暴露排名','小盘暴露排名']].T[0]>0.5].index.tolist()]
        winning_size=''.join(winning_size)

        if(size_p['集中度排名'][0]>th1 and size_p['换手率排名'][0]>th2 ):
            size_p['规模风格类型']='博弈'
            size_p['规模偏好']=winning_size
        elif(size_p['集中度排名'][0]>th1 and size_p['换手率排名'][0]<th2 ):
            size_p['规模风格类型'] = '专注'
            size_p['规模偏好'] = winning_size
        elif(size_p['集中度排名'][0]<th1 and size_p['换手率排名'][0]>th2 ):
            size_p['规模风格类型'] = '轮动'
            size_p['规模偏好'] = '均衡'
        elif(size_p['集中度排名'][0]<th1 and size_p['换手率排名'][0]<th2 ):
            size_p['规模风格类型'] = '配置'
            size_p['规模偏好'] ='均衡'

        size_p['基金简称']=jjjc
        size_p=size_p[['jjdm','基金简称','规模风格类型','规模偏好','换手率排名','集中度排名','大盘暴露排名',
                       '大盘绝对暴露','中盘暴露排名','中盘绝对暴露','小盘暴露排名','小盘绝对暴露', '经理是否未变更',
                         '换手率', '集中度','回归周期','asofdate']]

        # generate the label for hbs based :
        winning_size=[x[0] for x in size_p_hbs[['大盘暴露排名(持仓)','中盘暴露排名(持仓)','小盘暴露排名(持仓)']].T[size_p_hbs[['大盘暴露排名(持仓)','中盘暴露排名(持仓)','小盘暴露排名(持仓)']].T[0]>0.5].index.tolist()]
        winning_size=''.join(winning_size)

        if(size_p_hbs['集中度排名(持仓)'][0]>th1 and size_p_hbs['换手率排名(持仓)'][0]>th2 ):
            size_p_hbs['规模风格类型']='博弈'
            size_p_hbs['规模偏好']=winning_size
        elif(size_p_hbs['集中度排名(持仓)'][0]>th1 and size_p_hbs['换手率排名(持仓)'][0]<th2 ):
            size_p_hbs['规模风格类型'] = '专注'
            size_p_hbs['规模偏好'] = winning_size
        elif(size_p_hbs['集中度排名(持仓)'][0]<th1 and size_p_hbs['换手率排名(持仓)'][0]>th2 ):
            size_p_hbs['规模风格类型'] = '轮动'
            size_p_hbs['规模偏好'] = '均衡'
        elif(size_p_hbs['集中度排名(持仓)'][0]<th1 and size_p_hbs['换手率排名(持仓)'][0]<th2 ):
            size_p_hbs['规模风格类型'] = '配置'
            size_p_hbs['规模偏好'] ='均衡'

        size_p_hbs['基金简称']=jjjc
        size_p_hbs=size_p_hbs[['jjdm','基金简称','规模风格类型','规模偏好','集中度(持仓)', '换手率(持仓)', '大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)',
           '集中度排名(持仓)', '换手率排名(持仓)', '大盘暴露排名(持仓)', '中盘暴露排名(持仓)', '小盘暴露排名(持仓)',
        'asofdate']]
        if (if_percentage):
            for col in ['集中度(持仓)', '换手率(持仓)', '大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)',
               '集中度排名(持仓)', '换手率排名(持仓)', '大盘暴露排名(持仓)', '中盘暴露排名(持仓)', '小盘暴露排名(持仓)']:
                size_p_hbs[col]=size_p_hbs[col].map("{:.2%}".format)

        #shift property for nav based
        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from nav_shift_property_value where fre='{0}'"
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from nav_shift_property_value where jjdm='{0}' and asofdate='{1}' and fre='{2}' "\
            .format(jjdm,latest_date,fre)
        value_sp=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
        value_sp_float_col_list=value_sp.columns.tolist()
        value_sp_float_col_list.remove('jjdm')
        value_sp_float_col_list.remove('asofdate')
        value_sp_float_col_list.remove('fre')


        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from nav_shift_property_size where fre='{0}'"
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from nav_shift_property_size where jjdm='{0}' and asofdate='{1}' and fre='{2}' "\
            .format(jjdm,latest_date,fre)
        size_sp=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
        size_sp_float_col_list=size_sp.columns.tolist()
        size_sp_float_col_list.remove('jjdm')
        size_sp_float_col_list.remove('asofdate')
        size_sp_float_col_list.remove('fre')



        # shift property for hbs based
        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_shift_property_value"
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_shift_property_value where jjdm='{0}' and asofdate='{1}'  "\
            .format(jjdm,latest_date)
        value_sp_hbs=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
        value_sp_hbs_float_col_list=value_sp_hbs.columns.tolist()
        value_sp_hbs_float_col_list.remove('jjdm')
        value_sp_hbs_float_col_list.remove('asofdate')


        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_shift_property_size "
                .format(fre),con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_shift_property_size where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        size_sp_hbs=pd.read_sql(sql,con=localdb).set_index('项目名').fillna(0)
        size_sp_hbs_float_col_list=size_sp_hbs.columns.tolist()
        size_sp_hbs_float_col_list.remove('jjdm')
        size_sp_hbs_float_col_list.remove('asofdate')

        if (if_percentage):
            for col in ['换手率排名', '集中度排名', '成长暴露排名', '价值暴露排名',
                               '换手率', '集中度', ]:
                value_p[col]=value_p[col].map("{:.2%}".format)

            for col in ['换手率排名', '集中度排名', '大盘暴露排名', '中盘暴露排名','小盘暴露排名',
                               '换手率', '集中度', ]:
                size_p[col]=size_p[col].map("{:.2%}".format)


            for col in ['Total', '成长', '价值']:
                value_sp.loc[value_sp.index!='切换次数',col]=\
                    value_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
                value_sp_hbs.loc[value_sp_hbs.index!='切换次数',col]=\
                    value_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
            for col in ['Total_rank', '成长_rank', '价值_rank']:
                value_sp[col]=\
                    value_sp[col].astype(float).map("{:.2%}".format)
                value_sp_hbs[col]=\
                    value_sp_hbs[col].astype(float).map("{:.2%}".format)

            for col in ['Total', '大盘', '中盘', '小盘']:
                size_sp.loc[size_sp.index!='切换次数',col]=\
                    size_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
                size_sp_hbs.loc[size_sp_hbs.index!='切换次数',col]=\
                    size_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
            for col in ['Total_rank', '大盘_rank', '中盘_rank', '小盘_rank']:
                size_sp[col]=\
                    size_sp[col].astype(float).map("{:.2%}".format)
                size_sp_hbs[col]=\
                    size_sp_hbs[col].astype(float).map("{:.2%}".format)


        value_sp=value_sp[['Total_rank', '成长_rank', '价值_rank',
                           'Total', '成长', '价值','fre','asofdate']]
        value_sp_hbs=value_sp_hbs[['Total_rank', '成长_rank', '价值_rank',
                           'Total', '成长', '价值','asofdate']]
        size_sp = size_sp[['Total_rank','大盘_rank', '中盘_rank',
           '小盘_rank','Total', '大盘', '中盘', '小盘','fre','asofdate']]
        size_sp_hbs = size_sp_hbs[['Total_rank', '大盘_rank', '中盘_rank',
                           '小盘_rank', 'Total', '大盘', '中盘', '小盘', 'asofdate']]

        value_sp.reset_index(inplace=True)
        size_sp.reset_index(inplace=True)
        value_sp_hbs.reset_index(inplace=True)
        size_sp_hbs.reset_index(inplace=True)


        return  value_p,value_p_hbs,value_sp,value_sp_hbs, size_p,size_p_hbs,size_sp,size_sp_hbs

    @staticmethod
    def stock_trading_pci(jjdm,jjjc,ind_cen,th1=0.75,th2=0.25,th3=0.5,th4=0.5,th5=0.75,th6=0.5,if_percentage=True):

        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_holding_property "
            ,con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_holding_property where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        stock_p=pd.read_sql(sql,con=localdb)

        float_col=stock_p.columns.tolist()
        float_col.remove('jjdm')
        float_col.remove('asofdate')
        float_col.remove('持股数量')
        float_col.remove('PE')
        float_col.remove('PB')
        float_col.remove('ROE')
        float_col.remove('股息率')
        float_col.remove('PE_中位数')
        float_col.remove('PB_中位数')
        float_col.remove('ROE_中位数')
        float_col.remove('股息率_中位数')


        latest_date=pd.read_sql(
            "select max(asofdate) as asofdate from hbs_stock_trading_property "
            ,con=localdb)['asofdate'][0]

        sql="SELECT * from hbs_stock_trading_property where jjdm='{0}' and asofdate='{1}' "\
            .format(jjdm,latest_date)
        stock_tp=pd.read_sql(sql,con=localdb)

        tp_float_col=stock_tp.columns.tolist()
        tp_float_col.remove('jjdm')
        tp_float_col.remove('平均持有时间(出重仓前)')
        tp_float_col.remove('平均持有时间(出持仓前)')
        tp_float_col.remove('asofdate')


        #generate the labels

        if(stock_p['个股集中度'][0]>th1 and stock_tp['平均持有时间(出持仓前)_rank'][0]>th1 ):
            stock_p['个股风格A']='专注'
        elif(stock_p['个股集中度'][0]>th1 and stock_tp['平均持有时间(出持仓前)_rank'][0]<th2 ):
            stock_p['个股风格A'] = '博弈'
        elif(stock_p['个股集中度'][0]<th2 and stock_tp['平均持有时间(出持仓前)_rank'][0]>th1 ):
            stock_p['个股风格A'] = '配置'
        elif(stock_p['个股集中度'][0]<th2 and stock_tp['平均持有时间(出持仓前)_rank'][0]<th2 ):
            stock_p['个股风格A'] = '轮动'
        else:
            stock_p['个股风格A'] = '无'


        if(stock_p['个股集中度'][0]>th1 and ind_cen<th6 ):
            stock_p['个股风格B']='自下而上'
        elif(stock_p['个股集中度'][0]<th6 and ind_cen>th1 ):
            stock_p['个股风格B'] = '自上而下'

        else:
            stock_p['个股风格B'] = '无'

        if(stock_p['个股集中度'][0]>th1 and stock_p['个股集中度'][0]-stock_p['hhi'][0]>0.05):
            stock_p['是否有尾仓(针对高个股集中基金)']='有尾仓'
        else:
            stock_p['是否有尾仓(针对高个股集中基金)'] = '无尾仓'

        if(stock_tp['左侧概率(出持仓前,半年线)_rank'][0]>th3 and stock_tp['左侧程度(出持仓前,半年线)'][0]>th4):
            stock_tp['左侧标签']='深度左侧'
        elif(stock_tp['左侧概率(出持仓前,半年线)_rank'][0]>th3 and stock_tp['左侧程度(出持仓前,半年线)'][0]<th4):
            stock_tp['左侧标签'] = '左侧'
        else:
            stock_tp['左侧标签'] = '无'

        lable=''
        if(stock_tp['新股概率(出持仓前)_rank'][0]>th5):
            lable+='偏好新股'
        if( stock_tp['次新股概率(出持仓前)_rank'][0]>th5):
            lable+='偏好次新股'
        stock_tp['新股次新股偏好']=lable

        if(if_percentage):
            for col in float_col:
                stock_p[col]= stock_p[col].map("{:.2%}".format)
            for col in tp_float_col:
                stock_tp[col] = stock_tp[col].map("{:.2%}".format)



        stock_p['基金简称'] = jjjc
        stock_tp['基金简称'] = jjjc

        stock_p=stock_p[['jjdm','基金简称','个股风格A','个股风格B','是否有尾仓(针对高个股集中基金)','个股集中度', 'hhi','持股数量',
                         '前三大', '前五大', '前十大', '平均仓位', '仓位换手率','PE_rank', 'PB_rank', 'ROE_rank', '股息率_rank', 'PE_中位数_rank',
           'PB_中位数_rank', 'ROE_中位数_rank', '股息率_中位数_rank','PE', 'PB', 'ROE', '股息率',
                         'PE_中位数', 'PB_中位数', 'ROE_中位数', '股息率_中位数','asofdate'
                         ]]
        stock_tp=stock_tp[['jjdm','基金简称','左侧标签', '新股次新股偏好','左侧概率(出重仓前,半年线)_rank', '左侧概率(出持仓前,半年线)_rank',
           '左侧概率(出重仓前,年线)_rank', '左侧概率(出持仓前,年线)_rank',
                           '平均持有时间(出重仓前)_rank', '平均持有时间(出持仓前)_rank','出重仓前平均收益率_rank',
           '出全仓前平均收益率_rank',
                           '新股概率(出重仓前)_rank','新股概率(出持仓前)_rank', '次新股概率(出重仓前)_rank', '次新股概率(出持仓前)_rank','平均持有时间(出重仓前)', '平均持有时间(出持仓前)', '出重仓前平均收益率', '出全仓前平均收益率',
           '左侧概率(出重仓前,半年线)', '左侧概率(出持仓前,半年线)', '左侧概率(出重仓前,年线)', '左侧概率(出持仓前,年线)',
           '左侧程度(出重仓前,半年线)', '左侧程度(出持仓前,半年线)', '左侧程度(出重仓前,年线)', '左侧程度(出持仓前,年线)',
           '新股概率(出重仓前)', '新股概率(出持仓前)', '次新股概率(出重仓前)', '次新股概率(出持仓前)','asofdate'
                           ]]

        return stock_p,stock_tp


    def save_pic_as_excel(self,jjdm_list):

        value_df_list=[pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),
                       pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]

        industry_df_list=[pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]

        stock_df_list=[pd.DataFrame(),pd.DataFrame()]

        for jjdm in jjdm_list:

            jjjc=hbdb.db2df("select jjjc from st_fund.t_st_gm_jjxx where jjdm='{0}'".format(jjdm),db='funduser')['jjjc'][0]

            value_pic=self.style_pic(jjdm,jjjc,fre='M')
            #value_p,value_p_hbs,value_sp,value_sp_hbs, size_p,size_p_hbs,size_sp,size_sp_hbs=style_pic(jjdm,jjjc,fre='M')
            for i in range(8):
                value_pic[i]['jjdm']=jjdm
                value_df_list[i]=pd.concat([value_df_list[i],value_pic[i]],axis=0)

            ind_pic=self.industry_pic(jjdm,jjjc)
            #industry_p,industry_sp,theme_p,theme_sp,industry_detail_df_list=industry_pic(jjdm,jjjc)
            for i in range(4):
                ind_pic[i]['jjdm']=jjdm
                industry_df_list[i] = pd.concat([industry_df_list[i], ind_pic[i]], axis=0)
            for j in range(len(ind_pic[4])):
                ind_pic[4][j]['jjdm']=jjdm
                ind_pic[4][j]['industry_level'] =j+1
                industry_df_list[4]=pd.concat([industry_df_list[4], ind_pic[4][j]], axis=0)

            stock_pic=self.stock_trading_pci(jjdm,jjjc,ind_cen=float(ind_pic[0]['一级行业集中度'][0].split('%')[0])/100)
            for i in range(2):
                stock_df_list[i] = pd.concat([stock_df_list[i], stock_pic[i]], axis=0)
            # stock_p,stock_tp=stock_trading_pci(jjdm,jjjc,ind_cen=float(industry_p['一级行业集中度'][0].split('%')[0])/100)

        writer=pd.ExcelWriter("风格画像.xlsx")
        value_df_list[1].to_excel(writer,sheet_name='成长价值画像_基于持仓',index=False)
        value_df_list[3].to_excel(writer, sheet_name='成长价值切换属性_基于持仓',index=False)
        value_df_list[0].to_excel(writer,sheet_name='成长价值画像_基于净值',index=False)
        value_df_list[2].to_excel(writer, sheet_name='成长价值切换属性_基于净值',index=False)

        value_df_list[5].to_excel(writer,sheet_name='大中小盘画像_基于持仓',index=False)
        value_df_list[7].to_excel(writer, sheet_name='大中小盘切换属性_基于持仓',index=False)
        value_df_list[4].to_excel(writer,sheet_name='大中小盘画像_基于净值',index=False)
        value_df_list[6].to_excel(writer, sheet_name='大中小盘切换属性_基于净值',index=False)
        writer.save()

        writer = pd.ExcelWriter("行业主题画像.xlsx")
        industry_df_list[0].to_excel(writer,sheet_name="行业画像",index=False)
        industry_df_list[1].to_excel(writer, sheet_name="行业切换属性",index=False)
        industry_df_list[2].to_excel(writer,sheet_name="主题画像",index=False)
        industry_df_list[3].to_excel(writer,sheet_name="主题切换属性",index=False)
        industry_df_list[4].to_excel(writer, sheet_name="细分行业画像", index=False)
        writer.save()

        writer = pd.ExcelWriter("个股交易画像.xlsx")
        stock_df_list[0].to_excel(writer,sheet_name='画像A',index=False)
        stock_df_list[1].to_excel(writer,sheet_name='画像B',index=False)
        writer.save()

def get_annotations(asset_allo_series):


        name_map=dict(zip(['NETPROFITGROWRATE_sj',
       'NETPROFITGROWRATE_ticker','PE_sj', 'PE_ticker','PE_FY1_sj','PE_FY1_ticker'],['三级行业净利增速','净利增速',
                                                                                     '三级行业PE','PE','三级行业预期PE','预期PE']))

        asset_allo_series.reset_index(inplace=True)
        x_length=len(asset_allo_series)
        asset_allo_series=asset_allo_series[asset_allo_series['PE_ticker'] != 0]
        annotations=[]
        # index_list = asset_allo_series.T.index.tolist()
        # index_list.reverse()

        for i in range(len(asset_allo_series)):
            asset=asset_allo_series.iloc[i]
            x_position=asset.name/x_length
            y_position=asset['sl']
            text=""
            for col in ['NETPROFITGROWRATE_sj',
       'NETPROFITGROWRATE_ticker']:
                text=text+name_map[col]+": "+str('{:.2%}'.format(asset[col]))+"<br />"
            for col in ['PE_sj', 'PE_ticker','PE_FY1_sj','PE_FY1_ticker']:
                text = text + name_map[col] + ": " + str(round(asset[col],2)) + "<br />"
            #, yanchor='middle'
            #xref='paper',
            #yref = "y1"
            # labeling the left_side of the plot
            # if(max_value>0):
            #     x_index=asset_allo_series[asset].nlargest(1).index[0]
            #     x_position=asset_allo_series.index.tolist().index(x_index)/np.max([(len(asset_allo_series.index)-1),1])
            #     y_position=(asset_allo_series.T.loc[index_list]*100).loc[asset:][x_index].sum()-(asset_allo_series.T*100).loc[asset][x_index]+(asset_allo_series.T*100).loc[asset][x_index]/2
            #     if(x_position==0):
            #         xanchor='left'
            #     elif(x_position==1):
            #         xanchor='right'
            #     else:
            #         xanchor='center'
            annotations.append(dict(xref='paper',yref = "y2",x=x_position, y=y_position,
                                    xanchor='center',yanchor='bottom',
                                    text=text,
                                    font=dict(family='Arial',
                                              size=12),
                                    showarrow=False))


        return annotations

def get_pic_from_localdb(jjdm,asofdate='20220831',if_percentage=True,show_num=None):

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_value_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_value_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    value_p=pd.read_sql(sql,con=localdb)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_value_p_hbs where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_value_p_hbs where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    value_p_hbs=pd.read_sql(sql,con=localdb)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_value_sp where type='nav_based' and asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_value_sp where {0} and asofdate='{1}' and type='nav_based' "\
        .format(jjdm,latest_date)
    value_sp=pd.read_sql(sql,con=localdb).drop('type',axis=1)
    # value_sp=[]

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_value_sp where type='holding_based' and asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_value_sp where {0} and asofdate='{1}' and type='holding_based' "\
        .format(jjdm,latest_date)
    value_sp_hbs=pd.read_sql(sql,con=localdb).drop(['type','fre'],axis=1)
    # value_sp_hbs=[]

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_size_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_size_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    size_p=pd.read_sql(sql,con=localdb)
    # size_p=[]

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_size_p_hbs where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_size_p_hbs where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    size_p_hbs=pd.read_sql(sql,con=localdb)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_size_sp where type='nav_based' and asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_size_sp where {0} and asofdate='{1}' and type='nav_based' "\
        .format(jjdm,latest_date)
    size_sp=pd.read_sql(sql,con=localdb)
    # size_sp=[]

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_size_sp where type='holding_based' and asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_size_sp where {0} and asofdate='{1}' and type='holding_based' "\
        .format(jjdm,latest_date)
    size_sp_hbs=pd.read_sql(sql,con=localdb)
    # size_sp_hbs=[]

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_industry_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    ind_max_date=latest_date
    sql="SELECT * from jjpic_industry_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    industry_p=pd.read_sql(sql,con=localdb)

    float_col_list=industry_p.columns.tolist()
    float_col_list.remove('jjdm')
    float_col_list.remove('asofdate')
    float_col_list.remove('前五大行业')
    float_col_list.remove('二级行业前20大')
    float_col_list.remove('三级行业前20大')
    float_col_list.remove('基金简称')
    float_col_list.remove('一级行业类型')
    float_col_list.remove('二级行业类型')
    float_col_list.remove('三级行业类型')


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_theme_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_theme_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    theme_p=pd.read_sql(sql,con=localdb)


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_industry_sp where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_industry_sp where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    industry_sp=pd.read_sql(sql,con=localdb)
    ind_sp_float_col_list=industry_sp.columns.tolist()
    ind_sp_float_col_list.remove('jjdm')
    ind_sp_float_col_list.remove('asofdate')
    ind_sp_float_col_list.remove('项目名')

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_theme_sp where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_theme_sp where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    theme_sp=pd.read_sql(sql,con=localdb)
    theme_sp_float_col_list = theme_sp.columns.tolist()
    theme_sp_float_col_list.remove('jjdm')
    theme_sp_float_col_list.remove('asofdate')
    theme_sp_float_col_list.remove('项目名')

    latest_date = pd.read_sql(
        "select max(asofdate) as asofdate from hbs_ticker_contribution where asofdate<='{}'".format(asofdate),
        con=localdb)['asofdate'][0]
    sql = "SELECT * from hbs_ticker_contribution where  {0}  and asofdate='{1}' " \
        .format(jjdm, latest_date)
    tempdf = pd.read_sql(sql, con=localdb)[['jjdm','zqdm','CHINAMEABBR','contribution','asofdate']]
    tempdf = pd.merge(tempdf, theme_p[['jjdm', '基金简称']], how='left', on='jjdm')
    ticker_con=[]
    for jj in tempdf['jjdm'].unique():
        ticker_con.append(tempdf[tempdf['jjdm']==jj].reset_index(drop=True))
    ticker_con=pd.concat(ticker_con,axis=1)
    # ticker_con = pd.merge(ticker_con, theme_p[['jjdm', '基金简称']], how='left', on='jjdm')
    ticker_con['jjdm'] = ticker_con['基金简称']
    ticker_con.drop('基金简称', axis=1, inplace=True)

    industry_detail_df_list=[pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]
    industry_contribution_list=[pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]
    industry_contribution_perweight_list=[pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]
    industry_level=['yjxymc','ejxymc','sjxymc']
    ind_detail_date = pd.read_sql("SELECT max(asofdate) as max_date from jjpic_industry_detail_1 where asofdate<='{}' "
                              .format(asofdate),con=localdb)['max_date'][0]
    for i in range(3):
        latest_date=ind_detail_date
        sql = "SELECT * from jjpic_industry_detail_{2} where {0} and asofdate='{1}' " \
            .format(jjdm, latest_date,i+1)
        if(show_num is not None):
            temp_ind_detail=pd.read_sql(sql, con=localdb).sort_values(['jjdm','占持仓比例(时序均值)'],
                                                                      ascending=False)[0:show_num]
        else:
            temp_ind_detail = pd.read_sql(sql, con=localdb)

        if(i==0):

            #calculate the industry value and growth rank
            # industry_rank = temp_ind_detail.drop_duplicates(['行业名称'])
            # industry_rank[[ '行业PB(时序中位数)', '行业PE(时序中位数)']]=1/industry_rank[[ '行业PB(时序中位数)', '行业PE(时序中位数)']]
            # industry_rank[
            #     ['行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)', '行业净资产收益率(时序中位数)',
            #      '行业PB(时序中位数)', '行业PE(时序中位数)',
            #      '行业股息率(时序中位数)']] = industry_rank[['行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)', '行业净资产收益率(时序中位数)',
            #                                          '行业PB(时序中位数)', '行业PE(时序中位数)',
            #                                          '行业股息率(时序中位数)']].rank(method='min') / len(industry_rank)
            # industry_rank['行业综合成长排名'] = industry_rank[['行业净资产收益率(时序中位数)', '行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)']].mean(axis=1)
            # industry_rank['行业综合价值排名'] = industry_rank[['行业PB(时序中位数)','行业PE(时序中位数)','行业股息率(时序中位数)']].mean(axis=1)
            # industry_rank[['行业综合成长排名', '行业综合价值排名']] = industry_rank[['行业综合成长排名', '行业综合价值排名']].rank(method='min') / len(
            #     industry_rank)
            # value_industry = industry_rank[industry_rank['行业综合价值排名'] > industry_rank['行业综合成长排名']][
            #                      ['行业名称', '行业综合成长排名', '行业综合价值排名']].sort_values('行业综合价值排名')[-10:]
            # value_industry['行业类型']='价值'
            # growth_industry = industry_rank[industry_rank['行业综合成长排名'] > industry_rank['行业综合价值排名']][
            #                      ['行业名称', '行业综合成长排名', '行业综合价值排名']].sort_values('行业综合成长排名')[-10:]
            # growth_industry['行业类型'] = '成长'
            # industry_class=pd.concat([value_industry,growth_industry],axis=0)
            #
            # industry_rank=pd.merge(industry_rank[['行业名称']]
            #                        ,industry_class[['行业名称','行业类型']],
            #                        how='left',on='行业名称').fillna('无')
            industry_rank=pd.DataFrame()
            industry_rank['行业名称']=['交通运输', '银行', '公用事业', '钢铁', '石油石化', '家用电器', '建筑装饰', '房地产', '煤炭',
       '非银金融', '轻工制造', '美容护理', '电子', '电力设备', '食品饮料', '有色金属', '建筑材料',
       '基础化工', '国防军工', '医药生物', '环保', '社会服务', '纺织服饰', '商贸零售', '计算机', '通信',
       '农林牧渔', '传媒', '机械设备', '汽车']
            industry_rank['行业类型'] = ['价值', '价值', '价值', '价值', '价值', '价值', '价值', '价值', '价值', '价值', '成长',
       '成长', '成长', '成长', '成长', '成长', '成长', '成长', '成长', '成长', '无', '无',
       '无', '无', '无', '无', '无', '无', '无', '无']

            tempdf=temp_ind_detail
            tempdf=pd.merge(tempdf,industry_rank,how='left',on='行业名称')


            industry_class=tempdf.groupby(['jjdm','行业类型']).sum('占持仓比例(时序均值)')['占持仓比例(时序均值)'].reset_index()


            industry_class['一级行业策略']='无'
            industry_class.loc[(industry_class['占持仓比例(时序均值)'] > 0.45)&
                               (industry_class['行业类型']!="无"), '一级行业策略'] = \
            industry_class.loc[(industry_class['占持仓比例(时序均值)'] > 0.45)&
                               (industry_class['行业类型']!="无")]['行业类型']
            tempdf=pd.merge(tempdf.drop_duplicates('jjdm'),industry_class[industry_class['一级行业策略']!='无'][['jjdm','一级行业策略']],
                            how='left',on='jjdm')
            tempdf.loc[tempdf['一级行业策略'].isnull(),'一级行业策略']='无'
            tempdf=pd.merge(tempdf,industry_class.pivot_table('占持仓比例(时序均值)','jjdm','行业类型')
                            ,how='left',on='jjdm').rename(columns={'价值':'价值行业占比',
                                                                   '成长':'成长行业占比'})


            industry_p=pd.merge(industry_p,tempdf[['jjdm','一级行业策略', '成长行业占比',
       '价值行业占比']],how='left',on='jjdm')

        elif(i==1):

            #calculate the industry value and growth rank for secondary industry
            # industry_rank = temp_ind_detail.drop_duplicates(['行业名称'])
            # industry_rank['一级行业名称'] = [ind_map[x] for x in industry_rank['行业名称']]
            # industry_rank[[ '行业PB(时序中位数)', '行业PE(时序中位数)']]=1/industry_rank[[ '行业PB(时序中位数)', '行业PE(时序中位数)']]
            # industry_rank[['行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)', '行业净资产收益率(时序中位数)',
            #      '行业PB(时序中位数)', '行业PE(时序中位数)',
            #      '行业股息率(时序中位数)']] = industry_rank.groupby('一级行业名称').rank(method='min')[['行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)', '行业净资产收益率(时序中位数)',
            #      '行业PB(时序中位数)', '行业PE(时序中位数)',
            #      '行业股息率(时序中位数)']]
            #
            # industry_rank=pd.merge(industry_rank,
            #                        industry_rank.groupby('一级行业名称').count()['jjdm'].to_frame('count')
            #                        ,how='left',on='一级行业名称')
            # for col in ['行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)', '行业净资产收益率(时序中位数)',
            #      '行业PB(时序中位数)', '行业PE(时序中位数)',
            #      '行业股息率(时序中位数)']:
            #     industry_rank[col]=industry_rank[col]/industry_rank['count']
            #
            # industry_rank['行业综合成长排名'] = industry_rank[['行业净资产收益率(时序中位数)', '行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)']].mean(axis=1)
            # industry_rank['行业综合价值排名'] = industry_rank[['行业PB(时序中位数)','行业PE(时序中位数)','行业股息率(时序中位数)']].mean(axis=1)
            # industry_rank[['行业综合成长排名', '行业综合价值排名']] = industry_rank.groupby('一级行业名称').rank(method='min')[['行业综合成长排名', '行业综合价值排名']]
            # for col in ['行业综合成长排名', '行业综合价值排名']:
            #     industry_rank[col] = industry_rank[col] / industry_rank['count']
            #
            # value_industry=industry_rank[
            #     (industry_rank['行业综合价值排名'] > industry_rank['行业综合成长排名'])
            #     & (industry_rank['行业综合价值排名'] > 0.67)
            #     & (industry_rank['count'] > 1)]
            # value_industry['二级行业类型'] = '价值'
            #
            # growth_industry =industry_rank[
            #     (industry_rank['行业综合价值排名'] < industry_rank['行业综合成长排名'])
            #     & (industry_rank['行业综合成长排名'] > 0.67)
            #     & (industry_rank['count'] > 1)]
            # growth_industry['二级行业类型'] = '成长'
            # industry_class=pd.concat([value_industry,growth_industry],axis=0)
            #
            # industry_rank=pd.merge(industry_rank[['行业名称']]
            #                        ,industry_class[['行业名称','二级行业类型']],
            #                        how='left',on='行业名称').fillna('无')

            industry_rank=pd.DataFrame()
            industry_rank['行业名称']=['IT服务', '一般零售', '专业工程', '专业服务', '专业连锁', '专用设备', '个护用品', '中药'
                , '乘用车', '互联网电商', '休闲食品', '保险', '元件', '光伏设备', '光学光电子', '其他家电', '其他电子', '其他电源设备'
                , '养殖业', '军工电子', '农产品加工', '农化制品', '农商行', '出版', '动物保健', '包装印刷', '化妆品', '化学制品'
                , '化学制药', '化学原料', '化学纤维', '医疗器械', '医疗服务', '医疗美容', '医药商业', '半导体', '厨卫电器', '商用车'
                , '国有大型银行', '地面兵装', '城商行', '基础建设', '塑料', '多元金融', '家居用品', '家电零部件', '小家电', '小金属'
                , '工业金属', '工程咨询服务', '工程机械', '影视院线', '房地产开发', '房地产服务', '房屋建设', '摩托车及其他', '教育'
                , '数字媒体', '文娱用品', '旅游及景区', '旅游零售', '普钢', '服装家纺', '橡胶', '汽车服务', '汽车零部件', '油服工程'
                , '油气开采', '消费电子', '游戏', '炼化及贸易', '照明设备', '燃气', '物流', '特钢', '环保设备', '环境治理', '玻璃玻纤'
                , '生物制品', '电力', '电子化学品', '电机', '电池', '电网设备', '白色家电', '白酒', '种植业', '纺织制造', '股份制银行'
                , '能源金属', '自动化设备', '航天装备', '航空机场', '航空装备', '装修建材', '装修装饰', '计算机设备', '证券', '调味发酵品'
                , '贵金属', '贸易', '轨交设备', '软件开发', '通信设备', '通用设备', '造纸', '酒店餐饮', '金属新材料', '非白酒', '非金属材料'
                , '风电设备', '食品加工', '饮料乳品', '饰品', '饲料', '黑色家电', '冶钢原料', '广告营销', '水泥', '焦炭', '煤炭开采'
                , '电视广播', '综合', '航海装备', '航运港口', '通信服务', '铁路公路']
            industry_rank['二级行业类型'] =['无', '价值', '成长', '成长', '价值', '成长', '价值', '价值', '无', '无', '无'
                , '价值', '价值', '成长', '价值', '价值', '无', '价值', '成长', '成长', '无', '成长', '无', '价值', '价值'
                , '价值', '无', '成长', '无', '无', '价值', '成长', '无', '成长', '价值', '成长', '成长', '价值', '价值', '无'
                , '成长', '价值', '价值', '无', '成长', '无', '成长', '无', '无', '无', '成长', '无', '价值', '成长', '无', '无'
                , '成长', '成长', '无', '价值', '成长', '价值', '无', '无', '成长', '无', '成长', '无', '成长', '无', '价值'
                , '无', '成长', '成长', '成长', '无', '无', '无', '成长', '价值', '无', '无', '无', '无', '价值', '成长', '无'
                , '无', '无', '无', '无', '无', '无', '成长', '无', '无', '无', '成长', '无', '无', '成长', '价值', '无', '无'
                , '无', '价值', '价值', '无', '成长', '无', '价值', '价值', '价值', '无', '成长', '无', '无', '无', '无', '无'
                , '无', '价值', '无', '价值', '成长', '无', '价值']


            tempdf=temp_ind_detail
            tempdf=pd.merge(tempdf,industry_rank,how='left',on='行业名称')

            tempdf['成长综合排名']=tempdf[['主营业务增长率(时序中位数)排名','净利润增长率(时序中位数)排名','净资产收益率(时序中位数)排名']].mean(axis=1)
            tempdf[['PB(时序中位数)排名', 'PE(时序中位数)排名']]=1 - tempdf[['PB(时序中位数)排名', 'PE(时序中位数)排名']]
            tempdf['价值综合排名'] = tempdf[['PB(时序中位数)排名', 'PE(时序中位数)排名','股息率(时序中位数)排名']].mean(axis=1)


            tempdf['成长综合排名']=tempdf['成长综合排名']*tempdf['占持仓比例(时序均值)']
            tempdf['价值综合排名'] = tempdf['价值综合排名'] * tempdf['占持仓比例(时序均值)']

            industry_class=tempdf.groupby(['jjdm','二级行业类型']).sum('占持仓比例(时序均值)')['占持仓比例(时序均值)'].reset_index()

            #old version for calculating the 个股精选策略
            # tempdf['成长超额']=tempdf['成长超额']*tempdf['占持仓比例(时序均值)']
            # tempdf['价值超额'] = tempdf['价值超额'] * tempdf['占持仓比例(时序均值)']
            # # tempdf['行业综合成长排名']=tempdf['行业综合成长排名']*tempdf['占持仓比例(时序均值)']
            # # tempdf['行业综合价值排名'] = tempdf['行业综合价值排名'] * tempdf['占持仓比例(时序均值)']
            # tempdf['综合价值属性(时序均值)排名']=tempdf['综合价值属性(时序均值)排名']*tempdf['占持仓比例(时序均值)']
            # tempdf['综合成长属性(时序均值)排名'] = tempdf['综合成长属性(时序均值)排名'] * tempdf['占持仓比例(时序均值)']
            #
            # tempdf=tempdf.groupby('jjdm').sum()[['占持仓比例(时序均值)',
            #                                      '成长超额','价值超额','综合价值属性(时序均值)排名','综合成长属性(时序均值)排名']]
            # tempdf['成长超额']=tempdf['成长超额']/tempdf['占持仓比例(时序均值)']
            # tempdf['价值超额'] = tempdf['价值超额'] / tempdf['占持仓比例(时序均值)']
            # # tempdf['行业综合成长排名']=tempdf['行业综合成长排名']/tempdf['占持仓比例(时序均值)']
            # # tempdf['行业综合价值排名'] = tempdf['行业综合价值排名'] / tempdf['占持仓比例(时序均值)']
            # tempdf['综合价值属性(时序均值)排名']=tempdf['综合价值属性(时序均值)排名']/tempdf['占持仓比例(时序均值)']
            # tempdf['综合成长属性(时序均值)排名'] = tempdf['综合成长属性(时序均值)排名'] / tempdf['占持仓比例(时序均值)']
            #
            # tempdf['行业精选个股策略']=''
            # tempdf.loc[tempdf['成长超额']>=0.3,'行业精选个股策略']=tempdf.loc[tempdf['成长超额']>=0.3]['行业精选个股策略']+'精选成长,'
            # tempdf.loc[tempdf['成长超额'] <= -0.3, '行业精选个股策略'] = tempdf.loc[tempdf['成长超额'] <= -0.3]['行业精选个股策略'] + '避免成长,'
            # tempdf.loc[tempdf['价值超额']>=0.3,'行业精选个股策略']=tempdf.loc[tempdf['价值超额']>=0.3]['行业精选个股策略']+'精选价值,'
            # tempdf.loc[tempdf['价值超额'] <= -0.3, '行业精选个股策略'] = tempdf.loc[tempdf['价值超额'] <= -0.3]['行业精选个股策略'] + '避免价值,'
            # tempdf.loc[tempdf['行业精选个股策略']=='','行业精选个股策略']='无,'
            # tempdf['行业精选个股策略'] = [x[0:-1] for x in tempdf['行业精选个股策略']]

            #
            # tempvalue=(tempdf[['净资产收益率(时序中位数)', '主营业务增长率(时序中位数)', '净利润增长率(时序中位数)']].values-tempdf[
            #     ['行业净资产收益率(时序中位数)', '行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)']].values) / tempdf[
            #     ['行业净资产收益率(时序中位数)', '行业主营业务增长率(时序中位数)', '行业净利润增长率(时序中位数)']].values
            # tempvalue[tempvalue > 3] = 3
            # tempvalue[tempvalue < -3] = -3
            # tempdf['成长超额']=tempvalue.mean(axis=1)
            #
            # # tempdf[['PB(时序均值)','PE(时序均值)','PCF(时序均值)',
            # #         '行业PB(时序均值)','行业PE(时序均值)','行业PCF(时序均值)']]=1/tempdf[['PB(时序均值)','PE(时序均值)','PCF(时序均值)',
            # #         '行业PB(时序均值)','行业PE(时序均值)','行业PCF(时序均值)']]
            # tempvalue=pd.DataFrame(data= (tempdf[['PB(时序中位数)','PE(时序中位数)','PCF(时序中位数)','股息率(时序中位数)']].values-tempdf[
            #     ['行业PB(时序中位数)','行业PE(时序中位数)','行业PCF(时序中位数)','行业股息率(时序中位数)']].values) / tempdf[
            #     ['行业PB(时序中位数)','行业PE(时序中位数)','行业PCF(时序中位数)','行业股息率(时序中位数)']].values ,columns=['PB(时序中位数)','PE(时序中位数)',
            #                                            'PCF(时序中位数)','股息率(时序均值)'])
            #
            # tempvalue[['PB(时序中位数)','PE(时序中位数)','PCF(时序中位数)']]=-1*tempvalue[['PB(时序中位数)','PE(时序中位数)','PCF(时序中位数)']]
            #
            # tempvalue[tempvalue > 3] = 3
            # tempvalue[tempvalue < -3] = -3
            # tempdf['价值超额']=tempvalue.mean(axis=1)


            tempdf=tempdf.groupby('jjdm').sum()[['成长综合排名','价值综合排名']]
            tempdf['adjust_benchmark'] = tempdf[['成长综合排名', '价值综合排名']].sum(axis=1).values
            tempdf['成长综合排名']=tempdf['成长综合排名']/tempdf['adjust_benchmark']
            tempdf['价值综合排名'] = tempdf['价值综合排名'] / tempdf['adjust_benchmark']
            tempdf['行业精选个股策略']='无'
            tempdf.loc[tempdf['成长综合排名']-tempdf['价值综合排名']>=0.1,
                       '行业精选个股策略']='成长'
            tempdf.loc[tempdf['价值综合排名'] - tempdf['成长综合排名'] >= 0.1,
                       '行业精选个股策略'] = '价值'

            # tempdf['行业精选个股策略']=''
            # tempdf.loc[tempdf['成长超额']>=0.3,'行业精选个股策略']=tempdf.loc[tempdf['成长超额']>=0.3]['行业精选个股策略']+'精选成长,'
            # tempdf.loc[tempdf['成长超额'] <= -0.3, '行业精选个股策略'] = tempdf.loc[tempdf['成长超额'] <= -0.3]['行业精选个股策略'] + '避免成长,'
            # tempdf.loc[tempdf['价值超额']>=0.3,'行业精选个股策略']=tempdf.loc[tempdf['价值超额']>=0.3]['行业精选个股策略']+'精选价值,'
            # tempdf.loc[tempdf['价值超额'] <= -0.3, '行业精选个股策略'] = tempdf.loc[tempdf['价值超额'] <= -0.3]['行业精选个股策略'] + '避免价值,'
            # tempdf.loc[tempdf['行业精选个股策略']=='','行业精选个股策略']='无,'
            # tempdf['行业精选个股策略'] = [x[0:-1] for x in tempdf['行业精选个股策略']]

            industry_class['二级行业策略']='无'
            industry_class.loc[(industry_class['占持仓比例(时序均值)'] > 0.45)&
                               (industry_class['二级行业类型']!="无"), '二级行业策略'] = \
            industry_class.loc[(industry_class['占持仓比例(时序均值)'] > 0.45)&
                               (industry_class['二级行业类型']!="无")]['二级行业类型']
            tempdf=pd.merge(tempdf,industry_class[industry_class['二级行业策略']!='无'][['jjdm','二级行业策略']],
                            how='left',on='jjdm')
            tempdf.loc[tempdf['二级行业策略'].isnull(),'二级行业策略']='无'
            tempdf=pd.merge(tempdf,industry_class.pivot_table('占持仓比例(时序均值)','jjdm','二级行业类型')
                            ,how='left',on='jjdm').rename(columns={'价值':'二级价值行业占比',
                                                                   '成长':'二级成长行业占比'})


            industry_p = pd.merge(industry_p, tempdf[['jjdm', '行业精选个股策略', '二级行业策略', '二级价值行业占比', '二级成长行业占比',
                                                      '成长综合排名', '价值综合排名']],
                                  how='left', on='jjdm')
            industry_p = industry_p[
                ['jjdm', '基金简称', '一级行业类型', '一级行业集中度', '一级行业换手率', '前五大行业', '一级行业策略', '成长行业占比'
                    ,'价值行业占比','二级行业策略', '二级价值行业占比', '二级成长行业占比', '行业精选个股策略',
                 '成长综合排名', '价值综合排名', '龙头占比(时序均值)',
                 '龙头占比(时序中位数)', '龙头占比(时序均值)排名', '龙头占比(时序中位数)排名', '二级行业类型', '二级行业集中度',
                 '二级行业换手率', '三级行业类型', '三级行业集中度', '三级行业换手率',  '二级行业前20大',
                 '三级行业前20大', 'asofdate']]

        ind_detial_float_col = temp_ind_detail.columns.tolist()
        ind_detial_float_col.sort()
        for col in ['总市值(时序中位数)', '总市值(时序中位数)排名',
                    '总市值(时序均值)', '总市值(时序均值)排名', '行业平均市值(时序中位数)', '25分位数市值(时序中位数)',
                    '50分位数市值(时序中位数)', '75分位数市值(时序中位数)', '90分位数市值(时序中位数)', '行业平均市值(时序均值)', '25分位数市值(时序均值)',
                    '50分位数市值(时序均值)', '75分位数市值(时序均值)', '90分位数市值(时序均值)', 'asofdate', '行业名称',
                    'PE(时序中位数)', 'PE(时序均值)', 'PEG(时序中位数)', 'PEG(时序均值)','PCF(时序中位数)', 'PCF(时序均值)','行业PCF(时序均值)',
                    'PB(时序中位数)', 'PB(时序均值)', '行业PE(时序中位数)', '行业PB(时序中位数)', '行业PEG(时序中位数)', '行业PE(时序均值)', '行业PB(时序均值)',
                    '行业PEG(时序均值)','jjdm']:
            ind_detial_float_col.remove(col)

        industry_zjbl=temp_ind_detail.pivot_table('占持仓比例(时序均值)','行业名称','jjdm')
        industry_zjbl=industry_zjbl[set(theme_p['jjdm']).intersection(set(industry_zjbl.columns))]
        industry_zjbl.rename(columns=dict(zip(theme_p['jjdm'].tolist()
                                              ,theme_p['基金简称'].tolist())),inplace=True)

        if (if_percentage):
            for col in ind_detial_float_col:
                temp_ind_detail[col] = temp_ind_detail[col].map("{:.2%}".format)
        industry_detail_df_list[i] = temp_ind_detail


        #get the industry contribution
        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from hbs_industry_contribution",
                 con=localdb)['asofdate'][0]
        sql = "SELECT * from hbs_industry_contribution where  {0} and industry_lv='{2}' and asofdate='{1}' " \
            .format(jjdm,latest_date,industry_level[i])
        industry_con=pd.read_sql(sql,con=localdb)
        industry_con=pd.merge(industry_con,theme_p[['jjdm','基金简称']],how='left',on='jjdm')
        industry_con['jjdm']=industry_con['基金简称']
        industry_con.drop('基金简称',axis=1,inplace=True)
        industry_con_temp=industry_con.pivot_table('contribution','industry_name','jjdm')
        for jj in industry_con_temp.columns:

            industry_con_temp=pd.merge(industry_con_temp,
                                       (industry_con[industry_con['jjdm'] == jj][['industry_name', '个股贡献']].set_index('industry_name').rename(columns={'个股贡献': jj + '个股贡献'})).drop_duplicates(),
                                       how='left',on='industry_name')

        industry_contribution_list[i]=industry_con_temp.reset_index()
        industry_contribution_perweight_list[i]=(industry_con_temp.sort_index()[list(set(industry_zjbl.columns).intersection(set(industry_con_temp.columns)))]/industry_zjbl).reset_index()

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_stock_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_stock_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    stock_p=pd.read_sql(sql,con=localdb)
    float_col=stock_p.columns.tolist()
    float_col.remove('jjdm')
    float_col.remove('asofdate')
    float_col.remove('持股数量')
    float_col.remove('PE')
    float_col.remove('PB')
    float_col.remove('ROE')
    float_col.remove('股息率')
    float_col.remove('基金简称')
    float_col.remove('个股风格A')
    float_col.remove('个股风格B')
    float_col.remove('是否有尾仓(针对高个股集中基金)')

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_stock_tp where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_stock_tp where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    stock_tp=pd.read_sql(sql,con=localdb)
    tp_float_col=stock_tp.columns.tolist()
    tp_float_col.remove('jjdm')
    tp_float_col.remove('平均持有时间(出重仓前)')
    tp_float_col.remove('平均持有时间(出持仓前)')
    tp_float_col.remove('asofdate')
    tp_float_col.remove('基金简称')
    tp_float_col.remove('左侧标签')
    tp_float_col.remove('新股次新股偏好')
    tp_float_col.remove('基本面左右侧标签')
    tp_float_col.remove('PB-ROE选股')
    tp_float_col.remove('PEG选股')
    tp_float_col.remove('博弈基本面拐点')
    tp_float_col.remove('博弈估值修复')

    #update the industry label by ticker shift ratio
    industry_p = pd.merge(industry_p, stock_tp[['jjdm', '换手率_rank']],how='left',on='jjdm')
    industry_p.loc[(industry_p['一级行业类型']=='博弈')
                   &(industry_p['换手率_rank']<0.5),'一级行业类型']='博弈(被动)'
    industry_p.loc[(industry_p['一级行业类型']=='轮动')
                   &(industry_p['换手率_rank']<0.5),'一级行业类型']='轮动(被动)'
    industry_p.drop('换手率_rank',axis=1,inplace=True)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from nav_jj_ret_analysis where  asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from nav_jj_ret_analysis where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    jj_performance=pd.read_sql(sql,con=localdb).fillna(0)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from nav_hurst_index where  asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from nav_hurst_index where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    hurst=pd.read_sql(sql,con=localdb)
    hurst['业绩特征'] = '随机'
    hurst.loc[hurst['H'] <= 0.35,'业绩特征']='趋势反转'
    hurst.loc[hurst['H'] >= 0.65,'业绩特征']='趋势保持'

    jj_performance=pd.merge(jj_performance,hurst[['jjdm','业绩特征']],how='left',on='jjdm')

    jj_performance=jj_performance[['jjdm','业绩预期回归强度', '长期相对业绩表现', '相对业绩稳定性','业绩特征','month_rank_mean', 'month_rank_std', 'quarter_rank_mean',
       'quarter_rank_std', 'hy_rank_mean', 'hy_rank_std', 'yearly_rank_mean',
       'yearly_rank_std', 'ret_regress',
       'sharp_ratio', 'sharp_ratio_rank', 'downwards_ratio',
       'downwards_ratio_rank', 'sortino_ratio', 'sortino_ratio_rank',
       'max_drawback', 'max_drawback_rank', 'calmark_ratio',
       'calmark_ratio_rank', 'treynor_ratio', 'treynor_ratio_rank','moment','moment_rank',
       'asofdate']]
    performance_float_col=jj_performance.columns.tolist()
    performance_float_col.remove('jjdm')
    performance_float_col.remove('业绩预期回归强度')
    performance_float_col.remove('长期相对业绩表现')
    performance_float_col.remove('相对业绩稳定性')
    performance_float_col.remove('asofdate')
    performance_float_col.remove('业绩特征')

    #theme histroy data

    sql="SELECT * from hbs_theme_exp where  jjdm in ({0}) "\
        .format(util.list_sql_condition(value_p_hbs['jjdm'].astype(str).tolist()))
    theme_exp=pd.read_sql(sql,con=localdb).sort_values('jsrq')
    theme_exp['jjdm']=[("000000"+x)[-6:] for x in theme_exp['jjdm']]
    theme_exp=pd.merge(theme_exp,theme_p[['jjdm','基金简称']],how='left',on='jjdm').drop('jjdm',axis=1)

    #get the secondary industry exp

    sql="SELECT jjdm,jsrq,ejxymc,zjbl from hbs_industry_class2_exp where  jjdm in ({0})"\
        .format(util.list_sql_condition(value_p_hbs['jjdm'].astype(str).tolist()))
    ind2_exp=pd.read_sql(sql,con=localdb).sort_values('jsrq')
    #remove the Ⅱ in the ejxymc
    ind2_exp['ejxymc']=[x.replace('Ⅱ','') for x in ind2_exp['ejxymc']]
    ind2_exp['jjdm']=[("000000"+x)[-6:] for x in ind2_exp['jjdm']]
    ind2_exp=pd.merge(ind2_exp,theme_p[['jjdm','基金简称']],how='left',on='jjdm').drop('jjdm',axis=1)



    #get the value and growth  exp

    sql="SELECT * from hbs_style_exp where  jjdm in ({0})"\
        .format(util.list_sql_condition(value_p_hbs['jjdm'].astype(str).tolist()))
    style_exp=pd.read_sql(sql,con=localdb)

    sql="SELECT * from hbs_size_exp where  jjdm in ({0})"\
        .format(util.list_sql_condition(value_p_hbs['jjdm'].astype(str).tolist()))
    size_exp=pd.read_sql(sql,con=localdb)

    style_exp = pd.merge(style_exp, theme_p[['jjdm', '基金简称']], how='left', on='jjdm').drop(['jjdm','jjzzc'], axis=1)
    size_exp = pd.merge(size_exp, theme_p[['jjdm', '基金简称']], how='left', on='jjdm').drop(['jjdm','jjzzc'], axis=1)


    if (if_percentage):
        for col in float_col_list:
            industry_p[col] = industry_p[col].map("{:.2%}".format)
        for col in ind_sp_float_col_list[0:int(len(ind_sp_float_col_list) / 2)]:
            industry_sp[col] = \
                industry_sp[col].astype(float).map("{:.2%}".format)
        for col in ind_sp_float_col_list[int(len(ind_sp_float_col_list) / 2):]:
            industry_sp.loc[industry_sp['项目名'] != '切换次数', col] = \
                industry_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
        for col in theme_sp_float_col_list[0:int(len(theme_sp_float_col_list) / 2)]:
            theme_sp[col] = \
                theme_sp[col].astype(float).map("{:.2%}".format)
        for col in theme_sp_float_col_list[int(len(theme_sp_float_col_list) / 2):]:
            theme_sp.loc[theme_sp['项目名'] != '切换次数', col] = \
                theme_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
        for col in ['主题集中度', '主题换手率', '大金融', '消费', 'TMT', '周期',
       '制造']:
            theme_p[col]=theme_p[col].map("{:.2%}".format)


        for col in ['集中度(持仓)', '换手率(持仓)', '成长绝对暴露(持仓)', '价值绝对暴露(持仓)', '集中度排名(持仓)',
           '换手率排名(持仓)', '成长暴露排名(持仓)', '价值暴露排名(持仓)']:
            value_p_hbs[col]=value_p_hbs[col].map("{:.2%}".format)
        for col in ['集中度(持仓)', '换手率(持仓)', '大盘绝对暴露(持仓)', '中小盘绝对暴露(持仓)',
           '集中度排名(持仓)', '换手率排名(持仓)', '大盘暴露排名(持仓)', '中小盘暴露排名(持仓)']:
            size_p_hbs[col]=size_p_hbs[col].map("{:.2%}".format)
        for col in ['换手率排名', '集中度排名', '成长暴露排名', '价值暴露排名',
                           '换手率', '集中度', ]:
            value_p[col]=value_p[col].map("{:.2%}".format)
        for col in ['换手率排名', '集中度排名', '大盘暴露排名', '中盘暴露排名','小盘暴露排名',
                           '换手率', '集中度', ]:
            size_p[col]=size_p[col].map("{:.2%}".format)
        for col in ['Total', '成长', '价值']:
            value_sp.loc[value_sp['项目名']!='切换次数',col]=\
                value_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
            value_sp_hbs.loc[value_sp_hbs['项目名']!='切换次数',col]=\
                value_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
        for col in ['Total_rank', '成长_rank', '价值_rank']:
            value_sp[col]=\
                value_sp[col].astype(float).map("{:.2%}".format)
            value_sp_hbs[col]=\
                value_sp_hbs[col].astype(float).map("{:.2%}".format)
        for col in ['Total', '大盘', '中盘', '小盘']:
            size_sp.loc[size_sp['项目名']!='切换次数',col]=\
                size_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
            size_sp_hbs.loc[size_sp_hbs['项目名']!='切换次数',col]=\
                size_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
        for col in ['Total_rank', '大盘_rank', '中盘_rank', '小盘_rank']:
            size_sp[col]=\
                size_sp[col].astype(float).map("{:.2%}".format)
            size_sp_hbs[col]=\
                size_sp_hbs[col].astype(float).map("{:.2%}".format)

        for col in float_col:
            stock_p[col]= stock_p[col].map("{:.2%}".format)
        for col in tp_float_col:
            stock_tp[col] = stock_tp[col].map("{:.2%}".format)

        for col in performance_float_col:
            jj_performance[col] = jj_performance[col].map("{:.2%}".format)

    return value_p,value_p_hbs,value_sp,value_sp_hbs, size_p,size_p_hbs,size_sp,size_sp_hbs,\
           industry_p,industry_sp,theme_p,theme_sp,industry_detail_df_list,stock_p,\
           stock_tp,jj_performance,industry_contribution_list,ticker_con,theme_exp,ind2_exp\
        ,industry_contribution_perweight_list,style_exp,size_exp

def get_pic_from_localdb_simple_version(jjdm,asofdate='20220831',if_percentage=True,show_num=None):


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_value_p_hbs where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_value_p_hbs where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    value_p_hbs=pd.read_sql(sql,con=localdb).drop_duplicates('jjdm')


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_size_p_hbs where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_size_p_hbs where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    size_p_hbs=pd.read_sql(sql,con=localdb).drop_duplicates('jjdm')


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_industry_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]

    sql="SELECT * from jjpic_industry_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    industry_p=pd.read_sql(sql,con=localdb)

    float_col_list=industry_p.columns.tolist()
    float_col_list.remove('jjdm')
    float_col_list.remove('asofdate')
    float_col_list.remove('前五大行业')
    float_col_list.remove('二级行业前20大')
    float_col_list.remove('三级行业前20大')
    float_col_list.remove('基金简称')
    float_col_list.remove('一级行业类型')
    float_col_list.remove('二级行业类型')
    float_col_list.remove('三级行业类型')
    float_col_list.remove('一级行业策略')
    float_col_list.remove('行业精选个股策略')
    float_col_list.remove('二级行业策略')




    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_theme_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_theme_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    theme_p=pd.read_sql(sql,con=localdb)


    latest_date = pd.read_sql(
        "select max(asofdate) as asofdate from hbs_ticker_contribution where asofdate<='{}'".format(asofdate),
        con=localdb)['asofdate'][0]
    sql = "SELECT * from hbs_ticker_contribution where  {0}  and asofdate='{1}' " \
        .format(jjdm, latest_date)
    tempdf = pd.read_sql(sql, con=localdb)[['jjdm','zqdm','CHINAMEABBR','contribution','asofdate']]
    tempdf = pd.merge(tempdf, theme_p[['jjdm', '基金简称']], how='left', on='jjdm')
    tempdf['rank']=tempdf.groupby('jjdm').rank(ascending=False)['contribution']
    ticker_con2=tempdf[tempdf['rank']<=3]
    ticker_con2['top3'] = ticker_con2['CHINAMEABBR'] + "(" + ticker_con2['contribution'].map("{:.2%}".format) + "),"
    ticker_con2 = ticker_con2.groupby('jjdm')['top3'].sum()
    ticker_con=[]
    for jj in tempdf['jjdm'].unique():
        ticker_con.append(tempdf[tempdf['jjdm']==jj].reset_index(drop=True))
    ticker_con=pd.concat(ticker_con,axis=1)
    ticker_con['jjdm'] = ticker_con['基金简称']
    ticker_con.drop(['基金简称','asofdate','rank'], axis=1, inplace=True)


    industry_contribution_list=[pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]
    industry_level=['yjxymc','ejxymc','sjxymc']

    for i in range(1):

        #get the industry contribution
        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from hbs_industry_contribution",
                 con=localdb)['asofdate'][0]
        sql = "SELECT * from hbs_industry_contribution where  {0} and industry_lv='{2}' and asofdate='{1}' " \
            .format(jjdm,latest_date,industry_level[i])
        industry_con=pd.read_sql(sql,con=localdb)

        industry_con['rank'] = industry_con.groupby('jjdm').rank(ascending=False)['contribution']
        industry_con2=industry_con[industry_con['rank'] <= 3]
        industry_con2['top3'] = industry_con2['industry_name'] + "(" + industry_con2['contribution'].map("{:.2%}".format) + "),"
        industry_con2=industry_con2.groupby('jjdm')['top3'].sum()

        industry_con=pd.merge(industry_con,theme_p[['jjdm','基金简称']],how='left',on='jjdm')
        industry_con['jjdm']=industry_con['基金简称']
        industry_con.drop(['基金简称','rank','asofdate'],axis=1,inplace=True)
        industry_con_temp=industry_con.pivot_table('contribution','industry_name','jjdm')
        for jj in industry_con_temp.columns:

            industry_con_temp=pd.merge(industry_con_temp,
                                       (industry_con[industry_con['jjdm'] == jj][['industry_name', '个股贡献']].set_index('industry_name').rename(columns={'个股贡献': jj + '个股贡献'})).drop_duplicates(),
                                       how='left',on='industry_name')

        industry_contribution_list[i]=industry_con_temp.reset_index()


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_stock_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_stock_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    stock_p=pd.read_sql(sql,con=localdb)

    # financial_rank=stock_p[['jjdm','PE_rank', 'PB_rank',
    #    'PCF_rank', '股息率_rank','ROE_rank','净利增速_rank', 'PEG_rank',  '毛利率_rank', '净利率_rank',
    #    '市值_rank']]
    # financial_col=financial_rank.columns[1:]
    # for col in financial_col:
    #     financial_rank[col.replace('_rank','')]='中'
    #     financial_rank.loc[financial_rank[col] >= 2 / 3, col.replace('_rank','')] = '高'
    #     financial_rank.loc[financial_rank[col] <= 1 / 3, col.replace('_rank','')] = '低'


    financial_col=['PE', 'PB','PCF', '股息率','ROE','净利增速', 'PEG',  '毛利率', '净利率',
       '市值']

    float_col=stock_p.columns.tolist()
    float_col.remove('jjdm')
    float_col.remove('asofdate')
    float_col.remove('持股数量')
    float_col.remove('PE')
    float_col.remove('PB')
    float_col.remove('ROE')
    float_col.remove('PCF')
    float_col.remove('净利增速')
    float_col.remove('PEG')
    float_col.remove('毛利率')
    float_col.remove('净利率')
    float_col.remove('股息率')
    float_col.remove('市值')
    float_col.remove('基金简称')
    float_col.remove('个股风格A')
    float_col.remove('个股风格B')
    float_col.remove('是否有尾仓(针对高个股集中基金)')

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_stock_tp where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_stock_tp where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    stock_tp=pd.read_sql(sql,con=localdb)
    tp_float_col=stock_tp.columns.tolist()
    tp_float_col.remove('jjdm')
    tp_float_col.remove('平均持有时间(出重仓前)')
    tp_float_col.remove('平均持有时间(出持仓前)')
    tp_float_col.remove('asofdate')
    tp_float_col.remove('基金简称')
    tp_float_col.remove('左侧标签')
    tp_float_col.remove('新股次新股偏好')
    tp_float_col.remove('基本面左右侧标签')
    tp_float_col.remove('PB-ROE选股')
    tp_float_col.remove('PEG选股')
    tp_float_col.remove('博弈基本面拐点')
    tp_float_col.remove('博弈估值修复')
    tp_float_col.remove('是否抱团')



    #update the industry label by ticker shift ratio
    industry_p = pd.merge(industry_p, stock_tp[['jjdm', '换手率_rank']],how='left',on='jjdm')
    industry_p.loc[(industry_p['一级行业类型']=='博弈')
                   &(industry_p['换手率_rank']<0.5),'一级行业类型']='博弈(被动)'
    industry_p.loc[(industry_p['一级行业类型']=='轮动')
                   &(industry_p['换手率_rank']<0.5),'一级行业类型']='轮动(被动)'
    industry_p.drop('换手率_rank',axis=1,inplace=True)


    #theme histroy data

    sql="SELECT * from hbs_theme_exp where  jjdm in ({0}) "\
        .format(util.list_sql_condition(value_p_hbs['jjdm'].astype(str).tolist()))
    theme_exp=pd.read_sql(sql,con=localdb).sort_values('jsrq')
    theme_exp['jjdm']=[("000000"+x)[-6:] for x in theme_exp['jjdm']]
    theme_exp=pd.merge(theme_exp,theme_p[['jjdm','基金简称']],how='left',on='jjdm').drop('jjdm',axis=1)


    #get the value and growth  exp

    sql="SELECT * from hbs_style_exp where  jjdm in ({0})"\
        .format(util.list_sql_condition(value_p_hbs['jjdm'].astype(str).tolist()))
    style_exp=pd.read_sql(sql,con=localdb)

    sql="SELECT * from hbs_size_exp where  jjdm in ({0})"\
        .format(util.list_sql_condition(value_p_hbs['jjdm'].astype(str).tolist()))
    size_exp=pd.read_sql(sql,con=localdb)

    style_exp = pd.merge(style_exp, theme_p[['jjdm', '基金简称']], how='left', on='jjdm').drop(['jjdm','jjzzc'], axis=1)
    size_exp = pd.merge(size_exp, theme_p[['jjdm', '基金简称']], how='left', on='jjdm').drop(['jjdm','jjzzc'], axis=1)


    if (if_percentage):
        for col in float_col_list:
            industry_p[col] = industry_p[col].map("{:.2%}".format)

        for col in ['主题集中度', '主题换手率', '大金融', '消费', 'TMT', '周期',
       '制造']:
            theme_p[col]=theme_p[col].map("{:.2%}".format)


        for col in ['集中度(持仓)', '换手率(持仓)', '成长绝对暴露(持仓)', '价值绝对暴露(持仓)', '集中度排名(持仓)',
           '换手率排名(持仓)', '成长暴露排名(持仓)', '价值暴露排名(持仓)']:
            value_p_hbs[col]=value_p_hbs[col].map("{:.2%}".format)
        for col in ['集中度(持仓)', '换手率(持仓)', '大盘绝对暴露(持仓)', '中小盘绝对暴露(持仓)',
           '集中度排名(持仓)', '换手率排名(持仓)', '大盘暴露排名(持仓)', '中小盘暴露排名(持仓)']:
            size_p_hbs[col]=size_p_hbs[col].map("{:.2%}".format)

        # for col in ['Total', '成长', '价值']:
        #     value_sp.loc[value_sp['项目名']!='切换次数',col]=\
        #         value_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
        #     value_sp_hbs.loc[value_sp_hbs['项目名']!='切换次数',col]=\
        #         value_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)

        # for col in ['Total_rank', '大盘_rank', '中盘_rank', '小盘_rank']:
        #     size_sp[col]=\
        #         size_sp[col].astype(float).map("{:.2%}".format)
        #     size_sp_hbs[col]=\
        #         size_sp_hbs[col].astype(float).map("{:.2%}".format)

        for col in float_col:
            stock_p[col]= stock_p[col].map("{:.2%}".format)
        for col in financial_col:
            stock_p[col]= np.round(stock_p[col],2)
        financial_rank=stock_p[['jjdm']+financial_col]
        for col in tp_float_col:
            stock_tp[col] = stock_tp[col].astype(float).map("{:.2%}".format)


    return value_p_hbs,size_p_hbs,\
           industry_p,theme_p,stock_p,\
           stock_tp,industry_contribution_list,industry_con2,ticker_con,ticker_con2,theme_exp\
        ,style_exp,size_exp,financial_rank

def plot_picatlocal(jjdm):

    jjjc=hbdb.db2df("select jjjc from st_fund.t_st_gm_jjxx where jjdm='{0}'".format(jjdm),db='funduser')['jjjc'][0]

    jjdm_con="jjdm='{}'".format(jjdm)
    value_p, value_p_hbs, value_sp, value_sp_hbs, size_p, size_p_hbs, size_sp, size_sp_hbs, \
    industry_p, industry_sp, theme_p, theme_sp, industry_detail_df_list, stock_p, stock_tp,jj_performance=get_pic_from_localdb(jjdm_con,show_num=20)

    plot=functionality.Plot(2000,400)
    plot2=functionality.Plot(2000,100)

    print("%html <h3>行业画像</h3>")
    plot2.plotly_table(industry_p, 8000, 'asdf')
    plot.plotly_table(industry_sp, 6000, 'asdf')

    print("%html <h3>一级行业画像</h3>")
    plot.plotly_table(industry_detail_df_list[0][industry_detail_df_list[0].columns[0:45]],8000,'asdf')
    print("%html <h3>二级行业画像</h3>")
    plot.plotly_table(industry_detail_df_list[1][industry_detail_df_list[1].columns[0:45]],8000,'asdf')
    print("%html <h3>三级行业画像</h3>")
    plot.plotly_table(industry_detail_df_list[2][industry_detail_df_list[2].columns[0:45]],8000,'asdf')

    if(len(theme_p)>0):
        print("%html <h3>主题画像</h3>")
        plot2.plotly_table(theme_p, 2000, 'asdf')
        plot.plotly_table(theme_sp, 2000, 'asdf')
    else:
        print("%html <h3>主题画像暂无</h3>")


    print("%html <h3>风格画像_基于持仓</h3>")
    plot2.plotly_table(value_p_hbs, 2000, 'asdf')
    plot.plotly_table(value_sp_hbs, 2000, 'asdf')
    print("%html <h3>风格画像_基于净值</h3>")
    plot2.plotly_table(value_p, 2000, 'asdf')
    plot.plotly_table(value_sp, 2000, 'asdf')

    print("%html <h3>规模风格画像_基于持仓</h3>")
    plot2.plotly_table(size_p_hbs, 2000, 'asdf')
    plot.plotly_table(size_sp_hbs, 2000, 'asdf')
    print("%html <h3>规模风格画像_基于净值</h3>")
    plot2.plotly_table(size_p, 2000, 'asdf')
    plot.plotly_table(size_sp, 2000, 'asdf')


    print("%html <h3>个股交易画像</h3>")
    plot2.plotly_table(stock_p, 4000, 'asdf')
    plot2.plotly_table(stock_tp, 8000, 'asdf')

def industry_pic_all(jj_base_info,asofdate1,asofdate2,
                     th1=0.5, th2=0.5,if_prv=False,fre='Q',
                     manager_pic=False):


    if(if_prv):

        if(fre=='M'):
            fre_table='_monthly'
        else:
            fre_table=''
        property_table='hbs_prv_industry_property{}_new'.format(fre_table)
        industry_level_table = 'hbs_prv_industry_property{}'.format(fre_table)
        ind_shift_property_table='hbs_prv_industry_shift_property'
        theme_shift_property_table='hbs_prv_theme_shift_property'
        ind_property_pic_table='jjpic_prv_industry_p{}'.format(fre_table)
        ind_shift_pic_table='jjpic_prv_industry_sp{}'.format(fre_table)
        theme_property_pic_table='jjpic_prv_theme_p{}'.format(fre_table)
        theme_shift_pic_table='jjpic_prv_theme_sp{}'.format(fre_table)
        industry_level_pic_table = 'jjpic_prv_industry_detail{}'.format(fre_table)
    else:
        property_table='hbs_industry_property_new'
        industry_level_table='hbs_industry_property'
        ind_shift_property_table='hbs_industry_shift_property_new'
        theme_shift_property_table='hbs_theme_shift_property_new'
        ind_property_pic_table='jjpic_industry_p'
        ind_shift_pic_table='jjpic_industry_sp'
        theme_property_pic_table='jjpic_theme_p'
        theme_shift_pic_table='jjpic_theme_sp'
        industry_level_pic_table='jjpic_industry_detail'


    def label_style(df, cen_col, shift_col, style_col, n_clusters = 4):

        from sklearn.cluster import KMeans
        from sklearn import  preprocessing as pp

        for col in [cen_col, shift_col]:
            df.loc[df[col]<=df[col].quantile(0.01),col]=df[col].quantile(0.01)
            df.loc[df[col] >= df[col].quantile(0.99),col] = df[col].quantile(0.99)


        df[style_col] = \
            KMeans(n_clusters=n_clusters,init='k-means++',
                         random_state=0).fit_predict(pp.StandardScaler().fit_transform(df[[cen_col, shift_col]].fillna(0).values))

        type_dict=\
            df[[cen_col, shift_col,style_col]].groupby(style_col).median()[[cen_col, shift_col]].rank()

        if(n_clusters==3):
            type_dict.loc[(type_dict[cen_col] > 2) & (type_dict[shift_col] <= 2), style_col]= '专注'
            type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] > 2), style_col]= '轮动'
            type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] <= 2), style_col]= '配置'
        else:
            type_dict.loc[(type_dict[cen_col] > 2) & (type_dict[shift_col] <= 2), style_col]= '专注'
            type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] > 2), style_col]= '轮动'
            type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] <= 2), style_col]= '配置'
            type_dict.loc[(type_dict[cen_col] > 2) & (type_dict[shift_col] > 2), style_col]= '博弈'


        df[style_col]=[type_dict.loc[x][style_col] for x in df[style_col]]


        return df


    # latest_date =str( pd.read_sql(
    #     "select max(asofdate) as asofdate from {0}".format(property_table), con=localdb)['asofdate'][0])
    latest_date=asofdate1
    sql = "SELECT * from {1} where asofdate='{0}' " \
        .format( latest_date,property_table)
    industry_p = pd.read_sql(sql, con=localdb).rename(columns={'cen_ind_1_rank': '一级行业集中度',
                                                               'ratio_ind_1_rank': '一级行业换手率',
                                                               'cen_ind_2_rank': '二级行业集中度',
                                                               'ratio_ind_2_rank': '二级行业换手率',
                                                               'cen_ind_3_rank': '三级行业集中度',
                                                               'ratio_ind_3_rank': '三级行业换手率',
                                                               'industry_num': '行业暴露数',
                                                               'top5': '前五大行业',
                                                               'top20_2': '二级行业前20大',
                                                               'top20_3': '三级行业前20大',
                                                               'longtou_med': '龙头占比(时序中位数)',
                                                               'longtou_mean': '龙头占比(时序均值)',
                                                               'longtou_med_rank': '龙头占比(时序中位数)排名',
                                                               'longtou_mean_rank': '龙头占比(时序均值)排名',
                                                               'cen_theme_rank': '主题集中度',
                                                               'ratio_theme_rank': '主题换手率'
                                                               })

    # industry_p.drop(['cen_ind_1','cen_ind_2','cen_ind_3','cen_theme',
    #                  'ratio_ind_1','ratio_ind_2','ratio_ind_3','ratio_theme'],axis=1,inplace=True)
    industry_p[['龙头占比(时序均值)', '龙头占比(时序中位数)']] = industry_p[['龙头占比(时序均值)', '龙头占比(时序中位数)']] / 100
    float_col_list = industry_p.columns.tolist()
    float_col_list.remove('jjdm')
    float_col_list.remove('asofdate')
    float_col_list.remove('前五大行业')
    float_col_list.remove('二级行业前20大')
    float_col_list.remove('三级行业前20大')

    industry_detail_df_list = []
    class_name_list = ['yjxymc', 'ejxymc', 'sjxymc']
    name_map = dict(zip(['zsbl_mean', 'ROE_mean', 'PB_mean',
                         'DIVIDENDRATIO_mean', 'PCF_mean', 'TOTALMV_mean',
                         'PEG_mean', 'PE_mean', 'NETPROFITGROWRATE_mean',
                         'OPERATINGREVENUEYOY_mean', 'longtou_zjbl_for_ind_mean', 'zsbl_med',
                         'ROE_med', 'PB_med', 'DIVIDENDRATIO_med', 'PCF_med',
                         'TOTALMV_med', 'PEG_med', 'PE_med',
                         'NETPROFITGROWRATE_med', 'OPERATINGREVENUEYOY_med',
                         'longtou_zjbl_for_ind_med', 'jjdm', 'zsbl_mean_rank', 'ROE_mean_rank',
                         'PB_mean_rank', 'DIVIDENDRATIO_mean_rank',
                         'PCF_mean_rank', 'TOTALMV_mean_rank',  'PEG_mean_rank', 'PE_mean_rank',
                         'NETPROFITGROWRATE_mean_rank', 'OPERATINGREVENUEYOY_mean_rank',
                         'longtou_zjbl_for_ind_mean_rank', 'zsbl_med_rank', 'ROE_med_rank',
                         'PB_med_rank', 'DIVIDENDRATIO_med_rank',
                         'PCF_med_rank', 'TOTALMV_med_rank', 'PEG_med_rank', 'PE_med_rank',
                         'NETPROFITGROWRATE_med_rank', 'OPERATINGREVENUEYOY_med_rank',
                         'longtou_zjbl_for_ind_med_rank', 'growth_mean_rank', 'value_mean_rank',
                         'growth_med_rank', 'value_med_rank'], ['占持仓比例(时序均值)', '净资产收益率(时序均值)',
                                                                'PB(时序均值)', '股息率(时序均值)',
                                                                'PCF(时序均值)', '总市值(时序均值)',
                                                                 'PEG(时序均值)',
                                                                'PE(时序均值)', '净利润增长率(时序均值)',
                                                                '主营业务增长率(时序均值)', '行业龙头占比(时序均值)',
                                                                '占持仓比例(时序中位数)', '净资产收益率(时序中位数)',
                                                                'PB(时序中位数)', '股息率(时序中位数)',
                                                                'PCF(时序中位数)', '总市值(时序中位数)',
                                                                 'PEG(时序中位数)',
                                                                'PE(时序中位数)', '净利润增长率(时序中位数)',
                                                                '主营业务增长率(时序中位数)', '行业龙头占比(时序中位数)',
                                                                'jjdm', '占持仓比例(时序均值)排名', '净资产收益率(时序均值)排名',
                                                                'PB(时序均值)排名', '股息率(时序均值)排名',
                                                                'PCF(时序均值)排名', '总市值(时序均值)排名',
                                                                 'PEG(时序均值)排名',
                                                                'PE(时序均值)排名', '净利润增长率(时序均值)排名',
                                                                '主营业务增长率(时序均值)排名', '行业龙头占比(时序均值)排名',
                                                                '占持仓比例(时序中位数)排名', '净资产收益率(时序中位数)排名',
                                                                'PB(时序中位数)排名', '股息率(时序中位数)排名',
                                                                'PCF(时序中位数)排名', '总市值(时序中位数)排名',
                                                                 'PEG(时序中位数)排名',
                                                                'PE(时序中位数)排名', '净利润增长率(时序中位数)排名',
                                                                '主营业务增长率(时序中位数)排名', '行业龙头占比(时序中位数)排名',
                                                                '综合成长属性(时序均值)排名', '综合价值属性(时序均值)排名', '综合成长属性(时序中位数)排名',
                                                                '综合价值属性(时序中位数)排名', 'asofdate']))

    sql = " select * from hbs_industry_financial_stats where ENDDATE>='{0}' and ENDDATE<='{1}'" \
        .format(str(int(latest_date[0:4]) - 3) + latest_date[4:6], latest_date[0:6])
    industry_financial_info = pd.read_sql(sql, con=localdb)

    industry_financial_info[['ROE', 'NETPROFITGROWRATE',
                             'OPERATINGREVENUEYOY', 'DIVIDENDRATIO']] = industry_financial_info[
                                                                            ['ROE', 'NETPROFITGROWRATE',
                                                                             'OPERATINGREVENUEYOY',
                                                                             'DIVIDENDRATIO']] / 100

    industry_financial_info_mean = industry_financial_info \
        .groupby('industry_name').median().rename(columns={
        "ROE": "行业净资产收益率", "PE": "行业PE", "PCF": "行业PCF",
        "NETPROFITGROWRATE": "行业净利润增长率", "OPERATINGREVENUEYOY": "行业主营业务增长率",
        "PB": "行业PB", "DIVIDENDRATIO": "行业股息率", "AVERAGEMV": "行业平均市值", "TOTALMV": "行业总市值",
        "PEG": "行业PEG"})
    industry_financial_info_med = industry_financial_info \
        .groupby('industry_name').median().rename(columns={
        "ROE": "行业净资产收益率", "PE": "行业PE", "PCF": "行业PCF",
        "NETPROFITGROWRATE": "行业净利润增长率", "OPERATINGREVENUEYOY": "行业主营业务增长率",
        "PB": "行业PB", "DIVIDENDRATIO": "行业股息率", "AVERAGEMV": "行业平均市值", "TOTALMV": "行业总市值",
        "PEG": "行业PEG"})

    industry_financial_info = pd.merge(industry_financial_info_mean, industry_financial_info_med,
                                       how='inner', left_index=True, right_index=True)

    industry_financial_info.columns = industry_financial_info.columns.str.replace('TOP', "")
    industry_financial_info.columns = industry_financial_info.columns.str.replace('TOP', "")
    industry_financial_info.columns = industry_financial_info.columns.str.replace('MV', "市值")
    industry_financial_info.columns = industry_financial_info.columns.str.replace('%', "分位数")
    industry_financial_info.columns = industry_financial_info.columns.str.replace('_x', "(时序均值)")
    industry_financial_info.columns = industry_financial_info.columns.str.replace('_y', "(时序中位数)")
    industry_financial_info.reset_index(inplace=True)



    theme_weight = pd.DataFrame()
    for i in range(3):

        latest_date=asofdate1
        sql = "SELECT * from {2}_{1}_industry_level where asofdate='{0}' " \
            .format(latest_date, i + 1,industry_level_table)
        temp_ind_detail = pd.read_sql(sql, con=localdb).rename(columns=name_map)
        temp_ind_detail.rename(columns={class_name_list[i]: '行业名称'}, inplace=True)

        temp_ind_detail[['行业龙头占比(时序均值)', '行业龙头占比(时序中位数)',
                         '净资产收益率(时序均值)', '股息率(时序均值)', '净利润增长率(时序均值)',
                         '主营业务增长率(时序均值)', '净资产收益率(时序中位数)', '股息率(时序中位数)',
                         '净利润增长率(时序中位数)', '主营业务增长率(时序中位数)']] = temp_ind_detail[['行业龙头占比(时序均值)', '行业龙头占比(时序中位数)',
                                                                                '净资产收益率(时序均值)', '股息率(时序均值)',
                                                                                '净利润增长率(时序均值)',
                                                                                '主营业务增长率(时序均值)', '净资产收益率(时序中位数)',
                                                                                '股息率(时序中位数)',
                                                                                '净利润增长率(时序中位数)',
                                                                                '主营业务增长率(时序中位数)']] / 100

        temp_ind_detail = pd.merge(temp_ind_detail, industry_financial_info,
                                   how='left', left_on='行业名称', right_on='industry_name')

        temp_ind_detail = temp_ind_detail[['jjdm','行业名称', '占持仓比例(时序均值)',
                                           '占持仓比例(时序均值)排名',
                                           '综合价值属性(时序均值)排名', '综合成长属性(时序均值)排名',
                                           '行业龙头占比(时序均值)', '行业龙头占比(时序均值)排名',
                                           '主营业务增长率(时序均值)', '主营业务增长率(时序均值)排名', '行业主营业务增长率(时序均值)',
                                           '净利润增长率(时序均值)', '净利润增长率(时序均值)排名', '行业净利润增长率(时序均值)',
                                           '净资产收益率(时序均值)', '净资产收益率(时序均值)排名', '行业净资产收益率(时序均值)',
                                           'PB(时序均值)', 'PB(时序均值)排名', '行业PB(时序均值)',
                                           'PE(时序均值)', 'PE(时序均值)排名', '行业PE(时序均值)',
                                           'PCF(时序均值)', 'PCF(时序均值)排名', '行业PCF(时序均值)',
                                           '股息率(时序均值)', '股息率(时序均值)排名', '行业股息率(时序均值)',
                                           'PEG(时序均值)', 'PEG(时序均值)排名', '行业PEG(时序均值)',
                                           '总市值(时序均值)', '总市值(时序均值)排名', '行业平均市值(时序均值)', '25分位数市值(时序均值)', '50分位数市值(时序均值)',
                                           '75分位数市值(时序均值)',
                                           '90分位数市值(时序均值)', 'asofdate',
                                           '占持仓比例(时序中位数)', '占持仓比例(时序中位数)排名', '综合价值属性(时序中位数)排名',
                                           '综合成长属性(时序中位数)排名', '行业龙头占比(时序中位数)', '行业龙头占比(时序中位数)排名',
                                           '主营业务增长率(时序中位数)', '主营业务增长率(时序中位数)排名','行业主营业务增长率(时序中位数)',
                                           '净利润增长率(时序中位数)', '净利润增长率(时序中位数)排名', '行业净利润增长率(时序中位数)',
                                           '净资产收益率(时序中位数)', '净资产收益率(时序中位数)排名', '行业净资产收益率(时序中位数)',
                                           'PB(时序中位数)', 'PB(时序中位数)排名', '行业PB(时序中位数)',
                                           'PE(时序中位数)', 'PE(时序中位数)排名', '行业PE(时序中位数)',
                                           'PCF(时序中位数)', 'PCF(时序中位数)排名', '行业PCF(时序中位数)',
                                           '股息率(时序中位数)', '股息率(时序中位数)排名', '行业股息率(时序中位数)',
                                           'PEG(时序中位数)', 'PEG(时序中位数)排名', '行业PEG(时序中位数)',
                                           '总市值(时序中位数)', '总市值(时序中位数)排名',
                                           '行业平均市值(时序中位数)', '25分位数市值(时序中位数)', '50分位数市值(时序中位数)', '75分位数市值(时序中位数)',
                                           '90分位数市值(时序中位数)'
                                           ]]


        if(i==0):
            industry_rank = pd.DataFrame()
            industry_rank['行业名称'] = ['农林牧渔', '基础化工', '钢铁', '有色金属', '电子', '家用电器', '食品饮料',
                                         '纺织服饰', '轻工制造',
                                         '医药生物', '公用事业', '交通运输', '房地产', '商贸零售', '社会服务',
                                         '建筑材料', '建筑装饰',
                                         '电力设备', '国防军工', '计算机', '传媒', '通信', '银行', '非银金融', '汽车',
                                         '机械设备', '煤炭',
                                         '石油石化', '环保', '美容护理']
            industry_rank['行业类型'] = [0.41935483870967744, 0.8387096774193549, 0.12903225806451613,
                                         0.8709677419354839, 0.7419354838709677,
                                         0.967741935483871, 1.0, 0.5483870967741935, 0.6451612903225806,
                                         0.9032258064516129, 0.3548387096774194,
                                         0.25806451612903225, 0.0967741935483871, 0.45161290322580644,
                                         0.2903225806451613,
                                         0.4838709677419355, 0.3225806451612903, 0.9354838709677419, 0.5806451612903226,
                                         0.7096774193548387,
                                         0.5161290322580645, 0.3870967741935484, 0.03225806451612903,
                                         0.16129032258064516, 0.6129032258064516,
                                         0.7741935483870968, 0.1935483870967742, 0.22580645161290322,
                                         0.6774193548387096, 0.8064516129032258]
            tempdf = temp_ind_detail
            tempdf = pd.merge(tempdf, industry_rank, how='left', on='行业名称')

            tempdf['行业类型'] = tempdf['占持仓比例(时序均值)'] * tempdf['行业类型']


            industry_class = tempdf.groupby('jjdm').sum()['行业类型'].reset_index()

            industry_class['一级行业策略'] = '无'
            industry_class.loc[(industry_class['行业类型'] >= 2 / 3), '一级行业策略'] = '成长'
            industry_class.loc[(industry_class['行业类型'] <= 1 / 3), '一级行业策略'] = '价值'


            industry_p = pd.merge(industry_p, industry_class.drop('行业类型', axis=1), how='left', on='jjdm')


        if(i==1):
            industry_rank = pd.DataFrame()
            industry_rank['行业名称'] = ['IT服务', '一般零售', '专业工程', '专业服务', '专业连锁', '专用设备',
                                         '个护用品', '中药'
                , '乘用车', '互联网电商', '休闲食品', '保险', '元件', '光伏设备', '光学光电子', '其他家电', '其他电子',
                                         '其他电源设备'
                , '养殖业', '军工电子', '农产品加工', '农化制品', '农商行', '出版', '动物保健', '包装印刷', '化妆品',
                                         '化学制品'
                , '化学制药', '化学原料', '化学纤维', '医疗器械', '医疗服务', '医疗美容', '医药商业', '半导体',
                                         '厨卫电器', '商用车'
                , '国有大型银行', '地面兵装', '城商行', '基础建设', '塑料', '多元金融', '家居用品', '家电零部件',
                                         '小家电', '小金属'
                , '工业金属', '工程咨询服务', '工程机械', '影视院线', '房地产开发', '房地产服务', '房屋建设',
                                         '摩托车及其他', '教育'
                , '数字媒体', '文娱用品', '旅游及景区', '旅游零售', '普钢', '服装家纺', '橡胶', '汽车服务',
                                         '汽车零部件', '油服工程'
                , '油气开采', '消费电子', '游戏', '炼化及贸易', '照明设备', '燃气', '物流', '特钢', '环保设备',
                                         '环境治理', '玻璃玻纤'
                , '生物制品', '电力', '电子化学品', '电机', '电池', '电网设备', '白色家电', '白酒', '种植业',
                                         '纺织制造', '股份制银行'
                , '能源金属', '自动化设备', '航天装备', '航空机场', '航空装备', '装修建材', '装修装饰', '计算机设备',
                                         '证券', '调味发酵品'
                , '贵金属', '贸易', '轨交设备', '软件开发', '通信设备', '通用设备', '造纸', '酒店餐饮', '金属新材料',
                                         '非白酒', '非金属材料'
                , '风电设备', '食品加工', '饮料乳品', '饰品', '饲料', '黑色家电', '冶钢原料', '广告营销', '水泥',
                                         '焦炭', '煤炭开采'
                , '电视广播', '综合', '航海装备', '航运港口', '通信服务', '铁路公路']
            industry_rank['二级行业类型'] = ['无', '价值', '成长', '成长', '价值', '成长', '价值', '价值', '无', '无',
                                             '无'
                , '价值', '价值', '成长', '价值', '价值', '无', '价值', '成长', '成长', '无', '成长', '无', '价值', '价值'
                , '价值', '无', '成长', '无', '无', '价值', '成长', '无', '成长', '价值', '成长', '成长', '价值',
                                             '价值', '无'
                , '成长', '价值', '价值', '无', '成长', '无', '成长', '无', '无', '无', '成长', '无', '价值', '成长',
                                             '无', '无'
                , '成长', '成长', '无', '价值', '成长', '价值', '无', '无', '成长', '无', '成长', '无', '成长', '无',
                                             '价值'
                , '无', '成长', '成长', '成长', '无', '无', '无', '成长', '价值', '无', '无', '无', '无', '价值',
                                             '成长', '无'
                , '无', '无', '无', '无', '无', '无', '成长', '无', '无', '无', '成长', '无', '无', '成长', '价值',
                                             '无', '无'
                , '无', '价值', '价值', '无', '成长', '无', '价值', '价值', '价值', '无', '成长', '无', '无', '无',
                                             '无', '无'
                , '无', '价值', '无', '价值', '成长', '无', '价值']

            tempdf = temp_ind_detail
            tempdf = pd.merge(tempdf, industry_rank, how='left', on='行业名称')

            tempdf['成长综合排名'] = tempdf[['主营业务增长率(时序中位数)排名', '净利润增长率(时序中位数)排名',
                                             '净资产收益率(时序中位数)排名']].mean(axis=1)
            tempdf[['PB(时序中位数)排名', 'PE(时序中位数)排名']] = 1 - tempdf[
                ['PB(时序中位数)排名', 'PE(时序中位数)排名']]
            tempdf['价值综合排名'] = tempdf[
                ['PB(时序中位数)排名', 'PE(时序中位数)排名', '股息率(时序中位数)排名']].mean(axis=1)

            tempdf['成长综合排名'] = tempdf['成长综合排名'] * tempdf['占持仓比例(时序均值)']
            tempdf['价值综合排名'] = tempdf['价值综合排名'] * tempdf['占持仓比例(时序均值)']

            industry_class = tempdf.groupby(['jjdm', '二级行业类型']).sum('占持仓比例(时序均值)')[
                '占持仓比例(时序均值)'].reset_index()

            tempdf = tempdf.groupby('jjdm').sum()[['成长综合排名', '价值综合排名']]
            tempdf['adjust_benchmark'] = tempdf[['成长综合排名', '价值综合排名']].sum(axis=1).values
            tempdf['成长综合排名'] = tempdf['成长综合排名'] / tempdf['adjust_benchmark']
            tempdf['价值综合排名'] = tempdf['价值综合排名'] / tempdf['adjust_benchmark']
            tempdf['行业精选个股策略'] = '无'
            tempdf.loc[tempdf['成长综合排名'] - tempdf['价值综合排名'] >= 0.1,
            '行业精选个股策略'] = '成长'
            tempdf.loc[tempdf['价值综合排名'] - tempdf['成长综合排名'] >= 0.1,
            '行业精选个股策略'] = '价值'

            industry_class['二级行业策略'] = '无'
            industry_class.loc[(industry_class['占持仓比例(时序均值)'] > 0.45) &
                               (industry_class['二级行业类型'] != "无"), '二级行业策略'] = \
                industry_class.loc[(industry_class['占持仓比例(时序均值)'] > 0.45) &
                                   (industry_class['二级行业类型'] != "无")]['二级行业类型']
            tempdf = pd.merge(tempdf, industry_class[industry_class['二级行业策略'] != '无'][['jjdm', '二级行业策略']],
                              how='left', on='jjdm')
            tempdf.loc[tempdf['二级行业策略'].isnull(), '二级行业策略'] = '无'
            tempdf = pd.merge(tempdf, industry_class.pivot_table('占持仓比例(时序均值)', 'jjdm', '二级行业类型')
                              , how='left', on='jjdm').rename(columns={'价值': '二级价值行业占比',
                                                                       '成长': '二级成长行业占比'})

            industry_p = pd.merge(industry_p, tempdf[
                ['jjdm', '行业精选个股策略', '二级行业策略', '二级价值行业占比', '二级成长行业占比',
                 '成长综合排名', '价值综合排名']],
                               how='left', on='jjdm')



        ind_detial_float_col = temp_ind_detail.columns.tolist()
        ind_detial_float_col.sort()
        for col in ['总市值(时序中位数)', '总市值(时序中位数)排名',
                    '总市值(时序均值)', '总市值(时序均值)排名', '行业平均市值(时序中位数)', '25分位数市值(时序中位数)',
                    '50分位数市值(时序中位数)', '75分位数市值(时序中位数)', '90分位数市值(时序中位数)', '行业平均市值(时序均值)', '25分位数市值(时序均值)',
                    '50分位数市值(时序均值)', '75分位数市值(时序均值)', '90分位数市值(时序均值)', 'asofdate', '行业名称',
                    'PE(时序中位数)', 'PE(时序均值)', 'PEG(时序中位数)', 'PEG(时序均值)',
                    'PB(时序中位数)', 'PB(时序均值)', '行业PE(时序中位数)', '行业PB(时序中位数)', '行业PEG(时序中位数)', '行业PE(时序均值)', '行业PB(时序均值)',
                    '行业PEG(时序均值)']:
            ind_detial_float_col.remove(col)
        if (i == 0):
            theme_weight = temp_ind_detail[['jjdm','行业名称', '占持仓比例(时序均值)']]

        industry_detail_df_list.append(temp_ind_detail)

    latest_date = asofdate2
    sql = "SELECT * from {1} where  asofdate='{0}' " \
        .format(latest_date,ind_shift_property_table)
    industry_sp = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)
    ind_sp_float_col_list = industry_sp.columns.tolist()
    ind_sp_float_col_list.remove('jjdm')
    ind_sp_float_col_list.remove('asofdate')


    # generate the label:
    # industry_p['一级行业类型']='配置'
    # industry_p['二级行业类型'] = '配置'
    # industry_p['三级行业类型'] = '配置'
    # industry_p['主题类型'] = '配置'


    name_map=dict(zip(['ind_1','ind_2','ind_3','theme'],
                      ['一级行业类型','二级行业类型','三级行业类型','主题类型']))
    for class_lv in ['ind_1','ind_2','ind_3','theme']:

        industry_p = label_style(industry_p, 'cen_'+class_lv, 'ratio_'+class_lv, name_map[class_lv], 3)
        industry_p.loc[(industry_p[name_map[class_lv]] == '轮动') & (
                industry_p['cen_'+class_lv] > industry_p[industry_p[name_map[class_lv]] == '轮动'][
            'cen_'+class_lv].median()), name_map[class_lv]] = '博弈'
        plot.plotly_markers(industry_p.pivot_table('cen_'+class_lv, 'ratio_'+class_lv,name_map[class_lv]),
                            name_map[class_lv] + '_' + str(industry_p['asofdate'].unique()[0]), x_text=name_map[class_lv][0:-2]+'换手率',
                            y_text=name_map[class_lv][0:-2]+'集中度')

        # industry_p.loc[(industry_p[class_lv+'集中度']>th1)
        #                &(industry_p[class_lv+'换手率'] > th2),class_lv+'类型']='博弈'
        # industry_p.loc[(industry_p[class_lv+'集中度']>th1)
        #                &(industry_p[class_lv+'换手率'] < th2),class_lv+'类型']='专注'
        # industry_p.loc[(industry_p[class_lv+'集中度']<th1)
        #                &(industry_p[class_lv+'换手率'] > th2),class_lv+'类型']='轮动'
        # industry_p.loc[(industry_p[class_lv+'集中度']<th1)
        #                &(industry_p[class_lv+'换手率'] < th2),class_lv+'类型']='配置'


    industry_p=pd.merge(industry_p,jj_base_info,how='left',on='jjdm').rename(columns={'jjjc':'基金简称'})

    # theme picture
    # latest_date = pd.read_sql(
    #     "select max(asofdate) as asofdate from {0}".format(theme_shift_property_table), con=localdb)['asofdate'][0]
    latest_date=asofdate2
    sql = "SELECT * from {1} where asofdate='{0}' " \
        .format(latest_date,theme_shift_property_table)
    theme_sp = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)

    theme_sp_float_col_list = theme_sp.columns.tolist()
    theme_sp_float_col_list.remove('jjdm')
    theme_sp_float_col_list.remove('asofdate')

    theme_weight = pd.merge(theme_weight, ia.ind2thememap,
                            how='left', left_on='行业名称', right_on='industry_name').drop('industry_name', axis=1)
    theme_weight = theme_weight.groupby(['jjdm','theme']).sum().reset_index(level=0).T

    for theme in ia.theme_col:
        industry_p = pd.merge(industry_p,
                              theme_weight[theme].T,
                              how='left', on='jjdm').rename(columns={'占持仓比例(时序均值)':theme})


    theme_p = industry_p[['jjdm', '基金简称', '主题类型', '主题集中度', '主题换手率', '大金融', '消费', 'TMT',
                          '周期', '制造', 'asofdate']]
    theme_sp = theme_sp[['Total_rank',
                         '大金融_rank', '消费_rank', 'TMT_rank', '周期_rank', '制造_rank',
                         'Total', '大金融', '消费', 'TMT', '周期', '制造', 'jjdm','asofdate']]
    theme_sp.reset_index(inplace=True)

    industry_p = industry_p[['jjdm', '基金简称', '一级行业类型', '一级行业集中度', '一级行业换手率', '前五大行业','二级行业前20大','三级行业前20大', '龙头占比(时序均值)',
                             '龙头占比(时序中位数)', '龙头占比(时序均值)排名', '龙头占比(时序中位数)排名', '二级行业类型', '二级行业集中度', '二级行业换手率',
                             '三级行业类型', '三级行业集中度', '三级行业换手率','一级行业策略','行业精选个股策略','二级行业策略', '二级价值行业占比', '二级成长行业占比',
                 '成长综合排名', '价值综合排名','asofdate']]

    industry_sp = industry_sp[['Total_rank', '农林牧渔_rank',
                               '基础化工_rank', '钢铁_rank', '有色金属_rank', '电子_rank', '家用电器_rank',
                               '食品饮料_rank', '纺织服饰_rank', '轻工制造_rank', '医药生物_rank', '公用事业_rank',
                               '交通运输_rank', '房地产_rank', '商贸零售_rank', '社会服务_rank', '综合_rank',
                               '建筑材料_rank', '建筑装饰_rank', '电力设备_rank', '国防军工_rank', '计算机_rank',
                               '传媒_rank', '通信_rank', '银行_rank', '非银金融_rank', '汽车_rank', '机械设备_rank',
                               '煤炭_rank', '石油石化_rank', '环保_rank', '美容护理_rank', 'Total', '农林牧渔', '基础化工', '钢铁', '有色金属',
                               '电子', '家用电器', '食品饮料', '纺织服饰',
                               '轻工制造', '医药生物', '公用事业', '交通运输', '房地产', '商贸零售', '社会服务', '综合', '建筑材料',
                               '建筑装饰', '电力设备', '国防军工', '计算机', '传媒', '通信', '银行', '非银金融', '汽车', '机械设备',
                               '煤炭', '石油石化', '环保', '美容护理', 'jjdm','asofdate']]
    industry_sp.reset_index(inplace=True)

    #check if data already exist
    sql="delete from {1} where asofdate='{0}'".format(industry_p['asofdate'][0],ind_property_pic_table)
    localdb.execute(sql)
    industry_p.to_sql(ind_property_pic_table,con=localdb,index=False,if_exists='append')

    sql="delete from {1} where asofdate={0}".format(industry_sp['asofdate'][0],ind_shift_pic_table)
    localdb.execute(sql)
    industry_sp.to_sql(ind_shift_pic_table, con=localdb, index=False, if_exists='append')

    sql="delete from {1} where asofdate='{0}'".format(theme_p['asofdate'][0],theme_property_pic_table)
    localdb.execute(sql)
    theme_p.to_sql(theme_property_pic_table, con=localdb, index=False, if_exists='append')

    sql="delete from {1} where asofdate='{0}'".format(theme_sp['asofdate'][0],theme_shift_pic_table)
    localdb.execute(sql)
    theme_sp.to_sql(theme_shift_pic_table, con=localdb, index=False, if_exists='append')

    for i in range(3):
        sql = "delete from {2}_{1} where asofdate={0}"\
            .format(industry_detail_df_list[i]['asofdate'][0],str(i+1),industry_level_pic_table)
        localdb.execute(sql)
        industry_detail_df_list[i].to_sql("{1}_{0}".format(str(i+1),industry_level_pic_table),
                                          con=localdb, index=False, if_exists='append')

def style_pic_all(jj_base_info,asofdate,fre, th1=0.5, th2=0.5, if_percentage=True,if_prv=False,fre2='Q'):



    def label_style(df, cen_col, shift_col, style_col, bias_col, n_clusters = 4):

        from sklearn.cluster import KMeans
        # from sklearn import metrics

        for col in [cen_col, shift_col]:
            df.loc[df[col]<=df[col].quantile(0.01),col]=df[col].quantile(0.01)
            df.loc[df[col] >= df[col].quantile(0.99),col] = df[col].quantile(0.99)


        df[style_col] = \
            KMeans(n_clusters=n_clusters,init='k-means++',
                         random_state=0).fit_predict(df[[cen_col, shift_col]].fillna(0).values)
        # plot.plotly_markers(df.pivot_table('集中度','换手率','风格类型'), 'asdf')
        type_dict=\
            df[[cen_col, shift_col,style_col]].groupby(style_col).median()[[cen_col, shift_col]].rank()

        if(n_clusters==3):
            type_dict.loc[(type_dict[cen_col] > 2) & (type_dict[shift_col] <= 2), style_col]= '专注'
            type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] > 2), style_col]= '轮动'
            type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] <= 2), style_col]= '配置'
        else:
            type_dict.loc[(type_dict[cen_col] > 2) & (type_dict[shift_col] <= 2), style_col]= '专注'
            type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] > 2), style_col]= '轮动'
            type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] <= 2), style_col]= '配置'
            type_dict.loc[(type_dict[cen_col] > 2) & (type_dict[shift_col] > 2), style_col]= '博弈'


        df[style_col]=[type_dict.loc[x][style_col] for x in df[style_col]]
        df.loc[df[style_col].isin(['配置','轮动']),bias_col] = '均衡'
        df.loc[df[style_col].isin(['专注', '博弈']), bias_col] =df[df[style_col].isin(['专注', '博弈'])]['winning_value']


        return df.drop('winning_value', axis=1)

    if(if_prv):
        if(fre2=='M'):
            fre_table='_monthly'
        else:
            fre_table=''
        nav_property_table='nav_prv_style_property'
        hbs_property_table='hbs_prv{}'.format(fre_table)
        nav_shift_table='nav_prv_shift_property'
        jjpic_table='jjpic_prv{}'.format(fre_table)
    else:
        nav_property_table='nav_style_property'
        hbs_property_table='hbs'
        nav_shift_table='nav_shift_property'
        jjpic_table='jjpic'

    if(not if_prv):
        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from {1}_value where fre='{0}'"
                .format(fre,nav_property_table), con=localdb)['asofdate'][0]

        sql = "SELECT * from {2}_value where fre='{0}' and asofdate='{1}' " \
            .format( fre, latest_date,nav_property_table)
        value_p = pd.read_sql(sql, con=localdb).rename(columns={'shift_ratio_rank': '换手率排名',
                                                                'centralization_rank': '集中度排名',
                                                                '成长_mean': '成长暴露排名',
                                                                '价值_mean': '价值暴露排名',
                                                                '成长_abs_mean': '成长绝对暴露',
                                                                '价值_abs_mean': '价值绝对暴露',
                                                                'manager_change': '经理是否未变更',
                                                                'shift_ratio': '换手率',
                                                                'centralization': '集中度',
                                                                'fre': '回归周期',
                                                                })

        # generate the label for nav based :
        value_p['max'] = value_p[['成长暴露排名', '价值暴露排名']].max(axis=1)
        value_p.loc[value_p['成长暴露排名'] == value_p['max'], 'winning_value'] = '成长'
        value_p.loc[value_p['价值暴露排名'] == value_p['max'], 'winning_value'] = '价值'
        value_p.drop('max', axis=1, inplace=True)

        value_p = label_style(value_p, '集中度排名', '换手率排名', '风格类型', '风格偏好')
        value_p = pd.merge(value_p, jj_base_info, how='left', on='jjdm').rename(columns={'jjjc': '基金简称'})
        value_p = value_p[['jjdm', '基金简称', '风格类型', '风格偏好', '换手率排名', '集中度排名',
                           '成长暴露排名', '价值暴露排名', '成长绝对暴露', '价值绝对暴露', '经理是否未变更',
                           '换手率', '集中度', '回归周期', 'asofdate']]

        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from {1}_size where fre='{0}'"
                .format(fre, nav_property_table), con=localdb)['asofdate'][0]

        sql = "SELECT * from {2}_size where fre='{0}' and asofdate='{1}' " \
            .format(fre, latest_date, nav_property_table)
        size_p = pd.read_sql(sql, con=localdb).rename(columns={'shift_ratio_rank': '换手率排名',
                                                               'centralization_rank': '集中度排名',
                                                               '大盘_mean': '大盘暴露排名',
                                                               '中盘_mean': '中盘暴露排名',
                                                               '小盘_mean': '小盘暴露排名',
                                                               '大盘_abs_mean': '大盘绝对暴露',
                                                               '中盘_abs_mean': '中盘绝对暴露',
                                                               '小盘_abs_mean': '小盘绝对暴露',
                                                               'manager_change': '经理是否未变更',
                                                               'shift_ratio': '换手率',
                                                               'centralization': '集中度',
                                                               'fre': '回归周期',
                                                               })

        # generate the label for nav based :
        size_p['winning_value'] = ''
        size_p.loc[size_p['大盘暴露排名'] > 0.5, 'winning_value'] = size_p.loc[size_p['大盘暴露排名'] > 0.5]['winning_value'] + '大'
        size_p.loc[size_p['中盘暴露排名'] > 0.5, 'winning_value'] = size_p.loc[size_p['中盘暴露排名'] > 0.5]['winning_value'] + '中'
        size_p.loc[size_p['小盘暴露排名'] > 0.5, 'winning_value'] = size_p.loc[size_p['小盘暴露排名'] > 0.5]['winning_value'] + '小'

        size_p = label_style(size_p, '集中度排名', '换手率排名', '规模风格类型', '规模偏好')

        size_p = pd.merge(size_p, jj_base_info, how='left', on='jjdm').rename(columns={'jjjc': '基金简称'})
        size_p = size_p[['jjdm', '基金简称', '规模风格类型', '规模偏好', '换手率排名', '集中度排名', '大盘暴露排名',
                         '大盘绝对暴露', '中盘暴露排名', '中盘绝对暴露', '小盘暴露排名', '小盘绝对暴露', '经理是否未变更',
                         '换手率', '集中度', '回归周期', 'asofdate']]

        # shift property for nav based
        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from {1}_value where fre='{0}'"
                .format(fre, nav_shift_table), con=localdb)['asofdate'][0]

        sql = "SELECT * from {2}_value where asofdate='{0}' and fre='{1}' " \
            .format(latest_date, fre, nav_shift_table)
        value_sp = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)
        value_sp_float_col_list = value_sp.columns.tolist()
        value_sp_float_col_list.remove('jjdm')
        value_sp_float_col_list.remove('asofdate')
        value_sp_float_col_list.remove('fre')

        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from {1}_size where fre='{0}'"
                .format(fre, nav_shift_table), con=localdb)['asofdate'][0]

        sql = "SELECT * from {2}_size where asofdate='{0}' and fre='{1}' " \
            .format(latest_date, fre, nav_shift_table)
        size_sp = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)
        size_sp_float_col_list = size_sp.columns.tolist()
        size_sp_float_col_list.remove('jjdm')
        size_sp_float_col_list.remove('asofdate')
        size_sp_float_col_list.remove('fre')

        # shift property for hbs based
        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from {0}_shift_property_value"
                .format(hbs_property_table), con=localdb)['asofdate'][0]

        sql = "SELECT * from {1}_shift_property_value where asofdate='{0}'  " \
            .format(latest_date, hbs_property_table)
        value_sp_hbs = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)
        value_sp_hbs_float_col_list = value_sp_hbs.columns.tolist()
        value_sp_hbs_float_col_list.remove('jjdm')
        value_sp_hbs_float_col_list.remove('asofdate')

        latest_date = pd.read_sql(
            "select max(asofdate) as asofdate from {0}_shift_property_size "
                .format(hbs_property_table), con=localdb)['asofdate'][0]

        sql = "SELECT * from {1}_shift_property_size where asofdate='{0}' " \
            .format(latest_date, hbs_property_table)
        size_sp_hbs = pd.read_sql(sql, con=localdb).set_index('项目名').fillna(0)
        size_sp_hbs_float_col_list = size_sp_hbs.columns.tolist()
        size_sp_hbs_float_col_list.remove('jjdm')
        size_sp_hbs_float_col_list.remove('asofdate')

        if (if_percentage):
            for col in ['换手率排名', '集中度排名', '成长暴露排名', '价值暴露排名',
                        '换手率', '集中度', ]:
                value_p[col] = value_p[col].map("{:.2%}".format)

            for col in ['换手率排名', '集中度排名', '大盘暴露排名', '中盘暴露排名', '小盘暴露排名',
                        '换手率', '集中度', ]:
                size_p[col] = size_p[col].map("{:.2%}".format)

            for col in ['Total', '成长', '价值']:
                value_sp.loc[value_sp.index != '切换次数', col] = \
                    value_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
                value_sp_hbs.loc[value_sp_hbs.index != '切换次数', col] = \
                    value_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
            for col in ['Total_rank', '成长_rank', '价值_rank']:
                value_sp[col] = \
                    value_sp[col].astype(float).map("{:.2%}".format)
                value_sp_hbs[col] = \
                    value_sp_hbs[col].astype(float).map("{:.2%}".format)

            for col in ['Total', '大盘', '中盘', '小盘']:
                size_sp.loc[size_sp.index != '切换次数', col] = \
                    size_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
                size_sp_hbs.loc[size_sp_hbs.index != '切换次数', col] = \
                    size_sp_hbs.iloc[1:][col].astype(float).map("{:.2%}".format)
            for col in ['Total_rank', '大盘_rank', '中盘_rank', '小盘_rank']:
                size_sp[col] = \
                    size_sp[col].astype(float).map("{:.2%}".format)
                size_sp_hbs[col] = \
                    size_sp_hbs[col].astype(float).map("{:.2%}".format)

        value_sp = value_sp[['jjdm', 'Total_rank', '成长_rank', '价值_rank',
                             'Total', '成长', '价值', 'fre', 'asofdate']]
        value_sp['type'] = 'nav_based'
        value_sp_hbs = value_sp_hbs[['jjdm', 'Total_rank', '成长_rank', '价值_rank',
                                     'Total', '成长', '价值', 'asofdate']]
        value_sp_hbs['type'] = 'holding_based'
        value_sp = pd.concat([value_sp, value_sp_hbs], axis=0)

        size_sp = size_sp[['jjdm', 'Total_rank', '大盘_rank', '中盘_rank',
                           '小盘_rank', 'Total', '大盘', '中盘', '小盘', 'fre', 'asofdate']]
        size_sp['type'] = 'nav_based'
        size_sp_hbs = size_sp_hbs[['jjdm', 'Total_rank', '大盘_rank', '中盘_rank',
                                   '小盘_rank', 'Total', '大盘', '中盘', '小盘', 'asofdate']]
        size_sp_hbs['type'] = 'holding_based'
        size_sp = pd.concat([size_sp, size_sp_hbs], axis=0)

        value_sp.reset_index(inplace=True)
        size_sp.reset_index(inplace=True)

        sql = "delete from {1}_value_p where asofdate='{0}'".format(value_p['asofdate'][0], jjpic_table)
        localdb.execute(sql)
        value_p.to_sql('{0}_value_p'.format(jjpic_table), con=localdb, index=False, if_exists='append')

        sql = "delete from {1}_size_p where asofdate='{0}'".format(size_p['asofdate'][0], jjpic_table)
        localdb.execute(sql)
        size_p.to_sql('{0}_size_p'.format(jjpic_table), con=localdb, index=False, if_exists='append')

        sql = "delete from {2}_value_sp where asofdate='{0}' or asofdate='{1}'" \
            .format(value_sp['asofdate'].unique()[0], value_sp['asofdate'].unique()[1], jjpic_table)
        localdb.execute(sql)
        value_sp.to_sql('{0}_value_sp'.format(jjpic_table), con=localdb, index=False, if_exists='append')

        sql = "delete from {2}_size_sp where asofdate='{0}' or asofdate='{1}'" \
            .format(size_sp['asofdate'].unique()[0], size_sp['asofdate'].unique()[1], jjpic_table)
        localdb.execute(sql)
        size_sp.to_sql('{0}_size_sp'.format(jjpic_table), con=localdb, index=False, if_exists='append')

    # latest_date = pd.read_sql(
    #     "select max(asofdate) as asofdate from {0}_style_property "
    #         .format(hbs_property_table), con=localdb)['asofdate'][0]

    latest_date=asofdate
    sql = "SELECT * from {1}_style_property where asofdate='{0}' " \
        .format(latest_date,hbs_property_table)
    value_p_hbs = pd.read_sql(sql, con=localdb).rename(columns={'cen_lv': '集中度(持仓)',
                                                                'shift_lv': '换手率(持仓)',
                                                                '成长': '成长绝对暴露(持仓)',
                                                                '价值': '价值绝对暴露(持仓)',
                                                                '均衡': '均衡绝对暴露(持仓)',
                                                                'cen_lv_rank': '集中度排名(持仓)',
                                                                'shift_lv_rank': '换手率排名(持仓)',
                                                                '成长_rank': '成长暴露排名(持仓)',
                                                                '价值_rank': '价值暴露排名(持仓)',
                                                                '均衡_rank': '均衡暴露排名(持仓)',})

    # generate the label for hbs based :
    value_p_hbs['max']=value_p_hbs[['成长绝对暴露(持仓)', '价值绝对暴露(持仓)']].max(axis=1)
    value_p_hbs.loc[value_p_hbs['成长绝对暴露(持仓)']==value_p_hbs['max'],'winning_value']='成长'
    value_p_hbs.loc[value_p_hbs['价值绝对暴露(持仓)'] == value_p_hbs['max'], 'winning_value'] = '价值'
    value_p_hbs.drop('max', axis=1, inplace=True)


    value_p_hbs = label_style(value_p_hbs, '集中度(持仓)','换手率(持仓)',
                              '风格类型','风格偏好',n_clusters=3)
    plot.plotly_markers(value_p_hbs.pivot_table('集中度(持仓)','换手率(持仓)','风格类型'),
                        '风格类型' + '_' + value_p_hbs['asofdate'].unique()[0], x_text='换手率(持仓)', y_text='集中度(持仓)')
    #modify the jj style ticker by its real style weight, if any weight bigger than 50%,then put the style ticker


    value_p_hbs.loc[(value_p_hbs['风格偏好'] != '均衡')
                    & (value_p_hbs[ '均衡绝对暴露(持仓)'] >= 0.6), '风格偏好'] = '均衡'

    value_p_hbs.loc[(value_p_hbs['风格偏好'] != '成长')
                    & (value_p_hbs['均衡绝对暴露(持仓)']  < 0.6)
                    & (value_p_hbs['成长绝对暴露(持仓)']> value_p_hbs['价值绝对暴露(持仓)'])
                    &(value_p_hbs['成长暴露排名(持仓)']  >= 0.8), '风格偏好'] = '成长'

    value_p_hbs.loc[(value_p_hbs['风格偏好'] != '价值')
                    & (value_p_hbs['均衡绝对暴露(持仓)']  < 0.6)
                    & (value_p_hbs['成长绝对暴露(持仓)']/value_p_hbs['价值绝对暴露(持仓)']<=6/4)&
                    (value_p_hbs['价值暴露排名(持仓)']  >= 0.8), '风格偏好'] = '价值'

    # for col in ['成长', '价值', '均衡']:
    #     value_p_hbs.loc[(value_p_hbs['风格偏好']!=col)
    #                     &(value_p_hbs[col+'绝对暴露(持仓)']/value_p_hbs['总仓位']>=0.5),'风格偏好']=col



    value_p_hbs = pd.merge(value_p_hbs, jj_base_info, how='left', on='jjdm').rename(columns={'jjjc': '基金简称'})
    value_p_hbs = value_p_hbs[['jjdm', '基金简称', '风格类型', '风格偏好', '集中度(持仓)', '换手率(持仓)',
                               '成长绝对暴露(持仓)', '价值绝对暴露(持仓)', '集中度排名(持仓)',
                               '换手率排名(持仓)', '成长暴露排名(持仓)', '价值暴露排名(持仓)', 'asofdate']]

    if (if_percentage):
        for col in ['集中度(持仓)', '换手率(持仓)', '成长绝对暴露(持仓)', '价值绝对暴露(持仓)', '集中度排名(持仓)',
                    '换手率排名(持仓)', '成长暴露排名(持仓)', '价值暴露排名(持仓)']:
            value_p_hbs[col] = value_p_hbs[col].map("{:.2%}".format)

    # latest_date = pd.read_sql(
    #     "select max(asofdate) as asofdate from {0}_size_property "
    #         .format(hbs_property_table), con=localdb)['asofdate'][0]
    latest_date=asofdate
    sql = "SELECT * from {1}_size_property where  asofdate='{0}' " \
        .format(latest_date,hbs_property_table)
    size_p_hbs = pd.read_sql(sql, con=localdb).rename(columns={'cen_lv': '集中度(持仓)',
                                                               'shift_lv': '换手率(持仓)',
                                                               '大盘': '大盘绝对暴露(持仓)',
                                                               '中小盘': '中小盘绝对暴露(持仓)',
                                                               'cen_lv_rank': '集中度排名(持仓)',
                                                               'shift_lv_rank': '换手率排名(持仓)',
                                                               '大盘_rank': '大盘暴露排名(持仓)',
                                                               '中小盘_rank': '中小盘暴露排名(持仓)',
                                                               })


    # generate the label for hbs based :
    size_p_hbs['max']=size_p_hbs[['大盘绝对暴露(持仓)', '中小盘绝对暴露(持仓)']].max(axis=1)
    size_p_hbs.loc[size_p_hbs['大盘绝对暴露(持仓)']==size_p_hbs['max'],'winning_value']='大盘'
    size_p_hbs.loc[size_p_hbs['中小盘绝对暴露(持仓)'] == size_p_hbs['max'], 'winning_value'] = '中小盘'

    # size_p_hbs['winning_value'] = ''
    # size_p_hbs.loc[size_p_hbs['大盘绝对暴露(持仓)'] > 0.45, 'winning_value'] = size_p_hbs.loc[size_p_hbs['大盘绝对暴露(持仓)'] > 0.45]['winning_value'] + '大'
    # size_p_hbs.loc[size_p_hbs['中盘绝对暴露(持仓)'] > 0.45, 'winning_value'] = size_p_hbs.loc[size_p_hbs['中盘绝对暴露(持仓)'] > 0.45]['winning_value'] + '中'
    # size_p_hbs.loc[size_p_hbs['小盘绝对暴露(持仓)'] > 0.45, 'winning_value'] = size_p_hbs.loc[size_p_hbs['小盘绝对暴露(持仓)'] > 0.45]['winning_value'] + '小'
    # size_p_hbs.loc[size_p_hbs['winning_value']=='','winning_value']=size_p_hbs.loc[size_p_hbs['winning_value']==''][['大盘绝对暴露(持仓)','中盘绝对暴露(持仓)','小盘绝对暴露(持仓)']].idxmax(axis=1).astype(str).str[0]

    size_p_hbs = label_style(size_p_hbs, '集中度(持仓)', '换手率(持仓)',
                             '规模风格类型', '规模偏好', n_clusters=3)
    plot.plotly_markers(size_p_hbs.pivot_table('集中度(持仓)','换手率(持仓)','规模风格类型'),
                        '规模风格类型' + '_' + size_p_hbs['asofdate'].unique()[0], x_text='换手率(持仓)', y_text='集中度(持仓)')
    for col in ['大盘', '中小盘']:
        size_p_hbs.loc[(size_p_hbs['规模偏好'] == '均衡') & (size_p_hbs[col+'暴露排名(持仓)'] >= 0.8)& (size_p_hbs[col+'绝对暴露(持仓)'] >= 0.6), '规模偏好'] = col

    size_p_hbs = pd.merge(size_p_hbs, jj_base_info, how='left', on='jjdm').rename(columns={'jjjc': '基金简称'})
    size_p_hbs = size_p_hbs[
        ['jjdm', '基金简称', '规模风格类型', '规模偏好', '集中度(持仓)', '换手率(持仓)', '大盘绝对暴露(持仓)', '中小盘绝对暴露(持仓)',
         '集中度排名(持仓)', '换手率排名(持仓)', '大盘暴露排名(持仓)', '中小盘暴露排名(持仓)',
         'asofdate']]
    if (if_percentage):
        for col in ['集中度(持仓)', '换手率(持仓)', '大盘绝对暴露(持仓)', '中小盘绝对暴露(持仓)',
                    '集中度排名(持仓)', '换手率排名(持仓)', '大盘暴露排名(持仓)', '中小盘暴露排名(持仓)']:
            size_p_hbs[col] = size_p_hbs[col].map("{:.2%}".format)

    # value_sp_hbs.reset_index(inplace=True)
    # size_sp_hbs.reset_index(inplace=True)

    #delete already exist data


    sql="delete from {1}_value_p_hbs where asofdate='{0}'".format(value_p_hbs['asofdate'][0],jjpic_table)
    localdb.execute(sql)
    value_p_hbs.to_sql('{0}_value_p_hbs'.format(jjpic_table), con=localdb, index=False, if_exists='append')


    sql="delete from {1}_size_p_hbs where asofdate='{0}'".format(size_p_hbs['asofdate'][0],jjpic_table)
    localdb.execute(sql)
    size_p_hbs.to_sql('{0}_size_p_hbs'.format(jjpic_table), con=localdb, index=False, if_exists='append')

def stock_trading_pci_all(jj_base_info,asofdate,asofdate2, th1=0.75,
                          th2=0.25, th3=0.5, th4=0.5, th5=0.75, th6=0.5, if_percentage=True):
    # latest_date = pd.read_sql(
    #     "select max(asofdate) as asofdate from hbs_holding_property "
    #     , con=localdb)['asofdate'][0]
    latest_date=asofdate
    sql = "SELECT * from hbs_holding_property where  asofdate='{0}' " \
        .format(latest_date)
    stock_p = pd.read_sql(sql, con=localdb)

    float_col = stock_p.columns.tolist()
    float_col.remove('jjdm')
    float_col.remove('asofdate')
    float_col.remove('持股数量')
    float_col.remove('PE')
    float_col.remove('PB')
    float_col.remove('ROE')
    float_col.remove('股息率')
    float_col.remove('PE_中位数')
    float_col.remove('PB_中位数')
    float_col.remove('ROE_中位数')
    float_col.remove('股息率_中位数')
    ind_cen=pd.read_sql("SELECT jjdm, `一级行业类型` from jjpic_industry_p where asofdate='{0}' ".format(asofdate2),con=localdb)
    stock_p=pd.merge(stock_p,ind_cen,how='left',on='jjdm')

    # latest_date = pd.read_sql(
    #     "select max(asofdate) as asofdate from hbs_stock_trading_property "
    #     , con=localdb)['asofdate'][0]

    sql = "SELECT * from hbs_stock_trading_property where asofdate>='{0}' and asofdate<='{1}' " \
        .format(asofdate,asofdate2)
    stock_tp = pd.read_sql(sql, con=localdb)

    financial_left_ticker=pd.read_sql("SELECT * from financial_left_ticker where  asofdate>='{0}' and asofdate<='{1}'"
                                      .format(asofdate,asofdate2),con=localdb).drop('asofdate',axis=1)
    stock_tp=pd.merge(stock_tp,financial_left_ticker,how='left',on='jjdm')


    stock_tp.columns=stock_tp.columns.str.replace("（","(")
    stock_tp.columns = stock_tp.columns.str.replace("）", ")")
    stock_tp['换手率']=stock_tp['换手率']/100
    tp_float_col = stock_tp.columns.tolist()
    tp_float_col.remove('jjdm')
    tp_float_col.remove('平均持有时间(出重仓前)')
    tp_float_col.remove('平均持有时间(出持仓前)')
    tp_float_col.remove('asofdate')

    # generate the labels

    def label_style(df, cen_col, shift_col, style_col,n_clusters = 4):

        from sklearn.cluster import KMeans
        from sklearn import  preprocessing as pp

        for col in [cen_col, shift_col]:
            df.loc[df[col]<=df[col].quantile(0.1),col]=df[col].quantile(0.1)
            df.loc[df[col] >= df[col].quantile(0.9),col] = df[col].quantile(0.9)


        df[style_col] = \
            KMeans(n_clusters=n_clusters,init='k-means++',
                         random_state=0).fit_predict(pp.StandardScaler().fit_transform(df[[cen_col, shift_col]].fillna(0).values))

        type_dict=\
            df[[cen_col, shift_col,style_col]].groupby(style_col).median()[[cen_col, shift_col]].rank()

        if(n_clusters==3):
            type_dict.loc[(type_dict[cen_col] > 2) & (type_dict[shift_col] <= 2), style_col]= '专注'
            type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] > 2), style_col]= '轮动'
            type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] <= 2), style_col]= '配置'
        else:
            type_dict.loc[(type_dict[cen_col] > 2) & (type_dict[shift_col] <= 2), style_col]= '专注'
            type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] > 2), style_col]= '轮动'
            type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] <= 2), style_col]= '配置'
            type_dict.loc[(type_dict[cen_col] > 2) & (type_dict[shift_col] > 2), style_col]= '博弈'


        df[style_col]=[type_dict.loc[x][style_col] for x in df[style_col]]


        return df

    stock_p=pd.merge(stock_p,stock_tp[['jjdm','换手率','平均持有时间(出持仓前)']],how='left',on='jjdm')
    stock_p['个股集中度实际值']=stock_p[['前三大', '前五大', '前十大']].sum(axis=1)
    stock_p=label_style(stock_p,'个股集中度实际值','换手率','个股风格A')
    plot.plotly_markers(stock_p.pivot_table('个股集中度实际值','换手率','个股风格A'),
                        '个股风格A' + '_' + stock_p['asofdate'].unique()[0], x_text='换手率', y_text='个股集中度实际值')

    stock_p=label_style(stock_p,'个股集中度实际值','平均持有时间(出持仓前)','个股风格B')
    stock_p.loc[(stock_p['个股风格B']=='博弈'),'个股风格B']='自下而上'
    stock_p.loc[stock_p['个股风格B'] != '自下而上', '个股风格B'] = '无'
    stock_p.loc[(stock_p['一级行业类型'] == '博弈')&(stock_p['个股风格B']!='自下而上'), '个股风格B'] = '自上而下'
    plot.plotly_markers(stock_p.pivot_table('个股集中度实际值','平均持有时间(出持仓前)','个股风格B'),
                        '个股风格B' + '_' + stock_p['asofdate'].unique()[0], x_text='平均持有时间(出持仓前)', y_text='个股集中度实际值')

    stock_p['是否有尾仓(针对高个股集中基金)'] = '无尾仓'
    stock_tp['左侧标签'] = '无'
    stock_tp['新股次新股偏好']= ''
    # stock_tp['PB-ROE选股']=''
    # stock_tp['PEG选股'] = ''
    stock_tp['博弈基本面拐点']=''
    stock_tp['博弈估值修复'] = ''


    stock_p.loc[(stock_p['个股集中度'] > th1)
                & (stock_p['个股集中度'] - stock_p['hhi'] > 0.05),'是否有尾仓(针对高个股集中基金)']='有尾仓'
    stock_tp.loc[(stock_tp['左侧概率(出持仓前,半年线)_rank'] > th3)
                 & (stock_tp['左侧程度(出持仓前,半年线)'] > th4),'左侧标签']='深度左侧'
    stock_tp.loc[(stock_tp['左侧概率(出持仓前,半年线)_rank'] > th3)
                 & (stock_tp['左侧程度(出持仓前,半年线)'] < th4),'左侧标签']='左侧'
    stock_tp.loc[(stock_tp['买入 ROE-PB比例(出持仓前)_rank'] > 2/3)
                 & (stock_tp['卖出 ROE-PB比例(出持仓前)_rank'] > 2/3),'PB-ROE选股']="PB-ROE选股"
    stock_tp.loc[(stock_tp['买入 PEG比例(出持仓前)_rank'] > 2/3)
                 & (stock_tp['卖出 PEG比例(出持仓前)_rank'] > 2/3),'PEG选股']="PEG选股"
    stock_tp.loc[stock_tp['基本面左右侧标签']=='左侧','博弈基本面拐点']='博弈基本面拐点'
    stock_tp.loc[stock_tp['逆向买入比例(出持仓前)_rank'] >=2/3 , '博弈估值修复'] = '博弈估值修复'
    stock_tp.loc[(stock_tp['新股概率(出持仓前)_rank'] > th5),'新股次新股偏好']=\
        stock_tp[(stock_tp['新股概率(出持仓前)_rank'] > th5)]['新股次新股偏好']+'偏好新股'
    stock_tp.loc[(stock_tp['次新股概率(出持仓前)_rank'] > th5),'新股次新股偏好']=\
        stock_tp[(stock_tp['次新股概率(出持仓前)_rank'] > th5)]['新股次新股偏好']+'偏好次新股'
    stock_tp.loc[stock_tp['新股次新股偏好'] == '','新股次新股偏好']='无'


    if (if_percentage):
        for col in float_col:
            stock_p[col] = stock_p[col].map("{:.2%}".format)
        for col in tp_float_col:
            stock_tp[col] = stock_tp[col].map("{:.2%}".format)

    stock_p=pd.merge(stock_p,jj_base_info,how='left',on='jjdm').rename(columns={'jjjc':'基金简称'})
    # stock_p['基金简称'] = ''
    stock_tp = pd.merge(stock_tp, jj_base_info, how='left', on='jjdm').rename(columns={'jjjc': '基金简称'})
    # stock_tp['基金简称'] = ''

    #merge the baotuangu data
    sql="select fund_id as jjdm ,`{}` as baotuan_ratio from fund_baotuan_ratio ".format(stock_tp['asofdate'].unique()[0][0:6])
    baotuan_ratio=pd.read_sql(sql,con=localdb)
    stock_tp=pd.merge(stock_tp,baotuan_ratio,how='left',on='jjdm')
    stock_tp['baotuan_ratio']=stock_tp['baotuan_ratio'].rank(pct=True)
    stock_tp.loc[stock_tp['baotuan_ratio']>=2/3,'是否抱团']='抱团'
    stock_tp.loc[stock_tp['baotuan_ratio'] <= 1 / 3, '是否抱团'] = '逆向'


    stock_p = stock_p[['jjdm', '基金简称', '个股风格A', '个股风格B', '是否有尾仓(针对高个股集中基金)', '个股集中度', 'hhi', '持股数量',
                       '前三大', '前五大', '前十大', '平均仓位', '仓位换手率', 'PE_rank','PB_rank', 'ROE_rank', '股息率_rank', 'PEG_rank',
                       'PCF_rank', '毛利率_rank','净利率_rank', '市值_rank', '净利增速_rank','仓位换手率_rank',
                       'PE', 'PB', 'ROE', '股息率', 'PEG', 'PCF', '毛利率', '净利率', '市值', '净利增速', 'asofdate'
                       ]]
    stock_tp = stock_tp[['jjdm', '基金简称', '基本面左右侧标签', '左侧标签', '新股次新股偏好', 'PB-ROE选股', 'PEG选股', '博弈基本面拐点', '博弈估值修复','是否抱团',
                         '换手率_rank','平均持有时间(出重仓前)_rank', '平均持有时间(出持仓前)_rank', '出重仓前平均收益率_rank',
                         '出全仓前平均收益率_rank', '左侧概率(出重仓前,半年线)_rank', '左侧概率(出持仓前,半年线)_rank','左侧概率(出重仓前,年线)_rank',
                         '左侧概率(出持仓前,年线)_rank', '新股概率(出重仓前)_rank', '新股概率(出持仓前)_rank', '次新股概率(出重仓前)_rank', '次新股概率(出持仓前)_rank',
                         '买入 ROE(出重仓前)_rank', '买入 ROE(出持仓前)_rank', '卖出 ROE(出重仓前)_rank','卖出 ROE(出持仓前)_rank', '买入 净利润增速(出重仓前)_rank','买入 净利润增速(出持仓前)_rank',
                         '卖出 净利润增速(出重仓前)_rank', '卖出 净利润增速(出持仓前)_rank', '买入 股息率(出重仓前)_rank', '买入 股息率(出持仓前)_rank', '卖出 股息率(出重仓前)_rank',
                         '卖出 股息率(出持仓前)_rank', '买入 PE(出重仓前)_rank', '买入 PE(出持仓前)_rank', '卖出 PE(出重仓前)_rank', '卖出 PE(出持仓前)_rank', '买入 PB(出重仓前)_rank',
                         '买入 PB(出持仓前)_rank', '卖出 PB(出重仓前)_rank', '卖出 PB(出持仓前)_rank', '买入 毛利率(出重仓前)_rank', '买入 毛利率(出持仓前)_rank', '卖出 毛利率(出重仓前)_rank',
                         '卖出 毛利率(出持仓前)_rank', '买入 净利率(出重仓前)_rank', '买入 净利率(出持仓前)_rank', '卖出 净利率(出重仓前)_rank','卖出 净利率(出持仓前)_rank', '买入 PEG(出重仓前)_rank',
                         '买入 PEG(出持仓前)_rank', '卖出 PEG(出重仓前)_rank', '卖出 PEG(出持仓前)_rank', '买入 PCF(出重仓前)_rank','买入 PCF(出持仓前)_rank', '卖出 PCF(出重仓前)_rank', '卖出 PCF(出持仓前)_rank',
                         '买入 ROE-PB比例(出重仓前)_rank', '买入 ROE-PB比例(出持仓前)_rank', '卖出 ROE-PB比例(出重仓前)_rank','卖出 ROE-PB比例(出持仓前)_rank', '买入 PEG比例(出重仓前)_rank', '买入 PEG比例(出持仓前)_rank',
                         '卖出 PEG比例(出重仓前)_rank', '卖出 PEG比例(出持仓前)_rank','逆向买入比例(出持仓前)_rank',
                         '换手率','平均持有时间(出重仓前)', '平均持有时间(出持仓前)', '出重仓前平均收益率', '出全仓前平均收益率', '左侧概率(出重仓前,半年线)', '左侧概率(出持仓前,半年线)', '左侧概率(出重仓前,年线)',
                         '左侧概率(出持仓前,年线)', '左侧程度(出重仓前,半年线)','左侧程度(出持仓前,半年线)', '左侧程度(出重仓前,年线)', '左侧程度(出持仓前,年线)', '新股概率(出重仓前)', '新股概率(出持仓前)',
                         '次新股概率(出重仓前)', '次新股概率(出持仓前)', '买入 ROE(出重仓前)', '买入 ROE(出持仓前)','卖出 ROE(出重仓前)', '卖出 ROE(出持仓前)', '买入 净利润增速(出重仓前)',
                         '买入 净利润增速(出持仓前)', '卖出 净利润增速(出重仓前)', '卖出 净利润增速(出持仓前)', '买入 股息率(出重仓前)', '买入 股息率(出持仓前)', '卖出 股息率(出重仓前)',
                         '卖出 股息率(出持仓前)', '买入 PE(出重仓前)', '买入 PE(出持仓前)', '卖出 PE(出重仓前)', '卖出 PE(出持仓前)', '买入 PB(出重仓前)', '买入 PB(出持仓前)', '卖出 PB(出重仓前)',
                         '卖出 PB(出持仓前)', '买入 毛利率(出重仓前)', '买入 毛利率(出持仓前)', '卖出 毛利率(出重仓前)', '卖出 毛利率(出持仓前)', '买入 净利率(出重仓前)', '买入 净利率(出持仓前)', '卖出 净利率(出重仓前)','卖出 净利率(出持仓前)',
                         '买入 PEG(出重仓前)', '买入 PEG(出持仓前)', '卖出 PEG(出重仓前)', '卖出 PEG(出持仓前)', '买入 PCF(出重仓前)', '买入 PCF(出持仓前)', '卖出 PCF(出重仓前)',
                         '卖出 PCF(出持仓前)','买入 ROE-PB比例(出重仓前)', '买入 ROE-PB比例(出持仓前)', '卖出 ROE-PB比例(出重仓前)', '卖出 ROE-PB比例(出持仓前)', '买入 PEG比例(出重仓前)',
                         '买入 PEG比例(出持仓前)','卖出 PEG比例(出重仓前)', '卖出 PEG比例(出持仓前)','逆向买入比例(出持仓前)','baotuan_ratio',
                         'asofdate'
                         ]]

    sql="delete from jjpic_stock_p where asofdate='{}'".format(stock_p['asofdate'][0])
    localdb.execute(sql)
    stock_p.to_sql("jjpic_stock_p",con=localdb,index=False,if_exists='append')

    sql="delete from jjpic_stock_tp where asofdate='{}'".format(stock_tp['asofdate'][0])
    localdb.execute(sql)
    stock_tp.to_sql("jjpic_stock_tp", con=localdb, index=False, if_exists='append')
def save_entire_manangerpic2db(asofdate,th1=0.5, th2=0.5,th11=0.75,
                          th12=0.25, th3=0.5, th4=0.5, th5=0.75, th6=0.5,if_prv=False,fre='Q'):


    if(if_prv):

        if(fre=='M'):
            fre_table='_monthly'
        else:
            fre_table=''
        property_table='hbs_prv_industry_property{}_new'.format(fre_table)
        industry_level_table = 'hbs_prv_industry_property{}'.format(fre_table)
        ind_shift_property_table='hbs_prv_industry_shift_property'
        theme_shift_property_table='hbs_prv_theme_shift_property'
        ind_property_pic_table='jjpic_prv_industry_p{}'.format(fre_table)
        ind_shift_pic_table='jjpic_prv_industry_sp{}'.format(fre_table)
        theme_property_pic_table='jjpic_prv_theme_p{}'.format(fre_table)
        theme_shift_pic_table='jjpic_prv_theme_sp{}'.format(fre_table)
        industry_level_pic_table = 'jjpic_prv_industry_detail{}'.format(fre_table)
    else:
        ind_property_pic_table='jjpic_industry_p'
        ind_shift_pic_table='jjpic_industry_sp'
        theme_property_pic_table='jjpic_theme_p'
        theme_shift_pic_table='jjpic_theme_sp'
        industry_level_pic_table='jjpic_industry_detail'
        style_pic_table='jjpic_value_p_hbs'
        size_pic_table='jjpic_size_p_hbs'
        stock_pic_table='jjpic_stock_p'
        stock_trading_pic_table='jjpic_stock_tp'

    sql="select * from {0} where asofdate<='{1}'  ".format(ind_property_pic_table,asofdate)
    ind_pic=pd.read_sql(sql,con=localdb)

    sql="select * from {0} where asofdate<='{1}'  ".format(theme_property_pic_table,asofdate)
    themepic=pd.read_sql(sql,con=localdb)

    # sql="select * from {0}  ".format(ind_shift_pic_table)
    # jjpic_indsp=pd.read_sql(sql,con=localdb)

    # sql="select * from {0}  ".format(theme_shift_pic_table)
    # themesp_pic=pd.read_sql(sql,con=localdb)

    sql="select * from {0} where asofdate<='{1}' ".format(style_pic_table,asofdate)
    style_pic=pd.read_sql(sql,con=localdb)

    sql="select * from {0} where asofdate<='{1}' ".format(size_pic_table,asofdate)
    size_pic=pd.read_sql(sql,con=localdb)

    sql="select * from {0} where asofdate<='{1}' ".format(stock_pic_table,asofdate)
    stock_pic=pd.read_sql(sql,con=localdb)

    sql="select * from {0} where asofdate<='{1}' ".format(stock_trading_pic_table,asofdate)
    stock_trading_pic=pd.read_sql(sql,con=localdb)

    ind_pic['asofdate']=ind_pic['asofdate'].astype(str)
    asofdate_list1=ind_pic['asofdate'].unique().tolist()
    asofdate_list2 = stock_pic['asofdate'].unique().tolist()
    asofdate_list1.sort()
    asofdate_list2.sort()

    date_map=dict(zip(asofdate_list1,asofdate_list2))
    ind_pic['asofdate'] = [date_map[x] for x in ind_pic['asofdate']]
    themepic['asofdate'] = [date_map[x] for x in themepic['asofdate']]

    jjpic=pd.merge(ind_pic,themepic.drop('基金简称',axis=1),how='left',on=['jjdm','asofdate'])
    for df in [style_pic,size_pic,stock_pic,stock_trading_pic]:
        jjpic = pd.merge(jjpic, df.drop('基金简称', axis=1), how='left', on=['jjdm', 'asofdate'])

    float_col=[ '一级行业集中度','一级行业换手率',  '龙头占比(时序均值)', '龙头占比(时序中位数)', '龙头占比(时序均值)排名',
       '龙头占比(时序中位数)排名',  '二级行业集中度', '二级行业换手率',  '三级行业集中度',
       '三级行业换手率','主题集中度', '主题换手率','集中度(持仓)_x', '换手率(持仓)_x', '成长绝对暴露(持仓)', '价值绝对暴露(持仓)',
                '集中度(持仓)_y', '换手率(持仓)_y', '大盘绝对暴露(持仓)', '中小盘绝对暴露(持仓)'
        ,'个股集中度', 'hhi', '持股数量', '前三大', '前五大', '前十大', '平均仓位', '仓位换手率','换手率_rank'
        ,'平均持有时间(出重仓前)', '平均持有时间(出持仓前)', '出重仓前平均收益率', '出全仓前平均收益率', '换手率'
        ,'左侧概率(出重仓前,半年线)', '左侧概率(出持仓前,半年线)', '左侧概率(出重仓前,年线)', '左侧概率(出持仓前,年线)'
        , '左侧程度(出重仓前,半年线)', '左侧程度(出持仓前,半年线)', '左侧程度(出重仓前,年线)', '左侧程度(出持仓前,年线)', '新股概率(出重仓前)'
        ,'新股概率(出持仓前)', '次新股概率(出重仓前)', '次新股概率(出持仓前)']

    sql="select jjdm,ryxm,rydm,rzrq,lrrq from st_fund.t_st_gm_jjjl where jjdm in ({0}) and ryzw='基金经理'"\
        .format(util.list_sql_condition(jjpic['jjdm'].unique().tolist()))
    manager_info=hbdb.db2df(sql,db='funduser')

    manager_info=manager_info[manager_info['lrrq']>=20171231]
    manager_info.reset_index(drop=True,inplace=True)

    jjpic['asofdate']=jjpic['asofdate'].astype(int)
    asofdate_list=np.array(jjpic['asofdate'].unique().tolist())

    manager_pic=\
        manager_info.drop_duplicates('rydm')[['rydm','ryxm']].set_index('rydm').rename(columns={'ryxm':'基金经理'})

    today=\
        str(datetime.datetime.today())[0:10].replace('-','')
    #30715366
    for rydm in manager_pic.index.tolist():
        test = manager_info[manager_info['rydm'] == rydm].sort_values('rzrq')
        test['asofdate']=[asofdate_list[asofdate_list<=x].max() for x in test['lrrq']]
        test['lrrq'] = test['lrrq'].astype(int).astype(str).str.replace('29991231',today)

        for i in test.index:
            test.loc[i,'covered_date']=np.min([ (datetime.datetime.strptime(str(test.loc[i]['lrrq']), '%Y%m%d')-\
                                       datetime.datetime.strptime(str(test.loc[i]['rzrq']), '%Y%m%d')).days/365/3,1])

        test=pd.merge(test,jjpic[['jjdm','asofdate']+float_col]
                      ,how='left',on=['jjdm','asofdate'])
        test=test[test['一级行业集中度'].notnull()]
        for col in float_col:
            test[col]=test[col]*test['covered_date']
        test=pd.merge(test.groupby('asofdate').sum(),test.groupby('asofdate')['covered_date'].max().to_frame('max_date')
                      ,how='left',on='asofdate')
        for col in float_col:
            test[col]=test[col]/test['covered_date']*test['max_date']
            manager_pic.loc[rydm,col]=test[col].sum(axis=0)/test['max_date'].sum(axis=0)



    # generate the label:
    manager_pic['一级行业类型']='配置'
    manager_pic['二级行业类型'] = '配置'
    manager_pic['三级行业类型'] = '配置'
    manager_pic['主题类型'] = '配置'
    for class_lv in ['一级行业','二级行业','三级行业','主题']:
        manager_pic.loc[(manager_pic[class_lv+'集中度']>th1)
                       &(manager_pic[class_lv+'换手率'] > th2),class_lv+'类型']='博弈'
        manager_pic.loc[(manager_pic[class_lv+'集中度']>th1)
                       &(manager_pic[class_lv+'换手率'] < th2),class_lv+'类型']='专注'
        manager_pic.loc[(manager_pic[class_lv+'集中度']<th1)
                       &(manager_pic[class_lv+'换手率'] > th2),class_lv+'类型']='轮动'
        manager_pic.loc[(manager_pic[class_lv+'集中度']<th1)
                       &(manager_pic[class_lv+'换手率'] < th2),class_lv+'类型']='配置'


    def label_style(df, cen_col, shift_col, style_col, bias_col, th1, th2):

        from sklearn.cluster import KMeans
        # from sklearn import metrics
        n_clusters = 4
        df[style_col] = \
            KMeans(n_clusters=n_clusters).fit_predict(df[[cen_col, shift_col]].fillna(0).values)
        # plot.plotly_markers(df.pivot_table('集中度','换手率','风格类型'), 'asdf')
        type_dict=\
            df[[cen_col, shift_col,style_col]].groupby(style_col).median()[[cen_col, shift_col]].rank()

        type_dict.loc[(type_dict[cen_col] > 2) & (type_dict[shift_col] > 2), style_col]= '博弈'
        type_dict.loc[(type_dict[cen_col] > 2) & (type_dict[shift_col] <= 2), style_col]= '专注'
        type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] > 2), style_col]= '轮动'
        type_dict.loc[(type_dict[cen_col] <= 2) & (type_dict[shift_col] <= 2), style_col]= '配置'

        df[style_col]=[type_dict.loc[x][style_col] for x in df[style_col]]
        df.loc[df[style_col].isin(['配置','轮动']),bias_col] = '均衡'
        df.loc[df[style_col].isin(['专注', '博弈']), bias_col] =df[df[style_col].isin(['专注', '博弈'])]['winning_value']

        # df.loc[(df[cen_col] > th1) & (df[shift_col] > th2), style_col] = '博弈'
        # df.loc[(df[cen_col] > th1) & (df[shift_col] > th2), bias_col] = \
        #     df.loc[(df[cen_col] > th1) & (df[shift_col] > th2)]['winning_value']
        #
        # df.loc[(df[cen_col] > th1) & (df[shift_col] < th2), style_col] = '专注'
        # df.loc[(df[cen_col] > th1) & (df[shift_col] < th2), bias_col] = \
        #     df.loc[(df[cen_col] > th1) & (df[shift_col] < th2)]['winning_value']
        #
        # df.loc[(df[cen_col] < th1) & (df[shift_col] > th2), style_col] = '轮动'
        # df.loc[(df[cen_col] < th1) & (df[shift_col] > th2), bias_col] = '均衡'
        #
        # df.loc[(df[cen_col] < th1) & (df[shift_col] < th2), style_col] = '配置'
        # df.loc[(df[cen_col] < th1) & (df[shift_col] < th2), bias_col] = '均衡'
        #
        #
        # df.loc[(df[cen_col] > th1) & (df[shift_col] > th2), style_col] = '博弈'
        # df.loc[(df[cen_col] > th1) & (df[shift_col] > th2), bias_col] = \
        #     df.loc[(df[cen_col] > th1) & (df[shift_col] > th2)]['winning_value']
        #
        # df.loc[(df[cen_col] > th1) & (df[shift_col] < th2), style_col] = '专注'
        # df.loc[(df[cen_col] > th1) & (df[shift_col] < th2), bias_col] = \
        #     df.loc[(df[cen_col] > th1) & (df[shift_col] < th2)]['winning_value']
        #
        # df.loc[(df[cen_col] < th1) & (df[shift_col] > th2), style_col] = '轮动'
        # df.loc[(df[cen_col] < th1) & (df[shift_col] > th2), bias_col] = '均衡'
        #
        # df.loc[(df[cen_col] < th1) & (df[shift_col] < th2), style_col] = '配置'
        # df.loc[(df[cen_col] < th1) & (df[shift_col] < th2), bias_col] = '均衡'

        return df.drop('winning_value', axis=1)


    manager_pic['max']=manager_pic[['成长绝对暴露(持仓)', '价值绝对暴露(持仓)']].max(axis=1)
    manager_pic.loc[manager_pic['成长绝对暴露(持仓)']==manager_pic['max'],'winning_value']='成长'
    manager_pic.loc[manager_pic['价值绝对暴露(持仓)'] == manager_pic['max'], 'winning_value'] = '价值'
    manager_pic.drop('max', axis=1, inplace=True)


    manager_pic = label_style(manager_pic, '集中度(持仓)_x','换手率(持仓)_x',
                              '风格类型','风格偏好',th1,th2)

    #modify the jj style ticker by its real style weight, if any weight bigger than 50%,then put the style ticker

    manager_pic['成长暴露排名(持仓)']=manager_pic['成长绝对暴露(持仓)'].rank()/manager_pic['成长绝对暴露(持仓)'].rank().max()
    manager_pic['价值暴露排名(持仓)'] = manager_pic['价值绝对暴露(持仓)'].rank() / manager_pic[
        '价值绝对暴露(持仓)'].rank().max()

    manager_pic['均衡绝对暴露(持仓)']=1-manager_pic[ ['成长绝对暴露(持仓)','价值绝对暴露(持仓)']].sum(axis=1)
    manager_pic.loc[(manager_pic['风格偏好'] != '均衡')
                    & (manager_pic[ '均衡绝对暴露(持仓)'] >= 0.7), '风格偏好'] = '均衡'

    manager_pic.loc[(manager_pic['风格偏好'] != '成长')
                    & (manager_pic['均衡绝对暴露(持仓)']  < 0.7)
                    & (manager_pic['成长绝对暴露(持仓)']> manager_pic['价值绝对暴露(持仓)'])
                    &(manager_pic['成长暴露排名(持仓)']  >= 0.8), '风格偏好'] = '成长'

    manager_pic.loc[(manager_pic['风格偏好'] != '价值')
                    & (manager_pic['均衡绝对暴露(持仓)']  < 0.7)
                    & (manager_pic['成长绝对暴露(持仓)']/manager_pic['价值绝对暴露(持仓)']<=6/4)&
                    (manager_pic['价值暴露排名(持仓)']  >= 0.8), '风格偏好'] = '价值'

    # generate the label for hbs based :
    manager_pic['max']=manager_pic[['大盘绝对暴露(持仓)', '中小盘绝对暴露(持仓)']].max(axis=1)
    manager_pic.loc[manager_pic['大盘绝对暴露(持仓)']==manager_pic['max'],'winning_value']='大盘'
    manager_pic.loc[manager_pic['中小盘绝对暴露(持仓)'] == manager_pic['max'], 'winning_value'] = '中小盘'

    # size_p_hbs['winning_value'] = ''
    # size_p_hbs.loc[size_p_hbs['大盘绝对暴露(持仓)'] > 0.45, 'winning_value'] = size_p_hbs.loc[size_p_hbs['大盘绝对暴露(持仓)'] > 0.45]['winning_value'] + '大'
    # size_p_hbs.loc[size_p_hbs['中盘绝对暴露(持仓)'] > 0.45, 'winning_value'] = size_p_hbs.loc[size_p_hbs['中盘绝对暴露(持仓)'] > 0.45]['winning_value'] + '中'
    # size_p_hbs.loc[size_p_hbs['小盘绝对暴露(持仓)'] > 0.45, 'winning_value'] = size_p_hbs.loc[size_p_hbs['小盘绝对暴露(持仓)'] > 0.45]['winning_value'] + '小'
    # size_p_hbs.loc[size_p_hbs['winning_value']=='','winning_value']=size_p_hbs.loc[size_p_hbs['winning_value']==''][['大盘绝对暴露(持仓)','中盘绝对暴露(持仓)','小盘绝对暴露(持仓)']].idxmax(axis=1).astype(str).str[0]

    manager_pic = label_style(manager_pic, '集中度(持仓)_y', '换手率(持仓)_y',
                             '规模风格类型', '规模偏好', th1, th2)
    for col in ['大盘', '中小盘']:
        manager_pic.loc[(manager_pic['规模偏好'] == '均衡') & (manager_pic[col+'绝对暴露(持仓)'] >= 0.7), '规模偏好'] = col



    manager_pic['个股风格A'] = '无'
    manager_pic['个股风格B'] = '无'
    manager_pic['是否有尾仓(针对高个股集中基金)'] = '无尾仓'
    manager_pic['左侧标签'] = '无'
    manager_pic['新股次新股偏好']= ''

    manager_pic['左侧概率(出持仓前,半年线)_rank']=\
        manager_pic['左侧概率(出持仓前,半年线)'].rank()/manager_pic['左侧概率(出持仓前,半年线)'].rank().max()
    manager_pic['新股概率(出持仓前)_rank']=\
        manager_pic['新股概率(出持仓前)'].rank()/manager_pic['新股概率(出持仓前)'].rank().max()
    manager_pic['次新股概率(出持仓前)_rank']=\
        manager_pic['次新股概率(出持仓前)'].rank()/manager_pic['次新股概率(出持仓前)'].rank().max()

    manager_pic.loc[(manager_pic['个股集中度']>th11)&(manager_pic['换手率_rank'] < th11),
                '个股风格A']='专注'
    manager_pic.loc[(manager_pic['个股集中度']>th11)&(manager_pic['换手率_rank'] > th12),
                '个股风格A']='博弈'
    manager_pic.loc[(manager_pic['个股集中度']<th12)&(manager_pic['换手率_rank'] < th11),
                '个股风格A']='配置'
    manager_pic.loc[(manager_pic['个股集中度']<th12)&(manager_pic['换手率_rank'] > th12),
                '个股风格A']='轮动'
    manager_pic.loc[(manager_pic['个股集中度'] > th11)
                & (manager_pic['一级行业集中度'] < th6),'个股风格B']='自下而上'
    manager_pic.loc[(manager_pic['个股集中度'] < th6)
                & (manager_pic['一级行业集中度'] > th11),'个股风格B']='自上而上'
    manager_pic.loc[(manager_pic['个股集中度'] > th11)
                & (manager_pic['个股集中度'] - manager_pic['hhi'] > 0.05),'是否有尾仓(针对高个股集中基金)']='有尾仓'
    manager_pic.loc[(manager_pic['左侧概率(出持仓前,半年线)_rank'] > th3)
                 & (manager_pic['左侧程度(出持仓前,半年线)'] > th4),'左侧标签']='深度左侧'
    manager_pic.loc[(manager_pic['左侧概率(出持仓前,半年线)_rank'] > th3)
                 & (manager_pic['左侧程度(出持仓前,半年线)'] < th4),'左侧标签']='左侧'

    manager_pic.loc[(manager_pic['新股概率(出持仓前)_rank'] > th5),'新股次新股偏好']=\
        manager_pic[(manager_pic['新股概率(出持仓前)_rank'] > th5)]['新股次新股偏好']+'偏好新股'
    manager_pic.loc[(manager_pic['次新股概率(出持仓前)_rank'] > th5),'新股次新股偏好']=\
        manager_pic[(manager_pic['次新股概率(出持仓前)_rank'] > th5)]['新股次新股偏好']+'偏好次新股'
    manager_pic.loc[manager_pic['新股次新股偏好'] == '','新股次新股偏好']='无'

    manager_pic['asofdate']=asofdate_list2[-1]
    sql="delete from manager_pic where asofdate='{}'".format(manager_pic['asofdate'].iloc[0])
    localdb.execute(sql,con=localdb)
    manager_pic.reset_index(drop=False).to_sql('manager_pic',con=localdb,if_exists='append',index=False)

def save_entire_jjpic2db(asofdate1,asofdate2,if_prv=False,fre='Q'):

    print(asofdate1)
    if(if_prv):
        jj_base_info = hbdb.db2df("select jjdm,jjjc from st_hedge.t_st_jjxx",db='highuser')
    else:
        jj_base_info = hbdb.db2df("select jjdm,jjjc from st_fund.t_st_gm_jjxx", db='funduser')
    #industry_pic_all(jj_base_info,asofdate1,asofdate2,if_prv=if_prv,fre=fre)
    #stock_trading_pci_all(jj_base_info,asofdate2,asofdate1,if_percentage=False)
    style_pic_all(jj_base_info,asofdate2,fre='M', if_percentage=False,if_prv=if_prv,fre2=fre)

def save_pic_as_excelfromlocaldb(asofdate,jjdm_list=None,if_trade_history=True):

    import xlwings as xw

    if(jjdm_list is not None):
        jjdm_con="jjdm in ({})".format(util.list_sql_condition(jjdm_list))
    else:
        jjdm_con='1=1'


    value_p, value_p_hbs, value_sp, value_sp_hbs, size_p, size_p_hbs, size_sp, size_sp_hbs, \
    industry_p, industry_sp, theme_p, theme_sp, industry_detail_df_list, stock_p, stock_tp,\
    jj_performance,industry_contribution_list,ticker_con,theme_exp,ind2_exp\
        ,industry_contribution_perweight_list,style_exp,size_exp= \
        get_pic_from_localdb(jjdm_con,asofdate=asofdate)


    filename=r"E:\GitFolder\docs\池报告模板.xlsx"
    app = xw.App(visible=False)
    wb =app.books.open(filename)

    df_list=[industry_p, industry_sp, theme_p, theme_sp,
               industry_detail_df_list[0],industry_detail_df_list[1],industry_detail_df_list[2],
               value_p_hbs, value_sp_hbs, value_p, value_sp, size_p_hbs, size_sp_hbs, size_p, size_sp,
               stock_p,stock_tp,jj_performance,industry_contribution_list[0],
             industry_contribution_list[1],industry_contribution_list[2],ticker_con
        ,industry_contribution_perweight_list[0],industry_contribution_perweight_list[1],industry_contribution_perweight_list[2]]

    sheet_list=['行业画像','行业切换属性','主题画像','主题切换属性','细分行业画像_一级','细分行业画像_二级','细分行业画像_三级',
                '成长价值画像_基于持仓','成长价值切换属性_基于持仓','成长价值画像_基于净值','成长价值切换属性_基于净值',
                '大中小盘画像_基于持仓','大中小盘切换属性_基于持仓','大中小盘画像_基于净值','大中小盘切换属性_基于净值',
                '个股特征画像A','个股特征画像B','基金业绩画像','一级行业贡献','二级行业贡献','三级行业贡献','个股贡献'
        ,'一级行业单位贡献','二级行业单位贡献','三级行业单位贡献']

    newpath = r'E:\GitFolder\docs\私募股多持仓分析\pic_temp'
    ws = wb.sheets['主题画像']

    for pic in ws.pictures:
        pic.delete()
    upper_range =100
    x_position=len(theme_p)+3
    for jjjc in theme_exp['基金简称'].unique():
        data, layout = plot.plotly_area(100 * theme_exp[theme_exp['基金简称']==jjjc].set_index('jsrq').drop('基金简称',axis=1).T,
                                        '{}主题暴露时序'.format(jjjc), upper_range)
        plot.save_pic2local(data, layout, newpath + r"\{}主题暴露时序".format(jjjc))
        ws.pictures.add(newpath + r"\{}主题暴露时序.png".format(jjjc), left=ws.range('A{}'.format(int(x_position))).left, top=ws.range('A{}'.format(int(x_position))).top,
                        width=700, height=350)

        x_position+=30

    ws = wb.sheets['行业画像']
    x_position_list = ['A', 'O', 'AC', 'AQ', 'BE']
    ind2_exp['yjxymc']=[ind_map[x] for x in ind2_exp['ejxymc']]
    for pic in ws.pictures:
        pic.delete()
    x_position=len(theme_p)+3
    for jjjc in theme_exp['基金简称'].unique():
        i = 0
        top5_inds=industry_p.loc[industry_p['基金简称']==jjjc]['前五大行业'].values[0].split(',')
        for inds in top5_inds:
            upper_range =1.2 * ind2_exp.groupby(['基金简称','yjxymc','jsrq']).sum().loc[jjjc,inds.replace("'","")].max().values[0]
            data, layout = plot.plotly_area( (ind2_exp[(ind2_exp['基金简称']==jjjc)
                                                           &(ind2_exp['yjxymc']==inds.replace("'",""))]).pivot_table('zjbl','jsrq','ejxymc').fillna(0).T,
                                            '{0}_{1}_二级行业暴露时序'.format(jjjc,inds.replace("'","")), upper_range)
            plot.save_pic2local(data, layout, newpath + r"\{}二级行业暴露时序".format(jjjc))
            ws.pictures.add(newpath + r"\{}二级行业暴露时序.png".format(jjjc), left=ws.range('{0}{1}'
                                                                                     .format(x_position_list[i],int(x_position))).left, top=ws.range('{0}{1}'
                                                                                                                                                     .format(x_position_list[i],int(x_position))).top,
                            width=700, height=350)
            i+=1
        x_position += 30

    ws = wb.sheets['成长价值画像_基于持仓']
    for pic in ws.pictures:
        pic.delete()
    x_position=len(value_p_hbs)+3
    for jjjc in theme_exp['基金简称'].unique():
        data, layout = plot.plotly_area(style_exp[style_exp['基金简称']==jjjc].pivot_table('zjbl','jsrq','style_type').T,
                                        '{}风格暴露时序'.format(jjjc), 100)
        plot.save_pic2local(data, layout, newpath + r"\{}风格暴露时序".format(jjjc))
        ws.pictures.add(newpath + r"\{}风格暴露时序.png".format(jjjc), left=ws.range('A{0}'
                                                                               .format(int(x_position))).left
                        , top=ws.range('A{0}'.format(int(x_position))).top,width=700, height=350)

        x_position+=28

    ws = wb.sheets['大中小盘画像_基于持仓']
    for pic in ws.pictures:
        pic.delete()
    x_position=len(size_p_hbs)+3
    for jjjc in theme_exp['基金简称'].unique():
        data, layout = plot.plotly_area(size_exp[size_exp['基金简称']==jjjc].pivot_table('zjbl','jsrq','size_type').T,
                                        '{}规模暴露时序'.format(jjjc), 100)
        plot.save_pic2local(data, layout, newpath + r"\{}规模暴露时序".format(jjjc))
        ws.pictures.add(newpath + r"\{}规模暴露时序.png".format(jjjc), left=ws.range('A{0}'
                                                                               .format(int(x_position))).left
                        , top=ws.range('A{0}'.format(int(x_position))).top,width=700, height=350)

        x_position+=28



    ws = wb.sheets['前十大交易时序']
    ws.clear()
    for pic in ws.pictures:
        pic.delete()

    if(if_trade_history):


        #get the top10 ticker adjusted trade history
        sql="select * from hbs_hld_sl_history where {0} and asofdate='{1}'"\
            .format(jjdm_con,value_p_hbs['asofdate'].unique()[0])
        trade_history=pd.read_sql(sql,con=localdb)
        trade_history=trade_history.sort_values(['jjdm', 'zqdm', 'trade_date'])
        trade_history[['ROE_yj',
           'NETPROFITGROWRATE_yj', 'OPERATINGREVENUEYOY_yj','EST_NET_PROFIT_YOY_yj', 'EST_OPER_REVENUE_YOY_yj', 'ROE_FY1_yj', 'ROE_ej', 'NETPROFITGROWRATE_ej',
           'OPERATINGREVENUEYOY_ej', 'EST_NET_PROFIT_YOY_ej', 'EST_OPER_REVENUE_YOY_ej', 'ROE_FY1_ej','ROE_sj',
           'NETPROFITGROWRATE_sj', 'OPERATINGREVENUEYOY_sj','EST_NET_PROFIT_YOY_sj', 'EST_OPER_REVENUE_YOY_sj', 'ROE_FY1_sj', 'ROE_ticker',
           'NETPROFITGROWRATE_ticker', 'OPERATINGREVENUEYOY_ticker', 'ROE_FY1_ticker',
           'EST_NET_PROFIT_YOY_ticker', 'EST_OPER_REVENUE_YOY_ticker'
           ]]=trade_history[['ROE_yj',
           'NETPROFITGROWRATE_yj', 'OPERATINGREVENUEYOY_yj','EST_NET_PROFIT_YOY_yj', 'EST_OPER_REVENUE_YOY_yj', 'ROE_FY1_yj', 'ROE_ej', 'NETPROFITGROWRATE_ej',
           'OPERATINGREVENUEYOY_ej', 'EST_NET_PROFIT_YOY_ej', 'EST_OPER_REVENUE_YOY_ej', 'ROE_FY1_ej','ROE_sj',
           'NETPROFITGROWRATE_sj', 'OPERATINGREVENUEYOY_sj','EST_NET_PROFIT_YOY_sj', 'EST_OPER_REVENUE_YOY_sj', 'ROE_FY1_sj', 'ROE_ticker',
           'NETPROFITGROWRATE_ticker', 'OPERATINGREVENUEYOY_ticker', 'ROE_FY1_ticker',
           'EST_NET_PROFIT_YOY_ticker', 'EST_OPER_REVENUE_YOY_ticker'
           ]]/100
        trade_history['ajduested_sl_change']=\
            trade_history[['jjdm','zqdm','adjuested_sl']].groupby(['jjdm','zqdm']).pct_change().fillna(0)

        y_position=0
        x_position_list=['A','O','AC','AQ','BE']

        for jjdm in jjdm_list:
            print(jjdm)
            tempdf=trade_history[trade_history['jjdm']==jjdm]
            tempdf['zqdm'] = [("000000" + str(x))[-6:] for x in tempdf['zqdm']]
            top10_tickers=tempdf['zqdm'].unique().tolist()


            #calculate the sl change weight in all positive or negative change :
            tempdf=pd.concat([pd.merge(tempdf[tempdf['ajduested_sl_change'] > 0],
                            tempdf[tempdf['ajduested_sl_change'] > 0].groupby('zqdm').sum()['ajduested_sl_change'].to_frame('sumed_change_by_ticker'),how='left',on='zqdm'),
                              pd.merge(tempdf[tempdf['ajduested_sl_change'] < 0],
                                       tempdf[tempdf['ajduested_sl_change'] < 0].groupby('zqdm').sum()[
                                           'ajduested_sl_change'].to_frame('sumed_change_by_ticker'), how='left', on='zqdm'),
                              tempdf[tempdf['ajduested_sl_change']==0]
                              ],axis=0)

            tempdf=tempdf.sort_values(['jjdm', 'zqdm', 'trade_date']).reset_index(drop=True)
            tempdf['sl_change_weight']=0

            tempdf.loc[tempdf['ajduested_sl_change'] > 0,'sl_change_weight']=\
                tempdf[tempdf['ajduested_sl_change'] > 0]['ajduested_sl_change']/\
                tempdf[tempdf['ajduested_sl_change'] > 0]['sumed_change_by_ticker']
            tempdf.loc[tempdf['ajduested_sl_change'] < 0,'sl_change_weight']=\
                tempdf[tempdf['ajduested_sl_change'] < 0]['ajduested_sl_change']/\
                tempdf[tempdf['ajduested_sl_change'] < 0]['sumed_change_by_ticker']
            #calculated the weighed average buy and sell timing financial stats
            financial_col=[ 'ROE_yj',
           'NETPROFITGROWRATE_yj', 'OPERATINGREVENUEYOY_yj', 'PE_yj', 'PEG_yj',
           'EST_NET_PROFIT_YOY_yj', 'EST_OPER_REVENUE_YOY_yj', 'ROE_FY1_yj',
           'PE_FY1_yj', 'PEG_FY1_yj', 'ROE_rank_yj', 'NETPROFITGROWRATE_rank_yj',
           'OPERATINGREVENUEYOY_rank_yj', 'PE_rank_yj', 'PEG_rank_yj',
           'EST_NET_PROFIT_YOY_rank_yj', 'EST_OPER_REVENUE_YOY_rank_yj',
           'ROE_FY1_rank_yj', 'PE_FY1_rank_yj', 'PEG_FY1_rank_yj', 'ROE_ej',
           'NETPROFITGROWRATE_ej', 'OPERATINGREVENUEYOY_ej', 'PE_ej', 'PEG_ej',
           'EST_NET_PROFIT_YOY_ej', 'EST_OPER_REVENUE_YOY_ej', 'ROE_FY1_ej',
           'PE_FY1_ej', 'PEG_FY1_ej', 'ROE_rank_ej', 'NETPROFITGROWRATE_rank_ej',
           'OPERATINGREVENUEYOY_rank_ej', 'PE_rank_ej', 'PEG_rank_ej',
           'EST_NET_PROFIT_YOY_rank_ej', 'EST_OPER_REVENUE_YOY_rank_ej',
           'ROE_FY1_rank_ej', 'PE_FY1_rank_ej', 'PEG_FY1_rank_ej', 'ROE_sj',
           'NETPROFITGROWRATE_sj', 'OPERATINGREVENUEYOY_sj', 'PE_sj', 'PEG_sj',
           'EST_NET_PROFIT_YOY_sj', 'EST_OPER_REVENUE_YOY_sj', 'ROE_FY1_sj',
           'PE_FY1_sj', 'PEG_FY1_sj', 'ROE_rank_sj', 'NETPROFITGROWRATE_rank_sj',
           'OPERATINGREVENUEYOY_rank_sj', 'PE_rank_sj', 'PEG_rank_sj',
           'EST_NET_PROFIT_YOY_rank_sj', 'EST_OPER_REVENUE_YOY_rank_sj',
           'ROE_FY1_rank_sj', 'PE_FY1_rank_sj', 'PEG_FY1_rank_sj','ROE_ticker', 'NETPROFITGROWRATE_ticker',
           'OPERATINGREVENUEYOY_ticker', 'PE_ticker', 'PEG_ticker',
           'PE_FY1_ticker', 'PEG_FY1_ticker', 'ROE_FY1_ticker',
           'EST_NET_PROFIT_YOY_ticker', 'EST_OPER_REVENUE_YOY_ticker',
           'ROE_rank_ticker', 'NETPROFITGROWRATE_rank_ticker',
           'OPERATINGREVENUEYOY_rank_ticker', 'PE_rank_ticker', 'PEG_rank_ticker',
           'EST_NET_PROFIT_YOY_rank_ticker', 'EST_OPER_REVENUE_YOY_rank_ticker',
           'ROE_FY1_rank_ticker', 'PE_FY1_rank_ticker', 'PEG_FY1_rank_ticker']
            tempdf[[x + '_margin_change' for x in financial_col]]=tempdf.groupby(['jjdm','zqdm'])[financial_col].diff()
            financial_col=financial_col+[x + '_margin_change' for x in financial_col]
            for col in financial_col:
                tempdf[col+'_w']=tempdf[col]*tempdf['sl_change_weight']
            buy_timing=tempdf[tempdf['ajduested_sl_change'] > 0].groupby('zqdm').sum()[[x+'_w' for x in financial_col]+['sumed_change_by_ticker']].reset_index(drop=False)
            sell_timing=tempdf[tempdf['ajduested_sl_change'] < 0].groupby('zqdm').sum()[[x+'_w' for x in financial_col]+['sumed_change_by_ticker']].reset_index(drop=False)
            total_buy=0
            total_sell=0

            sell_timing.columns=['zqdm']+financial_col+['sumed_change_by_ticker']
            buy_timing.columns =['zqdm']+financial_col+['sumed_change_by_ticker']

            length_b=len(buy_timing)
            length_s = len(sell_timing)

            #get ticker chinese name
            sql="select zqdm,zqjc from st_ashare.t_st_ag_zqzb where zqdm in ({0}) and zqlb in (1,2)"\
                .format(util.list_sql_condition(top10_tickers))
            tempdf=pd.merge(tempdf,hbdb.db2df(sql,db='alluser'),how='left',on='zqdm')

            if(length_b>0):
                for n in range(length_b):
                    total_buy += buy_timing.iloc[n][financial_col] * buy_timing.iloc[n][
                                      'sumed_change_by_ticker']
                buy_timing.loc[length_b] = total_buy / buy_timing['sumed_change_by_ticker'].sum()
                buy_timing.loc[length_b, 'zqdm'] = '买入平均'
                buy_timing = pd.merge(buy_timing, hbdb.db2df(sql, db='alluser'), how='left', on='zqdm')
                buy_timing.loc[buy_timing['zqjc'].notnull(), 'zqdm'] = buy_timing['zqjc'] + '_买入'
            else:
                buy_timing=[]

            if (length_s > 0):
                for n in range(length_s):
                    total_sell += sell_timing.iloc[n][financial_col] * sell_timing.iloc[n][
                                      'sumed_change_by_ticker']


                sell_timing.loc[length_s] = total_sell / sell_timing['sumed_change_by_ticker'].sum()
                sell_timing.loc[length_s, 'zqdm'] = '平均卖出'
                sell_timing = pd.merge(sell_timing, hbdb.db2df(sql, db='alluser'), how='left', on='zqdm')
                sell_timing.loc[sell_timing['zqjc'].notnull(), 'zqdm'] = sell_timing['zqjc'] + '_卖出'
            else:
                sell_timing=[]

            trade_property=pd.concat([buy_timing, sell_timing], axis=0)
            trade_property.drop(['zqjc','sumed_change_by_ticker'],axis=1,inplace=True)

            tempdf.drop([x+'_w' for x in financial_col],axis=1,inplace=True)

            trade_property.columns=['证券简称', 'ROE_一级行业', '净利增速_一级行业', '主营收入增速_一级行业',
           'PE_一级行业', 'PEG_一级行业', '净利增速预期_一级行业', '主营收入增速预期_一级行业',
           'ROE预期_一级行业', 'PE预期_一级行业', 'PEG预期_一级行业', 'ROE_分位数_一级行业',
           '净利增速_分位数_一级行业', '主营收入增速_分位数_一级行业',
           'PE_分位数_一级行业', 'PEG_分位数_一级行业', '净利增速预期_分位数_一级行业',
           '主营收入增速预期_分位数_一级行业', 'ROE预期_分位数_一级行业', 'PE预期_分位数_一级行业',
           'PEG预期_分位数_一级行业', 'ROE_二级行业', '净利增速_二级行业',
           '主营收入增速_二级行业', 'PE_二级行业', 'PEG_二级行业', '净利增速预期_二级行业',
           '主营收入增速预期_二级行业', 'ROE预期_二级行业', 'PE预期_二级行业', 'PEG预期_二级行业',
           'ROE_分位数_二级行业', '净利增速_分位数_二级行业',
           '主营收入增速_分位数_二级行业', 'PE_分位数_二级行业', 'PEG_分位数_二级行业',
           '净利增速预期_分位数_二级行业', '主营收入增速预期_分位数_二级行业',
           'ROE预期_分位数_二级行业', 'PE预期_分位数_二级行业', 'PEG预期_分位数_二级行业', 'ROE_三级行业',
           '净利增速_三级行业', '主营收入增速_三级行业', 'PE_三级行业', 'PEG_三级行业',
           '净利增速预期_三级行业', '主营收入增速预期_三级行业', 'ROE预期_三级行业',
           'PE预期_三级行业', 'PEG预期_三级行业', 'ROE_分位数_三级行业', '净利增速_分位数_三级行业',
           '主营收入增速_分位数_三级行业', 'PE_分位数_三级行业', 'PEG_分位数_三级行业',
           '净利增速预期_分位数_三级行业', '主营收入增速预期_分位数_三级行业',
           'ROE预期_分位数_三级行业', 'PE预期_分位数_三级行业', 'PEG预期_分位数_三级行业', 'ROE_个股',
           '净利增速_个股', '主营收入增速_个股', 'PE_个股',
           'PEG_个股', 'PE预期_个股', 'PEG预期_个股', 'ROE预期_个股',
           '净利增速预期_个股', '主营收入增速预期_个股',
           'ROE_分位数_个股', '净利增速_分位数_个股',
           '主营收入增速_分位数_个股', 'PE_分位数_个股', 'PEG_分位数_个股',
           '净利增速预期_分位数_个股', '主营收入增速预期_分位数_个股',
           'ROE预期_分位数_个股', 'PE预期_分位数_个股', 'PEG预期_分位数_个股','ROE_一级行业_边际变动', '净利增速_一级行业_边际变动', '主营收入增速_一级行业_边际变动',
           'PE_一级行业_边际变动', 'PEG_一级行业_边际变动', '净利增速预期_一级行业_边际变动', '主营收入增速预期_一级行业_边际变动',
           'ROE预期_一级行业_边际变动', 'PE预期_一级行业_边际变动', 'PEG预期_一级行业_边际变动', 'ROE_分位数_一级行业_边际变动',
           '净利增速_分位数_一级行业_边际变动', '主营收入增速_分位数_一级行业_边际变动',
           'PE_分位数_一级行业_边际变动', 'PEG_分位数_一级行业_边际变动', '净利增速预期_分位数_一级行业_边际变动',
           '主营收入增速预期_分位数_一级行业_边际变动', 'ROE预期_分位数_一级行业_边际变动', 'PE预期_分位数_一级行业_边际变动',
           'PEG预期_分位数_一级行业_边际变动', 'ROE_二级行业_边际变动', '净利增速_二级行业_边际变动',
           '主营收入增速_二级行业_边际变动', 'PE_二级行业_边际变动', 'PEG_二级行业_边际变动', '净利增速预期_二级行业_边际变动',
           '主营收入增速预期_二级行业_边际变动', 'ROE预期_二级行业_边际变动', 'PE预期_二级行业_边际变动', 'PEG预期_二级行业_边际变动',
           'ROE_分位数_二级行业_边际变动', '净利增速_分位数_二级行业_边际变动',
           '主营收入增速_分位数_二级行业_边际变动', 'PE_分位数_二级行业_边际变动', 'PEG_分位数_二级行业_边际变动',
           '净利增速预期_分位数_二级行业_边际变动', '主营收入增速预期_分位数_二级行业_边际变动',
           'ROE预期_分位数_二级行业_边际变动', 'PE预期_分位数_二级行业_边际变动', 'PEG预期_分位数_二级行业_边际变动', 'ROE_三级行业_边际变动',
           '净利增速_三级行业_边际变动', '主营收入增速_三级行业_边际变动', 'PE_三级行业_边际变动', 'PEG_三级行业_边际变动',
           '净利增速预期_三级行业_边际变动', '主营收入增速预期_三级行业_边际变动', 'ROE预期_三级行业_边际变动',
           'PE预期_三级行业_边际变动', 'PEG预期_三级行业_边际变动', 'ROE_分位数_三级行业_边际变动', '净利增速_分位数_三级行业_边际变动',
           '主营收入增速_分位数_三级行业_边际变动', 'PE_分位数_三级行业_边际变动', 'PEG_分位数_三级行业_边际变动',
           '净利增速预期_分位数_三级行业_边际变动', '主营收入增速预期_分位数_三级行业_边际变动',
           'ROE预期_分位数_三级行业_边际变动', 'PE预期_分位数_三级行业_边际变动', 'PEG预期_分位数_三级行业_边际变动', 'ROE_个股_边际变动',
           '净利增速_个股_边际变动', '主营收入增速_个股_边际变动', 'PE_个股_边际变动',
           'PEG_个股_边际变动', 'PE预期_个股_边际变动', 'PEG预期_个股_边际变动', 'ROE预期_个股_边际变动',
           '净利增速预期_个股_边际变动', '主营收入增速预期_个股_边际变动',
           'ROE_分位数_个股_边际变动', '净利增速_分位数_个股_边际变动',
           '主营收入增速_分位数_个股_边际变动', 'PE_分位数_个股_边际变动', 'PEG_分位数_个股_边际变动',
           '净利增速预期_分位数_个股_边际变动', '主营收入增速预期_分位数_个股_边际变动',
           'ROE预期_分位数_个股_边际变动', 'PE预期_分位数_个股_边际变动', 'PEG预期_分位数_个股_边际变动']
            trade_property['基金名称']=value_p_hbs[value_p_hbs['jjdm'] == jjdm]['基金简称'].values[0]
            trade_property=trade_property[['基金名称','证券简称','ROE_个股_边际变动',
           '净利增速_个股_边际变动', '主营收入增速_个股_边际变动', 'PE_个股_边际变动',
           'PEG_个股_边际变动', 'PE预期_个股_边际变动', 'PEG预期_个股_边际变动', 'ROE预期_个股_边际变动',
           '净利增速预期_个股_边际变动', '主营收入增速预期_个股_边际变动','ROE_二级行业_边际变动', '净利增速_二级行业_边际变动',
           '主营收入增速_二级行业_边际变动', 'PE_二级行业_边际变动', 'PEG_二级行业_边际变动', '净利增速预期_二级行业_边际变动',
           '主营收入增速预期_二级行业_边际变动', 'ROE预期_二级行业_边际变动', 'PE预期_二级行业_边际变动', 'PEG预期_二级行业_边际变动','ROE_三级行业_边际变动',
           '净利增速_三级行业_边际变动', '主营收入增速_三级行业_边际变动', 'PE_三级行业_边际变动', 'PEG_三级行业_边际变动',
           '净利增速预期_三级行业_边际变动', '主营收入增速预期_三级行业_边际变动', 'ROE预期_三级行业_边际变动',
           'PE预期_三级行业_边际变动', 'PEG预期_三级行业_边际变动', 'ROE_分位数_三级行业_边际变动', '净利增速_分位数_三级行业_边际变动',
           '主营收入增速_分位数_三级行业_边际变动', 'PE_分位数_三级行业_边际变动', 'PEG_分位数_三级行业_边际变动',
           '净利增速预期_分位数_三级行业_边际变动', '主营收入增速预期_分位数_三级行业_边际变动','ROE_分位数_个股_边际变动', '净利增速_分位数_个股_边际变动',
           '主营收入增速_分位数_个股_边际变动', 'PE_分位数_个股_边际变动', 'PEG_分位数_个股_边际变动',
           '净利增速预期_分位数_个股_边际变动', '主营收入增速预期_分位数_个股_边际变动',
           'ROE预期_分位数_个股_边际变动', 'PE预期_分位数_个股_边际变动', 'PEG预期_分位数_个股_边际变动','ROE_分位数_一级行业_边际变动',
           '净利增速_分位数_一级行业_边际变动', '主营收入增速_分位数_一级行业_边际变动',
           'PE_分位数_一级行业_边际变动', 'PEG_分位数_一级行业_边际变动', '净利增速预期_分位数_一级行业_边际变动',
           '主营收入增速预期_分位数_一级行业_边际变动', 'ROE预期_分位数_一级行业_边际变动', 'PE预期_分位数_一级行业_边际变动',
           'PEG预期_分位数_一级行业_边际变动', 'ROE_分位数_二级行业_边际变动', '净利增速_分位数_二级行业_边际变动',
           '主营收入增速_分位数_二级行业_边际变动', 'PE_分位数_二级行业_边际变动', 'PEG_分位数_二级行业_边际变动',
           '净利增速预期_分位数_二级行业_边际变动', '主营收入增速预期_分位数_二级行业_边际变动',
           'ROE预期_分位数_二级行业_边际变动', 'PE预期_分位数_二级行业_边际变动', 'PEG预期_分位数_二级行业_边际变动','ROE_分位数_三级行业_边际变动', '净利增速_分位数_三级行业_边际变动',
           '主营收入增速_分位数_三级行业_边际变动', 'PE_分位数_三级行业_边际变动', 'PEG_分位数_三级行业_边际变动',
           '净利增速预期_分位数_三级行业_边际变动', '主营收入增速预期_分位数_三级行业_边际变动',
           'ROE预期_分位数_三级行业_边际变动', 'PE预期_分位数_三级行业_边际变动', 'PEG预期_分位数_三级行业_边际变动','ROE_个股',
           '净利增速_个股', '主营收入增速_个股', 'PE_个股',
           'PEG_个股', 'PE预期_个股', 'PEG预期_个股', 'ROE预期_个股',
           '净利增速预期_个股', '主营收入增速预期_个股','ROE_二级行业', '净利增速_二级行业',
           '主营收入增速_二级行业', 'PE_二级行业', 'PEG_二级行业', '净利增速预期_二级行业',
           '主营收入增速预期_二级行业', 'ROE预期_二级行业', 'PE预期_二级行业', 'PEG预期_二级行业','ROE_三级行业',
           '净利增速_三级行业', '主营收入增速_三级行业', 'PE_三级行业', 'PEG_三级行业',
           '净利增速预期_三级行业', '主营收入增速预期_三级行业', 'ROE预期_三级行业',
           'PE预期_三级行业', 'PEG预期_三级行业', 'ROE_分位数_三级行业', '净利增速_分位数_三级行业',
           '主营收入增速_分位数_三级行业', 'PE_分位数_三级行业', 'PEG_分位数_三级行业',
           '净利增速预期_分位数_三级行业', '主营收入增速预期_分位数_三级行业','ROE_分位数_个股', '净利增速_分位数_个股',
           '主营收入增速_分位数_个股', 'PE_分位数_个股', 'PEG_分位数_个股',
           '净利增速预期_分位数_个股', '主营收入增速预期_分位数_个股',
           'ROE预期_分位数_个股', 'PE预期_分位数_个股', 'PEG预期_分位数_个股','ROE_分位数_一级行业',
           '净利增速_分位数_一级行业', '主营收入增速_分位数_一级行业',
           'PE_分位数_一级行业', 'PEG_分位数_一级行业', '净利增速预期_分位数_一级行业',
           '主营收入增速预期_分位数_一级行业', 'ROE预期_分位数_一级行业', 'PE预期_分位数_一级行业',
           'PEG预期_分位数_一级行业', 'ROE_分位数_二级行业', '净利增速_分位数_二级行业',
           '主营收入增速_分位数_二级行业', 'PE_分位数_二级行业', 'PEG_分位数_二级行业',
           '净利增速预期_分位数_二级行业', '主营收入增速预期_分位数_二级行业',
           'ROE预期_分位数_二级行业', 'PE预期_分位数_二级行业', 'PEG预期_分位数_二级行业','ROE_分位数_三级行业', '净利增速_分位数_三级行业',
           '主营收入增速_分位数_三级行业', 'PE_分位数_三级行业', 'PEG_分位数_三级行业',
           '净利增速预期_分位数_三级行业', '主营收入增速预期_分位数_三级行业',
           'ROE预期_分位数_三级行业', 'PE预期_分位数_三级行业', 'PEG预期_分位数_三级行业']]


            m = 0
            # get the stock price data
            sql = """
              select b.SecuCode as ZQDM,a.TradingDay as JYRQ,a.ClosePrice as SPJG from hsjy_gg.SecuMain b left join hsjy_gg.QT_PerformanceData a on a.InnerCode=b.InnerCode where b.SecuCode in ({0})  and a.TradingDay>=to_date('{1}','yyyymmdd') and  a.TradingDay<=to_date('{2}','yyyymmdd')
               """.format(util.list_sql_condition(top10_tickers),
                          str(int(trade_history['trade_date'].min())-100),
                          (datetime.datetime.strptime(trade_history['trade_date'].max(), '%Y%m%d')+datetime.timedelta(days=30)).strftime('%Y%m%d') )
            price_df = hbdb.db2df(sql, db='readonly')

            sql = """
              select b.SecuCode as ZQDM,a.TradingDay as JYRQ,a.BackwardPrice as SPJG from hsjy_gg.SecuMain b left join hsjy_gg.LC_STIBPerformanceData a on a.InnerCode=b.InnerCode where b.SecuCode in ({0})  and a.TradingDay>=to_date('{1}','yyyymmdd') and  a.TradingDay<=to_date('{2}','yyyymmdd')
               """.format(util.list_sql_condition(top10_tickers),
                          str(int(trade_history['trade_date'].min())-100),
                          (datetime.datetime.strptime(trade_history['trade_date'].max(), '%Y%m%d')+datetime.timedelta(days=30)).strftime('%Y%m%d'))
            price_kcb_df = hbdb.db2df(sql, db='readonly')
            price_df = pd.concat([price_df, price_kcb_df], axis=0).drop('ROW_ID', axis=1)
            price_df.sort_values('JYRQ', inplace=True)
            price_df['JYRQ'] = price_df['JYRQ'].str[0:10].str.replace('-', '')

            y_position += 1
            ws["A{}".format(int(y_position))].options(pd.DataFrame,
                                                 header=1, index=False, expand='table').value =trade_property
            y_position+=23

            for ticker in top10_tickers:
                df_bar=tempdf[tempdf['zqdm'] == ticker].set_index('trade_date')
                sec_name=str(df_bar['zqjc'].values[0])
                industry_lv1=df_bar['yjxymc'].values[0]
                industry_lv2 = df_bar['ejxymc'].values[0]
                industry_lv3 = df_bar['sjxymc'].values[0]
                df_bar=df_bar[['adjuested_sl','sl','NETPROFITGROWRATE_sj',
                               'NETPROFITGROWRATE_ticker','PE_sj','PE_ticker','PE_FY1_sj','PE_FY1_ticker']]
                df_line=(price_df[price_df['ZQDM'] == ticker].set_index('JYRQ')['SPJG']).to_frame('股价')
                df_bar=pd.merge(df_line,df_bar,
                                how='left',left_index=True,right_index=True).fillna(0)[['adjuested_sl','sl','NETPROFITGROWRATE_sj',
                               'NETPROFITGROWRATE_ticker','PE_sj','PE_ticker','PE_FY1_sj','PE_FY1_ticker']]
                df_bar['index_count'] = df_bar.reset_index().index
                for position in df_bar[df_bar['sl']!=0]['index_count']:
                    df_bar.loc[(df_bar['index_count']<=position)&(df_bar['index_count']>=position-10),'sl']=\
                        df_bar[df_bar['index_count']==position]['sl'].values[0]
                    df_bar.loc[(df_bar['index_count']<=position-10)&(df_bar['index_count']>=position-20),'adjuested_sl']=\
                        df_bar[df_bar['index_count']==position]['adjuested_sl'].values[0]

                data,layout=plot.plotly_line_and_bar(df_line,
                                                     df_bar[['sl','adjuested_sl']].rename(columns={'sl':'实际手数',"adjuested_sl":"调整后手数"})
                                                     ,sec_name+"_"+industry_lv1+"_"+industry_lv2+"_"+industry_lv3,bar_width=1,
                                                     figsize=(max(len(df_line)*2,700), max(len(df_line),350)))
                annotations=get_annotations(df_bar[['adjuested_sl','sl','NETPROFITGROWRATE_sj',
                               'NETPROFITGROWRATE_ticker','PE_sj','PE_ticker','PE_FY1_sj','PE_FY1_ticker']])
                plot.save_pic2local(data, layout, newpath + r"\{}".format(jjdm+sec_name),annotations=annotations)
                ws.pictures.add(newpath + r"\{}.png".format(jjdm+sec_name),
                                left=ws.range('{0}{1}'.format(x_position_list[m],int(y_position))).left, top=ws.range('{0}{1}'.format(x_position_list[m],int(y_position))).top,
                                width=700, height=350)
                m += 1
                if(m>4):
                    m=0
                    y_position+=27


    for i in range(len(sheet_list)) :

        ws = wb.sheets[sheet_list[i]]
        ws.clear()
        ws["A1"].options(pd.DataFrame, header=1, index=False, expand='table').value = df_list[i]
        print('{} done'.format(sheet_list[i]))

    wb.save(filename)
    wb.close()
    app.quit()

    # writer=pd.ExcelWriter(r"E:\GitFolder\docs\公募核心池报告.xlsx")
    # industry_p.to_excel(r"E:\GitFolder\docs\公募核心池报告.xlsx", sheet_name="行业画像", index=False)
    # writer.save()

def get_mutual_fund_latest_pb_pe(input_fund_infor,latest_date,dir):

    fund_infor=input_fund_infor.copy()
    jjdm_list=fund_infor['基金代码'].tolist()
    fund_infor.set_index('基金代码',inplace=True)

    sql="select jjdm,jsrq,pe,pb,roe,dividend,zclb from st_fund.t_st_gm_jjggfg where jjdm in {0} and jsrq<='{1}'"\
        .format(tuple(jjdm_list),latest_date)
    db_data=hbdb.db2df(sql,db='funduser')
    db_data['jsrq']=db_data['jsrq'].astype(str)

    db_data=db_data.sort_values(['jsrq','zclb']).drop_duplicates(['jjdm','jsrq'],keep='last').drop('zclb',axis=1)

    #calculate the latest pe pb
    sql="select max(jsrq) as latest_jsrq from st_fund.t_st_gm_gpzh where jsrq<='{0}' "\
        .format(util.str_date_shift(latest_date,90,'-'))
    latest_jsrq=hbdb.db2df(sql,db='funduser')['latest_jsrq'].iloc[0]

    sql="select jjdm,zqdm,ccsl from st_fund.t_st_gm_gpzh where jsrq='{0}' and jjdm in {1}".format(latest_jsrq,tuple(jjdm_list))
    latest_hld_data=hbdb.db2df(sql,db='funduser')
    hk_zqdm_list=latest_hld_data[latest_hld_data['zqdm'].str.len()==5]['zqdm'].unique().tolist()
    zqdm_list=latest_hld_data['zqdm'].unique().tolist()

    #get pe,pb,dividend for ticker
    sql="select zqdm,eps_ttm,netassetps from st_main.t_st_gg_gszycwzb where zqdm in {0} and jsrq ='{1}'".format(tuple(zqdm_list),latest_jsrq)
    pe_pb_data=hbdb.db2df(sql,db='alluser')

    sql="select zqdm,dividend_tt from st_main.t_st_gg_gsgzfxrzb where zqdm in {0} and jsrq='{1}'".format(tuple(zqdm_list),latest_jsrq)
    dividen=hbdb.db2df(sql,db='alluser')


    #get ticker lastest price
    sql="select zqdm,spjg from st_ashare.t_st_ag_gpjy where zqdm in {0} and jyrq='{1}'".format(tuple(zqdm_list),latest_date)
    ticker_price=hbdb.db2df(sql,db='alluser')

    if(len(hk_zqdm_list)>0):
        from WindPy import w
        w.start()
        hk_ticker_fin_data = w.wss("{}".format([x[1:]+".HK" for x in hk_zqdm_list]).replace("'","").replace('[','').replace(']',''),
                                   "eps_ttm,bps,dividendyield2,close",
                     "tradeDate={0};rptDate={1};currencyType=;priceAdj=U;cycle=D".format(latest_date,latest_jsrq)
                     , usedf=True)[1]
        w.stop()
        hk_ticker_fin_data.index=["0"+x[0:4] for x in hk_ticker_fin_data.index]
        hk_ticker_fin_data.reset_index(inplace=True)
        hk_ticker_fin_data.rename(columns={'EPS_TTM':'eps_ttm','BPS':'netassetps',
                                           'DIVIDENDYIELD2':'dividend_tt',
                                           'index':'zqdm','CLOSE':'spjg'},inplace=True)


        pe_pb_data=pd.concat([pe_pb_data,hk_ticker_fin_data[['zqdm', 'eps_ttm', 'netassetps']]],axis=0)
        dividen=pd.concat([dividen,hk_ticker_fin_data[['zqdm','dividend_tt']]],axis=0)
        ticker_price=pd.concat([ticker_price,hk_ticker_fin_data[['zqdm','spjg']]],axis=0)



    latest_hld_data=pd.merge(latest_hld_data,ticker_price,how='left',on='zqdm')
    latest_hld_data['mv']=latest_hld_data['spjg']*latest_hld_data['ccsl']

    plot=functionality.Plot(600,300)

    for jjdm in jjdm_list:
        temp_summary=pd.DataFrame(columns=['pe', 'pb', 'dividend'])
        temp=latest_hld_data[latest_hld_data['jjdm']==jjdm]
        temp = pd.merge(temp,pe_pb_data,how='left',on='zqdm')
        temp = pd.merge(temp, dividen, how='left', on='zqdm')
        for col in [ 'netassetps', 'eps_ttm']:
            temp[col]=temp[col]*temp['ccsl']
        temp_summary.loc[0]=\
            [temp[temp['eps_ttm'].notnull()].sum()['mv']/temp[temp['eps_ttm'].notnull()].sum()['eps_ttm']
                ,temp[temp['netassetps'].notnull()].sum()['mv']/temp[temp['netassetps'].notnull()].sum()['netassetps']
                ,temp[temp['dividend_tt'].notnull()]['dividend_tt'].dot(temp[temp['dividend_tt'].notnull()]['mv'])
             /temp[temp['dividend_tt'].notnull()].sum()['mv']]

        temp_summary['jsrq']=str(latest_date)
        temp_summary['jjdm']=jjdm
        temp_summary['roe']=(temp_summary['pb']/temp_summary['pe']).iloc[0]*100
        db_data=pd.concat([db_data,temp_summary],axis=0)

        plot.plotly_line_multi_yaxis_general(db_data[db_data['jjdm']==jjdm].drop('jjdm',axis=1).set_index('jsrq')
                                             ,fund_infor.loc[jjdm]['基金名称'],['pb','roe','dividend'],dir)

def calculate_portfolio_summary(summary,barra_exp,barra_ret,core_pool):

    col_list=barra_exp.columns.tolist()

    barra_exp_new=pd.merge(barra_exp,core_pool[['基金代码','权重']],
                       how='left',left_on='fund_id',right_on='基金代码').set_index('基金代码')
    barra_ret_new=pd.merge(barra_ret,core_pool[['基金代码','权重']],
                       how='left',left_on='fund_id',right_on='基金代码').set_index('基金代码')

    for col in col_list:
        barra_exp_new[col]=barra_exp_new[col]*barra_exp_new['权重']
        barra_ret_new[col]=barra_ret_new[col]*barra_ret_new['权重']

    summary['基金池风格暴露']=barra_exp_new[col_list].sum()
    summary['基金池月收益贡献'] = barra_ret_new[col_list].sum()
    summary['基金池周收益贡献'] = np.nan

    return  summary

def mutual_pool_picture(pool_name,asofdate1,asofdate2,latest_date,fool_version=False,bmk_id='930950',if_portfolio=False):

    #read the pool file
    if(if_portfolio):

        core_pool=\
            pd.read_excel(r"E:\GitFolder\docs\基金池跟踪\公募池跟踪\公募跟踪池.xlsx"
                          ,sheet_name=pool_name)[['基金代码','基金名称','当前负责人员','入池逻辑','入池类型','权重']]
    else:
        core_pool=\
            pd.read_excel(r"E:\GitFolder\docs\基金池跟踪\公募池跟踪\公募跟踪池.xlsx"
                          ,sheet_name=pool_name)[['基金代码','基金名称','当前负责人员','入池逻辑','入池类型']]

    core_pool['基金代码']=[("000000"+str(x).replace('.OF',''))[-6:] for x in core_pool['基金代码']]


    #get funds history pe,pb data pic and save them in local file
    get_mutual_fund_latest_pb_pe(core_pool,latest_date,r'E:\GitFolder\docs\私募股多持仓分析\pic_temp\pb时序')

    jjdm_list=\
        core_pool['基金代码'].tolist()

    jjjc_data=hbdb.db2df("select jjdm,jjjc from st_fund.t_st_gm_jjxx where jjdm in ({})"
                    .format(util.list_sql_condition(jjdm_list)),db='funduser')
    jjjc_map=dict(zip(jjjc_data['jjdm'].tolist(),jjjc_data['jjjc'].tolist()))

    #get manager infor
    sql="select jjdm,ryxm as  基金经理 ,rzrq as 任职日期 from st_fund.t_st_gm_jjjl where jjdm in ({0}) and ryzt=-1 and ryzw='基金经理'"\
        .format(util.list_sql_condition(jjdm_list))
    manager_info=hbdb.db2df(sql,db='funduser')
    manager_info=manager_info.sort_values(['jjdm','任职日期']).drop_duplicates('jjdm',keep='first')

    from WindPy import w
    w.start()
    jjdm_of_list=[x+".OF" for x in jjdm_list]
    manager_size=w.wss(util.list_sql_condition(jjdm_of_list).replace("'",""),
                       "fund_manager_totalnetasset",
                       "unit=1;tradeDate=20230712;order=1",usedf=True)[1].reset_index(drop=False).rename(columns={'FUND_MANAGER_TOTALNETASSET':'经理管理规模(亿)',
                                                                                                                  'index':'jjdm'})
    manager_size['jjdm']=[x.replace(".OF","") for x in manager_size['jjdm']]
    manager_size['经理管理规模(亿)']=manager_size['经理管理规模(亿)']/100000000

    w.stop()
    manager_info=pd.merge(manager_info,manager_size,how='left',on='jjdm')

    if(jjdm_list is not None):
        jjdm_con="jjdm in ({})".format(util.list_sql_condition(jjdm_list))
    else:
        jjdm_con='1=1'

    style_pic, size_pic, \
        ind_pic,theme_pic, stock_pic_a, \
        stock_pic_b, industry_contribution_list,industry_con2, ticker_con,ticker_con2, theme_exp \
        , style_exp, size_exp,financial_rank=get_pic_from_localdb_simple_version(jjdm_con,asofdate=asofdate2,if_percentage=True,show_num=None)

    style_pic = style_pic[['jjdm', '风格类型', '风格偏好', '成长绝对暴露(持仓)',
                           '价值绝对暴露(持仓)', '集中度排名(持仓)', '换手率排名(持仓)', '成长暴露排名(持仓)',
                           '价值暴露排名(持仓)']].rename(columns={'集中度排名(持仓)': '风格集中度排名',
                                                                  '换手率排名(持仓)': '风格换手率排名'})

    size_pic = size_pic[['jjdm', '规模风格类型', '规模偏好', '大盘绝对暴露(持仓)',
                         '中小盘绝对暴露(持仓)', '集中度排名(持仓)', '换手率排名(持仓)', '大盘暴露排名(持仓)',
                         '中小盘暴露排名(持仓)']].rename(columns={'个股风格A': '个股交易风格',
                                                                  '个股风格B': '交易策略'}).rename(
        columns={'集中度排名(持仓)': '规模集中度排名',
                 '换手率排名(持仓)': '规模换手率排名'})


    stock_pic_a.rename(columns={'个股风格A': '个股交易风格',
                 '个股风格B': '交易策略'},inplace=True)

    stock_pic_b.rename(columns={'换手率_rank': '换手率排名', '平均持有时间(出持仓前)': '平均持有时间',
                                              '平均持有时间(出持仓前)_rank': '平均持有时间排名'},inplace=True)


    #get the secondary industry weight and finance
    sql="select * from hbs_industry_property_2_industry_level where jjdm in ({0}) and asofdate='{1}' and zsbl_mean>=0.03"\
        .format(util.list_sql_condition(jjdm_list),asofdate2)
    secondary_pic=pd.read_sql(sql,con=localdb)[['jjdm','ejxymc', 'zsbl_mean', 'ROE_mean', 'PB_mean', 'DIVIDENDRATIO_mean', 'PCF_mean',
                                                'PE_mean', 'PEG_mean', 'NETPROFITGROWRATE_mean', 'OPERATINGREVENUEYOY_mean',
                                                'ROE_mean_rank', 'PB_mean_rank', 'DIVIDENDRATIO_mean_rank', 'PCF_mean_rank',  'PE_mean_rank',
                                                'PEG_mean_rank','NETPROFITGROWRATE_mean_rank', 'OPERATINGREVENUEYOY_mean_rank']]
    name_map = dict(zip(['ejxymc','zsbl_mean', 'ROE_mean', 'PB_mean', 'DIVIDENDRATIO_mean', 'PCF_mean',
                                                'PE_mean', 'PEG_mean', 'NETPROFITGROWRATE_mean', 'OPERATINGREVENUEYOY_mean',
                                                'ROE_mean_rank', 'PB_mean_rank', 'DIVIDENDRATIO_mean_rank', 'PCF_mean_rank',  'PE_mean_rank',
                                                'PEG_mean_rank','NETPROFITGROWRATE_mean_rank', 'OPERATINGREVENUEYOY_mean_rank'], ['二级行业','占持仓比例', '净资产收益率',
                                                                'PB', '股息率','PCF', 'PEG','PE', '净利润增长率','主营业务增长率', '净资产收益率排名',
                                                                'PB排名', '股息率排名','PCF排名','PE排名','PEG排名','净利润增长率排名','主营业务增长率排名']))
    secondary_pic.rename(columns=name_map,inplace=True)
    sql = " select * from hbs_industry_financial_stats where ENDDATE>='{0}' and ENDDATE<='{1}' and class_level='2'" \
        .format(asofdate1[0:6], asofdate2[0:6])
    industry_financial_info = pd.read_sql(sql, con=localdb)
    industry_financial_info[['ROE', 'NETPROFITGROWRATE',
                             'OPERATINGREVENUEYOY', 'DIVIDENDRATIO']] = industry_financial_info[['ROE', 'NETPROFITGROWRATE',
                                                                             'OPERATINGREVENUEYOY',
                                                                             'DIVIDENDRATIO']] / 100
    industry_financial_info = industry_financial_info \
        .groupby('industry_name').mean().rename(columns={
        "ROE": "行业净资产收益率", "PE": "行业PE", "PCF": "行业PCF",
        "NETPROFITGROWRATE": "行业净利润增长率", "OPERATINGREVENUEYOY": "行业主营业务增长率",
        "PB": "行业PB", "DIVIDENDRATIO": "行业股息率", "AVERAGEMV": "行业平均市值", "TOTALMV": "行业总市值",
        "PEG": "行业PEG"})

    secondary_pic=pd.merge(secondary_pic,industry_financial_info,how='left',left_on='二级行业',right_index=True)
    secondary_pic = pd.merge(secondary_pic, jjjc_data, how='left', on='jjdm')
    secondary_pic=secondary_pic[['jjjc','二级行业', '占持仓比例', '净资产收益率','净资产收益率排名','行业净资产收益率', 'PB','PB排名','行业PB',
                                 '股息率','股息率排名','行业股息率','PCF','PCF排名', '行业PCF','PE','PE排名','行业PE',
                                  'PEG','PEG排名','行业PEG', '净利润增长率','净利润增长率排名', '行业净利润增长率',
                                 '主营业务增长率','主营业务增长率排名', '行业主营业务增长率']]


    #get industry_weight
    industry_w=[]
    for jjdm in jjdm_list:
        sql = "select jjdm,jsrq,flmc,zzjbl from st_fund.t_st_gm_jjhyzhyszb where jjdm ='{0}' and jsrq>='{1}' and jsrq<'{2}' and hyhfbz='2' and zclb='2' " \
            .format(jjdm, manager_info[manager_info['jjdm']==jjdm]['任职日期'], asofdate2)
        temp_w = hbdb.db2df(sql, db='funduser')
        industry_w.append(temp_w)

    industry_w=pd.concat(industry_w,axis=0)
    latest_industry_w=industry_w[industry_w['jsrq']==industry_w['jsrq'].max()].drop('jsrq',axis=1)
    latest_industry_w['rank'] = latest_industry_w.groupby('jjdm')['zzjbl'].rank(ascending=False)


    sql = "select max(jsrq) as jsrq from st_fund.t_st_gm_jjhyzhyszb where hyhfbz='2' and zclb='1' and jjdm='000001' "
    max_zc_date = hbdb.db2df(sql, db='funduser')['jsrq'].iloc[0]

    sql="select jjdm,flmc,zzjbl from st_fund.t_st_gm_jjhyzhyszb  where jjdm in {0} and zclb='1' and jsrq='{1}' and hyhfbz='2'"\
        .format(tuple(jjdm_list),max_zc_date)
    quarter_industr_w=hbdb.db2df(sql, db='funduser').pivot_table('zzjbl','jjdm','flmc').fillna(0)
    col_list=quarter_industr_w.columns.tolist()
    quarter_industr_w['total'] = quarter_industr_w.sum(axis=1)

    for col in col_list:
        quarter_industr_w[col]= quarter_industr_w[col]/ quarter_industr_w['total']*100

    latest_industry_w=pd.merge(latest_industry_w,latest_industry_w.groupby('jjdm')['zzjbl'].sum().to_frame('total'),how='left',on='jjdm')
    latest_industry_w['zgbl']=latest_industry_w['zzjbl']/latest_industry_w['total']*100
    latest_industry_w.drop('total',axis=1,inplace=True)

    quarter_industr_w=pd.merge(latest_industry_w.pivot_table('zgbl','jjdm','flmc').fillna(0),quarter_industr_w,on='jjdm',how='left')
    latest_industry_w.drop('zgbl',axis=1,inplace=True)
    quarter_industr_w=quarter_industr_w[quarter_industr_w['total']>=50]
    quarter_industr_w.drop('total',axis=1,inplace=True)
    for col in col_list:
        quarter_industr_w[col]=quarter_industr_w[col+'_x']-quarter_industr_w[col+'_y']
        quarter_industr_w.drop([col+'_x',col+'_y'],axis=1,inplace=True)

    if(int(max_zc_date)>int(asofdate1)):
        quarter_industr_w=quarter_industr_w*-1

    latest_industry_w=latest_industry_w[latest_industry_w['rank'] <= 5]


    #get the fund type from local db
    all_fund_list =list(set(util.get_stock_funds_pool(asofdate1, 2)+jjdm_list))
    latest_asofdate= \
        pd.read_sql("select max(asofdate) as asofdate from public_theme_pool_history where asofdate<='{}' "
                    .format(latest_date),con=localdb)['asofdate'].iloc[0]

    sql="select jjdm,theme from public_theme_pool_history where jjdm in ({0}) and asofdate={1}"\
        .format(util.list_sql_condition(all_fund_list),latest_asofdate)
    fund_type=pd.read_sql(sql,con=localdb)

    latest_asofdate2=pd.read_sql("select distinct(asofdate) as asofdate from extra_table_funds where asofdate<='{0}' "
                    .format(latest_date),con=localdb)[['asofdate']]
    latest_asofdate2['ym'] = latest_asofdate2['asofdate'].astype(str).str[4:6]
    latest_asofdate2=latest_asofdate2[latest_asofdate2['ym'].isin( ['12','06'])].iloc[-1]['asofdate']
    sql="select jjdm from extra_table_funds where jjdm in ({0}) and asofdate='{1}' "\
        .format(util.list_sql_condition(all_fund_list),latest_asofdate2)
    fund_type2 = pd.read_sql(sql, con=localdb)
    fund_type2=fund_type2[~fund_type2['jjdm'].isin(fund_type['jjdm'].tolist())]

    fund_type=pd.merge(pd.DataFrame(data=all_fund_list,columns=['jjdm']),fund_type,
                       how='left',on='jjdm')
    fund_type.loc[fund_type['jjdm'].isin(fund_type2['jjdm'].tolist()),'theme']='超额稳定型'
    fund_type['theme'] = fund_type['theme'].fillna('-')

    #get 930950 return info
    sql="select zbnp/100 as `基准`,zblb from st_market.t_st_zs_rqjhb where zqdm='930950' and jyrq='{0}' and zblb in ('2007','2101','2103','2106','2201','2202','2998')"\
        .format(latest_date)
    bmk_ret=hbdb.db2df(sql,db='alluser')
    sql="select zbnp/100 as `基准`,zblb from st_market.t_st_zs_rqjzdhc where zqdm='930950' and jyrq='{0}' and zblb in ('2201')"\
        .format(latest_date)
    bmk_db=hbdb.db2df(sql,db='alluser')
    bmk_db['zblb'] = 'max_drawback'
    bmk_ret=\
        pd.concat([bmk_ret,bmk_db],axis=0).set_index('zblb')

    #get fund return info
    sql="select jjdm,jzrq,zbnp,zblb from st_fund.t_st_gm_rqjhb where jjdm in ({0}) and jzrq='{1}' and zblb in ('2007','2101','2103','2106','2201','2202','2998') and zbnp!=99999 "\
        .format(util.list_sql_condition(all_fund_list),latest_date)
    fund_return_data=hbdb.db2df(sql,db='funduser').pivot_table('zbnp','jjdm','zblb')

    weekly_cont=\
        pd.concat([(fund_return_data.loc[core_pool['基金代码'].to_list()]['2007']/len(core_pool['基金代码'])).sort_values(ascending=False).iloc[0:5],(fund_return_data.loc[core_pool['基金代码'].to_list()]['2007']/len(core_pool['基金代码'])).sort_values(ascending=False).iloc[-5:]])
    weekly_cont=pd.merge(weekly_cont/100,core_pool[['基金代码', '基金名称']],how='left',left_on='jjdm',right_on='基金代码')
    weekly_cont.rename(columns={'2007':'最近一周'},inplace=True)


    fund_return_data=pd.merge(fund_return_data,fund_type,how='left',on='jjdm')

    sql="select jjdm,zbnp as max_drawback from st_fund.t_st_gm_rqjzdhc where jjdm in ({0}) and jzrq='{1}' and zblb in ('2201') and zbnp!=99999 "\
        .format(util.list_sql_condition(all_fund_list),latest_date)
    fund_db_data=hbdb.db2df(sql,db='funduser')
    fund_return_data=pd.merge(fund_return_data,fund_db_data,how='left',on='jjdm')

    bmk=fund_return_data.groupby('theme').mean()
    bmk.columns=[x+"_bmk" for x in bmk.columns]


    fund_return_rank=fund_return_data[['jjdm','theme']]
    fund_return_rank[['2007', '2101', '2103','2106', '2201','2202', '2998','max_drawback']]=\
        fund_return_data.groupby('theme')['2007', '2101', '2103','2106', '2201','2202', '2998','max_drawback'].rank(ascending=False)
    fund_return_rank=\
        pd.merge(fund_return_rank,fund_return_rank.groupby('theme')['jjdm'].count().to_frame('count'),how='left',on='theme')

    fund_return_data=pd.merge(fund_return_data,bmk,
                              how='left',on='theme')

    for col in ['2007', '2101', '2103','2106', '2201','2202', '2998','max_drawback']:

        fund_return_rank[col+'_ext_ret']=((fund_return_data[col]/100-bmk_ret.loc[col].iloc[0])).map("{:.2%}".format)
        fund_return_rank[col+'_rank']=\
            "'"+fund_return_rank[col].astype(str).str[0:-2]+"/"+\
            fund_return_rank['count'].astype(str)
        fund_return_rank[col]=(fund_return_data[col] / 100).map("{:.2%}".format)


    #get weekly return data
    sql="select jjdm,tjrq,hb1z from st_fund.t_st_gm_zhb where jjdm in ({0}) and tjrq>='{1}' and tjrq<='{2}' and hb1z!=99999 "\
        .format(util.list_sql_condition(fund_return_rank['jjdm'].tolist()),
                ( datetime.datetime.strptime(latest_date, '%Y%m%d') -datetime.timedelta(days=182)).strftime('%Y%m%d')
                ,latest_date)
    fund_return_data=\
        hbdb.db2df(sql,db='funduser').pivot_table('hb1z','jjdm','tjrq')

    #get the corr mat
    corr=fund_return_data.loc[jjdm_list].T.corr()
    corr.index=[jjjc_map[x]for x in corr.index]
    corr.columns=[jjjc_map[x]for x in corr.columns]


    fund_return_data=pd.merge(fund_return_data,fund_type
                              ,how='left',on='jjdm')
    bmk_weekly_ret=fund_return_data.groupby('theme').mean()
    week_date=bmk_weekly_ret.columns
    bmk_weekly_ret.columns=[str(x)+'_bmk' for x in week_date]
    fund_return_data=pd.merge(fund_return_data,bmk_weekly_ret
                              ,how='left',on='theme')
    for col in week_date:
        fund_return_data[col]=\
            fund_return_data[col]-fund_return_data[str(col)+'_bmk']

    fund_return_rank['infor_rate']\
        =fund_return_data[week_date.tolist()].mean(axis=1) / fund_return_data[week_date.tolist()].std(axis=1)
    fund_return_rank['infor_rate']=\
        fund_return_rank['infor_rate'].map("{:.2}".format)


    #calculate winning pro
    sql="select jjdm,tjyf,hb1y from st_fund.t_st_gm_yhb where jjdm in ({0}) and tjyf>='{1}' and tjyf<='{2}' and hb1y!=99999 "\
        .format(util.list_sql_condition(fund_return_rank['jjdm'].tolist()),
                ( datetime.datetime.strptime(latest_date, '%Y%m%d') -datetime.timedelta(days=182)).strftime('%Y%m%d')[0:6]
                ,latest_date[0:6])
    fund_return_data=\
        hbdb.db2df(sql,db='funduser').pivot_table('hb1y','jjdm','tjyf')
    fund_return_data=pd.merge(fund_return_data,fund_type
                              ,how='left',on='jjdm')
    bmk_monthly_ret=fund_return_data.groupby('theme').mean()
    month_date=bmk_monthly_ret.columns
    bmk_monthly_ret.columns=[str(x)+'_bmk' for x in month_date]
    month_date=month_date[-6:]
    fund_return_data=pd.merge(fund_return_data,bmk_monthly_ret
                              ,how='left',on='theme')
    for col in month_date:
        fund_return_data[col]=\
            fund_return_data[col]-fund_return_data[str(col)+'_bmk']

    fund_return_rank['winning_pro']=\
        (fund_return_data[month_date] > 0).sum(axis=1) / len(month_date)
    # fund_return_rank['winning_pro']=\
    #     fund_return_rank['winning_pro'].map("{:.2%}".format)


    #calculate the fund return self rank
    self_rank=manager_info.copy().set_index('jjdm')
    sql="select jyrq as jzrq,zbnp/100 as `基准` from st_market.t_st_zs_rqjhb where zqdm='930950' and jyrq<='{0}' and jyrq>='{1}' and zblb in ('2106') and zbnp!=99999"\
        .format(latest_date,manager_info['任职日期'].min())
    bmk_history=hbdb.db2df(sql,db='alluser')

    for jjdm in self_rank.index.tolist():

        sql = "select jzrq,zbnp from st_fund.t_st_gm_rqjhb where jjdm ='{0}' and jzrq<='{1}' and jzrq>='{2}' and zblb in ('2106') and zbnp!=99999 " \
            .format(jjdm, latest_date,np.min([self_rank.loc[jjdm]['任职日期'],int(latest_date)]))
        fund_return_his =pd.merge(hbdb.db2df(sql, db='funduser'),
                                  bmk_history,how='left',on='jzrq')
        fund_return_his['ext_ret']=fund_return_his['zbnp']-fund_return_his['基准']
        self_rank.loc[jjdm,'纵向分位数']=(fund_return_his['ext_ret'].rank() / len(fund_return_his)).iloc[-1]

    sql = "select jjdm,jzrq,zbnp from st_fund.t_st_gm_rqjhb where jjdm in ({0}) and jzrq='{1}' and zblb in ('2106') and zbnp!=99999 " \
        .format(util.list_sql_condition(all_fund_list), latest_date)
    fund_return_his=hbdb.db2df(sql, db='funduser')
    fund_return_his['zbnp']=fund_return_his['zbnp'].rank() / len(fund_return_his)
    self_rank=pd.merge(self_rank,fund_return_his
                       ,how='left',on='jjdm').rename(columns={'zbnp':'横向分位数'}).set_index('jjdm')


    #calculate the nav deviation

    for jjdm in self_rank.index.tolist():
        # print(jjdm)
        max_date=hbdb.db2df("select max(jsrq) as jsrq from st_fund.t_st_gm_gpzh where jsrq<={0} and jjdm='{1}' and (jsrq like '%12%' or jsrq like '%06%' ) "
                            .format(util.str_date_shift(latest_date,90,'-'),jjdm),db='funduser')['jsrq'].iloc[0]
        sql="select zqdm,zjbl from st_fund.t_st_gm_gpzh where jjdm='{0}' and jsrq='{1}' ".format(jjdm,max_date)
        latest_holding=hbdb.db2df(sql,db='funduser')
        latest_holding['zjbl']=latest_holding['zjbl']/latest_holding['zjbl'].sum()

        sql="select zqdm,spjg,jyrq from st_ashare.t_st_ag_gpjy where zqdm in ({0}) and jyrq <='{1}' and jyrq>='{2}' and spjg!=0"\
            .format(util.list_sql_condition(latest_holding['zqdm'].unique().tolist()),str(latest_date),str(max_date))
        stock_ret=hbdb.db2df(sql,db='alluser').pivot_table('spjg','jyrq','zqdm').pct_change()

        mimic_ret=pd.merge(latest_holding,stock_ret.T,how='left',on='zqdm')
        for date in stock_ret.index:
            mimic_ret[date]=mimic_ret[date]*mimic_ret['zjbl']
        mimic_ret=mimic_ret.sum(axis=0).loc[stock_ret.index]

        real_ret=hbdb.db2df("select hbdr,jzrq from st_fund.t_st_gm_rhb where jjdm='{0}' and jzrq <= {1} and jzrq>='{2}'"
                            .format(jjdm,str(latest_date),str(max_date)),db='funduser')
        mimic_ret = pd.merge(mimic_ret.astype(float).to_frame('mimic_ret')*100, real_ret, how='left', left_index=True, right_on='jzrq')
        nav_corr=(mimic_ret.drop('jzrq',axis=1).iloc[1:]).corr().iloc[1]['mimic_ret']

        self_rank.loc[jjdm, '累计净值偏离']=(mimic_ret/100+1).cumprod().iloc[-1]['hbdr']/(mimic_ret/100+1).cumprod().iloc[1]['hbdr']-(mimic_ret/100+1).cumprod().iloc[-1]['mimic_ret']/(mimic_ret/100+1).cumprod().iloc[1]['mimic_ret']
        self_rank.loc[jjdm, '虚拟与实际净值相关性']=nav_corr

    #get the industry average weight
    ind_detail_date = pd.read_sql("SELECT max(asofdate) as max_date from jjpic_industry_detail_1 where asofdate<='{}' "
                                  .format(asofdate2), con=localdb)['max_date'][0]
    latest_date2 = ind_detail_date
    sql = "SELECT jjdm, `行业名称`, `占持仓比例(时序均值)` from jjpic_industry_detail_1 where jjdm in ({0}) and asofdate='{1}' " \
        .format(util.list_sql_condition(jjdm_list), latest_date2)

    temp_ind_detail = pd.read_sql(sql, con=localdb)
    latest_industry_w = pd.merge(latest_industry_w, temp_ind_detail[['jjdm', '行业名称', '占持仓比例(时序均值)']],
                                 how='left', left_on=['jjdm', 'flmc'], right_on=['jjdm', '行业名称'])


    funds_focus_industry=latest_industry_w[latest_industry_w['zzjbl']>20]


    latest_industry_w['zzjbl']=(latest_industry_w['zzjbl']/100).map("{:.2%}".format)
    latest_industry_w['占持仓比例(时序均值)']=latest_industry_w['占持仓比例(时序均值)'].map("{:.2%}".format)
    latest_industry_w['前五大行业']=latest_industry_w['flmc']+":"+latest_industry_w['zzjbl']+"/"+latest_industry_w['占持仓比例(时序均值)']+" "
    latest_industry_w=latest_industry_w.groupby('jjdm')['前五大行业'].sum()

    #get the bmk comparison
    #industry part

    # get bmk exp
    bmk_list = util.get_930950_funds(asofdate2)
    sql="select jjdm,jsrq,zzjbl/100 as 中证偏股基金指数,flmc as 行业名称  from st_fund.t_st_gm_jjhyzhyszb where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}' and hyhfbz='2' and zclb='2'  "\
        .format(util.list_sql_condition(bmk_list),asofdate1,asofdate2)
    bmk_ind_dis=hbdb.db2df(sql,db='funduser')

    jsrq = pd.read_sql("select max(jsrq) as jsrq from hbs_9_lables_exp where jsrq<='{}'".format(asofdate2), con=localdb)[
        'jsrq'].iloc[0]
    sql = "select jjdm,jjzzc from hbs_9_lables_exp where jjdm in ({0}) and jsrq='{1}'".format(
        util.list_sql_condition(bmk_list), jsrq)
    bmk_mv_data = pd.read_sql(sql, con=localdb).drop_duplicates('jjdm')
    bmk_mv_data['total_mv'] = bmk_mv_data.groupby('jjdm')['jjzzc'].mean().sum()
    bmk_mv_data['jjzzc'] = bmk_mv_data['jjzzc'] / bmk_mv_data['total_mv']

    bmk_ind_dis = pd.merge(bmk_ind_dis, bmk_mv_data.drop_duplicates('jjdm'), how='left', on='jjdm')
    bmk_ind_dis['中证偏股基金指数'] = bmk_ind_dis['中证偏股基金指数'] * bmk_ind_dis['jjzzc']
    bmk_ind_dis = bmk_ind_dis.groupby('行业名称')[['中证偏股基金指数']].sum()



    sql="select flmc as `行业名称`,sum(zzjbl)/100 as `池` from st_fund.t_st_gm_jjhyzhyszb where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}' and hyhfbz='2' and zclb='2' group by flmc "\
        .format(util.list_sql_condition(core_pool['基金代码'].tolist()),asofdate1,asofdate2)
    core_pool_ind_dis=pd.merge(bmk_ind_dis,hbdb.db2df(sql,db='funduser'),how='left',on='行业名称').fillna(0)
    core_pool_ind_dis['池']=core_pool_ind_dis['池']/len(core_pool)
    core_pool_ind_dis['change'] = core_pool_ind_dis['池'] / core_pool_ind_dis['中证偏股基金指数']
    core_pool_ind_dis['diff'] = abs(core_pool_ind_dis['池']-core_pool_ind_dis['中证偏股基金指数'])
    core_pool_ind_dis['偏离度'] = core_pool_ind_dis['池'] - core_pool_ind_dis['中证偏股基金指数']
    ind_div_list = []
    warnings="行业上,超配："
    for ind in core_pool_ind_dis[(core_pool_ind_dis['change']>1)&(core_pool_ind_dis['diff']>=0.03)]['行业名称'].tolist():
        warnings+=ind
        ind_div_list.append(ind)
    warnings += "; 低配： "
    for ind in core_pool_ind_dis[(core_pool_ind_dis['change']<1)&(core_pool_ind_dis['diff']>=0.03)]['行业名称'].tolist():
        warnings += ind
        ind_div_list.append(ind)
    core_pool_ind_dis.drop(['change','diff'],axis=1,inplace=True)

    theme_col = ['大金融', '消费', 'TMT', '周期', '制造', '医药']
    theme_map = dict(zip(theme_col,
                         [['银行', '非银金融', '房地产'],
                          ['食品饮料', '家用电器', '社会服务', '农林牧渔', '商贸零售', '美容护理', '纺织服饰'],
                          ['通信', '计算机', '电子', '传媒'],
                          ['钢铁', '有色金属', '建筑装饰', '建筑材料', '基础化工', '石油石化', '煤炭'],
                          ['交通运输', '机械设备', '汽车', '轻工制造', '电力设备', '环保', '公用事业', '国防军工'],
                          ['医药生物']
                          ]
                         ))
    lista = []
    listb = []
    for theme in theme_col:
        for col in theme_map[theme]:
            lista.append(col)
            listb.append(theme)
    ind2thememap = pd.DataFrame()
    ind2thememap['industry_name'] = lista
    ind2thememap['theme'] = listb

    core_pool_theme_dis = pd.merge(core_pool_ind_dis, ind2thememap, how='left', left_on='行业名称',
                                 right_on='industry_name').groupby('theme').sum().reset_index()
    core_pool_theme_dis['change'] = core_pool_theme_dis['池'] / core_pool_theme_dis['中证偏股基金指数']
    core_pool_theme_dis['diff'] = abs(core_pool_theme_dis['池']-core_pool_theme_dis['中证偏股基金指数'])
    core_pool_theme_dis['偏离度'] = core_pool_theme_dis['池'] - core_pool_theme_dis['中证偏股基金指数']
    theme_div_list=[]
    warnings+="主题上,超配："
    for ind in core_pool_theme_dis[(core_pool_theme_dis['change']>1)&(core_pool_theme_dis['diff']>=0.05)]['theme'].tolist():
        warnings+=ind
        theme_div_list.append(ind)
    warnings += "; 低配： "
    for ind in core_pool_theme_dis[(core_pool_theme_dis['change']<1)&(core_pool_theme_dis['diff']>=0.05)]['theme'].tolist():
        warnings += ind
        theme_div_list.append(ind)
    core_pool_theme_dis.drop(['change','diff'],axis=1,inplace=True)


    #style level
    sql="SELECT style_type as `风格类型`, zjbl/100 as `中证偏股基金指数` ,jjdm from hbs_style_exp where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}'  "\
        .format(util.list_sql_condition(bmk_list),asofdate1,asofdate2)
    bmk_style_dis =pd.read_sql(sql,con=localdb)

    bmk_style_dis = pd.merge(bmk_style_dis, bmk_mv_data.drop_duplicates('jjdm'), how='left', on='jjdm')
    bmk_style_dis['中证偏股基金指数'] = bmk_style_dis['中证偏股基金指数'] * bmk_style_dis['jjzzc']
    bmk_style_dis = bmk_style_dis.groupby('风格类型')[['中证偏股基金指数']].sum()


    sql="SELECT style_type as `风格类型`, avg(zjbl)/100 as `池` from hbs_style_exp where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}' GROUP BY style_type "\
        .format(util.list_sql_condition(core_pool['基金代码'].tolist()),asofdate1,asofdate2)
    core_pool_style_dis =pd.merge(bmk_style_dis, pd.read_sql(sql,con=localdb),how='left',on='风格类型')
    core_pool_style_dis['change'] = core_pool_style_dis['池'] / core_pool_style_dis['中证偏股基金指数']
    core_pool_style_dis['diff'] = abs(core_pool_style_dis['池']-core_pool_style_dis['中证偏股基金指数'])
    core_pool_style_dis['偏离度'] = core_pool_style_dis['池'] - core_pool_style_dis['中证偏股基金指数']
    style_div_list=[]
    warnings+="  风格上,超配："
    for ind in core_pool_style_dis[(core_pool_style_dis['change']>=1.3)&(core_pool_style_dis['diff']>=0.05)]['风格类型'].tolist():
        warnings+=ind
        style_div_list.append(ind)
    warnings += "; 低配： "
    for ind in core_pool_style_dis[(core_pool_style_dis['change']<=0.7)&(core_pool_style_dis['diff']>=0.05)]['风格类型'].tolist():
        warnings += ind
        style_div_list.append(ind)
    core_pool_style_dis.drop(['change','diff'],axis=1,inplace=True)

    #get industry history position and month return
    def get_industry_historyposition_and_month_return():

        sql = "select jyrq,hbdr from st_market.t_st_zs_rhb where jyrq >='{0}' and jyrq<='{1}' and zqdm ='881001' " \
            .format(util._shift_date(util.str_date_shift(str(latest_date), 365 * 3, '-')), str(latest_date))
        market_index_his = hbdb.db2df(sql, db='alluser')
        market_index_his['hbdr'] = (market_index_his['hbdr'] / 100 + 1).cumprod()
        market_index_his['jyrq'] = market_index_his['jyrq'].astype(str)
        new_col_name = ['农林牧渔', '基础化工', '钢铁', '有色金属', '电子', '家用电器', '食品饮料',
                        '纺织服饰', '轻工制造', '医药生物', '公用事业', '交通运输', '房地产', '商贸零售',
                        '社会服务', '综合', '建筑材料', '建筑装饰', '电力设备', '国防军工', '计算机', '传媒',
                        '通信', '银行', '非银金融', '汽车', '机械设备', '煤炭', '石油石化', '环保', '美容护理']
        index_code_list = ['801010', '801030', '801040', '801050', '801080', '801110',
                           '801120', '801130', '801140', '801150', '801160', '801170',
                           '801180', '801200', '801210', '801230', '801710', '801720',
                           '801730', '801740', '801750', '801760', '801770', '801780',
                           '801790', '801880', '801890', '801950', '801960', '801970', '801980']
        index_code_map = dict(zip(index_code_list, new_col_name))


        sql = "select jyrq,zqdm,spjg from st_market.t_st_zs_hq where jyrq in {0} and zqdm in ({1})" \
            .format(tuple([util._shift_date(util.str_date_shift(str(latest_date), 30, '-')), str(latest_date)]),
                    util.list_sql_condition(['801010', '801030', '801040', '801050', '801080', '801110',
                                             '801120', '801130', '801140', '801150', '801160', '801170',
                                             '801180', '801200', '801210', '801230', '801710', '801720',
                                             '801730', '801740', '801750', '801760', '801770', '801780',
                                             '801790', '801880', '801890', '801950', '801960', '801970', '801980']))
        ind_index = \
            hbdb.db2df(sql, db='alluser').pivot_table('spjg', 'jyrq', 'zqdm').pct_change().iloc[-1]

        ind_index.index = [index_code_map[x] for x in ind_index.index.tolist()]

        sql = "select jyrq,zqdm,spjg from st_market.t_st_zs_hq where jyrq >= '{0}' and jyrq<='{1}' and zqdm in ({2})" \
            .format(util._shift_date(util.str_date_shift(str(latest_date), 365 * 3, '-')), str(latest_date),
                    util.list_sql_condition(['801010', '801030', '801040', '801050', '801080', '801110',
                                             '801120', '801130', '801140', '801150', '801160', '801170',
                                             '801180', '801200', '801210', '801230', '801710', '801720',
                                             '801730', '801740', '801750', '801760', '801770', '801780',
                                             '801790', '801880', '801890', '801950', '801960', '801970', '801980']))
        ind_index_his = \
            hbdb.db2df(sql, db='alluser').pivot_table('spjg', 'jyrq', 'zqdm')

        ind_index_his.columns = [index_code_map[x] for x in ind_index_his.columns.tolist()]
        ind_index_his = ind_index_his / ind_index_his.iloc[0]
        market_index_his['hbdr'] = market_index_his['hbdr'] / market_index_his['hbdr'].iloc[0]
        for col in ind_index_his.columns:
            ind_index_his[col] = ind_index_his[col].values - market_index_his['hbdr'].values
        ind_index_his = ind_index_his.rank(pct=True).iloc[-1].to_frame('超额分位数')

        return  ind_index_his,ind_index,market_index_his

    ind_index_his, ind_index,market_index_his=get_industry_historyposition_and_month_return()


    def add_alert(core_pool,asofdate1,latest_date):

        core_pool['业绩预警']=''

        core_pool['temp']=[float(x.replace("'", "").split('/')[0]) / float(x.replace("'", "").split('/')[1]) for x in
         core_pool['回撤同策略排名']]
        core_pool.loc[core_pool['temp']>2/3,'业绩预警']=core_pool[core_pool['temp']>2/3]['业绩预警']+"业绩波动较大;"
        core_pool.drop('temp',axis=1,inplace=True)
        core_pool.loc[core_pool['近6月胜率']<1/3,'业绩预警']=core_pool[core_pool['近6月胜率']<1/3]['业绩预警']+"业绩表现不佳;"

        day_laps=(datetime.datetime.strptime(latest_date, '%Y%m%d')-datetime.datetime.strptime(asofdate1, '%Y%m%d')).days
        if(day_laps<=90):
            div_threshield=0.05
        elif(day_laps>=90 and day_laps<=180):
            div_threshield=0.1
        elif(day_laps>=180):
            div_threshield=0.15

        core_pool.loc[(core_pool['累计净值偏离'].abs() > div_threshield)|(core_pool['虚拟与实际净值相关性']<0.95), '业绩预警'] = \
            core_pool[(core_pool['累计净值偏离'].abs() > div_threshield)|(core_pool['虚拟与实际净值相关性']<0.95)]['业绩预警'] + "风格迁移(调仓)风险;"

        return  core_pool

    def get_bad_ticker(jsrq, latest_date, zqdm_list, ticke_hld, threshield):

        sql = "select spjg,jyrq,zqdm,zqmc from st_ashare.t_st_ag_gpjy where zqdm in {0} and jyrq in {1}" \
            .format(tuple(zqdm_list), tuple([util._shift_date(str(jsrq)), latest_date]))
        ticker_price = hbdb.db2df(sql, db='alluser')
        ticker_price['ret'] = \
            ticker_price.sort_values('jyrq').groupby('zqdm')['spjg'].pct_change()
        ticker_price = ticker_price[ticker_price['ret'].notnull()]

        sql = "select spjg,jyrq from st_market.t_st_zs_hq where zqdm='881001' and jyrq in {0}" \
            .format(tuple([util._shift_date(str(jsrq)), latest_date]))
        bmk_ret = hbdb.db2df(sql, db='alluser')
        bmk_ret = \
            bmk_ret.sort_values('jyrq').pct_change()['spjg'].iloc[-1]

        ticker_price['ret'] = ticker_price['ret'] - bmk_ret
        ticker_price = ticker_price[ticker_price['ret'] <= threshield]

        ticke_hld_out = pd.merge(ticke_hld, ticker_price[['zqdm', 'zqmc', 'ret']], how='left', on='zqdm')

        ticke_hld_out = ticke_hld_out[ticke_hld_out['ret'].notnull()]
        ticke_hld_out['ret'] = ticke_hld_out['ret'].map("{:.2%}".format)

        return ticke_hld_out

    def add_holding_alert(core_pool,stock_pic_a,latest_date):

        core_pool['持仓个股预警'] = ''
        #get funds whose top 3 ticker weight bigger than 20%
        stock_cen_list=\
            stock_pic_a[stock_pic_a['前三大'].str.replace('%', '').astype(float) >= 20]['jjdm'].tolist()


        #get target funds ticker holding details
        sql="select max(jsrq) as jsrq from st_fund.t_st_gm_gpzh where jjdm='000001'"
        jsrq=hbdb.db2df(sql,db='funduser')['jsrq'].iloc[0]

        last_month=\
            util._shift_date(util.str_date_shift(latest_date,30,'-'))

        sql="select jjdm,zqdm,zjbl from st_fund.t_st_gm_gpzh where jjdm in {0} and jsrq='{1}' and zjbl>=5 "\
            .format(tuple(stock_cen_list),jsrq)
        ticke_hld=hbdb.db2df(sql,db='funduser')
        ticke_hld=ticke_hld.sort_values(['jjdm', 'zjbl'], ascending=False).groupby('jjdm').head(3)

        zqdm_list=ticke_hld['zqdm'].unique().tolist()


        #get tickers that are outperformanced by bmk more than 10% from last report date or more than 5% from last month
        ticke_hld1=get_bad_ticker(jsrq,latest_date,zqdm_list,ticke_hld,-0.1)
        ticke_hld2=get_bad_ticker(last_month,latest_date,zqdm_list,ticke_hld,-0.05)

        for jjdm in ticke_hld1['jjdm'].unique():

            temp_df=ticke_hld1[ticke_hld1['jjdm']==jjdm]
            for zqmc in temp_df['zqmc'].tolist():
                alert=\
                    "{0}从{1} 到 {2} 期间,相比万得全A超额为{3}".format(zqmc,jsrq,latest_date,temp_df[temp_df['zqmc']==zqmc]['ret'].iloc[0])

            core_pool.loc[core_pool['基金代码']==jjdm+'.OF','持仓个股预警']=core_pool[core_pool['基金代码']==jjdm+'.OF']['持仓个股预警']+"基金个股集中,但是在前三大个股中,"+alert

        for jjdm in ticke_hld2['jjdm'].unique():

            temp_df=ticke_hld2[ticke_hld2['jjdm']==jjdm]
            for zqmc in temp_df['zqmc'].tolist():
                alert=\
                    "{0}上个月,相比万得全A超额为{1}".format(zqmc,temp_df[temp_df['zqmc']==zqmc]['ret'].iloc[0])

            if(core_pool[core_pool['基金代码']==jjdm+'.OF']['持仓个股预警'].iloc[0]!=''):
                core_pool.loc[core_pool['基金代码'] == jjdm + '.OF', '持仓个股预警'] = core_pool[core_pool['基金代码']==jjdm+'.OF']['持仓个股预警']+alert
            else:
                core_pool.loc[core_pool['基金代码']==jjdm+'.OF','持仓个股预警']=\
                    core_pool[core_pool['基金代码']==jjdm+'.OF']['持仓个股预警']+"基金个股集中,但是在前三大个股中,"+alert

        return  core_pool

    def add_funds_industry_alert(core_pool,stock_pic_a,ind_index_his, ind_index,quarter_industr_w):

        core_pool['持仓行业预警'] = ''

        for jjdm in stock_pic_a['jjdm'].unique():
            alert=''
            temp_df=stock_pic_a[stock_pic_a['jjdm']==jjdm]
            for hymc in temp_df['flmc'].tolist():
                alert0=''
                if(ind_index_his.loc[hymc]['超额分位数']>=0.75):
                    alert0+=\
                        "相比万得全A超额处在过去3年历史{0}分位数.".format(str(ind_index_his.loc[hymc]['超额分位数']*100)[0:4])

                if(ind_index.loc[hymc]<=-0.05):
                    alert0 += \
                        "相比万得全A过去一个月负超额显著，为{0}%.".format( str(
                            ind_index.loc[hymc] * 100)[0:4])
                if(alert0!=''):
                    alert0=hymc+alert0

                alert+=alert0


            if(alert!=''):
                core_pool.loc[core_pool['基金代码']==jjdm+'.OF','持仓行业预警']=core_pool[core_pool['基金代码']==jjdm+'.OF']['持仓行业预警']+"基金行业集中,其中,"+alert

        for jjdm in quarter_industr_w.index.tolist():

            tempdf2=quarter_industr_w.T[jjdm][quarter_industr_w.T[jjdm].abs()>=10]
            alert2=''
            if(len(tempdf2)>0):
                alert2="基金在"
                for ind in tempdf2.index.tolist():
                    alert2+=ind+"(变动：{})".format(str(tempdf2.loc[ind])[0:5])+','
                alert2+="的仓位有显著的变动"

                core_pool.loc[core_pool['基金代码']==jjdm+'.OF','持仓行业预警']=\
                    core_pool[core_pool['基金代码']==jjdm+'.OF']['持仓行业预警']+alert2


        return  core_pool

    def merge_pic(core_pool,fund_return_rank):

        core_pool=pd.merge(core_pool,manager_info,how='left',
                           left_on='基金代码',right_on='jjdm').drop('jjdm',axis=1)

        core_pool=core_pool[['基金代码', '基金名称', '当前负责人员', '任职日期', '基金经理', '经理管理规模(亿)','入池逻辑', '入池类型']]

        core_pool=pd.merge(core_pool,fund_type,how='left',
                           left_on='基金代码',right_on='jjdm').drop('jjdm',axis=1).fillna('未满两年')


        core_pool=pd.merge(core_pool,size_pic[['jjdm','规模偏好']],how='left',right_on='jjdm',left_on='基金代码')
        core_pool = pd.merge(core_pool, style_pic[['jjdm', '风格偏好']], how='left', on='jjdm')
        # core_pool['风格类型'] = core_pool['规模偏好'] + core_pool['风格偏好']
        core_pool.drop(['jjdm'],axis=1,inplace=True)


        core_pool = pd.merge(core_pool, stock_pic_b[['jjdm','PB-ROE选股', 'PEG选股', '博弈基本面拐点', '博弈估值修复','是否抱团']], how='left',
                             right_on='jjdm', left_on='基金代码').drop('jjdm',axis=1)

        # core_pool['市场逆向 / 跟随选股']=""

        core_pool = pd.merge(core_pool, ind_pic[['jjdm','行业精选个股策略','一级行业策略','一级行业类型']], how='left',
                             right_on='jjdm', left_on='基金代码').drop('jjdm',axis=1).rename(columns={'一级行业类型':'行业类型'})


        core_pool = pd.merge(core_pool, stock_pic_a[['jjdm','交易策略']], how='left',
                             right_on='jjdm', left_on='基金代码').rename(columns={'交易策略':'投资策略类型'}).drop('jjdm',axis=1)

        core_pool.loc[core_pool['行业精选个股策略'] == '无', '行业精选个股策略'] = np.NAN
        core_pool[['行业精选个股策略']] = "行业内选择高" + core_pool[['行业精选个股策略']] + "属性个股"
        core_pool[['个股交易策略']]=""
        for col in ['PB-ROE选股', 'PEG选股', '博弈基本面拐点', '博弈估值修复', '是否抱团', '行业精选个股策略']:
            core_pool['个股交易策略'] =core_pool['个股交易策略']+ (core_pool[col] + ',').fillna(' ')
        core_pool.drop(['PB-ROE选股', 'PEG选股', '博弈基本面拐点', '博弈估值修复', '是否抱团', '行业精选个股策略'],axis=1,inplace=True)


        core_pool.loc[core_pool['一级行业策略'] == '无', '一级行业策略'] = np.NAN
        core_pool.loc[core_pool['投资策略类型'] == '无', '投资策略类型'] = np.NAN
        core_pool[['一级行业策略']] = "倾向" + core_pool[['一级行业策略']] + "行业"
        core_pool.loc[core_pool['行业类型']=='配置','行业类型']='行业分散配置'
        core_pool.loc[core_pool['行业类型'] == '专注', '行业类型'] = '行业配置集中且稳定'
        core_pool.loc[core_pool['行业类型'] == '轮动', '行业类型'] = '行业小幅轮动'
        core_pool.loc[core_pool['行业类型'].astype(str).str.contains('博弈'),
        '行业类型'] = '行业大幅轮动'


        core_pool[['行业交易策略']]=""
        for col in ['一级行业策略','行业类型','投资策略类型']:
            core_pool['行业交易策略'] =core_pool['行业交易策略']+ (core_pool[col] + ',').fillna(' ')
        core_pool.drop(
            ['一级行业策略','行业类型','投资策略类型'],
            axis=1, inplace=True)

        core_pool=pd.merge(core_pool,financial_rank,how='left',right_on='jjdm',left_on='基金代码').drop('jjdm',axis=1)

        core_pool=pd.merge(core_pool,latest_industry_w.to_frame('前五大行业:最新/3年平均'),how='left',right_on='jjdm',left_on='基金代码')

        core_pool = pd.merge(core_pool, industry_con2.to_frame('前三大贡献行业'), how='left',
                             right_on='jjdm', left_on='基金代码')
        core_pool = pd.merge(core_pool, ticker_con2.to_frame('前三大贡献个股'), how='left',
                             right_on='jjdm', left_on='基金代码')

        fund_return_rank=pd.merge(fund_return_rank,self_rank[['纵向分位数','横向分位数','累计净值偏离','虚拟与实际净值相关性']],how='left',on='jjdm')

        core_pool=\
            pd.merge(core_pool,
                           fund_return_rank[['jjdm','2007','2007_ext_ret', '2007_rank', '2101','2101_ext_ret', '2101_rank',
                                             '2103','2103_ext_ret', '2103_rank','2106','2106_ext_ret', '2106_rank',  '2201','2201_ext_ret',
                                             '2201_rank','2202','2202_ext_ret', '2202_rank',
                                             '2998','2998_ext_ret', '2998_rank','纵向分位数','横向分位数', 'max_drawback','max_drawback_ext_ret','max_drawback_rank',
                                            'infor_rate','winning_pro','累计净值偏离','虚拟与实际净值相关性']],
                           how='left',right_on='jjdm',left_on='基金代码').rename(columns=dict(zip(['2007','2007_ext_ret', '2007_rank', '2101','2101_ext_ret', '2101_rank',
                                             '2103','2103_ext_ret', '2103_rank','2106','2106_ext_ret', '2106_rank',  '2201','2201_ext_ret'
                                                                                                                  , '2201_rank','2202','2202_ext_ret', '2202_rank',
                                             '2998','2998_ext_ret', '2998_rank', 'max_drawback','max_drawback_ext_ret','max_drawback_rank',
                                            'infor_rate','winning_pro'],
                                                                         ['收益','超额','同策略排名','收益','超额','同策略排名',
                                                                          '收益','超额','同策略排名','收益','超额','同策略排名','收益','超额','同策略排名',
                                                                          '收益','超额','同策略排名','收益','超额','同策略排名',
                                                                          '最大回撤','回撤超额','回撤同策略排名','近6月信息比率','近6月胜率']))).drop('jjdm',axis=1)


        core_pool=core_pool.rename(columns={'theme':'策略类型','infor_rate':'近6月信息比率','winning_pro':'近6月胜率'})
        core_pool['基金代码']=[("000000"+x)[-6:]+".OF" for x in core_pool['基金代码']]
        core_pool=add_alert(core_pool,asofdate1,latest_date)
        core_pool = add_holding_alert(core_pool,stock_pic_a,latest_date)
        core_pool = add_funds_industry_alert(core_pool,funds_focus_industry,ind_index_his, ind_index,quarter_industr_w)

        return  core_pool


    if(if_portfolio):
        summary, barra_exp, barra_ret = \
            pra.get_funds_barra_data(last_month=util._shift_date(util.str_date_shift(str(latest_date), 30, '-')),
                                 last_week=util._shift_date(util.str_date_shift(str(latest_date), 7, '-')),
                                 end_date=str(latest_date), jjdm_list=jjdm_list, factor_type='style', bmk_id='930950',
                                 jjdm_weight=core_pool[['基金代码', '权重']])
        summary_sector, barra_exp_sector, barra_ret_sector = \
            pra.get_funds_barra_data(last_month=util._shift_date(util.str_date_shift(str(latest_date), 30, '-')),
                                 last_week=util._shift_date(util.str_date_shift(str(latest_date), 7, '-')),
                                 end_date=str(latest_date), jjdm_list=jjdm_list, factor_type='sector', bmk_id='930950',
                                 jjdm_weight=core_pool[['基金代码', '权重']])
        summary_style, barra_exp_style, barra_ret_style = \
            pra.get_funds_barra_data(last_month=util._shift_date(util.str_date_shift(str(latest_date), 30, '-')),
                                 last_week=util._shift_date(util.str_date_shift(str(latest_date), 7, '-')),
                                 end_date=str(latest_date), jjdm_list=jjdm_list, factor_type='style_allo',
                                 bmk_id='930950', jjdm_weight=core_pool[['基金代码', '权重']])
    else:
                # get the barra analysis result
        summary, barra_exp, barra_ret = \
            pra.get_funds_barra_data(last_month=util._shift_date(util.str_date_shift(str(latest_date), 30, '-')),
                                     last_week=util._shift_date(util.str_date_shift(str(latest_date), 7, '-')),
                                     end_date=str(latest_date), jjdm_list=jjdm_list, factor_type='style', bmk_id=bmk_id)
        summary_sector, barra_exp_sector, barra_ret_sector = \
            pra.get_funds_barra_data(last_month=util._shift_date(util.str_date_shift(str(latest_date), 30, '-')),
                                     last_week=util._shift_date(util.str_date_shift(str(latest_date), 7, '-')),
                                     end_date=str(latest_date), jjdm_list=jjdm_list, factor_type='sector',
                                     bmk_id=bmk_id)
        summary_style, barra_exp_style, barra_ret_style = \
            pra.get_funds_barra_data(last_month=util._shift_date(util.str_date_shift(str(latest_date), 30, '-')),
                                     last_week=util._shift_date(util.str_date_shift(str(latest_date), 7, '-')),
                                     end_date=str(latest_date), jjdm_list=jjdm_list, factor_type='style_allo',
                                     bmk_id=bmk_id)

    core_pool= merge_pic(core_pool,fund_return_rank)

    #save nav based data to local database
    # summary['date'] = latest_date
    # summary['type'] = 'barra'
    # total_summary.append(summary)
    # summary_sector['date'] = latest_date
    # summary_sector['type'] = '行业'
    # total_summary.append(summary_sector)
    # summary_style['date'] = latest_date
    # summary_style['type'] = '风格'
    # total_summary.append(summary_style)
    # total_summary=pd.concat(total_summary).reset_index().rename(columns={'index':'项目名称'})
    # localdb.execute("delete from pool_attribution_history where date='{}'".format(latest_date))
    # total_summary.to_sql('pool_attribution_history',con=localdb,index=False,if_exists='append')


    for col in [ '基金池月收益贡献', '基金池周收益贡献','BMK月收益贡献', 'BMK周收益贡献']:
        summary[col]=summary[col].map("{:.2%}".format)
    for col in ['基金池风格暴露', 'BMK风格暴露']:
        summary[col]=summary[col].map("{:.2}".format)
    for col in barra_exp.columns:
        barra_exp[col]=barra_exp[col].map("{:.2}".format)
    for col in barra_ret.columns:
        barra_exp[col] = barra_exp[col].astype(float).map("{:.2%}".format)

    for col in summary.columns:
        summary_sector[col] = summary_sector[col].map("{:.2%}".format)
        summary_style[col] = summary_style[col].map("{:.2%}".format)
    for col in barra_exp_sector.columns:
        barra_exp_sector[col] = barra_exp_sector[col].map("{:.2%}".format)
    for col in barra_ret_sector.columns:
        barra_ret_sector[col] = barra_ret_sector[col].map("{:.2%}".format)
    for col in barra_exp_style.columns:
        barra_exp_style[col] = barra_exp_style[col].map("{:.2%}".format)
    for col in barra_ret_style.columns:
        barra_ret_style[col] = barra_ret_style[col].map("{:.2%}".format)

    summary.index.name = 'Barra归因汇总'
    barra_exp.index.name = '个基Barra因子暴露'
    barra_ret.index.name = '个基Barra因子收益'

    summary_sector.index.name = '行业主题归因汇总'
    barra_exp_sector.index.name = '个基行业主题暴露'
    barra_ret_sector.index.name = '个基行业主题收益'

    summary_style.index.name = '风格归因汇总'
    barra_exp_style.index.name = '个基风格暴露'
    barra_ret_style.index.name = '个基风格收益'


    #get the holding based analysis result
    summary_hbs,funds_exp,funds_month_ret,funds_week_ret= pra.get_holding_based_data(last_month=util._shift_date(util.str_date_shift(str(latest_date),30,'-')),
                                                                         last_week=util._shift_date(util.str_date_shift(str(latest_date),7,'-'))
                                                                                     ,end_date=str(latest_date),
                                                                         jjdm_list=jjdm_list,factor_type='style',bmk_id=bmk_id)
    summary_hbs_sector,funds_exp_sector,\
        funds_month_ret_sector,funds_week_ret_sector= pra.get_holding_based_data(last_month=util._shift_date(util.str_date_shift(str(latest_date),30,'-')),
                                                                         last_week=util._shift_date(util.str_date_shift(str(latest_date),7,'-')),end_date=str(latest_date),
                                                                         jjdm_list=jjdm_list,factor_type='sector')

    #get the holding based analysis result by pool type angle
    jjdm_info=core_pool[['基金代码','入池类型']]
    jjdm_info['基金代码']=jjdm_info['基金代码'].str[0:6]
    pool_summary,pool_funds_summary= pra.subjective_label_analysis(last_month=util._shift_date(util.str_date_shift(str(latest_date),30,'-')),
                                                                   last_week=util._shift_date(util.str_date_shift(str(latest_date),7,'-')),
                                                                   end_date=str(latest_date),
                                                                   jjdm_info=jjdm_info)


    #get the holding based brinson result
    info_t0,brinson_w,brinson_m,gj_t1_m,gj_t2_m  = pra.fund_pool_brinson(last_month=util._shift_date(util.str_date_shift(str(latest_date),30,'-'))
                                                ,last_week=util._shift_date(util.str_date_shift(str(latest_date),7,'-')),
                                                end_date=(latest_date),jjdm_list=jjdm_list)
    info_t0=info_t0.set_index('资产类别')
    brinson_w=brinson_w.set_index('资产类别')
    brinson_m=brinson_m.set_index('资产类别')
    gj_t1_m=gj_t1_m.set_index('基金代码')
    gj_t2_m=gj_t2_m.set_index('基金代码')

    info_t0.index.name = '资产收益汇总'
    brinson_w.index.name = 'Brinson周度贡献'
    brinson_m.index.name = 'Brinson月度贡献'


    new_index_list=core_pool.sort_values('基金代码')['基金名称'].tolist()
    for df in [barra_exp,barra_ret,barra_exp_sector,barra_ret_sector,barra_exp_style,barra_ret_style,
               funds_exp,funds_month_ret,funds_week_ret,funds_exp_sector,funds_month_ret_sector,funds_week_ret_sector
        ,gj_t1_m,gj_t2_m]:
        df.sort_index(inplace=True)
        df.index=new_index_list
        df.loc[:, :] = df

    gj_t1_m.index.name = '个基暴露'
    gj_t2_m.index.name = '个基Brinson月度贡献'

    pool_funds_summary=pool_funds_summary.sort_values('基金代码')
    pool_funds_summary['基金简称']=new_index_list
    pool_funds_summary=pool_funds_summary[['基金简称', '入池类型','月超额收益','同类平均月收益', '周超额收益','同类平均周收益']]

    def plot_pool_bmk_exp_comparison(style_exp_his, col_list,pic_name,newpath):

        style_exp_his = pd.merge(
            style_exp_his.pivot_table('基金池风格暴露', 'date', '风格').drop(['alpha', '误差'], axis=1)
            , style_exp_his.pivot_table('BMK风格暴露', 'date', '风格').drop(['alpha', '误差'], axis=1)
            , on='date', how='inner')
        style_exp_his.columns = [x.replace('_x', '_基金池') for x in style_exp_his.columns]
        style_exp_his.columns = [x.replace('_y', '_BMK') for x in style_exp_his.columns]

        for i in range(1, len(col_list)):
            style_exp_his[col_list[i] + '_BMK'] = style_exp_his[col_list[i] + '_BMK'] + style_exp_his[
                [x + '_基金池' for x in col_list[0:i]]].sum(axis=1)

        data, layout =plot.plotly_line_and_area_under_same_axis(style_exp_his,line_col=[x + '_BMK' for x in col_list],
                                  area_col=[x + '_基金池' for x in col_list],title_text=pic_name,
                                  left_axis_name='暴露占比',right_axis_name='')

        plot.save_pic2local(data, layout, newpath + r"\{}".format(pic_name))

    if(pool_name=='公募核心池'):

        #get the pool and bmk exp from contribution history tabel
        sql = "SELECT * from pool_attribution_history where type ='风格'"
        style_exp_his=pd.read_sql(sql,con=localdb)

        style_exp_his.loc[style_exp_his['项目名称'].isin(['中盘价值', '小盘价值', '大盘价值']), '风格'] = '价值'
        style_exp_his.loc[style_exp_his['项目名称'].isin(['中盘成长', '小盘成长', '大盘成长']), '风格'] = '成长'
        style_exp_his.loc[style_exp_his['项目名称'] == '中证全债', '风格'] = '中证全债'
        style_exp_his.loc[style_exp_his['项目名称'] == '误差', '风格'] = '误差'
        style_exp_his.loc[style_exp_his['项目名称'] == 'alpha', '风格'] = 'alpha'

        style_exp_his2 = style_exp_his.copy()
        style_exp_his2.loc[style_exp_his2['项目名称'].isin(['大盘价值', '大盘成长']), '风格'] = '大盘'
        style_exp_his2.loc[style_exp_his2['项目名称'].isin(['中盘成长', '小盘成长', '中盘价值', '小盘价值']), '风格'] = '中小盘'
        style_exp_his2.loc[style_exp_his2['项目名称'] == '中证全债', '风格'] = '中证全债'
        style_exp_his2.loc[style_exp_his2['项目名称'] == '误差', '风格'] = '误差'
        style_exp_his2.loc[style_exp_his2['项目名称'] == 'alpha', '风格'] = 'alpha'

        style_exp_his=style_exp_his.groupby(['date', '风格']).sum().reset_index()
        style_exp_his2=style_exp_his2.groupby(['date', '风格']).sum().reset_index()


        sql = "SELECT * from pool_attribution_history where type ='行业'"
        theme_exp_his=pd.read_sql(sql,con=localdb)
        theme_exp_his['风格']=theme_exp_his['项目名称']

        sql = "SELECT * from pool_attribution_history where type ='barra'"
        barra_exp_his=pd.read_sql(sql,con=localdb)
        barra_exp_his['风格']=barra_exp_his['项目名称']


        #add the warnning sheet part data

        sql = "select zqdm,jyrq,spjg from st_market.t_st_zs_hq where jyrq in {} and zqdm ='881001' "\
            .format(tuple([util._shift_date(util.str_date_shift(str(latest_date), 30, '-')), str(latest_date)]))
        all_market_index = \
            hbdb.db2df(sql, db='alluser')['spjg'].pct_change().iloc[-1]


        sql = "select bigfinance as 大金融,consuming as 消费 ,tmt as TMT ,cycle as 周期, manufacture as 制造  from st_market.r_st_sector_factor where trade_date >={0} and trade_date<={1}" \
            .format(util._shift_date(util.str_date_shift(str(latest_date), 30, '-')), str(latest_date))
        theme_index=(hbdb.db2df(sql,db='alluser')+1).cumprod()
        theme_index=(theme_index.iloc[-1] / theme_index.iloc[0] - 1-all_market_index).to_frame('月超额收益')


        sql = "select bigfinance as 大金融,consuming as 消费 ,tmt as TMT ,cycle as 周期, manufacture as 制造, trade_date as jyrq  from st_market.r_st_sector_factor where trade_date >={0} and trade_date<={1}" \
            .format(util._shift_date(util.str_date_shift(str(latest_date), 365*3, '-')), str(latest_date))
        theme_index_his=hbdb.db2df(sql,db='alluser')
        for col in ['制造', '大金融', 'TMT', '消费', '周期']:
            theme_index_his[col]=(theme_index_his[col]+1).cumprod()

        sql = "select jyrq,hbdr from st_market.t_st_zs_rhb where jyrq >='{0}' and jyrq<='{1}' and zqdm ='881001' "\
            .format(util._shift_date(util.str_date_shift(str(latest_date), 365*3, '-')),str(latest_date))
        market_index_his=hbdb.db2df(sql,db='alluser')
        market_index_his['hbdr']=(market_index_his['hbdr']/100+1).cumprod()
        market_index_his['jyrq']=market_index_his['jyrq'].astype(str)

        theme_index_his=pd.merge(theme_index_his,market_index_his,how='left',on='jyrq')
        for col in ['制造', '大金融', 'TMT', '消费', '周期']:
            theme_index_his[col]=theme_index_his[col]-theme_index_his['hbdr']

        theme_index_his = theme_index_his[['制造', '大金融', 'TMT', '消费', '周期']].rank(pct=True).iloc[-1].to_frame(
            '超额分位数')

        core_pool_theme_dis['风险提示']=''
        for theme in core_pool_theme_dis[core_pool_theme_dis['theme']!='医药']['theme'].unique().tolist():

            nav_exp_month_change = (theme_exp_his.loc[theme_exp_his['风格'] == theme]['基金池风格暴露'].iloc[-1] -
                                    theme_exp_his.loc[theme_exp_his['风格'] == theme]['BMK风格暴露'].iloc[-1]) - (
                                               theme_exp_his.loc[theme_exp_his['风格'] == theme]['基金池风格暴露'].iloc[
                                                   -4] -
                                               theme_exp_his.loc[theme_exp_his['风格'] == theme]['BMK风格暴露'].iloc[-4])
            month_ext_ret=theme_index.loc[theme]['月超额收益']
            ext_position=theme_index_his.loc[theme]['超额分位数']

            core_pool_theme_dis.loc[core_pool_theme_dis['theme'] == theme, '净值暴露偏离变动'] = nav_exp_month_change
            core_pool_theme_dis.loc[core_pool_theme_dis['theme'] == theme, '本月超额'] = month_ext_ret
            core_pool_theme_dis.loc[core_pool_theme_dis['theme'] == theme, '超额分位数'] = ext_position


            if(theme in theme_div_list):

                warnnings="在基金池" + key_words + '的' + theme+"上,"

                position_warnnings=''
                if(core_pool_theme_dis[core_pool_theme_dis['theme']==theme]['偏离度'].values[0]>0):
                    key_words='超配'
                    if(ext_position>=0.75):
                        position_warnnings='相对基准超额处在过去三年历史{}分位数'.format(100*ext_position)
                else:
                    key_words='低配'
                    if(ext_position<=0.25):
                        position_warnnings='相对基准超额处在过去三年历史{}分位数'.format(100*ext_position)


                warnnings+=position_warnnings

                #if index move the same direction as the diviation, then add the warnnings
                if(core_pool_theme_dis[core_pool_theme_dis['theme']==theme]['偏离度'].values[0]*nav_exp_month_change>0):
                    warnnings+="基金池与基准的偏离在本月有扩大的趋势。"

                if(np.abs(month_ext_ret)>=0.025):
                    warnnings+="最近一月超额幅度显著"

                if(warnnings=="在基金池" + key_words + '的' + theme+"上,"):
                    warnnings=''

                core_pool_theme_dis.loc[core_pool_theme_dis['theme']==theme,'风险提示']=warnnings

        core_pool_theme_dis=core_pool_theme_dis[['theme', '中证偏股基金指数', '池', '偏离度','净值暴露偏离变动', '本月超额','超额分位数','风险提示']]
        core_pool_theme_dis.columns=['theme', '基准暴露', '池暴露', '偏离度','净值暴露偏离变动', '本月超额','超额分位数','风险提示']


        sql = "select zqdm,jyrq,spjg from st_market.t_st_zs_hq where jyrq in {} and zqdm in ('399370','399371','399314','399315','399316','399311') "\
            .format(tuple([util._shift_date(util.str_date_shift(str(latest_date), 30, '-')), str(latest_date)]))
        style_index = \
            hbdb.db2df(sql, db='alluser').pivot_table('spjg','jyrq','zqdm').pct_change()
        style_index.columns=['基准','大盘','中','小','成长','价值']
        style_index['中小盘']=style_index[['中','小']].mean(axis=1)
        style_index=style_index .iloc[-1].to_frame('月超额收益')
        style_index-=style_index.loc['基准']['月超额收益']


        sql = "select zqdm,jyrq,spjg from st_market.t_st_zs_hq where jyrq >= {0} and jyrq<={1} and zqdm in ('399370','399371','399314','399315','399316','399311') "\
            .format(util._shift_date(util.str_date_shift(str(latest_date), 365*3, '-')), str(latest_date))
        style_index_his = hbdb.db2df(sql, db='alluser').pivot_table('spjg','jyrq','zqdm')
        style_index_his=style_index_his / style_index_his.iloc[0]
        style_index_his.columns=['基准','大盘','中','小','成长','价值']
        style_index_his['中小盘']=style_index_his[['中','小']].mean(axis=1)
        for col in ['大盘','中小盘','成长','价值']:
            style_index_his[col]=style_index_his[col]-style_index_his['基准']

        style_index_his=style_index_his.rank(pct=True)[['大盘', '中小盘', '成长', '价值']].iloc[-1].to_frame('超额分位数')


        core_pool_style_dis['风险提示'] = ''

        for theme in ['价值', '成长']:

            nav_exp_month_change = ((style_exp_his.loc[style_exp_his['风格'] == theme]['基金池风格暴露'].iloc[-1] -
                                     style_exp_his.loc[style_exp_his['风格'] == theme]['BMK风格暴露'].iloc[-1]) - (
                                            style_exp_his.loc[style_exp_his['风格'] == theme]['基金池风格暴露'].iloc[-4] -
                                            style_exp_his.loc[style_exp_his['风格'] == theme]['BMK风格暴露'].iloc[-4]))

            month_ext_ret=style_index.loc[theme]['月超额收益']
            ext_position=style_index_his.loc[theme]['超额分位数']

            core_pool_style_dis.loc[core_pool_style_dis['风格类型'] == theme, '净值暴露偏离变动'] = nav_exp_month_change
            core_pool_style_dis.loc[core_pool_style_dis['风格类型'] == theme, '本月超额'] = month_ext_ret
            core_pool_style_dis.loc[core_pool_style_dis['风格类型'] == theme, '超额分位数'] = ext_position



            if(theme in style_div_list):


                position_warnnings=''

                if(core_pool_style_dis[core_pool_style_dis['风格类型']==theme]['偏离度'].values[0]>0):
                    key_words='超配'
                    if(ext_position>=0.8):
                        position_warnnings='相对基准超额处在过去三年历史{}分位数'.format(100*ext_position)
                else:
                    key_words='低配'
                    if(ext_position<=0.2):
                        position_warnnings='相对基准超额处在过去三年历史{}分位数'.format(100*ext_position)

                warnnings="在基金池" + key_words + '的' + theme+"上,"
                warnnings+=position_warnnings


                # if index move the same direction as the diviation, then add the warnnings
                if(core_pool_style_dis.loc[core_pool_style_dis['风格类型']==theme]['偏离度'].values[0]*nav_exp_month_change>0):
                    warnnings+="基金池与基准的偏离在本月有扩大的趋势。"

                if(np.abs(month_ext_ret)>=0.025):
                    warnnings+="最近一月超额幅度显著"

                if(warnnings=="在基金池" + key_words + '的' + theme+"上,"):
                    warnnings=''

                core_pool_style_dis.loc[core_pool_style_dis['风格类型']==theme,'风险提示']=warnnings

        core_pool_style_dis = core_pool_style_dis[
            ['风格类型', '中证偏股基金指数', '池', '偏离度','净值暴露偏离变动','本月超额', '超额分位数', '风险提示']]
        core_pool_style_dis.columns=['风格类型', '基准暴露', '池暴露', '偏离度','净值暴露偏离变动','本月超额', '超额分位数', '风险提示']

        new_col_name = ['农林牧渔', '基础化工', '钢铁', '有色金属', '电子', '家用电器', '食品饮料',
                        '纺织服饰', '轻工制造', '医药生物', '公用事业', '交通运输', '房地产', '商贸零售',
                        '社会服务', '综合', '建筑材料', '建筑装饰', '电力设备', '国防军工', '计算机', '传媒',
                        '通信', '银行', '非银金融', '汽车', '机械设备', '煤炭', '石油石化', '环保', '美容护理']
        index_code_list = ['801010', '801030', '801040', '801050', '801080', '801110',
                           '801120', '801130', '801140', '801150', '801160', '801170',
                           '801180', '801200', '801210', '801230', '801710', '801720',
                           '801730', '801740', '801750', '801760', '801770', '801780',
                           '801790', '801880', '801890', '801950', '801960', '801970', '801980']
        index_code_map = dict(zip(index_code_list, new_col_name))

        sql = "select jyrq,zqdm,spjg from st_market.t_st_zs_hq where jyrq in {0} and zqdm in ({1})" \
            .format(tuple([util._shift_date(util.str_date_shift(str(latest_date), 30, '-')), str(latest_date)]),
                    util.list_sql_condition(['801010', '801030', '801040', '801050', '801080', '801110',
                                             '801120', '801130', '801140', '801150', '801160', '801170',
                                             '801180', '801200', '801210', '801230', '801710', '801720',
                                             '801730', '801740', '801750', '801760', '801770', '801780',
                                             '801790', '801880', '801890', '801950', '801960', '801970', '801980']))
        ind_index = \
            hbdb.db2df(sql, db='alluser').pivot_table('spjg','jyrq','zqdm').pct_change().iloc[-1]

        ind_index.index=[index_code_map[x] for x in ind_index.index.tolist()]

        sql = "select jyrq,zqdm,spjg from st_market.t_st_zs_hq where jyrq >= '{0}' and jyrq<='{1}' and zqdm in ({2})" \
            .format(util._shift_date(util.str_date_shift(str(latest_date), 365*3, '-')), str(latest_date),
                    util.list_sql_condition(['801010', '801030', '801040', '801050', '801080', '801110',
                                             '801120', '801130', '801140', '801150', '801160', '801170',
                                             '801180', '801200', '801210', '801230', '801710', '801720',
                                             '801730', '801740', '801750', '801760', '801770', '801780',
                                             '801790', '801880', '801890', '801950', '801960', '801970', '801980']))
        ind_index_his = \
            hbdb.db2df(sql, db='alluser').pivot_table('spjg','jyrq','zqdm')

        ind_index_his.columns=[index_code_map[x] for x in ind_index_his.columns.tolist()]
        ind_index_his=ind_index_his/ind_index_his.iloc[0]
        market_index_his['hbdr']=market_index_his['hbdr']/market_index_his['hbdr'].iloc[0]
        for col in ind_index_his.columns:
            ind_index_his[col]=ind_index_his[col].values-market_index_his['hbdr'].values
        ind_index_his=ind_index_his.rank(pct=True).iloc[-1].to_frame('超额分位数')


        core_pool_ind_dis['风险提示'] = ''
        #交通运输
        for theme in core_pool_ind_dis['行业名称'].tolist():
            # print(theme)
            month_ext_ret=ind_index.loc[theme]
            ext_position = ind_index_his.loc[theme]['超额分位数']

            core_pool_ind_dis.loc[core_pool_ind_dis['行业名称'] == theme, '本月超额'] = month_ext_ret
            core_pool_ind_dis.loc[core_pool_ind_dis['行业名称'] == theme, '超额分位数'] = ext_position

            if(theme in ind_div_list):

                position_warnnings=''

                if(core_pool_ind_dis[core_pool_ind_dis['行业名称']==theme]['偏离度'].values[0]>0):
                    key_words='超配'
                    if(ext_position>=0.75):
                        position_warnnings='相对基准超额处在过去三年历史{}分位数'.format(100*ext_position)
                else:
                    key_words='低配'
                    if(ext_position<=0.25):
                        position_warnnings='相对基准超额处在过去三年历史{}分位数'.format(100*ext_position)

                warnnings="在基金池" + key_words + '的' + theme+"上,"
                warnnings+= position_warnnings

                if(np.abs(month_ext_ret)>=0.025):
                    warnnings+="基金池"+key_words+'的'+theme+"最近一月超额幅度显著"


                if(warnnings=="在基金池" + key_words + '的' + theme+"上,"):
                    warnnings=''

                core_pool_ind_dis.loc[core_pool_ind_dis['行业名称'] == theme, '风险提示'] = warnnings
        core_pool_ind_dis=core_pool_ind_dis[['行业名称', '中证偏股基金指数', '池', '偏离度','本月超额', '超额分位数', '风险提示']]
        core_pool_ind_dis.columns=['行业名称', '基准暴露', '池暴露', '偏离度','本月超额', '超额分位数', '风险提示']

    #get the funds alert dataframe
    funds_alert=core_pool[['基金代码', '基金名称', '当前负责人员', '任职日期', '基金经理', '经理管理规模(亿)', '入池逻辑', '入池类型',
       '策略类型', '规模偏好', '风格偏好','最大回撤', '回撤超额', '回撤同策略排名',
       '近6月信息比率', '近6月胜率', '累计净值偏离','虚拟与实际净值相关性', '业绩预警', '持仓个股预警', '持仓行业预警']]
    core_pool.drop(['最大回撤', '回撤超额', '回撤同策略排名',
       '近6月信息比率', '近6月胜率', '累计净值偏离','虚拟与实际净值相关性', '业绩预警', '持仓个股预警', '持仓行业预警'],axis=1,inplace=True)


    pool_ret=\
        pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2023-07\公募非债基金池.xlsx")
    import xlwings as xw
    if(fool_version):
        filename=r"E:\GitFolder\docs\基金池跟踪\公募池跟踪\池跟踪表模板简化版.xlsx"

    else:
        filename=r"E:\GitFolder\docs\基金池跟踪\公募池跟踪\池跟踪表模板.xlsx"
    app = xw.App(visible=False)
    wb =app.books.open(filename)

    ws = wb.sheets['Dashboard']
    ws.range("A13:BI900").clear_contents()
    ws["A13"].options(pd.DataFrame, header=1, index=False, expand='table').value = core_pool

    ws["E2"].options(pd.DataFrame, header=0, index=False, expand='table').value=pool_ret[['Unnamed: 1','基准']]/100
    ws["B10"].options( index=False).value = warnings

    style_pic['jjdm'] = [("000000" + x)[-6:] + ".OF" for x in style_pic['jjdm']]
    size_pic['jjdm'] = [("000000" + x)[-6:] + ".OF" for x in size_pic['jjdm']]
    style_pic=pd.merge(core_pool[['基金代码','基金名称']],style_pic,how='left',left_on='基金代码',right_on='jjdm').drop('jjdm',axis=1)
    size_pic = pd.merge(core_pool[['基金代码','基金名称']], size_pic, how='left', left_on='基金代码', right_on='jjdm').drop('jjdm',axis=1)

    df_list=[corr.reset_index(),ind_pic, secondary_pic,theme_pic,style_pic, size_pic,stock_pic_a, stock_pic_b,industry_contribution_list[0],ticker_con]
    if(fool_version):
        sheet_list=['池内基金相关性']
    else:
        sheet_list=['池内基金相关性','行业画像','二级行业画像','主题画像','成长价值画像','大中小盘画像','个股特征画像A','个股特征画像B','一级行业贡献','个股贡献']

    newpath = r'E:\GitFolder\docs\私募股多持仓分析\pic_temp'

    ws = wb.sheets['个基风险预警']
    ws.range("A18:U900").clear_contents()
    ws["A18"].options(pd.DataFrame, header=1, index=False, expand='table').value = funds_alert

    if (pool_name == '公募核心池'):
        ws = wb.sheets['池均衡情况_基于持仓']
        for pic in ws.pictures:
            pic.delete()

        ws["B8"].options(pd.DataFrame, header=1, index=False, expand='table').value = core_pool_ind_dis
        ws["A43"].options(pd.DataFrame, header=1, index=False, expand='table').value = core_pool_theme_dis
        ws["A63"].options(pd.DataFrame, header=1, index=False, expand='table').value = core_pool_style_dis
        # ws["O1"].options(pd.DataFrame, header=1, index=False, expand='table').value = weekly_cont

        data, layout = plot.plotly_jjpic_bar (core_pool_ind_dis[['行业名称', '基准暴露', '池暴露']].set_index('行业名称'),'穿透后行业对齐情况',legend_x=1)
        plot.save_pic2local(data, layout, newpath + r"\穿透后行业对齐")
        ws.pictures.add(newpath + r"\穿透后行业对齐.png", left=ws.range('J8').left,
                        top=ws.range('J8').top,
                        width=600, height=300)
        data, layout = plot.plotly_jjpic_bar (core_pool_theme_dis[['theme',  '基准暴露', '池暴露']].set_index('theme'),'穿透后主题对齐情况',legend_x=1)
        plot.save_pic2local(data, layout, newpath + r"\穿透后行业对齐")
        ws.pictures.add(newpath + r"\穿透后行业对齐.png", left=ws.range('J43').left,
                        top=ws.range('J43').top,
                        width=600, height=300)
        data, layout = plot.plotly_jjpic_bar (core_pool_style_dis[['风格类型',  '基准暴露', '池暴露']].set_index('风格类型'),'穿透后风格对齐情况',legend_x=1)
        plot.save_pic2local(data, layout, newpath + r"\穿透后行业对齐")
        ws.pictures.add(newpath + r"\穿透后行业对齐.png", left=ws.range('J63').left,
                        top=ws.range('J63').top,
                        width=600, height=300)


    # plot.plotly_pie(core_pool.groupby('策略类型').count()[['基金代码']],"策略类型分布",save_local_file=newpath+r"\\")
    # ws.pictures.add(newpath + r"\策略类型分布.png", left=ws.range('A54').left,
    #                 top=ws.range('A54').top,
    #                 width=500, height=300)
    #
    # plot.plotly_pie(core_pool.groupby('规模偏好').count()['基金代码'],"规模偏好分布",save_local_file=newpath+r"\\")
    # ws.pictures.add(newpath + r"\规模偏好分布.png", left=ws.range('J54').left,
    #                 top=ws.range('J54').top,
    #                 width=500, height=300)
    #
    # plot.plotly_pie(core_pool.groupby('风格偏好').count()['基金代码'],"风格偏好分布",save_local_file=newpath+r"\\")
    # ws.pictures.add(newpath + r"\风格偏好分布.png", left=ws.range('T54').left,
    #                 top=ws.range('T54').top,
    #                 width=500, height=300)
    if (pool_name == '公募核心池'):
        ws = wb.sheets['池均衡情况_基于净值']

        for pic in ws.pictures:
            pic.delete()

        pic_name='基金池风格暴露'
        data, layout=\
            plot.plotly_area(style_exp_his.pivot_table('基金池风格暴露','风格','date',).drop(['alpha', '误差']*100, axis=0),title_text=pic_name,range_upper=1)
        plot.save_pic2local(data, layout, newpath + r"\{}".format(pic_name))
        ws.pictures.add(newpath + r"\{}.png".format(pic_name), left=ws.range('B3').left,
                        top=ws.range('B3').top,
                        width=600, height=300)

        # style_exp_his['池偏离'] = style_exp_his['基金池风格暴露'] - style_exp_his['BMK风格暴露']
        data, layout=\
            plot.plotly_area(style_exp_his.pivot_table('BMK风格暴露','风格','date',).drop(['alpha', '误差']*100, axis=0),title_text='BMK风格暴露',range_upper=1)
        plot.save_pic2local(data, layout, newpath + r"\{}".format('BMK风格暴露'))

        ws.pictures.add(newpath + r"\{}.png".format('BMK风格暴露'), left=ws.range('O3').left,
                        top=ws.range('O3').top,
                        width=600, height=300)


        pic_name='基金池市值风格暴露'
        data, layout=\
            plot.plotly_area(style_exp_his2.pivot_table('基金池风格暴露','风格','date').drop(['alpha', '误差']*100, axis=0),title_text=pic_name,range_upper=1)
        plot.save_pic2local(data, layout, newpath + r"\{}".format(pic_name))
        ws.pictures.add(newpath + r"\{}.png".format(pic_name), left=ws.range('B22').left,
                        top=ws.range('B22').top,
                        width=600, height=300)

        # style_exp_his2['池偏离'] = style_exp_his2['基金池风格暴露'] - style_exp_his2['BMK风格暴露']
        data, layout=\
            plot.plotly_area(style_exp_his2.pivot_table('BMK风格暴露','风格','date').drop(['alpha', '误差']*100, axis=0),title_text='BMK市值风格暴露',range_upper=1)
        plot.save_pic2local(data, layout, newpath + r"\{}".format('BMK市值风格暴露'))

        ws.pictures.add(newpath + r"\{}.png".format('BMK市值风格暴露'), left=ws.range('O22').left,
                        top=ws.range('O22').top,
                        width=600, height=300)

        pic_name='基金池行业主题暴露'
        data, layout=\
            plot.plotly_area(theme_exp_his.pivot_table('基金池风格暴露','项目名称','date').drop(['alpha', '误差']*100, axis=0),title_text=pic_name,range_upper=1)
        plot.save_pic2local(data, layout, newpath + r"\{}".format(pic_name))
        ws.pictures.add(newpath + r"\{}.png".format(pic_name), left=ws.range('B42').left,
                        top=ws.range('B42').top,
                        width=600, height=300)

        # theme_exp_his['池偏离'] = theme_exp_his['基金池风格暴露'] - theme_exp_his['BMK风格暴露']
        data, layout=\
            plot.plotly_area(theme_exp_his.pivot_table('BMK风格暴露','风格','date').drop(['alpha', '误差']*100, axis=0),title_text='BMK行业主题暴露暴露',range_upper=1)
        plot.save_pic2local(data, layout, newpath + r"\{}".format('BMK行业主题暴露暴露'))

        ws.pictures.add(newpath + r"\{}.png".format('BMK行业主题暴露暴露'), left=ws.range('O42').left,
                        top=ws.range('O42').top,
                        width=600, height=300)


        pic_name='基金池Barra暴露'
        plot.plotly_line_style(barra_exp_his.pivot_table('基金池风格暴露','date','项目名称').drop([ '误差'], axis=1),title_text=pic_name,
                                   save_local_file=newpath+r"\\" ,line_width=0.1)

        ws.pictures.add(newpath + r"\{}.png".format(pic_name), left=ws.range('B62').left,
                        top=ws.range('B62').top,
                        width=600, height=300)

        # barra_exp_his['池偏离'] = barra_exp_his['基金池风格暴露'] - barra_exp_his['BMK风格暴露']
        plot.plotly_line_style(barra_exp_his.pivot_table('BMK风格暴露','date','项目名称').drop([ '误差'], axis=1),title_text='基准Barra暴露',
                                   save_local_file=newpath+r"\\" ,line_width=0.1)

        ws.pictures.add(newpath + r"\{}.png".format('基准Barra暴露'), left=ws.range('O62').left,
                        top=ws.range('O62').top,
                        width=600, height=300)


    #业绩归因sheet1
    ws = wb.sheets['收益归因_基于净值']
    ws.clear_contents()
    for pic in ws.pictures:
        pic.delete()

    barra_exp.index=["'"+str(x) for x in barra_exp.index]
    barra_exp.index.name='个基暴露'
    barra_ret.index=["'"+str(x) for x in barra_ret.index]
    barra_ret.index.name = '个基月度收益贡献'

    barra_exp_sector.index=["'"+str(x) for x in barra_exp.index]
    barra_exp_sector.index.name='个基暴露'
    barra_ret_sector.index=["'"+str(x) for x in barra_ret.index]
    barra_ret_sector.index.name='个基月度收益贡献'

    barra_exp_style.index=["'"+str(x) for x in barra_exp.index]
    barra_exp_style.index.name='个基暴露'
    barra_ret_style.index=["'"+str(x) for x in barra_ret.index]
    barra_ret_style.index.name='个基月度收益贡献'

    ws["A1"].options(pd.DataFrame, header=1, index=True, expand='table').value = summary_style
    ws["I1"].options(pd.DataFrame, header=1, index=True, expand='table').value = barra_exp_style
    ws["W1"].options(pd.DataFrame, header=1, index=True, expand='table').value = barra_ret_style

    ws["A13".format(3+len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = summary_sector
    ws["I{}".format(3+len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = barra_exp_sector
    ws["W{}".format(3+len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = barra_ret_sector

    ws["A24".format(6+2*len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = summary
    ws["I{}".format(6+2*len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = barra_exp
    ws["W{}".format(6+2*len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = barra_ret

    # 业绩归因sheet2
    ws = wb.sheets['收益归因_基于持仓']
    ws.clear_contents()
    for pic in ws.pictures:
        pic.delete()

    ws["A1"].options(pd.DataFrame, header=1, index=True, expand='table').value = summary_hbs
    ws["A14"].options(pd.DataFrame, header=1, index=True, expand='table').value = summary_hbs_sector


    funds_exp.index=["'"+str(x) for x in funds_exp.index]
    funds_week_ret.index=["'"+str(x) for x in funds_week_ret.index]
    funds_month_ret.index=["'"+str(x) for x in funds_month_ret.index]
    funds_exp.index.name = '个基暴露'
    funds_month_ret.index.name = '个基月度收益贡献'
    funds_week_ret.index.name = '个基周度收益贡献'


    funds_exp_sector.index=["'"+str(x) for x in funds_exp_sector.index]
    funds_week_ret_sector.index=["'"+str(x) for x in funds_week_ret_sector.index]
    funds_month_ret_sector.index=["'"+str(x) for x in funds_month_ret_sector.index]
    funds_exp_sector.index.name = '个基暴露'
    funds_month_ret_sector.index.name = '个基月度收益贡献'
    funds_week_ret_sector.index.name = '个基周度收益贡献'


    ws["I{}".format(1)].options(pd.DataFrame, header=1, index=True, expand='table').value = funds_exp
    ws["I{}".format(4+len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = funds_week_ret
    ws["I{}".format(8+2*len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = funds_month_ret

    ws["U{}".format(1)].options(pd.DataFrame, header=1, index=True, expand='table').value = funds_exp_sector
    ws["U{}".format(4+len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = funds_week_ret_sector
    ws["U{}".format(8+2*len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = funds_month_ret_sector


    ws = wb.sheets['收益归因_基于核心分类']
    ws.clear_contents()
    for pic in ws.pictures:
        pic.delete()
    ws["A1"].options(pd.DataFrame, header=1, index=False, expand='table').value = pool_summary
    pool_funds_summary.index=["'"+str(x) for x in pool_funds_summary.index]
    ws["G1"].options(pd.DataFrame, header=1, index=False, expand='table').value = pool_funds_summary


    ws = wb.sheets['基金PBROE等时序变动']
    ws.clear_contents()
    for pic in ws.pictures:
        pic.delete()
    x_position=1
    count=0
    for jjjc in core_pool['基金名称'].unique():

        if(count%2==0):
            ws.pictures.add(newpath + r"\pb时序{}.png".format(jjjc), left=ws.range('A{}'.format(int(x_position))).left,
                            top=ws.range('A{}'.format(int(x_position))).top,
                            width=700, height=350)
        else:
            ws.pictures.add(newpath + r"\pb时序{}.png".format(jjjc), left=ws.range('O{}'.format(int(x_position))).left,
                            top=ws.range('O{}'.format(int(x_position))).top,
                            width=700, height=350)
            x_position+=25

        count+=1

    if(fool_version is False):
        ws = wb.sheets['主题画像']
        for pic in ws.pictures:
            pic.delete()

        upper_range =100
        x_position=len(theme_pic)+3
        for jjjc in theme_exp['基金简称'].unique():
            data, layout = plot.plotly_area(100 * theme_exp[theme_exp['基金简称']==jjjc].set_index('jsrq').drop('基金简称',axis=1).T,
                                            '{}主题暴露时序'.format(jjjc), upper_range)
            plot.save_pic2local(data, layout, newpath + r"\{}主题暴露时序".format(jjjc))
            ws.pictures.add(newpath + r"\{}主题暴露时序.png".format(jjjc), left=ws.range('A{}'.format(int(x_position))).left, top=ws.range('A{}'.format(int(x_position))).top,
                            width=700, height=350)

            x_position+=25

        ws = wb.sheets['行业画像']
        x_position_list = ['A', 'O', 'AC', 'AQ', 'BE','BS']
        theme_list = ['大金融', '消费', 'TMT', '周期', '制造', '医药']
        lista = ['银行', '非银金融', '房地产', '食品饮料', '家用电器', '社会服务', '农林牧渔', '商贸零售', '美容护理',
                 '通信',
                 '计算机', '电子', '传媒', '钢铁', '有色金属', '建筑装饰', '建筑材料', '基础化工', '石油石化', '煤炭',
                 '交通运输', '机械设备', '汽车', '纺织服饰', '轻工制造', '电力设备', '环保', '公用事业', '医药生物']
        listb = ['大金融', '大金融', '大金融', '消费', '消费', '消费', '消费', '消费', '消费', 'TMT', 'TMT', 'TMT', 'TMT',
                 '周期', '周期', '周期', '周期', '周期', '周期', '周期', '制造', '制造', '制造', '制造', '制造', '制造',
                 '制造', '制造', '医药']
        ind2thememap = pd.DataFrame()
        ind2thememap['flmc'] = lista
        ind2thememap['theme'] = listb

        industry_w = pd.merge(industry_w, ind2thememap, how='left', on='flmc')
        for pic in ws.pictures:
            pic.delete()
        x_position=len(theme_pic)+3
        for jjdm in jjdm_list:

            i = 0
            jjjc=jjjc_data[jjjc_data['jjdm']==jjdm]['jjjc'].iloc[0]
            for theme in industry_w[(industry_w['jjdm']==jjdm)&((industry_w['theme'].isin(theme_list)))]['theme'].unique().tolist():

                upper_range =1.2 * industry_w.groupby(['jjdm','theme','jsrq']).sum().loc[jjdm,theme].max().iloc[0]
                data, layout = plot.plotly_area( (industry_w[(industry_w['jjdm']==jjdm)
                                                               &(industry_w['theme']==theme)]).pivot_table('zzjbl','jsrq','flmc').fillna(0).T,
                                                '{0}_{1}_一级行业暴露时序'.format(jjjc
                                                                                  ,theme), upper_range)
                plot.save_pic2local(data, layout, newpath + r"\{}一级行业暴露时序".format(jjjc))
                ws.pictures.add(newpath + r"\{}一级行业暴露时序.png".format(jjjc), left=ws.range('{0}{1}'
                                                                                         .format(x_position_list[i],int(x_position))).left, top=ws.range('{0}{1}'
                                                                                                                                                         .format(x_position_list[i],int(x_position))).top,
                                width=700, height=350)
                i+=1
            x_position += 25


        ws = wb.sheets['成长价值画像']
        for pic in ws.pictures:
            pic.delete()
        x_position=len(style_pic)+3
        for jjjc in theme_exp['基金简称'].unique():
            data, layout = plot.plotly_area(style_exp[style_exp['基金简称']==jjjc].pivot_table('zjbl','jsrq','style_type').T,
                                            '{}风格暴露时序'.format(jjjc), 100)
            plot.save_pic2local(data, layout, newpath + r"\{}风格暴露时序".format(jjjc))
            ws.pictures.add(newpath + r"\{}风格暴露时序.png".format(jjjc), left=ws.range('A{0}'
                                                                                   .format(int(x_position))).left
                            , top=ws.range('A{0}'.format(int(x_position))).top,width=700, height=350)

            x_position+=25

        ws = wb.sheets['大中小盘画像']
        for pic in ws.pictures:
            pic.delete()
        x_position=len(size_pic)+3
        for jjjc in theme_exp['基金简称'].unique():
            data, layout = plot.plotly_area(size_exp[size_exp['基金简称']==jjjc].pivot_table('zjbl','jsrq','size_type').T,
                                            '{}规模暴露时序'.format(jjjc), 100)
            plot.save_pic2local(data, layout, newpath + r"\{}规模暴露时序".format(jjjc))
            ws.pictures.add(newpath + r"\{}规模暴露时序.png".format(jjjc), left=ws.range('A{0}'
                                                                                   .format(int(x_position))).left
                            , top=ws.range('A{0}'.format(int(x_position))).top,width=700, height=350)

            x_position+=25

    ws = wb.sheets['收益归因_基于Brinson']
    ws.clear_contents()
    ws["A1"].options(pd.DataFrame, header=1, index=True, expand='table').value = brinson_w
    ws["A7"].options(pd.DataFrame, header=1, index=True, expand='table').value = brinson_m
    ws["A13"].options(pd.DataFrame, header=1, index=True, expand='table').value = info_t0

    ws["I1"].options(pd.DataFrame, header=1, index=True, expand='table').value = gj_t1_m
    ws["I{}".format(3+len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = gj_t2_m


    for i in range(len(sheet_list)) :

        ws = wb.sheets[sheet_list[i]]
        ws.range("C1:GZ1000").clear_contents()
        ws["C1"].options(pd.DataFrame, header=1, index=False, expand='table').value = df_list[i]
        print('{} done'.format(sheet_list[i]))


    wb.save(filename)
    wb.close()
    app.quit()
    print('done')

def prv_pool_picture(latest_date,style_date,latest_HB1001_spjg,cl_end_date,cl_start_date):


    from hbshare.fe.mutual_analysis import  nav_based as nb
    raw_data=nb.prv_pool_report(latest_date,style_date,cl_end_date,cl_start_date)


    last_3_years=str(int(str(latest_date)[0:4])-3)+str(latest_date)[4:]

    #get pool nav
    sql = "SELECT tjyf,`私募股多FOF可投_净值` from prv_pool_nav where tjyf>='{0}' and tjyf<='{1}'".format(
        str(last_3_years).replace('-', '')[0:6], str(latest_date).replace('-', '')[0:6])
    prv_pool_ret = pd.read_sql(sql, con=localdb).set_index('tjyf')
    prv_pool_ret = prv_pool_ret.pct_change()

    sql = "select spjg,tjyf from st_hedge.t_st_sm_hmzs where zsdm='HB1001' and tjyf>='{0}' and tjyf<='{1}'".format(
        str(last_3_years).replace('-', '')[0:6], str(latest_date).replace('-', '')[0:6])
    bmk_ret = hbdb.db2df(sql, db='highuser').set_index('tjyf')
    bmk_ret = bmk_ret.pct_change()

    prv_pool_ret = pd.merge(prv_pool_ret, bmk_ret, how='left', on='tjyf')
    prv_pool_ret.columns = ['私募股多基金池', '好买私募股多指数']
    prv_pool_ret['基金池月度超额'] = prv_pool_ret['私募股多基金池'] - prv_pool_ret['好买私募股多指数']


    #get pool exp history
    sql = "SELECT date,`基金池风格暴露`,`BMK风格暴露`,`项目名称`,type from pool_attribution_history_prv where date >='{0}' and date<='{1}'".format(
        str(last_3_years).replace('-', ''), str(latest_date).replace('-', ''))

    exp_data = pd.read_sql(sql, con=localdb)
    exp_data['ym'] = exp_data['date'].astype(str).str[0:6]
    exp_data.drop_duplicates(['项目名称','type','ym'],keep='last',inplace=True)

    barra_type_list =pd.concat([exp_data[(exp_data['type'] == 'barra') ].pivot_table('基金池风格暴露','date','项目名称')
                                   ,exp_data[(exp_data['type'] == 'barra') ].pivot_table('BMK风格暴露','date','项目名称')],axis=1).drop(['alpha','误差'],axis=1)
    style_type_list =pd.concat([exp_data[(exp_data['type'] == '风格') ].pivot_table('基金池风格暴露','date','项目名称')
                                   ,exp_data[(exp_data['type'] == '风格') ].pivot_table('BMK风格暴露','date','项目名称')],axis=1).drop(['alpha','误差'],axis=1)
    theme_type_list =pd.concat([exp_data[(exp_data['type'] == '行业') ].pivot_table('基金池风格暴露','date','项目名称')
                                   ,exp_data[(exp_data['type'] == '行业') ].pivot_table('BMK风格暴露','date','项目名称')],axis=1).drop(['alpha','误差'],axis=1)


    import  time

    start_date=util._shift_date(util.str_date_shift(str(latest_date),91,'-'))

    filename=r"E:\GitFolder\docs\基金池跟踪\股多池跟踪\私募主观股多池跟踪表{}.xlsx".format(latest_date)
    # fund_infor=pd.read_excel(filename,sheet_name='Dashboard',header=1)

    fund_infor=raw_data.copy()

    jjdm_list=fund_infor['基金代码'].to_list()
    jjjc_map=dict(zip(jjdm_list,fund_infor['代表产品'].to_list()))

    t0 = time.time()
    #get the barra analysis result
    summary,barra_exp,barra_ret=\
        pra.get_funds_barra_data_prv(last_month=start_date,
                                                         last_week=util._shift_date(util.str_date_shift(str(latest_date),28,'-')),
                                                     end_date=str(latest_date),jjdm_list=jjdm_list,factor_type='style'
                                     ,missing_data=latest_HB1001_spjg)
    t1 = time.time()
    print("barra归因用时: ", t1 - t0)

    for col in [ '基金池季度收益贡献', '基金池月收益贡献','BMK季度收益贡献', 'BMK月收益贡献']:
        summary[col]=summary[col].map("{:.2%}".format)
    for col in ['基金池风格暴露', 'BMK风格暴露']:
        summary[col]=summary[col].map("{:.2}".format)
    for col in barra_exp.columns:
        barra_exp[col]=barra_exp[col].map("{:.2}".format)
    for col in barra_ret.columns:
        barra_ret[col] = barra_ret[col].astype(float).map("{:.2%}".format)

    t0 = time.time()
    summary_sector,barra_exp_sector,barra_ret_sector=\
        pra.get_funds_barra_data_prv(last_month=start_date,
                                                         last_week=util._shift_date(util.str_date_shift(str(latest_date),28,'-')),
                                                     end_date=str(latest_date),jjdm_list=jjdm_list,factor_type='sector'
                                     ,missing_data=latest_HB1001_spjg)
    t1 = time.time()
    print("行业归因用时: ", t1 - t0)

    t0 = time.time()
    summary_style,barra_exp_style,barra_ret_style=\
        pra.get_funds_barra_data_prv(last_month=start_date,
                                                         last_week=util._shift_date(util.str_date_shift(str(latest_date),28,'-')),
                                                     end_date=str(latest_date),jjdm_list=jjdm_list,factor_type='style_allo'
                                     ,missing_data=latest_HB1001_spjg)

    t1 = time.time()
    print("风格归因用时: ", t1 - t0)

    t0 = time.time()
    gj_bl, gj_gx, pool_bmk_bl_gx=\
        pra.TM_regression(end_date=str(latest_date),jjdm_list=jjdm_list,latest_HB1001_spjg=latest_HB1001_spjg)
    t1 = time.time()
    print("T-M归因用时: ", t1 - t0)

    for col in [ '池(季度)贡献', '基准(季度)贡献', '池(周度)贡献', '基准(周度)贡献']:
        pool_bmk_bl_gx[col]=pool_bmk_bl_gx[col].map("{:.2%}".format)
    for col in ['池暴露', '基准暴露']:
        pool_bmk_bl_gx[col]=pool_bmk_bl_gx[col].map("{:.2}".format)
    for col in gj_bl.columns:
        gj_bl[col]=gj_bl[col].map("{:.2}".format)
    for col in gj_gx.columns:
        gj_gx[col] = gj_gx[col].astype(float).map("{:.2%}".format)



    for col in summary.columns:
        summary_sector[col]=summary_sector[col].map("{:.2%}".format)
        summary_style[col]=summary_style[col].map("{:.2%}".format)
    for col in barra_exp_sector.columns:
        barra_exp_sector[col]=barra_exp_sector[col].map("{:.2%}".format)
    for col in barra_ret_sector.columns:
        barra_ret_sector[col]=barra_ret_sector[col].map("{:.2%}".format)
    for col in barra_exp_style.columns:
        barra_exp_style[col]=barra_exp_style[col].map("{:.2%}".format)
    for col in barra_ret_style.columns:
        barra_ret_style[col]=barra_ret_style[col].map("{:.2%}".format)

    summary.index.name='Barra归因汇总'
    barra_exp.index=[jjjc_map[x] for x in barra_exp.index ]
    barra_exp.index.name='个基Barra因子暴露'
    barra_ret.index=[jjjc_map[x] for x in barra_ret.index ]
    barra_ret.index.name='个基Barra因子收益'

    summary_sector.index.name='行业主题归因汇总'
    barra_exp_sector.index=[jjjc_map[x] for x in barra_exp_sector.index ]
    barra_exp_sector.index.name='个基行业主题暴露'
    barra_ret_sector.index=[jjjc_map[x] for x in barra_ret_sector.index ]
    barra_ret_sector.index.name='个基行业主题收益'

    summary_style.index.name='风格归因汇总'
    barra_exp_style.index=[jjjc_map[x] for x in barra_exp_style.index ]
    barra_exp_style.index.name='个基风格暴露'
    barra_ret_style.index=[jjjc_map[x] for x in barra_ret_style.index ]
    barra_ret_style.index.name='个基风格收益'

    pool_bmk_bl_gx.index.name='T-M归因汇总'
    gj_bl.index=[jjjc_map[x] for x in gj_bl.index ]
    gj_bl.index.name='个基T-M因子暴露'
    gj_gx.index=[jjjc_map[x] for x in gj_gx.index ]
    gj_gx.index.name='个基T-M因子收益'



    #pool alert part

    last_5_years=str(int(latest_date)-50000)

    sql=("select trade_date,consuming as '消费',manufacture as '制造',bigfinance as '大金融',tmt as 'TMT',cycle as '周期' from st_market.r_st_sector_factor where trade_date>='{0}' and trade_date<='{1}' and m_opt_type!='03'"
         .format(last_5_years,latest_date))
    theme_ret=hbdb.db2df(sql,db='alluser').set_index('trade_date')[['TMT', '制造', '周期', '大金融', '消费']]*100

    sql=("select jyrq,hbdr,zqdm from st_market.t_st_zs_rhb where jyrq>='{0}' and jyrq<='{1}' and m_opt_type!='03' and zqdm in ('399376','399374','399375','399377','399372','399373','399303','881001')"
         .format(last_5_years,latest_date))
    style_ret=hbdb.db2df(sql,db='alluser').pivot_table('hbdr','jyrq','zqdm')
    style_ret.columns=['国证2000','大盘成长','大盘价值','中盘成长','中盘价值','小盘成长','小盘价值','万得全A']
    style_ret.index=style_ret.index.astype(str)

    theme_ret=pd.merge(theme_ret,style_ret[['万得全A']],how='left',
                       left_index=True,right_index=True)
    theme_ret=theme_ret.sub(theme_ret['万得全A'], axis=0).drop('万得全A',axis=1)
    style_ret=style_ret.sub(style_ret['国证2000'], axis=0).drop(['万得全A','国证2000'],axis=1)

    theme_ret=(theme_ret/ 100 + 1).cumprod()
    style_ret=(style_ret/ 100 + 1).cumprod()


    theme_div=pd.DataFrame(columns=['TMT', '中证全债', '制造', '周期', '大金融', '消费'])
    for i in range(6):
        theme_div[theme_div.columns[i]]=[(
                theme_type_list.iloc[-1:].T.iloc[i].values[0]-theme_type_list.iloc[-1:].T.iloc[i+6].values[0])]
    theme_div = theme_div.drop('中证全债',axis=1)

    style_div=pd.DataFrame(columns=['中盘价值', '中盘成长', '中证全债', '大盘价值', '大盘成长', '小盘价值', '小盘成长'])
    for i in range(7):
        style_div[style_div.columns[i]]=[(
                style_type_list.iloc[-1:].T.iloc[i].values[0]-style_type_list.iloc[-1:].T.iloc[i+7].values[0])]
    style_div = style_div[['大盘成长','大盘价值','中盘成长','中盘价值','小盘成长','小盘价值']]

    pool_div=pd.concat([theme_div,style_div],axis=1)
    pool_div.index=['基金池偏离度']
    pool_div.loc['近30天收益']=((theme_ret.iloc[-1]/theme_ret.iloc[-30]-1).tolist()+
                          (style_ret.iloc[-1]/style_ret.iloc[-30]-1).tolist())

    pool_div.loc['超额分位数'] =(
            theme_ret.rolling(250*3).rank(pct = True).iloc[-1].tolist()+
            style_ret.rolling(250*3).rank(pct = True).iloc[-1].tolist())

    theme_ret[[x+'75分位数' for x in ['TMT', '制造', '周期', '大金融', '消费']]]=(
        theme_ret[['TMT', '制造', '周期', '大金融', '消费']].rolling(250 * 3).quantile(0.75))
    theme_ret[[x+'25分位数' for x in ['TMT', '制造', '周期', '大金融', '消费']]]=(
        theme_ret[['TMT', '制造', '周期', '大金融', '消费']].rolling(250 * 3).quantile(0.25))

    style_ret[[x+'75分位数' for x in ['大盘成长','大盘价值','中盘成长','中盘价值','小盘成长','小盘价值']]]=(
        style_ret[['大盘成长','大盘价值','中盘成长','中盘价值','小盘成长','小盘价值']].rolling(250 * 3).quantile(0.75))
    style_ret[[x+'25分位数' for x in ['大盘成长','大盘价值','中盘成长','中盘价值','小盘成长','小盘价值']]]=(
        style_ret[['大盘成长','大盘价值','中盘成长','中盘价值','小盘成长','小盘价值']].rolling(250 * 3).quantile(0.25))



    import xlwings as xw

    app = xw.App(visible=False)
    wb =app.books.open(filename)

    ws=wb.sheets['基金池基本特征']
    ws.range('A1:C100').clear_contents()
    ws["A1"].options(pd.DataFrame, header=1, index=True, expand='table').value = prv_pool_ret.iloc[-35:]


    ws=wb.sheets['分策略收益']
    ws.range('A2:BZ200').clear_contents()

    i=0
    for f_type in raw_data['策略类型'].unique():

        ws[(1,i*5)].options(pd.DataFrame, header=1, index=False, expand='table').value=(
            raw_data)[raw_data['策略类型']==f_type][['管理人','基金经理','近一月','今年以来']]
        i+=1

    for f_type in ['稳健成长','成长','激进成长','均衡','深度价值','价值','积极价值']:

        ws[(1,i*5)].options(pd.DataFrame, header=1, index=False, expand='table').value=(
            raw_data)[raw_data['风格2']==f_type][['管理人','基金经理','近一月','今年以来']]
        i+=1


    ws[(1,i*5)].options(pd.DataFrame, header=1, index=False, expand='table').value = (
        raw_data)[raw_data['最近3个月最大回撤'].str.replace('%','').astype(float)/100>=0.1 ][['管理人', '基金经理', '最近3个月最大回撤']]
    i += 1
    ws[(1,i*5-1)].options(pd.DataFrame, header=1, index=False, expand='table').value = (
        raw_data)[raw_data['最近6个月最大回撤'].str.replace('%','').astype(float)/100 >= 0.15 ][['管理人', '基金经理', '最近6个月最大回撤']]
    i += 1
    ws[(1,i*5-2)].options(pd.DataFrame, header=1, index=False, expand='table').value = (
        raw_data)[raw_data['最近一年最大回撤'].str.replace('%','').astype(float)/100 >=0.2][['管理人', '基金经理', '最近一年最大回撤']]
    i += 1

    ws=wb.sheets['基金池风格暴露']
    ws.range('A2:AW100').clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=True, expand='table').value = barra_type_list.iloc[-36:]
    ws["V2"].options(pd.DataFrame, header=1, index=True, expand='table').value = style_type_list.iloc[-36:]
    ws["AK2"].options(pd.DataFrame, header=1, index=True, expand='table').value = theme_type_list.iloc[-36:]

    ws=wb.sheets['基金池风格收益归因']
    ws["A1"].options(pd.DataFrame, header=1, index=True, expand='table').value = summary_style
    ws["A13".format(3+len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = summary_sector
    ws["A24".format(5+2*len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = pool_bmk_bl_gx
    ws["A32".format(2+3*len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = summary

    plot=functionality.Plot(1000,700)
    newpath = r'E:\GitFolder\docs\私募股多持仓分析\pic_temp'
    ws=wb.sheets['基金池预警']
    ws.range("A2:L4").clear_contents()
    for pic in ws.pictures:
        pic.delete()

    ws["A1"].options(pd.DataFrame, header=1, index=True, expand='table').value = pool_div
    i=0
    for col in ['TMT', '制造', '周期', '大金融', '消费']:
        plot.plotly_line_style(theme_ret[[col,col+'75分位数',col+'25分位数']].iloc[-500:],
                               title_text=col+'净值时序', save_local_file=newpath + r"\\")
        ws.pictures.add(newpath + r"\{}.png".format(col+'净值时序'), left=ws.range('A{}'.format(7+i*17)).left,
                        top=ws.range('A{}'.format(7+i*17)).top,
                        width=500, height=250)
        i+=1
    i = 0
    for col in ['大盘成长', '大盘价值', '中盘成长', '中盘价值', '小盘成长', '小盘价值']:
        plot.plotly_line_style(style_ret[[col,col+'75分位数',col+'25分位数']].iloc[-500:],
                               title_text=col+'净值时序', save_local_file=newpath + r"\\")
        ws.pictures.add(newpath + r"\{}.png".format(col+'净值时序'), left=ws.range('L{}'.format(7+i*17)).left,
                        top=ws.range('L{}'.format(7+i*17)).top,
                        width=500, height=250)
        i+=1

    ws = wb.sheets['原始数据']
    ws.clear_contents()
    ws["A1"].options(pd.DataFrame, header=1, index=False, expand='table').value = raw_data

    ws = wb.sheets['个基收益归因']
    ws.clear_contents()

    # ws["A1"].options(pd.DataFrame, header=1, index=True, expand='table').value = summary_style
    ws["A1"].options(pd.DataFrame, header=1, index=True, expand='table').value = barra_exp_style
    ws["O1"].options(pd.DataFrame, header=1, index=True, expand='table').value = barra_ret_style

    # ws["A13".format(3+len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = summary_sector
    ws["A{}".format(3+len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = barra_exp_sector
    ws["O{}".format(3+len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = barra_ret_sector

    # ws["A24".format(5+2*len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = pool_bmk_bl_gx
    ws["A{}".format(5+2*len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = gj_bl
    ws["O{}".format(5+2*len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = gj_gx

    # ws["A32".format(2+3*len(jjdm_list))].options(pd.DataFrame, header=1, index=True, expand='table').value = summary
    ws["A{}".format(7+3*len(gj_bl))].options(pd.DataFrame, header=1, index=True, expand='table').value = barra_exp
    ws["O{}".format(7+3*len(gj_bl))].options(pd.DataFrame, header=1, index=True, expand='table').value = barra_ret


    wb.save(filename)
    wb.close()
    app.quit()
    print('done')

def save_fund_industry_weight_his_tolocal(jjdm_list,start_date,end_date,
                                          dir=r"E:\GitFolder\docs\个基研究",zclb='2',hyhfbz='2'):

    sql="select jjdm,jsrq,flmc,zzjbl from st_fund.t_st_gm_jjhyzhyszb where hyhfbz='{0}' and zclb='{1}' and jjdm in ({2}) and jsrq>='{3}' and jsrq<='{4}' "\
        .format(hyhfbz,zclb,util.list_sql_condition(jjdm_list),start_date,end_date)
    industry_w=hbdb.db2df(sql,db='funduser')

    industry_w.to_excel(dir+"\基金行业持仓权重.xlsx")

def calculate_cat_std(asofdate,jjdm_list,weight_list):

    sql="select jjdm,zblb,zbnp from st_hedge.t_st_sm_rqjhb where jjdm in {0} and jzrq={1} and zblb in ('2107','2101','2103','2106','2201','2202','2203') and zbnp!=99999"\
        .format(tuple(jjdm_list),int(asofdate))
    funds_return_summary=hbdb.db2df(sql,db='highuser').pivot_table('zbnp','jjdm','zblb')

    sql="select jjdm,hb1z/100 as hb1z,rqzh from st_hedge.t_st_sm_zhb where jjdm in {0} and rqzh>='{1}' and rqzh<='{2}' and hb1z!=99999"\
        .format(tuple(jjdm_list),util.str_date_shift(asofdate,180,'-'),asofdate)
    funds_return=hbdb.db2df(sql,db='highuser').pivot_table('hb1z','rqzh','jjdm')
    funds_std=funds_return.std()*np.sqrt(52)
    cov_mat=funds_return.cov()

    weight_list=weight_list.loc[cov_mat.columns]
    weight_list['weight']=weight_list['weight']/weight_list['weight'].sum()

    from hbshare.quant.CChen import  func
    portfolio_var=\
        np.sqrt( func.portfolio_var(weight_list['weight'],cov_mat)*52)
    risk_contri=func.risk_contribute(weight_list['weight'],cov_mat)

    risk_contri=[x[0]*np.sqrt(52) for x in risk_contri.tolist()]


    return funds_std,funds_return_summary,portfolio_var,risk_contri

def cta_track(asofdate,dir):

    pool_de=pd.read_excel(dir
                          ,sheet_name='量化池列表')
    pool_fo=pd.read_excel(dir
                          ,sheet_name='量化海外池')

    import xlwings as xw
    filename=r"E:\GitFolder\docs\基金池跟踪\CTA基金池跟踪.xlsx"

    app = xw.App(visible=False)
    wb =app.books.open(filename)


    plot=functionality.Plot(600,300)
    newpath = r'E:\GitFolder\docs\私募股多持仓分析\pic_temp'

    def get_sub_pool_pic(pool_sub,title,ws,position='F1',if_sub_pool=True):

        pool_sub=pool_sub[pool_sub['一级策略']=='CTA']
        weight_list=pool_sub[['基金代码']]
        weight_list['weight']=1/len(weight_list)

        funds_std,funds_return_summary,portfolio_var,risk_contri=\
            calculate_cat_std(asofdate, pool_sub['基金代码'].tolist(),
                  weight_list.set_index('基金代码'))

        plot.plotly_hist(funds_std.to_frame('std'),title+'产品波动率分布',save_local_file=newpath+r"\\")
        ws.pictures.add(newpath + r"\{}.png".format(title+'产品波动率分布'), left=ws.range(position).left,
                        top=ws.range(position).top,
                        width=600, height=300)
        if(if_sub_pool):
            return portfolio_var
        else:
            return  funds_return_summary,portfolio_var,funds_std


    ws = wb.sheets['池跟踪']
    ws.clear_contents()

    pools_var=pd.DataFrame()
    funds_return_summary,pool_var,funds_std=get_sub_pool_pic(pool_de,'CTA国内',ws,'F1',if_sub_pool=False)
    pools_var['国内CTA整体波动率']=[pool_var]
    pools_var['国内CTA代销波动率']=[get_sub_pool_pic(pool_de[pool_de['子池'] == '代销'],'CTA国内代销',ws,'F24')]
    pools_var['国内CTAFOF波动率']=[get_sub_pool_pic(pool_de[pool_de['子池'] != '代销'],'CTA国内FOF',ws,'F47')]
    ws["A1"].options(pd.DataFrame, header=1, index=False, expand='table').value = pools_var


    ws = wb.sheets['个基跟踪']

    funds_std=funds_std.to_frame('年化波动率')
    threshield=(funds_std.mean() + 2 * funds_std.std()).values[0]
    funds_std.loc[funds_std['年化波动率']>=threshield,'波动率预警']='基金波动率较高'

    funds_return_summary.columns=['近一月','近三月','近六月','近一年','近两年','近三年']
    funds_summary_df=pool_de[pool_de['一级策略']=='CTA'][['子池','基金管理人','代表产品','基金代码']]
    funds_summary_df=pd.merge(funds_summary_df,funds_return_summary,how='left',left_on='基金代码',right_index=True)
    funds_summary_df=pd.merge(funds_summary_df,funds_std,how='left',left_on='基金代码',right_index=True)

    ws.range("A2:U900").clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=False, expand='table').value = funds_summary_df


    wb.save(filename)
    wb.close()
    app.quit()
    print('done')

def FOF_track_pic(product,start_date,end_date,prv_alter_date):


    from hbshare.fe.FOF.fof_analysis import  FOF_analysis
    import hbshare.fe.FOF.fof_analysis as fofa

    fa = FOF_analysis(dir=r"E:\FOF分析\{}\交易流水.xlsx"
                      .format(product), end_date=end_date)

    fa.valuation_table_analysis(product=product, start_date=start_date, end_date=end_date)

    attribution_by_class,ret_cont_his_table,ret_his_table,yj_weight_his,cyj_weight_his,hold_df=\
        fa.holding_analysis_for_weekly_tracking(dir=r"E:\FOF分析\{}\基金持仓数据.xlsx".format(product),
                        start_date=start_date, end_date=end_date, CTA_bmk_w=1 / 3, stock_bmk_w=1 / 3,
                        bond_bmk_w=1 / 3)

    hold_last_date=hold_df['date'].max()
    mutual_asset_list = list(set(yj_weight_his.columns).intersection(
        set(['灵活配置型', '偏股混合型', '普通股票型'])))
    yj_weight_his['公募偏股']=yj_weight_his[mutual_asset_list].sum(axis=1)
    attack_asset_list = list(set(yj_weight_his.columns).intersection(
        set(['公募偏股', '主观多头', '量化多头'])))


    asset_annually_ret,asset_vol,asset_corr,asset_VAR,fof_stress_test=(
        fofa.get_super_asset_index_stats(hold_df[hold_df['date']==hold_last_date][['jjdm', 'jjjc','yjcl','cpfl','ejfl','weight']],hold_last_date))


    core_pool=\
        hold_df[(hold_df['cpfl'] == '公募基金')
                & (hold_df['yjcl'] == '进攻性资产')
                &(hold_df['ejfl']!='偏债混合型')&(hold_df['date']==hold_last_date)][['jjdm','jjjc','weight']]
    core_con=hold_df[(hold_df['cpfl'] == '公募基金')
        & (hold_df['yjcl'] == '进攻性资产')
        & (hold_df['ejfl'] != '偏债混合型') ].groupby('jjjc')['contribute_ret'].sum()
    core_pool=pd.merge(core_pool,core_con.to_frame('cont'),how='outer',on='jjjc')
    core_pool.columns=['基金代码','基金简称','权重','累计贡献']
    core_total_w=core_pool['权重'].sum()
    core_pool['权重']=core_pool['权重']/core_total_w

    jjdm_list=\
        core_pool[core_pool['基金代码'].notnull()]['基金代码'].unique().tolist()

    def mutual_fund_attr_resoning(jjdm_list,last_month,last_week,end_date,bmk_id,core_pool):


        #get the barra analysis result
        summary,barra_exp,barra_ret=\
            pra.get_funds_barra_data(last_month=last_month,last_week=last_week,
                                                         end_date=str(end_date),jjdm_list=jjdm_list,factor_type='style',bmk_id=bmk_id)
        summary_sector,barra_exp_sector,barra_ret_sector=\
            pra.get_funds_barra_data(last_month=last_month,last_week=last_week,
                                                         end_date=str(end_date),jjdm_list=jjdm_list,factor_type='sector',bmk_id=bmk_id)
        summary_style,barra_exp_style,barra_ret_style=\
            pra.get_funds_barra_data(last_month=last_month,last_week=last_week,
                                                         end_date=str(end_date),jjdm_list=jjdm_list,factor_type='style_allo',bmk_id=bmk_id)


        summary=calculate_portfolio_summary(summary,barra_exp,barra_ret,core_pool)
        summary_sector=calculate_portfolio_summary(summary_sector,barra_exp_sector,barra_ret_sector,core_pool)
        summary_style=calculate_portfolio_summary(summary_style,barra_exp_style,barra_ret_style,core_pool)

        sql="select jjjc,jjdm from st_fund.t_st_gm_jjxx where jjdm in {} ".format(tuple(jjdm_list))
        jjjc=hbdb.db2df(sql,db='funduser')

        jjjc=pd.merge(barra_exp,jjjc,how='left',left_index=True,right_on='jjdm')['jjjc'].tolist()
        barra_exp.index=jjjc
        barra_ret.index=jjjc
        barra_exp_sector.index=jjjc
        barra_ret_sector.index=jjjc
        barra_exp_style.index=jjjc
        barra_ret_style.index=jjjc

        barra_exp.index.name='个基风格暴露'
        barra_ret.index.name='个基风格贡献'
        barra_exp_sector.index.name='个基风格暴露'
        barra_ret_sector.index.name='个基风格贡献'
        barra_exp_style.index.name='个基风格暴露'
        barra_ret_style.index.name='个基风格贡献'

        return [summary.drop(['基金池周收益贡献','BMK周收益贡献'],axis=1),barra_exp,barra_ret,\
            summary_sector.drop(['基金池周收益贡献','BMK周收益贡献'],axis=1),barra_exp_sector,barra_ret_sector,\
            summary_style.drop(['基金池周收益贡献','BMK周收益贡献'],axis=1),barra_exp_style,barra_ret_style]

    def prv_fund_attr_resoning(jjdm_list,last_month,last_week,end_date,core_pool):


        sql="select count(hbdr),jjdm from st_hedge.t_st_rhb where jjdm in {0} and  jzrq>='{1}' and jzrq<='{2}' group by jjdm"\
            .format(tuple(jjdm_list),last_month,end_date)
        data_check=hbdb.db2df(sql,db='highuser')

        print("以下基金无法取得净值数据:{}".format(tuple( set(jjdm_list).difference(set(data_check['jjdm'].tolist())) )))

        jjdm_list=data_check['jjdm'].tolist()

        total_w = core_pool[core_pool['基金代码'].isin(jjdm_list)]['权重'].sum()
        core_pool['权重'] = \
            core_pool['权重'] / total_w

        #get the barra analysis result
        summary, barra_exp, barra_ret = \
            pra.get_funds_barra_data_prv(last_month=last_month,
                                         last_week=last_week,
                                         end_date=end_date, jjdm_list=jjdm_list, factor_type='style'
                                         )
        summary_sector, barra_exp_sector, barra_ret_sector = \
            pra.get_funds_barra_data_prv(last_month=last_month,
                                         last_week=last_week,
                                         end_date=end_date, jjdm_list=jjdm_list, factor_type='sector'
                                         )
        summary_style, barra_exp_style, barra_ret_style = \
            pra.get_funds_barra_data_prv(last_month=last_month,
                                         last_week=last_week,
                                         end_date=end_date, jjdm_list=jjdm_list, factor_type='style_allo'
                                         )


        summary=calculate_portfolio_summary(summary,barra_exp,barra_ret,core_pool)
        summary_sector=calculate_portfolio_summary(summary_sector,barra_exp_sector,barra_ret_sector,core_pool)
        summary_style=calculate_portfolio_summary(summary_style,barra_exp_style,barra_ret_style,core_pool)

        sql = "select jjjc,jjdm from st_hedge.t_st_jjxx where jjdm in {} ".format(tuple(jjdm_list))
        jjjc = hbdb.db2df(sql, db='highuser')

        jjjc = pd.merge(barra_exp, jjjc, how='left', left_index=True, right_on='jjdm')['jjjc'].tolist()
        barra_exp.index = jjjc
        barra_ret.index = jjjc
        barra_exp_sector.index = jjjc
        barra_ret_sector.index = jjjc
        barra_exp_style.index = jjjc
        barra_ret_style.index = jjjc

        barra_exp.index.name = '个基风格暴露'
        barra_ret.index.name = '个基风格贡献'
        barra_exp_sector.index.name = '个基风格暴露'
        barra_ret_sector.index.name = '个基风格贡献'
        barra_exp_style.index.name = '个基风格暴露'
        barra_ret_style.index.name = '个基风格贡献'



        return [summary.drop(['基金池月收益贡献','BMK月收益贡献','基金池周收益贡献'],axis=1),barra_exp,barra_ret,\
            summary_sector.drop(['基金池月收益贡献','BMK月收益贡献','基金池周收益贡献'],axis=1),barra_exp_sector,barra_ret_sector,\
            summary_style.drop(['基金池月收益贡献','BMK月收益贡献','基金池周收益贡献'],axis=1),barra_exp_style,barra_ret_style],total_w

    mutual_attr_list=mutual_fund_attr_resoning(jjdm_list,util._shift_date(util.str_date_shift(str(end_date),30,'-'))
                                         ,util._shift_date(util.str_date_shift(str(end_date),7,'-'))
                                         ,str(end_date),'930950',core_pool)

    core_pool['权重']=core_pool['权重']*core_total_w

    mutual_funds_alert=pd.read_excel(r"E:\GitFolder\docs\基金池跟踪\公募池跟踪\公募基金跟踪池.xlsx",sheet_name='个基预警',header=17)
    mutual_funds_alert['基金代码']=mutual_funds_alert['基金代码'].str[0:6]

    mutual_funds_alert=pd.merge(core_pool,mutual_funds_alert,how='left',on='基金代码')
    mutual_funds_alert.loc[mutual_funds_alert['基金代码'].isnull(),'最大回撤']='基金已经被移除核心池，请经理尽快调整'
    # mutual_funds_alert['基金名称']=mutual_attr_list[1].index

    prv_core_pool=\
        hold_df[(hold_df['cpfl'] == '私募基金')
                & (hold_df['yjcl'] == '进攻性资产')& (hold_df['ejfl'] == '主观多头')&(hold_df['date']==hold_last_date)
                ][['jjdm','jjjc','weight']]

    prv_con=hold_df[(hold_df['cpfl'] == '私募基金')
        & (hold_df['yjcl'] == '进攻性资产')
        & (hold_df['ejfl'] == '主观多头') ].groupby('jjjc')['contribute_ret'].sum()
    prv_core_pool=pd.merge(prv_core_pool,prv_con.to_frame('cont'),how='outer',on='jjjc')

    prv_core_pool.columns=['基金代码','基金简称','权重','累计贡献']


    jjdm_list=\
        prv_core_pool[prv_core_pool['基金代码'].notnull()]['基金代码'].unique().tolist()

    prv_attr_list,prv_total_w=prv_fund_attr_resoning(jjdm_list,util._shift_date(util.str_date_shift(str(end_date),91,'-'))
                                         ,util._shift_date(util.str_date_shift(str(end_date),28,'-'))
                                         ,str(end_date),prv_core_pool)

    # prv_core_pool['权重']=prv_core_pool['权重']*prv_total_w

    sql="select jjdm,jjjc,sjglr,glrm from st_hedge.t_st_jjxx where jjdm in {}".format(tuple(jjdm_list))
    prv_base_info=hbdb.db2df(sql,db='highuser')
    prv_base_info.loc[prv_base_info['sjglr'].isnull(),'sjglr']=prv_base_info[prv_base_info['sjglr'].isnull()]['glrm']
    sql="select jgdm,jgjc from st_main.t_st_gg_jgxx where jgdm in {0}"\
        .format(tuple(prv_base_info['sjglr'].unique().tolist()))
    jgmc=hbdb.db2df(sql,db='alluser')
    sql="select rydm,jjdm from st_hedge.t_st_jjjl where ryzt=-1 and jjdm in {} "\
        .format(tuple(jjdm_list))
    prv_manager=hbdb.db2df(sql,db='highuser')
    sql="select rydm,ryxm from st_hedge.t_st_sm_jlpf where rydm in {0}"\
        .format(tuple(prv_manager['rydm'].unique()))
    prv_manager=pd.merge(prv_manager,hbdb.db2df(sql,db='highuser'),how='left',on='rydm').drop_duplicates(['jjdm','rydm'],keep='last')
    prv_base_info=pd.merge(prv_base_info,jgmc,how='left',left_on='sjglr',right_on='jgdm')
    prv_base_info=pd.merge(prv_base_info,prv_manager,how='left',on='jjdm')

    prv_alter=\
        pd.read_excel(r"E:\GitFolder\docs\基金池跟踪\股多池跟踪\私募主观股多池跟踪表{}.xlsx".format(prv_alter_date)
                      ,sheet_name='预警',header=1)[['管理人', '基金经理','策略类型', '金工标签','配置预警', '行业变动预警']]
    prv_base_info=\
        pd.merge(prv_base_info,prv_alter,
                 left_on=['jgjc','ryxm'],right_on=['管理人','基金经理']
                 ,how='left').drop(['jgjc','ryxm','sjglr', 'glrm','jgdm', 'rydm'],axis=1)
    prv_base_info=prv_base_info[prv_base_info['管理人'].notnull()]
    prv_base_info.rename(columns={'jjdm': '基金代码', 'jjjc': '基金简称'}, inplace=True)


    #quant pool contribution

    quant_core_pool=\
        hold_df[(hold_df['cpfl'] == '私募基金')
                & (hold_df['yjcl'] == '进攻性资产')& (hold_df['ejfl'] == '量化多头')&(hold_df['date']==hold_last_date)
                ][['jjdm','jjjc','weight']]

    quant_con=hold_df[(hold_df['cpfl'] == '私募基金')
        & (hold_df['yjcl'] == '进攻性资产')
        & (hold_df['ejfl'] == '量化多头') ].groupby('jjjc')['contribute_ret'].sum()
    quant_core_pool=pd.merge(quant_core_pool,quant_con.to_frame('cont'),how='outer',on='jjjc')

    quant_core_pool.columns=['基金代码','基金简称','权重','累计贡献']

    # quant_total_w=quant_core_pool[quant_core_pool['基金代码'].notnull()]['权重'].sum()
    # quant_core_pool['权重']=\
    #     quant_core_pool['权重']/quant_total_w

    jjdm_list=\
        quant_core_pool[quant_core_pool['基金代码'].notnull()]['基金代码'].unique().tolist()

    quant_attr_list,quant_total_w=prv_fund_attr_resoning(jjdm_list,util._shift_date(util.str_date_shift(str(end_date),91,'-'))
                                         ,util._shift_date(util.str_date_shift(str(end_date),28,'-'))
                                         ,str(end_date),quant_core_pool)

    quant_core_pool['权重']=quant_core_pool['权重']*quant_total_w


    #
    attack_asset_attr_list=[]
    attack_asset_attr_list.append((prv_attr_list[0]*prv_total_w+
                                   mutual_attr_list[0]*core_total_w+
                                   quant_attr_list[0]*quant_total_w)[['基金池风格暴露', 'BMK风格暴露']].drop(['alpha','误差']
                                                                                                             ,axis=0)/(prv_total_w+core_total_w+quant_total_w))
    attack_asset_attr_list.append((prv_attr_list[3]*prv_total_w+
                                   mutual_attr_list[3]*core_total_w+
                                   quant_attr_list[3]*quant_total_w)[['基金池风格暴露', 'BMK风格暴露']].drop(['alpha','误差']
                                                                                                             ,axis=0)/(prv_total_w+core_total_w+quant_total_w))
    attack_asset_attr_list.append((prv_attr_list[6]*prv_total_w+
                                   mutual_attr_list[6]*core_total_w+
                                   quant_attr_list[6]*quant_total_w)[['基金池风格暴露', 'BMK风格暴露']].drop(['alpha','误差']
                                                                                                             ,axis=0)/(prv_total_w+core_total_w+quant_total_w))

    def get_alert_df(asset_annually_ret,name='资产年化收益率'):

        ejfl2_alert=asset_annually_ret[['FOF：进攻性资产', 'FOF：CTA', 'FOF：稳健性资产', 'FOF：公募偏股', 'FOF：量化多头',
           'FOF：主观多头']].iloc[-1].to_frame(name)
        ejfl2_alert['预警上限']=(asset_annually_ret[
            ['基准：进攻性资产', '基准：CTA', '基准：稳健性资产', '基准：公募偏股', '基准：量化多头', '基准：主观多头']].mean()+asset_annually_ret[
            ['基准：进攻性资产', '基准：CTA', '基准：稳健性资产', '基准：公募偏股', '基准：量化多头', '基准：主观多头']].std()).tolist()
        ejfl2_alert['预警下限']=(asset_annually_ret[
            ['基准：进攻性资产', '基准：CTA', '基准：稳健性资产', '基准：公募偏股', '基准：量化多头', '基准：主观多头']].mean()-asset_annually_ret[
            ['基准：进攻性资产', '基准：CTA', '基准：稳健性资产', '基准：公募偏股', '基准：量化多头', '基准：主观多头']].std()).tolist()

        return ejfl2_alert

    ejfl2_alert_ret=get_alert_df(asset_annually_ret,'资产年化收益率')
    ejfl2_alert_vol=get_alert_df(asset_vol,'资产年化波动率')
    ejfl2_alert_var=get_alert_df(asset_VAR,'资产年收益VAR')

    ejfl2_alert_ret.index=[x.replace('FOF：','') for x in  ejfl2_alert_ret.index]
    ejfl2_alert_vol.index=[x.replace('FOF：','') for x in  ejfl2_alert_vol.index]
    ejfl2_alert_var.index=[x.replace('FOF：','') for x in  ejfl2_alert_var.index]

    #cta alert

    cta_pool= hold_df[(hold_df['yjcl']=='CTA')&(hold_df['date']==hold_last_date)][['jjdm','jjjc','weight']]

    cta_con=hold_df[(hold_df['yjcl'] == 'CTA') ].groupby('jjjc')['contribute_ret'].sum()
    cta_pool=pd.merge(cta_pool,cta_con.to_frame('cont'),how='left',on='jjjc')

    cta_total_w=cta_pool['weight'].sum()

    cta_funds_std,cta_funds_return_summary,cta_portfolio_var,cta_risk_contri\
        =calculate_cat_std(end_date, cta_pool['jjdm'].tolist(), cta_pool.set_index('jjdm'))
    cta_funds_std=cta_funds_std.to_frame('年化波动率')
    cta_funds_std['波动率贡献']=cta_risk_contri
    cta_funds_std=pd.merge(cta_funds_std,cta_funds_return_summary/100,how='left',on='jjdm')
    cta_funds_std=pd.merge(cta_pool,cta_funds_std,how='left',on='jjdm')
    cta_funds_std.columns=['基金代码','基金简称', '持仓权重','累计贡献', '年化波动率', '波动率贡献', '最近一月', '最近3月',
                           '最近6月', '最近1年', '最近2年','最近3年', ]
    cta_funds_std['持仓权重']=cta_funds_std['持仓权重']*cta_total_w


    import xlwings as xw
    filename=r"E:\GitFolder\docs\基金池跟踪\FOF跟踪表\大类配置FOF跟踪表样例.xlsx"
    app = xw.App(visible=False)
    wb =app.books.open(filename)

    plot=functionality.Plot(800,700)
    newpath = r'E:\GitFolder\docs\私募股多持仓分析\pic_temp'

    ws = wb.sheets['资产占比']
    ws.range("A2:Z300").clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=False, expand='table').value = cyj_weight_his.rename(columns={'date':'日期'}).iloc[-60:]
    ws["E2"].options(pd.DataFrame, header=1, index=False, expand='table').value = yj_weight_his.rename(columns={'date':'日期'})[['日期']+attack_asset_list].iloc[-60:]

    ws = wb.sheets['资产贡献']
    ws.range("A2:Z300").clear_contents()
    ret_cont_his_table.index.name='日期'
    ws["A2"].options(pd.DataFrame, header=1, index=True, expand='table').value = ret_cont_his_table.iloc[-60:]


    ws = wb.sheets['资产收益率']
    ws.range("A2:Z62").clear_contents()
    ret_his_table.index.name='日期'
    ws["A2"].options(pd.DataFrame, header=1, index=True, expand='table').value = ret_his_table.iloc[-60:]

    ws = wb.sheets['公募偏股基金收益归因']
    ws.range("A2:AB300").clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=True, expand='table').value = mutual_attr_list[6].T
    ws["A8"].options(pd.DataFrame, header=1, index=True, expand='table').value = mutual_attr_list[3].T
    ws["A14"].options(pd.DataFrame, header=1, index=True, expand='table').value = mutual_attr_list[0].T

    ws["A21"].options(pd.DataFrame, header=1, index=False, expand='table').value =core_pool[['基金简称','权重','累计贡献']]


    ws["O2"].options(pd.DataFrame, header=1, index=True, expand='table').value = mutual_attr_list[7]
    ws["O{}".format(2+len(mutual_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = mutual_attr_list[8]

    ws["O{}".format(2+2+2*len(mutual_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = mutual_attr_list[4]
    ws["O{}".format(1+2+2+3*len(mutual_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = mutual_attr_list[5]

    ws["O{}".format(1+4+2+4*len(mutual_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = mutual_attr_list[1]
    ws["O{}".format(2+4+2+5*len(mutual_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = mutual_attr_list[2]

    for pic in ws.pictures:
        pic.delete()
    plot.plotly_pie(core_pool[['基金简称','权重']].set_index('基金简称'),title_text='持仓权重占比',save_local_file=newpath + r"\\")

    ws.pictures.add(newpath + r"\{}.png".format('持仓权重占比'), left=ws.range('D21').left,
                    top=ws.range('D21').top,
                    width=300, height=250)

    plot.plotly_jjpic_bar(core_pool[['基金简称','累计贡献']].set_index('基金简称'),title_text='近60天累计收益贡献',save_local_file=newpath + r"\\")

    ws.pictures.add(newpath + r"\{}.png".format('近60天累计收益贡献'), left=ws.range('I21').left,
                    top=ws.range('I21').top,
                    width=400, height=250)


    ws = wb.sheets['进攻资产风格暴露']
    ws.range("A2:AB300").clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=True, expand='table').value = attack_asset_attr_list[2].T
    ws["A8"].options(pd.DataFrame, header=1, index=True, expand='table').value = attack_asset_attr_list[1].T
    ws["A14"].options(pd.DataFrame, header=1, index=True, expand='table').value = attack_asset_attr_list[0].T


    ws = wb.sheets['私募股多资产收益归因']
    ws.range("A2:AB300").clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=True, expand='table').value = prv_attr_list[6].T
    ws["A8"].options(pd.DataFrame, header=1, index=True, expand='table').value = prv_attr_list[3].T
    ws["A14"].options(pd.DataFrame, header=1, index=True, expand='table').value = prv_attr_list[0].T

    ws["A21"].options(pd.DataFrame, header=1, index=False, expand='table').value =prv_core_pool[['基金简称','权重','累计贡献']]

    ws["O2"].options(pd.DataFrame, header=1, index=True, expand='table').value = prv_attr_list[7]
    ws["O{}".format(2+len(prv_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = prv_attr_list[8]

    ws["O{}".format(2+2+2*len(prv_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = prv_attr_list[4]
    ws["O{}".format(1+2+2+3*len(prv_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = prv_attr_list[5]

    ws["O{}".format(1+4+2+4*len(prv_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = prv_attr_list[1]
    ws["O{}".format(2+4+2+5*len(prv_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = prv_attr_list[2]

    for pic in ws.pictures:
        pic.delete()

    plot.plotly_pie(prv_core_pool[['基金简称','权重']].set_index('基金简称'),title_text='持仓权重占比',save_local_file=newpath + r"\\")

    ws.pictures.add(newpath + r"\{}.png".format('持仓权重占比'), left=ws.range('D21').left,
                    top=ws.range('D21').top,
                    width=300, height=250)

    plot.plotly_jjpic_bar(prv_core_pool[['基金简称','累计贡献']].set_index('基金简称'),title_text='近60天累计收益贡献',save_local_file=newpath + r"\\")

    ws.pictures.add(newpath + r"\{}.png".format('近60天累计收益贡献'), left=ws.range('I21').left,
                    top=ws.range('I21').top,
                    width=400, height=250)


    ws = wb.sheets['量化多头资产收益归因']
    ws.range("A2:AB300").clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=True, expand='table').value = quant_attr_list[6].T
    ws["A8"].options(pd.DataFrame, header=1, index=True, expand='table').value = quant_attr_list[3].T
    ws["A14"].options(pd.DataFrame, header=1, index=True, expand='table').value = quant_attr_list[0].T

    ws["A21"].options(pd.DataFrame, header=1, index=False, expand='table').value =quant_core_pool[['基金简称','权重','累计贡献']]

    ws["O2"].options(pd.DataFrame, header=1, index=True, expand='table').value = quant_attr_list[7]
    ws["O{}".format(2+len(quant_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = quant_attr_list[8]

    ws["O{}".format(2+2+2*len(quant_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = quant_attr_list[4]
    ws["O{}".format(1+2+2+3*len(quant_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = quant_attr_list[5]

    ws["O{}".format(1+4+2+4*len(quant_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = quant_attr_list[1]
    ws["O{}".format(2+4+2+5*len(quant_attr_list[1]))].options(pd.DataFrame, header=1, index=True, expand='table').value = quant_attr_list[2]

    for pic in ws.pictures:
        pic.delete()

    plot.plotly_pie(quant_core_pool[['基金简称','权重']].set_index('基金简称'),title_text='持仓权重占比',save_local_file=newpath + r"\\")

    ws.pictures.add(newpath + r"\{}.png".format('持仓权重占比'), left=ws.range('D21').left,
                    top=ws.range('D21').top,
                    width=300, height=250)

    plot.plotly_jjpic_bar(quant_core_pool[['基金简称','累计贡献']].set_index('基金简称'),title_text='近60天累计收益贡献',save_local_file=newpath + r"\\")

    ws.pictures.add(newpath + r"\{}.png".format('近60天累计收益贡献'), left=ws.range('I21').left,
                    top=ws.range('I21').top,
                    width=400, height=250)




    ws = wb.sheets['公募偏股基金预警']
    ws.clear_contents()
    ws["A1"].options(pd.DataFrame, header=1, index=False, expand='table').value =mutual_funds_alert.drop('基金名称',axis=1)

    ws = wb.sheets['私募股多基金预警']
    ws.clear_contents()
    ws["A1"].options(pd.DataFrame, header=1, index=False, expand='table').value =prv_base_info

    ws = wb.sheets['CTA资产预警']
    ws.range("A2:Z300").clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=False, expand='table').value =\
        cta_funds_std[['基金代码', '基金简称', '持仓权重','累计贡献', '年化波动率', '波动率贡献', '最近一月', '最近3月', '最近6月', '最近1年', '最近2年',
       '最近3年']]

    ws.range("E{}".format(len(cta_funds_std)+5)).value="CTA资产整体波动率"
    ws.range("F{}".format(len(cta_funds_std)+5)).value=cta_portfolio_var


    ws = wb.sheets['大类资产基本信息']
    ws.range("A2:Z1000").clear_contents()
    asset_corr.index.name=''
    asset_annually_ret.index.name=''
    asset_vol.index.name = ''
    asset_VAR.index.name =''
    ws["A1"].options(pd.DataFrame, header=1, index=True, expand='table').value =(
        asset_corr)[['基准：进攻性资产-CTA', '基准：进攻性资产-稳健性资产', '基准：CTA-稳健性资产', 'FOF：进攻性资产-CTA',
       'FOF：进攻性资产-稳健性资产', 'FOF：CTA-稳健性资产']]
    ws["I1"].options(pd.DataFrame, header=1, index=True, expand='table').value =asset_annually_ret[['基准：进攻性资产', '基准：CTA', '基准：稳健性资产',
                                                                                                    'FOF：进攻性资产', 'FOF：CTA', 'FOF：稳健性资产']]
    ws["Q1"].options(pd.DataFrame, header=1, index=True, expand='table').value =asset_vol[['基准：进攻性资产', '基准：CTA', '基准：稳健性资产',
                                                                                           'FOF：进攻性资产', 'FOF：CTA', 'FOF：稳健性资产']]
    ws["Y1"].options(pd.DataFrame, header=1, index=True, expand='table').value =asset_VAR[['基准：进攻性资产', '基准：CTA', '基准：稳健性资产',
                                                                                           'FOF：进攻性资产', 'FOF：CTA', 'FOF：稳健性资产']]

    ws = wb.sheets['进攻资产基本信息']
    ws.range("A2:Z1000").clear_contents()
    ws["A1"].options(pd.DataFrame, header=1, index=True, expand='table').value =(
        asset_corr)[['基准：公募偏股-主观多头',
       '基准：主观多头-量化多头', '基准：公募偏股-量化多头','FOF：公募偏股-主观多头', 'FOF：主观多头-量化多头', 'FOF：公募偏股-量化多头']]
    ws["I1"].options(pd.DataFrame, header=1, index=True, expand='table').value =(
        asset_annually_ret)[['基准：主观多头', '基准：量化多头', '基准：公募偏股','FOF：主观多头', 'FOF：量化多头','FOF：公募偏股']]
    ws["Q1"].options(pd.DataFrame, header=1, index=True, expand='table').value =(
        asset_vol)[['基准：主观多头', '基准：量化多头', '基准：公募偏股','FOF：主观多头', 'FOF：量化多头','FOF：公募偏股']]
    ws["Y1"].options(pd.DataFrame, header=1, index=True, expand='table').value =\
        asset_VAR[['基准：主观多头', '基准：量化多头', '基准：公募偏股','FOF：主观多头', 'FOF：量化多头','FOF：公募偏股']]


    ws = wb.sheets['资产压力测试与风险提示']
    ws.range("A2:E8").clear_contents()
    ws.range("A10:D20").clear_contents()
    ws.range("G10:J20").clear_contents()
    ws.range("M10:P20").clear_contents()

    ws["A2"].options(pd.DataFrame, header=1, index=True, expand='table').value =fof_stress_test
    ws["A10"].options(pd.DataFrame, header=1, index=True, expand='table').value = ejfl2_alert_ret
    ws["G10"].options(pd.DataFrame, header=1, index=True, expand='table').value = ejfl2_alert_vol
    ws["M10"].options(pd.DataFrame, header=1, index=True, expand='table').value = ejfl2_alert_var


    wb.save(filename)
    wb.close()
    app.quit()
    print('done')

def calculate_index_yjd(index_code,start_date,end_date,index_cjl):

    if(index_code!='3800'):
        sql=("select cfgdm,qz from st_market.t_st_zs_zscfgqz where zqdm='{0}' and m_opt_type!='03'"
             .format(index_code))
        index_info=hbdb.db2df(sql,db='alluser')

        sql=("select jyrq,zsz from st_market.t_st_zs_hq where  zqdm = {0} and jyrq>='{1}' and jyrq<='{2}' "
             .format(index_code,start_date,end_date))
        index_ret=hbdb.db2df(sql,db='alluser')

        sql=("select jyrq,new_highest_w_{2} as new_highest_w ,above_ma20_w_{2} as above_ma20_w  from index_narrow_factors where  jyrq>='{0}' and jyrq<='{1}' "
             .format(start_date,end_date,index_code))
        index_factors_a=pd.read_sql(sql,con=localdb).set_index('jyrq')

        index_factors_a = pd.merge(index_factors_a, index_ret, how='left', on='jyrq')
        if(index_code=='000300'):
            narrow_factors=(
                pd.merge(index_factors_a,index_cjl[['交易日期','沪深300_成交量占比','全市场']],how='left',left_on='jyrq',right_on='交易日期').set_index('交易日期'))
            narrow_factors['clj_w']=narrow_factors['沪深300_成交量占比']
            narrow_factors[index_code]=narrow_factors['沪深300_成交量占比']*narrow_factors['全市场']/100
        elif(index_code=='000905'):
            narrow_factors=(
                pd.merge(index_factors_a,index_cjl[['交易日期','中证500_成交量占比','全市场']],how='left',left_on='jyrq',right_on='交易日期').set_index('交易日期'))
            narrow_factors['clj_w']=narrow_factors['中证500_成交量占比']
            narrow_factors[index_code]=narrow_factors['中证500_成交量占比']*narrow_factors['全市场']/100
        elif(index_code=='000852'):
            narrow_factors=(
                pd.merge(index_factors_a,index_cjl[['交易日期','中证1000_成交量占比','全市场']],how='left',left_on='jyrq',right_on='交易日期').set_index('交易日期'))
            narrow_factors['clj_w']=narrow_factors['中证1000_成交量占比']
            narrow_factors[index_code]=narrow_factors['中证1000_成交量占比']*narrow_factors['全市场']/100
        elif(index_code=='932000'):
            narrow_factors=(
                pd.merge(index_factors_a,index_cjl[['交易日期','中证2000_成交量占比','全市场']],how='left',left_on='jyrq',right_on='交易日期').set_index('交易日期'))
            narrow_factors['clj_w']=narrow_factors['中证2000_成交量占比']
            narrow_factors[index_code]=narrow_factors['中证2000_成交量占比']*narrow_factors['全市场']/100

        narrow_factors['hsl'] = narrow_factors[index_code] / narrow_factors['zsz']
        narrow_factors=narrow_factors[['jyrq', 'new_highest_w', 'above_ma20_w', 'clj_w','hsl']].set_index('jyrq')

    else:
        narrow_factors=pd.read_sql("select * from mimic_index_3800 where JYRQ>='{0}' and JYRQ<='{1}' "
                                   .format(start_date,end_date)
                                   ,con=localdb)[['JYRQ','new_highest_w','above_ma20_w','TURNOVER']].rename(columns={'JYRQ':'jyrq'})

        narrow_factors=pd.merge(narrow_factors,index_cjl[['交易日期','其他股票成交量']],
                                how='left',left_on='jyrq',right_on='交易日期').drop('交易日期',axis=1).set_index('jyrq')

    import sklearn.preprocessing as pp
    for col in narrow_factors.columns:
        narrow_factors.loc[(narrow_factors[col]>=narrow_factors.quantile(0.975)[col])|(narrow_factors[col]<=narrow_factors.quantile(0.025)[col]),col]=np.nan
    narrow_factors[narrow_factors.columns]=pp.StandardScaler().fit_transform(narrow_factors)

    if(index_code!='3800'):
        index_info['index_code']=index_code
    else:
        index_info=pd.DataFrame(columns=['cfgdm','index_code'])
    return (narrow_factors.mean(axis=1).to_frame(index_code).rolling(20,15).mean().iloc[20:],
            index_info[['cfgdm','index_code']])

def quant_pool_picture(end_date):

    from hbshare.fe.CYP import  quant_week_data as qwd

    pool_info=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\WeDrive\好买财富\量化存量产品打标（季度）\量化基金池202402.xlsx"
                            ,sheet_name='量化池列表',header=1)
    pool_info.loc[pool_info['子池'] != '代销', '子池'] = 'FOF'
    index_enhance=pool_info[pool_info['三级策略'].isin(['1000指数增强','500指数增强','全市场指数增强'])][['基金代码','代表产品','三级策略','子池']]
    market_netuarl=pool_info[pool_info['二级策略']=='市场中性'][['基金代码','代表产品','子池']]
    market_netuarl=market_netuarl[market_netuarl['基金代码']!='SER285']

    localdb2 = db_engine.PrvFunDB().engine2
    sql=("SELECT fund_name,fund_type,max(trade_date) from private_fund_holding GROUP BY fund_name,fund_type"
         .format(tuple(index_enhance['代表产品'].tolist()+market_netuarl['代表产品'].tolist())))
    latest_holding_list=pd.read_sql(sql,con=localdb2)

    sql="select jjdm,jjjc,glrm,sjglr from st_hedge.t_st_jjxx where jjjc in {0}".format(tuple(latest_holding_list['fund_name']))
    jjdm_map=hbdb.db2df(sql,db='highuser')
    jjdm_map.loc[jjdm_map['sjglr'].isnull(), 'sjglr'] = jjdm_map.loc[jjdm_map['sjglr'].isnull()]['glrm']

    sql = "select jgdm,jgjc from st_main.t_st_gg_jgxx where jgdm in {}" \
        .format(tuple(list(set(jjdm_map['glrm'].tolist() + jjdm_map['sjglr'].tolist()))))
    glrmc = hbdb.db2df(sql, db='alluser')
    jjdm_map=pd.merge(jjdm_map,glrmc,how='left',left_on='glrm',right_on='jgdm')

    latest_holding_list=pd.merge(latest_holding_list,jjdm_map[['jjjc','jgjc']],how='left',
                                 left_on='fund_name',right_on='jjjc')
    local_name_map=pd.read_excel(r"E:\GitFolder\docs\基金池跟踪\量化基金池\产品名称映射.xlsx")
    latest_holding_list=pd.merge(latest_holding_list,local_name_map[['fund_name','管理人']],how='left',on='fund_name')
    latest_holding_list.loc[latest_holding_list['jgjc'].isnull(),'jgjc']=latest_holding_list[latest_holding_list['jgjc'].isnull()]['管理人']

    latest_holding_list=latest_holding_list.sort_values('max(trade_date)').drop_duplicates(['fund_type','jgjc'],keep='last').drop(['管理人','jjjc'],axis=1)
    latest_holding_list=latest_holding_list[latest_holding_list['jgjc'].notnull()].set_index('fund_name')

    #get funds ret
    start_date=str(int(end_date)-20000)
    sql=("select hb1z,rqzh as tjrq,jjdm from st_hedge.t_st_sm_zhb where jjdm in {0} and rqzh>='{1}' and rqzh<='{2}' and hb1z!=99999"
         .format(tuple(index_enhance['基金代码'].tolist()),start_date,end_date))
    index_enhance_nav=hbdb.db2df(sql,db='highuser').pivot_table('hb1z','tjrq','jjdm')
    last_year=index_enhance_nav.index[-52]
    sql=("select hb1z,rqzh as tjrq,jjdm from st_hedge.t_st_sm_zhb where jjdm in {0} and rqzh>='{1}' and rqzh<='{2}' and hb1z!=99999"
         .format(tuple(market_netuarl['基金代码'].tolist()),start_date,end_date))
    market_netuarl_nav=hbdb.db2df(sql,db='highuser').pivot_table('hb1z','tjrq','jjdm')
    latest_date=index_enhance_nav.index[-1]

    #get fund qujian return
    sql=("select zbnp,zblb,jjdm,jzrq from st_hedge.t_st_sm_qjhb_zj where jjdm in {0} and jzrq>'{1}' and jzrq<='{2}' and zblb in ('2007','2101','2106','2998','2201') and zbnp!=99999"
         .format(tuple(index_enhance['基金代码'].tolist()+market_netuarl['基金代码'].tolist()),last_year,latest_date))
    funds_return_interval = hbdb.db2df(sql, db='highuser').sort_values('jzrq').drop_duplicates(['zblb','jjdm'],keep='last')
    funds_return_interval=funds_return_interval.pivot_table('zbnp','jjdm','zblb')
    funds_return_interval.columns=['近1周','近一月','近6月','近一年','今年以来']

    fund_cl_data=pd.read_excel(r"E:\GitFolder\docs\基金池跟踪\量化基金池\量化_存量明细表20240131.xlsx")[['真实管理人','二级策略','代销还是FOF','存量市值']]
    fund_cl_data.loc[fund_cl_data['真实管理人'] == '上海宽德私募', '真实管理人'] = '宽德投资'
    fund_cl_data.loc[fund_cl_data['二级策略'].astype(str).str.contains('市场中性'), '二级策略'] = '市场中性'
    fund_cl_data=fund_cl_data.groupby(['真实管理人', '二级策略', '代销还是FOF'])[['存量市值']].sum().reset_index()

    sql = "select jjdm,glrm,sjglr from st_hedge.t_st_jjxx where jjdm in {}" \
        .format(tuple(index_enhance['基金代码'].tolist()+market_netuarl['基金代码'].tolist()))
    glrm = hbdb.db2df(sql, db='highuser')

    glrm.loc[glrm['sjglr'].isnull(), 'sjglr'] = glrm.loc[glrm['sjglr'].isnull()]['glrm']

    sql = "select jgdm,jgjc from st_main.t_st_gg_jgxx where jgdm in {}" \
        .format(tuple(list(set(glrm['glrm'].tolist() + glrm['sjglr'].tolist()))))
    glrmc = hbdb.db2df(sql, db='alluser')
    glrm=pd.merge(glrm,glrmc,how='left',left_on='glrm',right_on='jgdm')
    glrm=pd.merge(glrm,pool_info[['基金代码','三级策略','子池']],how='left',left_on='jjdm',right_on='基金代码')
    glrm.loc[glrm['三级策略']=='全市场指数增强','三级策略']='量化多头'
    glrm.loc[glrm['三级策略'].isnull(),'三级策略']='市场中性'
    glrm.loc[glrm['jgjc'].str.contains('宽德'),'jgjc']='宽德投资'

    fund_cl_data=pd.merge(fund_cl_data,glrm
                          ,how='left',left_on=['真实管理人','二级策略','代销还是FOF'],right_on=['jgjc','三级策略','子池'])[['基金代码','jgjc','三级策略','存量市值']]


    cl_label=(
        pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\WeDrive\好买财富\量化存量产品打标（季度）\量化存量产品更新表（打标）20240131.xlsx"))
    cl_label.loc[cl_label['二级策略'].str.contains('市场中性'),'二级策略']='市场中性'
    fund_cl_data=pd.merge(fund_cl_data,cl_label.drop_duplicates(['基金管理人','二级策略'],keep='first')[['基金管理人','二级策略',cl_label.columns[6]]],how='left',left_on=['jgjc','三级策略'],right_on=['基金管理人','二级策略']).drop(['基金管理人','二级策略'],axis=1)

    eft_cjl=qwd.etf_cjl(start_date,end_date)
    sql="SELECT * from  stock_narrow"
    stock_A_cjl=pd.read_sql(sql,con=localdb).sort_values('交易日期')
    index_cjl=qwd.index_cjl(start_date,end_date)
    index_return_history,index_return_mat=qwd.index_return(int(end_date))
    sql="SELECT * from  stock_relative_ret"
    market_ext_ret_nav=pd.read_sql(sql,con=localdb)


    #get index ret
    sql=("select hb1z,rqzh as tjrq,zqdm from st_market.t_st_zs_zhb where zqdm in ('000300','000905','000852','932000') and rqzh>='{0}' and rqzh<='{1}' and m_opt_type!='03'"
         .format(start_date,end_date))
    index_ret=hbdb.db2df(sql,db='alluser').pivot_table('hb1z','tjrq','zqdm')
    index_ret.index=index_ret.index.astype(str)

    sql="select * from mimic_index_3800 "
    index_3800=pd.read_sql(sql,con=localdb)
    index_3800['spjg']=(index_3800['PCHG']/100+1).cumprod()
    index_3800['3800之外']=index_3800['spjg'].pct_change()*100
    index_3800['JYRQ']=index_3800['JYRQ'].astype(str)
    index_ret=pd.merge(index_ret,index_3800[['3800之外','JYRQ']],left_on='tjrq',right_on='JYRQ',how='left').set_index('JYRQ')
    index_ret.index.name='tjrq'
    index_ret.columns=['300', '1000', '500', '2000','3800之外']

    index_jyd_3800,cfg_list_3800=calculate_index_yjd('3800', str(int(end_date)-50000), end_date,index_cjl)
    index_jyd_300,cfg_list_300=calculate_index_yjd('000300', str(int(end_date)-50000), end_date,index_cjl)
    index_jyd_500,cfg_list_500=calculate_index_yjd('000905', str(int(end_date)-50000), end_date,index_cjl)
    index_jyd_1000,cfg_list_1000=calculate_index_yjd('000852', str(int(end_date)-50000), end_date,index_cjl)
    index_jyd_2000,cfg_list_2000=calculate_index_yjd('932000', str(int(end_date)-50000), end_date,index_cjl)
    #index_jyd_wpg,cfg_list_wp=calculate_index_yjd('8841431', start_date, end_date)
    index_cjl.drop('全市场',axis=1,inplace=True)



    cfg_list=pd.concat([cfg_list_300,cfg_list_500,cfg_list_1000,cfg_list_2000],axis=0)


    index_jyd=pd.merge(index_jyd_300,index_jyd_500,how='inner',on='jyrq')
    index_jyd=pd.merge(index_jyd,index_jyd_1000,how='inner',on='jyrq')
    index_jyd=pd.merge(index_jyd,index_jyd_2000,how='inner',on='jyrq')
    index_jyd=pd.merge(index_jyd,index_jyd_3800,how='inner',on='jyrq')
    index_jyd.columns=['300','500','1000','2000','3800之外']
    index_jyd.sort_index(inplace=True)

    #add the yjd alter
    yjd_alert=index_jyd.rank(pct=True).iloc[-1].to_frame('宽基拥挤度分位数')
    # yjd_alert=pd.merge(yjd_alert,index_jyd.diff(1).iloc[-1].to_frame('最近一周变动')
    #                    ,how='left',left_index=True,right_index=True)
    # yjd_alert=pd.merge(yjd_alert,index_jyd.diff(1).abs().quantile(0.8).to_frame('变动阈值')
    #                    ,how='left',left_index=True,right_index=True)


    list_500=['300', '1000', '2000','3800之外']
    list_1000=['300', '500', '2000','3800之外']
    list_all=['300', '500', '1000', '2000','3800之外']

    index_enhance_nav=pd.merge(index_enhance_nav,index_ret,how='left',on='tjrq')
    market_netuarl_nav=pd.merge(market_netuarl_nav,index_ret,how='left',on='tjrq')


    corr_500=index_enhance_nav.sub(index_enhance_nav['500'],
                                   axis=0).drop('500',axis=1).rolling(26,12).corr().loc[(slice(None),list(
        set(index_enhance_nav.columns).intersection(index_enhance[index_enhance['三级策略']=='500指数增强']['基金代码'].tolist()))),:][list_500].reset_index(drop=False)

    corr_1000=index_enhance_nav.sub(index_enhance_nav['1000'],
                                   axis=0).drop('1000',axis=1).rolling(26,12).corr().loc[(slice(None),list(
        set(index_enhance_nav.columns).intersection(index_enhance[index_enhance['三级策略']=='1000指数增强']['基金代码'].tolist()))),:][list_1000].reset_index(drop=False)

    all_corr=index_enhance_nav.rolling(26,12).corr().loc[(slice(None),list(
        set(index_enhance_nav.columns).intersection(index_enhance[index_enhance['三级策略']=='全市场指数增强']['基金代码'].tolist()))),:][list_all].reset_index(drop=False)

    netuarl_corr=market_netuarl_nav.sub(market_netuarl_nav['500'],
                                   axis=0).drop('500',axis=1).rolling(26,12).corr().loc[(slice(None),list(
        set(market_netuarl_nav.columns).intersection(market_netuarl['基金代码'].tolist()))),:][list_500].reset_index(drop=False)


    corr_500=pd.merge(corr_500,fund_cl_data,how='left',left_on='level_1',right_on='基金代码').drop('基金代码',axis=1)
    corr_1000 = pd.merge(corr_1000, fund_cl_data, how='left',left_on='level_1',right_on='基金代码').drop('基金代码',axis=1)
    all_corr = pd.merge(all_corr, fund_cl_data, how='left',left_on='level_1',right_on='基金代码').drop('基金代码',axis=1)
    netuarl_corr=pd.merge(netuarl_corr,fund_cl_data,how='left',left_on='level_1',right_on='基金代码').drop('基金代码',axis=1)

    def merge_glm_name(corr_500,glrm):

        corr_500=pd.merge(corr_500,glrm[['jjdm','jgjc']],how='left'
                          ,left_on='level_1',right_on='jjdm').drop('jjdm',axis=1).rename(columns={'jgjc_x':'jgjc'})
        corr_500.loc[corr_500['jgjc'].isnull(),'jgjc']=corr_500[corr_500['jgjc'].isnull()]['jgjc_y']
        corr_500['三级策略']=corr_500[corr_500['三级策略'].notnull()]['三级策略'].unique()[0]

        return corr_500.drop('jgjc_y',axis=1)

    corr_500=merge_glm_name(corr_500,glrm)
    corr_1000=merge_glm_name(corr_1000,glrm)
    all_corr=merge_glm_name(all_corr,glrm)
    netuarl_corr = merge_glm_name(netuarl_corr, glrm)

    corr_500=pd.merge(corr_500,funds_return_interval,how='left',left_on='level_1',right_index=True)
    corr_1000 = pd.merge(corr_1000, funds_return_interval, how='left', left_on='level_1',right_index=True)
    all_corr = pd.merge(all_corr, funds_return_interval, how='left', left_on='level_1',right_index=True)
    netuarl_corr=pd.merge(netuarl_corr,funds_return_interval,how='left',left_on='level_1',right_index=True)


    corr_500=pd.merge(corr_500,index_enhance[['基金代码','代表产品','子池']],how='left',
                      left_on='level_1',right_on='基金代码').drop(['基金代码','level_1'],axis=1)
    corr_1000=pd.merge(corr_1000,index_enhance[['基金代码','代表产品','子池']],how='left'
                       ,left_on='level_1',right_on='基金代码').drop(['基金代码','level_1'],axis=1)
    all_corr=pd.merge(all_corr,index_enhance[['基金代码','代表产品','子池']],how='left',
                      left_on='level_1',right_on='基金代码').drop(['基金代码','level_1'],axis=1)
    netuarl_corr=pd.merge(netuarl_corr,market_netuarl[['基金代码','代表产品','子池']],how='left',
                          left_on='level_1',right_on='基金代码').drop(['基金代码','level_1'],axis=1)


    pool_500_history=(corr_500[corr_500['tjrq']>=last_year].drop(['jgjc', '三级策略', '存量市值', '近1周',
                                                                 '近一月','近6月', '今年以来', '近一年', '子池'],axis=1)).groupby('tjrq').mean()
    pool_1000_history=corr_1000[corr_1000['tjrq']>=last_year].drop(['jgjc', '三级策略', '存量市值', '近1周',
                                                                 '近一月','近6月', '今年以来', '近一年', '子池'],axis=1).groupby('tjrq').mean()
    pool_all_history=all_corr[all_corr['tjrq']>=last_year].drop(['jgjc', '三级策略', '存量市值', '近1周',
                                                                 '近一月','近6月', '今年以来', '近一年', '子池'],axis=1).groupby('tjrq').mean()
    pool_netural_history = netuarl_corr[netuarl_corr['tjrq'] >= last_year].drop(['jgjc', '三级策略', '存量市值', '近1周',
                                                                 '近一月','近6月', '今年以来', '近一年', '子池'],axis=1).groupby('tjrq').mean()


    corr_500_his_list=[]
    corr_1000_his_list=[]
    corr_all_his_list=[]
    corr_netural_his_list = []

    for name in corr_500[corr_500['子池']=='代销']['代表产品'].unique():

        corr_500_his_list.append(
            corr_500[(corr_500['子池']=='代销')&(corr_500['tjrq']>=last_year)
                     &(corr_500['代表产品']==name)][['tjrq', '300', '1000', '2000', '3800之外']].rename(columns={'tjrq':name}).set_index(name))

    for name in corr_1000[corr_1000['子池']=='代销']['代表产品'].unique():

        corr_1000_his_list.append(
            corr_1000[(corr_1000['子池']=='代销')&
                      (corr_1000['tjrq']>=last_year)&
                      (corr_1000['代表产品']==name)][['tjrq', '300', '500', '2000', '3800之外']].rename(columns={'tjrq':name}).set_index(name))

    for name in all_corr[all_corr['子池']=='代销']['代表产品'].unique():

        corr_all_his_list.append(
            all_corr[(all_corr['子池']=='代销')&
                     (all_corr['tjrq']>=last_year)&
                     (all_corr['代表产品']==name)][['tjrq', '300','500', '1000', '2000', '3800之外']].rename(columns={'tjrq':name}).set_index(name))

    for name in netuarl_corr[netuarl_corr['子池']=='代销']['代表产品'].unique():

        corr_netural_his_list.append(
            netuarl_corr[(netuarl_corr['子池']=='代销')&
                         (netuarl_corr['tjrq']>=last_year)&
                         (netuarl_corr['代表产品']==name)][['tjrq', '300', '1000', '2000', '3800之外']].rename(columns={'tjrq':name}).set_index(name))


    corr_500=corr_500[corr_500['tjrq']==latest_date].drop('tjrq',axis=1).set_index('代表产品').sort_values(['子池','3800之外'],ascending=False)
    corr_1000=corr_1000[corr_1000['tjrq']==latest_date].drop('tjrq',axis=1).set_index('代表产品').sort_values(['子池','3800之外'],ascending=False)
    all_corr=all_corr[all_corr['tjrq']==latest_date].drop('tjrq',axis=1).set_index('代表产品').sort_values(['子池','3800之外'],ascending=False)
    netuarl_corr=netuarl_corr[netuarl_corr['tjrq']==latest_date].drop('tjrq',axis=1).set_index('代表产品').sort_values(['子池','3800之外'],ascending=False)

    def get_funds_index_distribution_from_hld(latest_holding_list,corr_500,index_type):
        hld_index_dis=[]
        for glr in list(set(latest_holding_list[latest_holding_list['fund_type']==index_type]['jgjc']).intersection(set(corr_500['jgjc'])) ):

            name=latest_holding_list[(latest_holding_list['jgjc']==glr)&(latest_holding_list['fund_type']==index_type)].index[0]
            sql=("SELECT ticker,weight,fund_name as '代表产品' from private_fund_holding where fund_name='{0}' and trade_date='{1}' "
                 .format(name,str(latest_holding_list.loc[name]['max(trade_date)']).replace('-','')))
            temp_hld=pd.read_sql(sql,con=localdb2)
            temp_hld=pd.merge(temp_hld,cfg_list,how='left',left_on='ticker',right_on='cfgdm').fillna('3800之外').drop('cfgdm',axis=1)
            temp_hld.groupby('index_code')[['weight']].sum()
            temp_hld=temp_hld.groupby('index_code')[['weight']].sum().T/100
            temp_hld.index = [corr_500[corr_500['jgjc']==glr].index[0]]
            temp_hld['最新估值表日期']=str(latest_holding_list.loc[name]['max(trade_date)']).replace('-','')
            hld_index_dis.append(temp_hld)

        if(index_type=='市场中性'):
            corr_500=pd.concat([corr_500, pd.DataFrame(columns=['300暴露_持仓', '1000暴露_持仓',
                                '500暴露_持仓', '3800之外暴露_持仓',
                                '2000暴露_持仓', '最新估值表日期'])],axis=1)
            corr_500.columns = ['300暴露_净值', '1000暴露_净值', '2000暴露_净值', '3800之外暴露_净值', '管理人',
                                '细分策略', '存量市值','最新打标', '近1周', '近一月',
                                '近6月',  '近一年','今年以来', '子池', '300暴露_持仓', '1000暴露_持仓',
                                '500暴露_持仓', '3800之外暴露_持仓',
                                '2000暴露_持仓', '最新估值表日期']

            return corr_500[
                ['子池', '管理人', '细分策略', '存量市值','最新打标', '300暴露_净值', '1000暴露_净值', '2000暴露_净值',
                 '3800之外暴露_净值', '300暴露_持仓', '500暴露_持仓', '1000暴露_持仓', '2000暴露_持仓',
                 '3800之外暴露_持仓', '最新估值表日期', '近1周', '近一月',
                 '近6月','近一年', '今年以来']]
        else:
            corr_500=pd.merge(corr_500,pd.concat(hld_index_dis,axis=0),
                              how='left',left_on='代表产品',right_index=True)
            if(index_type=='500指增' ):
                corr_500.columns=['300暴露_净值', '1000暴露_净值', '2000暴露_净值', '3800之外暴露_净值', '管理人', '细分策略', '存量市值','最新打标', '近1周', '近一月',
               '近6月', '近一年','今年以来',  '子池', '300暴露_持仓', '1000暴露_持仓', '500暴露_持仓', '3800之外暴露_持仓',
               '2000暴露_持仓','最新估值表日期']

                return  corr_500[['子池','管理人', '细分策略', '存量市值','最新打标','300暴露_净值', '1000暴露_净值', '2000暴露_净值',
                                  '3800之外暴露_净值','300暴露_持仓', '500暴露_持仓','1000暴露_持仓','2000暴露_持仓', '3800之外暴露_持仓','最新估值表日期','近1周', '近一月',
               '近6月', '今年以来', '近一年']]
            elif(index_type=='1000指增'):
                corr_500.columns = ['300暴露_净值', '500暴露_净值', '2000暴露_净值', '3800之外暴露_净值', '管理人',
                                    '细分策略', '存量市值','最新打标', '近1周', '近一月',
                                    '近6月','近一年', '今年以来',  '子池', '300暴露_持仓', '1000暴露_持仓', '500暴露_持仓',
                                    '3800之外暴露_持仓',
                                    '2000暴露_持仓','最新估值表日期']

                return corr_500[['子池', '管理人', '细分策略', '存量市值','最新打标', '300暴露_净值', '500暴露_净值', '2000暴露_净值',
                                 '3800之外暴露_净值', '300暴露_持仓', '500暴露_持仓', '1000暴露_持仓', '2000暴露_持仓',
                                 '3800之外暴露_持仓', '最新估值表日期','近1周', '近一月',
                                 '近6月','近一年' ,'今年以来' ]]
            elif(index_type=='量化多头'):
                corr_500.columns = ['300暴露_净值', '500暴露_净值','1000暴露_净值', '2000暴露_净值', '3800之外暴露_净值', '管理人',
                                    '细分策略', '存量市值','最新打标', '近1周', '近一月',
                                    '近6月',  '近一年','今年以来', '子池', '300暴露_持仓', '1000暴露_持仓', '500暴露_持仓',
                                    '3800之外暴露_持仓',
                                    '2000暴露_持仓','最新估值表日期']

                return corr_500[['子池', '管理人', '细分策略', '存量市值','最新打标', '300暴露_净值', '500暴露_净值','1000暴露_净值', '2000暴露_净值',
                                 '3800之外暴露_净值', '300暴露_持仓', '500暴露_持仓', '1000暴露_持仓', '2000暴露_持仓',
                                 '3800之外暴露_持仓','最新估值表日期', '近1周', '近一月',
                                 '近6月', '近一年', '今年以来']]


    corr_500=get_funds_index_distribution_from_hld(latest_holding_list,corr_500,'500指增')
    corr_1000=get_funds_index_distribution_from_hld(latest_holding_list,corr_1000,'1000指增')
    all_corr=get_funds_index_distribution_from_hld(latest_holding_list,all_corr,'量化多头')
    netuarl_corr=get_funds_index_distribution_from_hld(latest_holding_list,netuarl_corr,'市场中性')


    local_weight=pd.read_excel(r"E:\GitFolder\docs\基金池跟踪\量化基金池\存量标的持仓分布.xlsx",header=1)
    def merge_local_weight(corr_500,local_weight):

        corr_500=pd.merge(corr_500.reset_index(),local_weight,how='left',left_on=['管理人','细分策略','子池'],right_on=['Unnamed: 0','Unnamed: 2','Unnamed: 3'])

        corr_500.loc[corr_500['最新估值表日期'].isnull(),'300暴露_持仓']=corr_500[corr_500['最新估值表日期'].isnull()]['沪深300']
        corr_500.loc[corr_500['最新估值表日期'].isnull(),'500暴露_持仓']=corr_500[corr_500['最新估值表日期'].isnull()]['中证500']
        corr_500.loc[corr_500['最新估值表日期'].isnull(), '1000暴露_持仓'] = corr_500[corr_500['最新估值表日期'].isnull()]['中证1000']
        corr_500.loc[corr_500['最新估值表日期'].isnull(), '2000暴露_持仓'] = corr_500[corr_500['最新估值表日期'].isnull()]['中证2000']
        corr_500.loc[corr_500['最新估值表日期'].isnull(), '3800之外暴露_持仓'] = corr_500[corr_500['最新估值表日期'].isnull()]['微盘']
        corr_500.loc[corr_500['最新估值表日期'].isnull(), '最新估值表日期'] = corr_500[corr_500['最新估值表日期'].isnull()]['估值表/定性']

        return  corr_500.drop(local_weight.columns.tolist(),axis=1).set_index('代表产品')

    corr_500=merge_local_weight(corr_500,local_weight)
    corr_1000=merge_local_weight(corr_1000,local_weight)
    all_corr=merge_local_weight(all_corr,local_weight)

    #add funds real holding alert
    fund_alert=[]
    fund_alert.append(corr_500[corr_500['3800之外暴露_持仓'] >= 0.2][
        ['子池', '管理人', '细分策略', '3800之外暴露_净值', '3800之外暴露_持仓','最新估值表日期']])
    fund_alert.append(corr_1000[corr_1000['3800之外暴露_持仓'] >= 0.25][
        ['子池', '管理人', '细分策略', '3800之外暴露_净值', '3800之外暴露_持仓','最新估值表日期']])
    fund_alert.append(all_corr[all_corr['3800之外暴露_持仓'] >= 0.30][
        ['子池', '管理人', '细分策略', '3800之外暴露_净值', '3800之外暴露_持仓','最新估值表日期']])
    fund_alert=pd.concat(fund_alert,axis=0)
    fund_alert['预警类型']='3800之外暴露较高'

    fund_alert_netural=netuarl_corr[netuarl_corr['近1周']<=-5][['子池', '管理人', '细分策略', '近1周']]
    fund_alert_netural['阈值']=[-0.05]
    fund_alert_netural['近1周']=fund_alert_netural['近1周']/100
    fund_alert_netural['预警类型']='中性产品波动过大'
    fund_alert_netural.index_name='代表产品'


    pool_all_corr=pd.merge(pool_500_history.iloc[-1].to_frame('500指增平均'),pool_1000_history.iloc[-1].to_frame('1000指增平均')
                           ,how='outer',left_index=True,right_index=True)
    pool_all_corr=pd.merge(pool_all_corr,pool_all_history.iloc[-1].to_frame('全市场指增平均')
                           ,how='outer',left_index=True,right_index=True)
    pool_all_corr=pd.merge(pool_all_corr,pool_netural_history.iloc[-1].to_frame('市场中性平均')
                           ,how='outer',left_index=True,right_index=True)

    pool_all_corr['指增与中性整体平均相关性']=pool_all_corr.mean(axis=1)

    from hbshare.quant.CChen.fut import wind_stk_index_basis
    from hbshare.quant.CChen.cons import sql_write_path_hb as path
    sql_path = path['daily']
    include_cols=['t_date', 'basis']

    start_date=datetime.datetime.strptime(start_date, '%Y%m%d')
    end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
    if_df_0 = wind_stk_index_basis(code='IF', start_date=start_date,
                                 end_date=end_date,
                                 sql_path=sql_path, table="futures_wind")[0][include_cols]
    if_df_2 = wind_stk_index_basis(code='IF', start_date=start_date,
                                 end_date=end_date,
                                 sql_path=sql_path, table="futures_wind")[2][include_cols]
    ic_df_0 = wind_stk_index_basis(code='IC', start_date=start_date, end_date=end_date,
                                 sql_path=sql_path, table="futures_wind")[0][include_cols]
    ic_df_2 = wind_stk_index_basis(code='IC', start_date=start_date, end_date=end_date,
                                 sql_path=sql_path, table="futures_wind")[2][include_cols]
    im_df_0 = wind_stk_index_basis(code='IM', start_date=start_date, end_date=end_date,
                                 sql_path=sql_path, table="futures_wind")[0][include_cols]
    im_df_2 = wind_stk_index_basis(code='IM', start_date=start_date, end_date=end_date,
                                 sql_path=sql_path, table="futures_wind")[2][include_cols]


    interest_bais=if_df_0[if_df_0['basis'].abs()<99999].rename(columns={'basis':'IF_次月'})
    interest_bais=pd.merge(interest_bais
                           ,if_df_2[if_df_2['basis'].abs()<99999].rename(columns={'basis':'IF_当季(右轴'})
                           ,how='outer',on='t_date')
    interest_bais=pd.merge(interest_bais
                           ,ic_df_0[ic_df_0['basis'].abs()<99999].rename(columns={'basis':'IC_次月'})
                           ,how='outer',on='t_date')
    interest_bais=pd.merge(interest_bais
                           ,ic_df_2[ic_df_2['basis'].abs()<99999].rename(columns={'basis':'IC_当季(右轴'})
                           ,how='outer',on='t_date')
    interest_bais = pd.merge(interest_bais
                         , im_df_0[im_df_0['basis'].abs()<99999].rename(columns={'basis':'IM_次月'})
                         , how='outer', on='t_date')
    interest_bais = pd.merge(interest_bais
                         , im_df_2[im_df_2['basis'].abs() < 99999].rename(columns={'basis': 'IM_当季(右轴'})
                         , how='outer', on='t_date')
    interest_bais.sort_values('t_date',inplace=True)


    #add the interest bais alert
    interest_alert=interest_bais.drop('t_date',axis=1).iloc[-1].to_frame('基差')
    interest_alert=pd.merge(interest_alert,interest_bais.quantile(0.8).to_frame('上限')
                       ,how='left',left_index=True,right_index=True)
    interest_alert=pd.merge(interest_alert,interest_bais.quantile(0.2).to_frame('下限')
                       ,how='left',left_index=True,right_index=True)


    subjective_view_info=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\WeDrive\好买财富\量化策略跟踪表（月度）\量化Alpha基金画像202312.xlsx"
                                       ,sheet_name='量化股票策略',header=1)[['Unnamed: 0','管理人', 'Unnamed: 3', '300/500/1000/量化多头/市场中性','Unnamed: 5','市值', '行业偏离']]
    subjective_view_info=pd.concat([subjective_view_info
                                       ,pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\WeDrive\好买财富\量化策略跟踪表（月度）\量化Alpha基金画像202312.xlsx"
                                       ,sheet_name='市场中性及多空策略',header=1)],axis=0)[['Unnamed: 0','管理人', 'Unnamed: 2', '300/500/1000/量化多头/市场中性','Unnamed: 4','市值', '行业偏离']]
    subjective_view_info.columns=['子池','管理人', '当前策略规模', '300/500/1000/量化多头/市场中性', '换手率', '市值',
       '行业偏离']

    filename=r"E:\GitFolder\docs\基金池跟踪\量化基金池\量化基金池跟踪表.xlsx"
    import xlwings as xw

    app = xw.App(visible=False)
    wb =app.books.open(filename)

    ws = wb.sheets['预警']
    ws.range("A4:B9").clear_contents()
    ws["A4"].options(pd.DataFrame, header=1, index=True, expand='table').value =yjd_alert
    ws.range("A12:D18").clear_contents()
    ws["A12"].options(pd.DataFrame, header=1, index=True, expand='table').value =interest_alert
    ws.range("J18:Q200").clear_contents()
    ws["J18"].options(pd.DataFrame, header=1, index=True, expand='table').value =fund_alert
    ws["J{}".format(20+len(fund_alert))].options(pd.DataFrame, header=1, index=True, expand='table').value =fund_alert_netural

    ws = wb.sheets['宽基涨跌幅']
    ws.range("A2:G500").clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=True, expand='table').value =index_return_mat.iloc[-243:]
    ws["H2"].options(pd.DataFrame, header=1, index=False, expand='table').value = index_return_history

    ws = wb.sheets['市场成交量统计']
    ws.range("A2:Z500").clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=False, expand='table').value = index_cjl.iloc[-486:]
    ws["H2"].options(pd.DataFrame, header=1, index=False, expand='table').value = eft_cjl.iloc[-323:]
    ws["P2"].options(pd.DataFrame, header=1, index=False, expand='table').value = stock_A_cjl.iloc[-486:]
    ws["U2"].options(pd.DataFrame, header=1, index=False, expand='table').value = market_ext_ret_nav.iloc[-761:]


    ws = wb.sheets['宽基拥挤度']
    ws.range("A2:F500").clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=True, expand='table').value = index_jyd.iloc[-446:]

    ws = wb.sheets['个基定量跟踪表']
    ws.range("A2:BZ200").clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=True, expand='table').value = corr_500
    ws["W2"].options(pd.DataFrame, header=1, index=True, expand='table').value = corr_1000
    ws["AS2"].options(pd.DataFrame, header=1, index=True, expand='table').value = all_corr
    ws["BP2"].options(pd.DataFrame, header=1, index=True, expand='table').value = netuarl_corr

    # ws=wb.sheets['个基金定性跟踪表']
    # ws.range("A3:AZ500").clear_contents()
    # ws["A3"].options(pd.DataFrame, header=0, index=False, expand='table').value = subjective_view_info



    plot=functionality.Plot(1000,700)
    newpath = r'E:\GitFolder\docs\私募股多持仓分析\pic_temp'

    ws=wb.sheets['500指增个基宽基暴露时序']
    for pic in ws.pictures:
        pic.delete()
    ws.range("A1:BZ500").clear_contents()
    for i in range(len(corr_500_his_list)):
        ws[(0,i*6)].options(pd.DataFrame, header=1, index=True, expand='table').value = corr_500_his_list[i]
        plot.plotly_line_style(corr_500_his_list[i],
                              title_text=corr_500_his_list[i].index[0], save_local_file=newpath + r"\\")
        ws.pictures.add(newpath + r"\{}.png".format(corr_500_his_list[i].index[0]), left=ws.range((5,i*6+1)).left,
                        top=ws.range((5,i*6+1)).top,
                        width=500, height=250)

    ws=wb.sheets['1000指增个基宽基暴露时序']
    for pic in ws.pictures:
        pic.delete()
    ws.range("A2:BZ500").clear_contents()
    for i in range(len(corr_1000_his_list)):
        ws[(0,i*6)].options(pd.DataFrame, header=1, index=True, expand='table').value = corr_1000_his_list[i]
        plot.plotly_line_style(corr_1000_his_list[i],
                              title_text=corr_1000_his_list[i].index[0], save_local_file=newpath + r"\\")
        ws.pictures.add(newpath + r"\{}.png".format(corr_500_his_list[i].index[0]), left=ws.range((5,i*6+1)).left,
                        top=ws.range((5,i*6+1)).top,
                        width=500, height=250)

    ws=wb.sheets['全市场指增个基宽基暴露时序']
    for pic in ws.pictures:
        pic.delete()
    ws.range("A2:BZ500").clear_contents()
    for i in range(len(corr_all_his_list)):
        ws[(0,i*7)].options(pd.DataFrame, header=1, index=True, expand='table').value = corr_all_his_list[i]
        plot.plotly_line_style(corr_all_his_list[i],
                              title_text=corr_all_his_list[i].index[0], save_local_file=newpath + r"\\")
        ws.pictures.add(newpath + r"\{}.png".format(corr_500_his_list[i].index[0]), left=ws.range((5,i*7+1)).left,
                        top=ws.range((5,i*7+1)).top,
                        width=500, height=250)

    ws=wb.sheets['市场中性个基宽基暴露时序']
    for pic in ws.pictures:
        pic.delete()
    ws.range("A2:BZ500").clear_contents()
    for i in range(len(corr_netural_his_list)):
        ws[(0,i*6)].options(pd.DataFrame, header=1, index=True, expand='table').value = corr_netural_his_list[i]
        plot.plotly_line_style(corr_netural_his_list[i],
                              title_text=corr_netural_his_list[i].index[0], save_local_file=newpath + r"\\")
        ws.pictures.add(newpath + r"\{}.png".format(corr_500_his_list[i].index[0]), left=ws.range((5,i*6+1)).left,
                        top=ws.range((5,i*6+1)).top,
                        width=500, height=250)


    ws = wb.sheets['整池宽基相关性']
    ws.range("A2:G100").clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=True, expand='table').value = pool_all_corr

    ws["H2"].options(pd.DataFrame, header=1, index=True, expand='table').value = pool_500_history
    ws["M2"].options(pd.DataFrame, header=1, index=True, expand='table').value = pool_1000_history
    ws["R2"].options(pd.DataFrame, header=1, index=True, expand='table').value = pool_all_history
    ws["X2"].options(pd.DataFrame, header=1, index=True, expand='table').value = pool_netural_history


    ws = wb.sheets['基差跟踪']
    ws.range("A2:G300").clear_contents()
    ws["A2"].options(pd.DataFrame, header=1, index=False, expand='table').value = interest_bais.iloc[-200:]



    wb.save(filename)
    wb.close()
    app.quit()
    print('done')

def save_3800_index2db(start_date,end_date):

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


    sql = "select TDATE as jyrq,SYMBOL as zqdm,PCHG as zdfd,VATURNOVER as cjl,TURNOVER as hsbl,MCAP as zjsz from finchina.CHDQUOTE where TDATE>='{0}' and TDATE<='{1}' ".format(start_date,end_date)
    index_data=download_hbs_by_page('readonly', sql, page_num=300, data_name='Data in CHDQUOTE')

    index_data=pd.merge(index_data,
                        index_data.groupby('jyrq')['zjsz'].sum().to_frame('total_mv'),how='left',on='jyrq')
    index_data['w']=index_data['zjsz']/index_data['total_mv']
    for col in ['zdfd','hsbl','cjl']:
        index_data[col]=index_data[col]*index_data['w']

    index_data=index_data.groupby('jyrq')[['zdfd', 'hsbl','cjl']].sum().reset_index()

    index_data.to_sql('mimic_index_3800',if_exists='append',index=False,con=localdb)



if __name__ == '__main__':


    #end date must be week end date
    #FOF_track_pic('大类配置', '20230101', '20230825', '20231229')
    #
    # save_entire_jjpic2db(asofdate1='20230831',asofdate2='20230630'
    #                       ,if_prv=False,fre='Q')
    # get_mutual_fund_latest_pb_pe(['005827','001476'],'20231117')

    prv_pool_picture(latest_date='20240301',style_date='20231231',latest_HB1001_spjg=2052.97998314
                     ,cl_end_date='20240229',cl_start_date='20240131')
    #mutual_pool_picture('君瑞','20230630', '20230831', '20231130',fool_version=True,bmk_id='885001')
    #mutual_pool_picture('FOF1号','20230630', '20230831', '20231130',fool_version=True,bmk_id='885001')
    #mutual_pool_picture('公募核心池','20230630', '20230831', '20240229',fool_version=True)
    #mutual_pool_picture('公募30池偏股基金', '20230630', '20230831', '20240222',fool_version=True)
    #mutual_pool_picture('公募机构池', '20230630', '20230831', '20240222',fool_version=True)
    #mutual_pool_picture('牛基宝进取型', '20230630', '20230831', '20240222',fool_version=True,if_portfolio=True)
    #mutual_pool_picture('牛基宝全股型', '20230630', '20230831', '20240222',fool_version=True,if_portfolio=True)
    #quant_pool_picture('20240301')

    #
    #
    print('')

   # save_fund_industry_weight_his_tolocal(jjdm_list, "20150101", "20230501")



