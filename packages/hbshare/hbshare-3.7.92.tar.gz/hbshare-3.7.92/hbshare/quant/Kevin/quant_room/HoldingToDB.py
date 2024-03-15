"""
私募基金估值表持仓入库
"""
import datetime
import os
import pandas as pd
from sqlalchemy import create_engine
from hbshare.quant.Kevin.rm_associated.config import engine_params
from hbshare.quant.Kevin.asset_allocation.macro_index.util import create_table, delete_duplicate_records, WriteToDB


class HoldingExtractor:
    def __init__(self, data_path, table_name, fund_name, fund_type, is_increment=1):
        self.data_path = data_path
        self.table_name = table_name
        self.fund_name = fund_name
        self.fund_type = fund_type
        self.is_increment = is_increment

    def _load_portfolio_weight(self):
        filenames = os.listdir(self.data_path)
        filenames = [x for x in filenames if x.split('.')[-1] in ['xls', 'xlsx']]

        portfolio_weight_list = []
        for name in filenames:
            date = name.split('_')[-2]
            # 国君 & 海通
            if self.fund_name in ['因诺聚配中证500指数增强', '凡二中证500增强9号1期', '赫富500指数增强一号', '赫富1000指数增强一号',
                                  '宽德金选中证500指数增强6号', 'TEST', '量锐62号', '启林广进中证1000指数增强',
                                  '白鹭精选量化鲲鹏十号', '伯兄建康', '伯兄熙宁', '伯兄至道', '世纪前沿指数增强2号',
                                  '云起量化指数增强1号', '罗维盈安凌云增强2号', '朋锦永宁', '宽德中证1000指数增强8号',
                                  '稳博金选中证500指数增强6号', '稳博广博中证1000', '艾悉财赋1号', '艾悉财赋6号',
                                  '星阔广川21号中证500指数增强', '宽德飞虹1号', '龙旗500指增1号', '龙旗股票量化多头1号',
                                  '安子极客中证500指增一号', '致邃投资-智慧矩阵指数增强量化1号', '鸣熙中证500指数增强1号',
                                  '稳博对冲18号', '磐松1000指增', '仲阳500指增', '托特春晓中证1000指数增强2号',
                                  '宽德云飞扬1号', '宽德小洞天1号', '本利达利磐十五号', '超量子好买专享', '黑翼优选成长1号',
                                  '盛冠达股票量化2号', '致邃-量化6号', '玄信500指增', '玄信1000指增', '阳泽1000指增', '绰瑞金轮3号',
                                  '天算指数增强3号', '衍合1000指数增强1号', '衍合招享300指数增强2号', '宽辅中证500指数增强1号',
                                  '宽辅量化选股1号', '锐天福兴一号', '锐天核心二号', '艮岳新运1号', '聚宽500指增', '因诺500指增1号',
                                  '元图中证1000指数增强1号']:
                context = "市值占净值%"
                if self.fund_name in ['伯兄建康', '伯兄熙宁', '伯兄至道', '宽德飞虹1号', '盛冠达股票量化2号',
                                      '致邃-量化6号', '绰瑞金轮3号']:
                    hd = 2
                    context = "市值占净值(%)"
                elif self.fund_name in ['世纪前沿指数增强2号']:
                    hd = 2 if date >= '20210630' else 0
                    context = "市值占净值(%)"
                else:
                    hd = 3
                data = pd.read_excel(
                    os.path.join(self.data_path, name), sheet_name=0, header=hd).dropna(subset=['科目代码'])
                sh = data[data['科目代码'].str.startswith('11020101')]
                sz = data[data['科目代码'].str.startswith('11023101')]
                cyb = data[data['科目代码'].str.startswith('11024101')]
                kcb = data[data['科目代码'].str.startswith('1102C101')]
                df = pd.concat([sh, sz, cyb, kcb], axis=0).dropna()
                if self.fund_name in ['因诺聚配中证500指数增强']:
                    df['len'] = df['科目代码'].apply(lambda x: len(x))
                    df = df[df['len'] > 8]
                df['ticker'] = df['科目代码'].apply(lambda x: x[-6:])
                df.rename(columns={"科目名称": "sec_name", context: "weight"}, inplace=True)
                if self.fund_name in ['稳博对冲18号', '黑翼优选成长1号', '阳泽1000指增']:
                    df['weight'] = 100 * df['weight'] / df['weight'].sum()
                if self.fund_name in ['凡二中证500增强9号1期', '量锐62号', '罗维盈安凌云增强2号'] and \
                        type(df['weight'].tolist()[0]) == str:
                    df['weight'] = df['weight'].str.strip('%').astype(float)
            # 招商
            elif self.fund_name in ['星阔广厦1号中证500指数增强', '星阔上林1号', '星阔山海6号',
                                    '量客卓宇六号', '乾象中证500指数增强1号', '水木博雅500指增',
                                    '概率1000指增1号', '概率500指增2号', '稳博中性稳稳系列1号', '稳博中性稳稳系列2号',
                                    '稳博1000指数增强1号', '蒙玺量化对冲钧衡3号', '天戈500指增', '宽德九臻',
                                    '顽岩中证500指数增强5号', '托特中证500指数增强2号', '卓识500指数增强一号', '卓识辰熙',
                                    '世纪前沿指数增强24号', '世纪前沿量化优选一号', '本利达利磐八号', '锋滔指数增强2号',
                                    '知行通达500指增', '伯兄永隆', '华钧真观1期', '盛丰量化对冲9号', '信弘500指数增强1号',
                                    '千衍六和3号', '衍复臻选指数增强一号', '衍复臻选中证1000指数增强一号', '信弘征程2号',
                                    '凯读稳健8号', '凯读投资成长4号', '铭量中证500增强1号', '绰瑞金轮1号',
                                    '半鞅中证500指数增强1号', '半鞅量化精选', '睿量智行1号', '衍复小市值指数增强一号',
                                    '凡二量化选股3号1期', '托特中证500指数增强3号', '托特中证1000指数增强1号',
                                    '托特量化优选1号', '超量子500增强2号', '超量子1000增强9号', '磐松500指增',
                                    '博普万维指数增强1号', '博普心享1号', '博普万维指数增强2号', '博普万维量化多头1号',
                                    '联海星辰1号', '益清证金中证500指数增强一号', '卓胜中证500指数增强一号', '衍合500指数增强1号',
                                    '衍合量化选股1号', '锐天麦克斯韦一号', '元图中证500指数增强1号']:
                header = 6 if self.fund_name in ['星阔上林1号', '水木博雅500指增', '乾象中证500指数增强1号',
                                                 '稳博中性稳稳系列1号', '稳博中性稳稳系列2号',
                                                 '本利达利磐八号', '锋滔指数增强2号', '知行通达500指增', '华钧真观1期',
                                                 '盛丰量化对冲9号', '信弘500指数增强1号', '千衍六和3号', '信弘征程2号',
                                                 '铭量中证500增强1号', '半鞅量化精选', '睿量智行1号', '衍复小市值指数增强一号',
                                                 '托特中证500指数增强3号', '托特中证1000指数增强1号', '托特量化优选1号',
                                                 '超量子500增强2号', '超量子1000增强9号',
                                                 '磐松500指增', '博普万维指数增强2号'] else 7
                data = pd.read_excel(
                    os.path.join(self.data_path, name), sheet_name=0, header=header).dropna(subset=['科目代码'])
                data['科目代码'] = data['科目代码'].map(str)
                sh = data[data['科目代码'].str.endswith('SH')]
                sz = data[data['科目代码'].str.endswith('SZ')]
                df = pd.concat([sh, sz], axis=0)
                if self.fund_name in ['睿量智行1号', '千衍六和3号', '托特中证1000指数增强1号']:
                    df['科目名称'] = df['科目名称'].apply(lambda x: x.split('-')[-1])
                # add
                # df = df[df['科目代码'].str.startswith('1')]
                df = df[df['科目代码'].str.startswith('1102')]
                df['ticker'] = df['科目代码'].apply(lambda x: x.split(' ')[0][-6:])
                df.rename(columns={"科目名称": "sec_name", "市值占比": "weight"}, inplace=True)
                # if type(df['weight'].tolist()[0]) == str:
                #     df['weight'] = df['weight'].str.strip('%').astype(float)
                if self.fund_name in ["乾象中证500指数增强1号", "天戈500指增", '信弘500指数增强1号', '睿量智行1号',
                                      '托特中证500指数增强3号', '托特量化优选1号', '千衍六和3号']:
                    # 处理一下分红
                    ratio = data[data['科目代码'] == '资产净值']['市值占比'].values[0] / \
                        data[data['科目代码'] == '资产合计']['市值占比'].values[0]
                    df['weight'] *= ratio
                if self.fund_name in ['蒙玺量化对冲钧衡3号', '盛丰量化对冲9号', '凯读稳健8号', '凯读投资成长4号',
                                      '博普心享1号', '联海星辰1号']:
                    df['weight'] = df['weight'] / df['weight'].sum()
                # 衍复
                if self.fund_name in ['衍复臻选指数增强一号', '衍复臻选中证1000指数增强一号']:
                    if '1108.02' in data['科目代码'].tolist():
                        other_ratio = data.loc[data['科目代码'] == '1108.02', '市值占比'].values[0]
                    else:
                        other_ratio = 0.
                    df['weight'] *= (df['weight'].sum() + other_ratio) / df['weight'].sum()
                if self.fund_name in ['半鞅量化精选']:
                    if date == "20230531":
                        df['weight'] = 0.95 * df['weight'] / df['weight'].sum()
                if self.fund_name in ['磐松500指增']:
                    df['sec_name'] = df['sec_name'].apply(lambda x: x.split('-')[-1])
                if self.fund_name in ['衍合量化选股1号']:
                    if date == "20230331":
                        df['weight'] = 0.985 * df['weight'] / df['weight'].sum()
                df['weight'] *= 100.
            # 海通但有信用账户
            elif self.fund_name in ['朋锦金石炽阳']:
                data = pd.read_excel(
                    os.path.join(self.data_path, name), sheet_name=0, header=3).dropna(subset=['科目代码'])
                sh1 = data[data['科目代码'].str.startswith('11020101')]
                sh2 = data[data['科目代码'].str.startswith('11021101')]
                sz1 = data[data['科目代码'].str.startswith('11023101')]
                sz2 = data[data['科目代码'].str.startswith('11023201')]
                cyb1 = data[data['科目代码'].str.startswith('11024101')]
                cyb2 = data[data['科目代码'].str.startswith('11021501')]
                kcb1 = data[data['科目代码'].str.startswith('1102C101')]
                kcb2 = data[data['科目代码'].str.startswith('1102D201')]
                df = pd.concat([sh1, sh2, sz1, sz2, cyb1, cyb2, kcb1, kcb2], axis=0).dropna()
                df['ticker'] = df['科目代码'].apply(lambda x: x[-6:])
                df.rename(columns={"科目名称": "sec_name", "市值占净值%": "weight"}, inplace=True)
                df['weight'] = 100. * df['weight'] / df['weight'].sum()
            # 国君但有信用账户
            elif self.fund_name in ['思勰中证500指数增强1号', '丰润稳健6号', '垒昂金鹿指数增强6号', '宽德飞虹5号']:
                data = pd.read_excel(
                    os.path.join(self.data_path, name), sheet_name=0, header=3).dropna(subset=['科目代码'])
                del data['估值增值']
                sh1 = data[data['科目代码'].str.startswith('11020101')]
                sh2 = data[data['科目代码'].str.startswith('11021101')]
                sz1 = data[data['科目代码'].str.startswith('11023101')]
                sz2 = data[data['科目代码'].str.startswith('11021201')]
                cyb1 = data[data['科目代码'].str.startswith('11024101')]
                cyb2 = data[data['科目代码'].str.startswith('11021501')]
                kcb1 = data[data['科目代码'].str.startswith('1102C101')]
                kcb2 = data[data['科目代码'].str.startswith('1102D201')]
                df = pd.concat([sh1, sh2, sz1, sz2, cyb1, cyb2, kcb1, kcb2], axis=0).dropna()
                df['ticker'] = df['科目代码'].apply(lambda x: x[-6:])
                df.rename(columns={"科目名称": "sec_name", "市值占净值%": "weight"}, inplace=True)
            elif self.fund_name in ['致邃-量化5号']:
                data = pd.read_excel(
                    os.path.join(self.data_path, name), sheet_name=0, header=4).dropna(subset=['科目代码'])
                del data['权益信息']
                sh = data[data['科目代码'].str.startswith('1102.01.01')]
                kcb = data[data['科目代码'].str.startswith('1102.02.01')]
                sz = data[data['科目代码'].str.startswith('1102.33.01')]
                cyb = data[data['科目代码'].str.startswith('1102.34.01')]
                df = pd.concat([sh, sz, cyb, kcb], axis=0).dropna()
                df['ticker'] = df['科目代码'].apply(lambda x: x.split('.')[-1].split(' ')[0])
                df['市值比'] = df['市值比'].str.strip('%').astype(float)
                df.rename(columns={"科目名称": "sec_name", "市值比": "weight"}, inplace=True)
            elif self.fund_name in ['久期量和500指增']:
                data = pd.read_excel(
                    os.path.join(self.data_path, name), sheet_name=0, header=4).dropna(subset=['科目代码'])
                del data['权益信息']
                sh = data[data['科目代码'].str.startswith('1102.05.01')]
                kcb = data[data['科目代码'].str.startswith('1102.85.01')]
                sz = data[data['科目代码'].str.startswith('1102.37.01')]
                cyb1 = data[data['科目代码'].str.startswith('1102.34.01')]
                cyb2 = data[data['科目代码'].str.startswith('1102.38.01')]
                df = pd.concat([sh, sz, cyb1, cyb2, kcb], axis=0)
                df = df.dropna(how='all', axis=1).dropna()
                df['ticker'] = df['科目代码'].apply(lambda x: x.split('.')[-1].split(' ')[0])
                df['市值占比'] = df['市值占比'].str.strip('%').astype(float)
                df.rename(columns={"科目名称": "sec_name", "市值占比": "weight"}, inplace=True)
                df['weight'] = 100. * df['weight'] / df['weight'].sum()
            else:
                date = None
                df = pd.DataFrame()

            df['trade_date'] = date
            portfolio_weight_list.append(df[['trade_date', 'ticker', 'sec_name', 'weight']])

        portfolio_weight_df = pd.concat(portfolio_weight_list)
        portfolio_weight_df = portfolio_weight_df.groupby(
            ['trade_date', 'ticker', 'sec_name'])['weight'].sum().reset_index()
        portfolio_weight_df['fund_name'] = self.fund_name
        portfolio_weight_df['fund_type'] = self.fund_type
        portfolio_weight_df = portfolio_weight_df[portfolio_weight_df['ticker'].str[0].isin(('3', '0', '6'))]  # 剔除货基

        print(portfolio_weight_df.groupby('trade_date')['weight'].sum().sort_index())

        # portfolio_weight_df = pd.read_csv("D:\\holding_df.csv", dtype={"trade_date": str, "ticker": "str"})
        # self.fund_name = "新方程量化中小盘"

        trans_dict = {
            "托特春晓中证1000指数增强2号": "托特中证1000指数增强1号",
            "超量子好买专享": "超量子500增强2号",
            "绰瑞金轮3号": "绰瑞金轮1号"
        }
        if self.fund_name in trans_dict.keys():
            portfolio_weight_df['fund_name'] = portfolio_weight_df['fund_name'].map(trans_dict)
            self.fund_name = trans_dict[self.fund_name]

        # print(portfolio_weight_df['trade_date'].value_counts().sort_index())

        return portfolio_weight_df

    def writeToDB(self):
        if self.is_increment == 1:
            data = self._load_portfolio_weight()
            sql_script = "SELECT distinct trade_date FROM {} WHERE fund_name = '{}'".format(
                self.table_name, self.fund_name)
            engine = create_engine(engine_params)
            trade_dates = pd.read_sql(sql_script, engine)
            trade_dates['trade_date'] = trade_dates['trade_date'].apply(
                lambda x: datetime.datetime.strftime(x, "%Y%m%d"))
            add_data = data[~data['trade_date'].isin(trade_dates['trade_date'].tolist())]
            # add new records
            WriteToDB().write_to_db(add_data, self.table_name)
        else:
            sql_script = """
                create table {}(
                id int auto_increment primary key,
                trade_date date not null,
                ticker varchar(10),
                sec_name varchar(20),
                weight decimal(5, 4),
                fund_name varchar(20),
                fund_type varchar(20))
            """.format(self.table_name)
            create_table(self.table_name, sql_script)
            data = self._load_portfolio_weight()
            WriteToDB().write_to_db(data, self.table_name)


def holding_to_db_by():
    trade_date = "20230430"
    filename = "D:\\估值表基地\\倍漾中证1000指增1期\\SXZ461_倍漾中证1000指数增强1期私募证券投资基金_产品估值表_日报_20230427.xlsx"
    xls = pd.ExcelFile(filename)
    tables = xls.sheet_names
    header_data = pd.read_excel(filename, sheet_name=tables[0], header=1)
    share_columns = header_data.columns
    data_list = [header_data]
    for s_name in tables[1:]:
        data = pd.read_excel(filename, sheet_name=s_name, header=None)
        data.columns = share_columns
        data_list.append(data)
    holding_df = pd.concat(data_list).dropna(subset=['科目代码'])
    holding_df['科目代码'] = holding_df['科目代码'].map(str)
    sh = holding_df[holding_df['科目代码'].str.endswith('SH')]
    sz = holding_df[holding_df['科目代码'].str.endswith('SZ')]
    df = pd.concat([sh, sz], axis=0)
    df = df[df['科目代码'].str.startswith('1102')]
    df['ticker'] = df['科目代码'].apply(lambda x: x.split(' ')[0][-6:])
    df.rename(columns={"科目名称": "sec_name", "市值占比": "weight"}, inplace=True)
    df['weight'] *= 100.
    df['trade_date'] = trade_date
    df['sec_name'] = df['sec_name'].apply(lambda x: x.split('-')[-1])
    all_data = df.groupby(['trade_date', 'ticker', 'sec_name'])['weight'].sum().reset_index()
    all_data['fund_name'] = "倍漾中证1000指增1期"
    all_data['fund_type'] = "1000指增"
    all_data = all_data[all_data['ticker'].str[0].isin(('3', '0', '6'))]

    return all_data


if __name__ == '__main__':
    name_outer = '元图中证1000指数增强1号'
    HoldingExtractor(data_path='D:\\估值表基地\\{}'.format(name_outer), table_name="private_fund_holding",
                     fund_name=name_outer, fund_type="1000指增").writeToDB()
    # holding_to_db_by()