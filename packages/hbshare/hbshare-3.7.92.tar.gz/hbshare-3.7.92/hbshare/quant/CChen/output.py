#!/usr/bin/python
# coding:utf-8
from hbshare.quant.CChen.data.data import load_funds_data, load_funds_alpha
from hbshare.quant.CChen.fund_stats.perf import ret
import pandas as pd
import numpy as np
import pyecharts.options as opts
from datetime import datetime, timedelta
from pyecharts.charts import Line, Grid, Bar, Boxplot, Pie
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
import pymysql
from sqlalchemy import create_engine
from hbshare.quant.CChen.cons import index_underlying, underlying_code
from hbshare.quant.CChen.fut import (
    wind_fin_fut_index,
    wind_com_fut_sec_index,
    wind_stk_index_basis,
    fin_fut_daily_k_by_contracts,
    fut_com_amount_by_ex,
    rolling_volatility,
)
from hbshare.quant.CChen.data.hsjy_data import load_fut_fin
from hbshare.quant.CChen.stk import load_index
from hbshare.quant.CChen.cons import sql_write_path_hb as path_hb, HSJY_VIRTUAL_CONTRACT

pymysql.install_as_MySQLdb()


# def nav_lines(
#         fund_list, start_date, end_date, db_path=path_hb['daily'], cal_path=path_hb['work'],
#         title='', zz=False, axis_cross=None, all_selected=True, print_info=True
# ):
#     if axis_cross:
#         axis_cross = opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
#
#     if zz:
#         funds_data = load_funds_alpha(
#             fund_list=fund_list,
#             first_date=start_date,
#             end_date=end_date,
#             db_path=db_path,
#             cal_db_path=cal_path,
#             print_info=print_info,
#         )['eav']
#     else:
#         funds_data = load_funds_data(
#             fund_list=fund_list,
#             first_date=start_date,
#             end_date=end_date,
#             db_path=db_path,
#             cal_db_path=cal_path,
#             print_info=print_info,
#             # freq='',
#             # fillna=False
#         )
#
#     web = Line(
#         init_opts=opts.InitOpts(
#             page_title=title,
#             width='700px',
#             height='500px',
#             theme=ThemeType.CHALK
#         )
#     ).set_global_opts(
#         tooltip_opts=opts.TooltipOpts(is_show=True),
#         toolbox_opts=opts.ToolboxOpts(is_show=True),
#         xaxis_opts=opts.AxisOpts(type_="category"),
#         yaxis_opts=opts.AxisOpts(
#             type_="value",
#             axistick_opts=opts.AxisTickOpts(is_show=True),
#             splitline_opts=opts.SplitLineOpts(is_show=True),
#         ),
#     ).add_xaxis(
#         xaxis_data=funds_data['t_date'].tolist()
#     )
#     funds = funds_data.columns.tolist()
#
#     funds.remove('t_date')
#     for j in funds:
#         nav_data = funds_data[j] / funds_data[funds_data[j] > 0][j].tolist()[0]
#         web.add_yaxis(
#             series_name=j,
#             y_axis=nav_data.round(4).tolist(),
#             symbol="emptyCircle",
#             is_symbol_show=True,
#             label_opts=opts.LabelOpts(is_show=False),
#             is_selected=all_selected
#         )
#
#     web.set_global_opts(
#         xaxis_opts=opts.AxisOpts(
#             is_scale=True,
#             type_="category", boundary_gap=False
#         ),
#         yaxis_opts=opts.AxisOpts(
#             is_scale=True,
#             splitarea_opts=opts.SplitAreaOpts(
#                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
#             ),
#         ),
#         legend_opts=opts.LegendOpts(
#             # type_='scroll',
#             pos_top='5%'
#         ),
#         datazoom_opts=[
#             opts.DataZoomOpts(range_start=0, range_end=100),
#             # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
#             # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
#             opts.DataZoomOpts(type_="inside")
#         ],
#         title_opts=opts.TitleOpts(title=title),
#         tooltip_opts=axis_cross
#     )
#
#     return web
#
#
# def gen_grid(
#         end_date, funds, zz=False, lookback_years=3, db_path=path_hb['work'], cal_path=path_hb['daily'],
#         grid_width=1200, grid_height=500, pos_top=23,
#         axis_cross=None,
#         all_selected=True,
#         print_info=True
# ):
#     if axis_cross:
#         axis_cross = opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
#
#     engine = create_engine(db_path)
#     start_date = end_date - timedelta(days=365 * lookback_years + 7)
#     start_date2 = end_date - timedelta(days=365 + 7)
#     if len(funds) > 1:
#         fund_list = pd.read_sql_query(
#             'select * from fund_list where `name` in ' + str(tuple(funds)) + ' order by `name`', engine
#         )
#     else:
#         fund_list = pd.read_sql_query(
#             'select * from fund_list where `name`="' + str(funds[0]) + '"', engine
#         )
#
#     grid_nav = Grid(init_opts=opts.InitOpts(width=str(grid_width) + "px", height=str(grid_height) + "px"))
#
#     web = nav_lines(
#         fund_list=fund_list,
#         start_date=start_date,
#         end_date=end_date,
#         zz=zz,
#         db_path=db_path,
#         cal_path=cal_path,
#         all_selected=all_selected,
#         print_info=print_info,
#     )
#
#     web2 = nav_lines(
#         fund_list=fund_list,
#         start_date=start_date2,
#         end_date=end_date,
#         zz=zz,
#         db_path=db_path,
#         cal_path=cal_path,
#         all_selected=all_selected,
#         print_info=print_info,
#     )
#
#     grid_nav.add(
#         web.set_global_opts(
#             title_opts=opts.TitleOpts(
#                 title='近' + str(lookback_years) + '年: '
#                       + start_date.strftime('%Y/%m/%d')
#                       + '~' + end_date.strftime('%Y/%m/%d'),
#                 pos_right="5%"
#             ),
#             tooltip_opts=axis_cross,
#             legend_opts=opts.LegendOpts(
#                 pos_top="7%"
#             )
#         ),
#         grid_opts=opts.GridOpts(pos_left='55%', pos_top=str(pos_top) + "%")
#     ).add(
#         web2.set_global_opts(
#             title_opts=opts.TitleOpts(
#                 title='近一年: '
#                       + start_date2.strftime('%Y/%m/%d') + '~' + end_date.strftime('%Y/%m/%d')
#                 ,
#                 pos_left="5%"
#             ),
#             tooltip_opts=axis_cross,
#             legend_opts=opts.LegendOpts(
#                 pos_top="7%"
#             )
#         ),
#         grid_opts=opts.GridOpts(pos_right='55%', pos_top=str(pos_top) + "%")
#     )
#     return grid_nav


def index_fut_basis_wind(
        index_code, start_date, end_date, sql_path=path_hb['daily'], table='futures_wind',
        grid_width=1200, grid_height=400, zoom_left=0, zoom_right=100, chart_pos_left=10, chart_pos_right=15,
):
    data_00, data_01, data_02, data_03 = wind_stk_index_basis(
        code=index_code, start_date=start_date, end_date=end_date, sql_path=sql_path, table=table
    )

    web = Line(
        # init_opts=opts.InitOpts(width="1200px", height="400px")
    ).add_xaxis(
        xaxis_data=data_00['t_date'].tolist()
    ).add_yaxis(
        series_name=index_underlying[index_code],
        y_axis=(data_00['underlying'] / data_00['underlying'][0]).round(4),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        is_selected=False,
    ).add_yaxis(
        series_name='当月',
        y_axis=(data_00['close'] / data_00['close'][0]).round(4),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        is_selected=False,
    ).add_yaxis(
        series_name='次月',
        y_axis=(data_01['close'] / data_01['close'][0]).round(4),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        is_selected=False,
    ).add_yaxis(
        series_name='季月',
        y_axis=(data_02['close'] / data_02['close'][0]).round(4),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        is_selected=False,
    ).add_yaxis(
        series_name='次季',
        y_axis=(data_03['close'] / data_03['close'][0]).round(4),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        is_selected=False,
    ).extend_axis(
        yaxis=opts.AxisOpts(
            name='年化基差',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            position="right",
            # interval=5,
            min_='dataMin',
            max_='dataMax',
        )
    ).extend_axis(
            yaxis=opts.AxisOpts(
                name='基差变化',
                axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                position="right",
                offset=80,
                min_='dataMin',
                max_='dataMax',
                # interval=5
                )
    ).set_global_opts(
        title_opts=opts.TitleOpts(
            title=data_00['t_date'][len(data_00) - 1]
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        # toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            min_='dataMin',
            max_='dataMax',
        ),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=zoom_left, range_end=zoom_right),
            # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
            # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
            opts.DataZoomOpts(type_="inside")
        ],
        legend_opts=opts.LegendOpts(
            pos_top="7%",
            pos_left='10%',
            pos_right='10%'
        )
    )

    web2 = Line().add_xaxis(
        xaxis_data=data_00['t_date'].tolist()
    ).add_yaxis(
        series_name='当月基差',
        y_axis=data_00['basis'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=1,
        is_selected=False,
    ).add_yaxis(
        series_name='次月基差',
        y_axis=data_01['basis'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=1,
        # is_selected=False,
    ).add_yaxis(
        series_name='季月基差',
        y_axis=data_02['basis'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=1,
        # is_selected=False,
    ).add_yaxis(
        series_name='次季基差',
        y_axis=data_03['basis'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=1,
        # is_selected=False,
    ).add_yaxis(
        series_name='4基差简单平均',
        y_axis=(data_00['basis'] + data_01['basis'] + data_02['basis'] + data_03['basis']).round(2).tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=1,
        is_selected=False,
    ).add_yaxis(
        series_name='4基差成交量加权平均',
        y_axis=(
            (
                    data_00['basis'] * data_00['volume']
                    + data_01['basis'] * data_01['volume']
                    + data_02['basis'] * data_02['volume']
                    + data_03['basis'] * data_03['volume']
            ) / (data_00['volume'] + data_01['volume'] + data_02['volume'] + data_03['volume'])
        ).round(2).tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=1,
        is_selected=False,
    )

    web3 = Bar().add_xaxis(
        xaxis_data=data_00['t_date'].tolist()
    ).add_yaxis(
        series_name='变化/当月',
        y_axis=data_00['basis_chg'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=2,
        is_selected=False,
    ).add_yaxis(
        series_name='变化/次月',
        y_axis=data_01['basis_chg'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=2,
        is_selected=False,
    ).add_yaxis(
        series_name='变化/季月',
        y_axis=data_02['basis_chg'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=2,
        is_selected=False,
    ).add_yaxis(
        series_name='变化/次季',
        y_axis=data_03['basis_chg'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=2,
        is_selected=False,
    )

    web.overlap(web2).overlap(web3)

    grid = (
        Grid(init_opts=opts.InitOpts(
            width=str(grid_width) + "px", height=str(grid_height) + "px")
        ).add(
            web, grid_opts=opts.GridOpts(
                pos_right=str(chart_pos_right) + "%",
                pos_left=str(chart_pos_left) + "%",
                pos_top='25%',
            ),
            is_control_axis_index=True
        )
    )
    return grid


def index_fut_basis_wind_detail(
        index_code, start_date, end_date, sql_path=path_hb['daily'], table='futures_wind',
        grid_width=1200, grid_height=400, zoom_left=0, zoom_right=100, chart_pos_left=10, chart_pos_right=15,
):
    engine = create_engine(sql_path)

    data_raw = pd.read_sql_query(
        'select * from ' + table
        + ' where `t_date`<=' + end_date.strftime('%Y%m%d')
        + ' and `t_date`>=' + start_date.strftime('%Y%m%d')
        + ' and `product`=\'' + index_code + '\' order by `t_date`',
        engine
    )
    contracts = data_raw['code'].drop_duplicates().sort_values(ascending=False).tolist()

    data_o = data_raw[['t_date', 'underlying']].drop_duplicates(['t_date']).reset_index(drop=True)
    web = Line(
        # init_opts=opts.InitOpts(width="1200px", height="400px")
    ).add_xaxis(
        xaxis_data=data_o['t_date']
    ).add_yaxis(
        series_name=index_underlying[index_code],
        y_axis=(data_o['underlying'] / data_o['underlying'][0]).round(4),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        # is_selected=False,
    )

    data_bucket = {}
    for c in range(min(len(contracts), 4)):
        data_bucket[contracts[c]] = data_o[['t_date']].merge(
            data_raw[data_raw['code'] == contracts[c]].reset_index(drop=True),
            on='t_date', how='left'
        )

        # data_bucket[contracts[c]]['remain'] = (
        #         data_bucket[contracts[c]]['delist_date'] - data_bucket[contracts[c]]['t_date']
        # ).map(lambda x: x.days)
        data_bucket[contracts[c]]['basis'] = round(
            - data_bucket[contracts[c]]['basis']
            / data_bucket[contracts[c]]['underlying']
            # / data_bucket[contracts[c]]['remain'] * 365
            * 100,
            2
        )
        data_bucket[contracts[c]]['basis_chg'] = round(
            (
                    data_bucket[contracts[c]]['close'] / data_bucket[contracts[c]]['close'].shift(1)
                    - data_bucket[contracts[c]]['underlying'] / data_bucket[contracts[c]]['underlying'].shift(1)
            ) * 100, 2
        )
        if c == 1:
            selected = True
        else:
            selected = False
        web.add_yaxis(
            series_name=contracts[c][2:6],
            y_axis=(
                    data_bucket[contracts[c]]['close']
                    / data_bucket[contracts[c]][data_bucket[contracts[c]]['close'] > 0]['close'].tolist()[0]
            ).round(4),
            label_opts=opts.LabelOpts(is_show=False),
            yaxis_index=0,
            is_selected=selected,
        )

    web.extend_axis(
        yaxis=opts.AxisOpts(
            name='基差',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            position="right",
            # interval=5,
            min_='dataMin',
            max_='dataMax',
        )
    ).extend_axis(
        yaxis=opts.AxisOpts(
            name='基差变化',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            position="right",
            offset=80,
            min_='dataMin',
            max_='dataMax',
            # interval=5
        )
    ).set_global_opts(
        title_opts=opts.TitleOpts(
            title=data_raw['t_date'][len(data_raw) - 1]
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        # toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            min_='dataMin',
            max_='dataMax',
        ),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=zoom_left, range_end=zoom_right),
            # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
            # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
            opts.DataZoomOpts(type_="inside")
        ],
        legend_opts=opts.LegendOpts(
            pos_top="7%",
            pos_left='10%',
            pos_right='10%'
        )
    )

    web2 = Line().add_xaxis(
        xaxis_data=data_o['t_date']
    )
    web3 = Bar().add_xaxis(
        xaxis_data=data_o['t_date']
    )
    for c in range(min(len(contracts), 4)):
        if c == 1:
            selected = True
        else:
            selected = False
        web2.add_yaxis(
            series_name=contracts[c][2:6] + '基差',
            y_axis=data_bucket[contracts[c]]['basis'].tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            yaxis_index=1,
            is_selected=False,
        )

        web3.add_yaxis(
            series_name=contracts[c][2:6] + '变化',
            y_axis=data_bucket[contracts[c]]['basis_chg'].tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            yaxis_index=2,
            is_selected=selected,
            # areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        )

    web.overlap(web2).overlap(web3)

    grid = (
        Grid(init_opts=opts.InitOpts(
            width=str(grid_width) + "px", height=str(grid_height) + "px")
        ).add(
            web, grid_opts=opts.GridOpts(
                pos_right=str(chart_pos_right) + "%",
                pos_left=str(chart_pos_left) + "%",
                pos_top='25%',
            ),
            is_control_axis_index=True
        )
    )
    return grid


def index_fut_basis_hsjy(
        index_code, start_date, end_date,
        grid_width=1200, grid_height=400, zoom_left=0, zoom_right=100, chart_pos_left=10, chart_pos_right=15,
):
    data = load_fut_fin(index_code=index_code, start_date=start_date, end_date=end_date)
    data_o = load_index(index_list=[underlying_code[index_code]], start_date=start_date, end_date=end_date)
    data_o['TDATE'] = pd.to_datetime(data_o['TDATE']).dt.date
    data['TDATE'] = pd.to_datetime(data['TDATE']).dt.date

    contracts = data[['CODE']].drop_duplicates()
    contracts['keep'] = contracts['CODE'].apply(lambda x: True if 'y' in x.lower() else False)
    contracts = contracts[contracts['keep']].sort_values(by='CODE', ascending=False)['CODE'].tolist()

    data = data.pivot(index='TDATE', columns='CODE', values='CLOSE')

    web = Line(
        # init_opts=opts.InitOpts(width="1200px", height="400px")
    ).add_xaxis(
        xaxis_data=data_o['TDATE']
    ).add_yaxis(
        series_name=index_underlying[index_code],
        y_axis=(data_o['CLOSE'] / data_o['CLOSE'][0]).round(4),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        # is_selected=False,
    )

    data_bucket = {}
    for c in range(min(len(contracts), 4)):
        data_bucket[contracts[c]] = data_o[['TDATE', 'CLOSE']].merge(
            data[contracts[c]].reset_index(),
            on='TDATE', how='left'
        )

        data_bucket[contracts[c]]['basis'] = round(
            (data_bucket[contracts[c]][contracts[c]] - data_bucket[contracts[c]]['CLOSE'])
            / data_bucket[contracts[c]]['CLOSE'] * 100,
            2
        )
        data_bucket[contracts[c]]['basis_chg'] = round(
            (
                    data_bucket[contracts[c]][contracts[c]] / data_bucket[contracts[c]][contracts[c]].shift(1)
                    - data_bucket[contracts[c]]['CLOSE'] / data_bucket[contracts[c]]['CLOSE'].shift(1)
            ) * 100, 2
        )
        if c == 1:
            selected = True
        else:
            selected = False
        web.add_yaxis(
            series_name=contracts[c][2:6],
            y_axis=(
                    data_bucket[contracts[c]][contracts[c]]
                    / data_bucket[contracts[c]][data_bucket[contracts[c]][contracts[c]] > 0][contracts[c]].tolist()[0]
            ).round(4),
            label_opts=opts.LabelOpts(is_show=False),
            yaxis_index=0,
            is_selected=selected,
        )

    web.extend_axis(
        yaxis=opts.AxisOpts(
            name='基差',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            position="right",
            # interval=5,
            min_='dataMin',
            max_='dataMax',
        )
    ).extend_axis(
        yaxis=opts.AxisOpts(
            name='基差变化',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            position="right",
            offset=80,
            min_='dataMin',
            max_='dataMax',
            # interval=5
        )
    ).set_global_opts(
        title_opts=opts.TitleOpts(
            title=data_o['TDATE'][len(data_o) - 1]
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        # toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            min_='dataMin',
            max_='dataMax',
        ),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=zoom_left, range_end=zoom_right),
            # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
            # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
            opts.DataZoomOpts(type_="inside")
        ],
        legend_opts=opts.LegendOpts(
            pos_top="7%",
            pos_left='10%',
            pos_right='10%'
        )
    )

    web2 = Line().add_xaxis(
        xaxis_data=data_o['TDATE']
    )
    web3 = Bar().add_xaxis(
        xaxis_data=data_o['TDATE']
    )
    for c in range(min(len(contracts), 4)):
        if c == 1:
            selected = True
        else:
            selected = False
        web2.add_yaxis(
            series_name=contracts[c][2:6] + '基差',
            y_axis=data_bucket[contracts[c]]['basis'].tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            yaxis_index=1,
            is_selected=False,
        )

        web3.add_yaxis(
            series_name=contracts[c][2:6] + '变化',
            y_axis=data_bucket[contracts[c]]['basis_chg'].tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            yaxis_index=2,
            is_selected=selected,
            # areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        )

    web.overlap(web2).overlap(web3)

    grid = (
        Grid(init_opts=opts.InitOpts(
            width=str(grid_width) + "px", height=str(grid_height) + "px")
        ).add(
            web, grid_opts=opts.GridOpts(
                pos_right=str(chart_pos_right) + "%",
                pos_left=str(chart_pos_left) + "%",
                pos_top='25%',
            ),
            is_control_axis_index=True
        )
    )
    return grid


def index_fut_basis_hsjy_detail(
        index_code, start_date, end_date,
        grid_width=1200, grid_height=400, zoom_left=0, zoom_right=100, chart_pos_left=10, chart_pos_right=15,
):

    data = load_fut_fin(index_code=index_code, start_date=start_date, end_date=end_date)
    data_o = load_index(index_list=[underlying_code[index_code]], start_date=start_date, end_date=end_date)
    data_o['TDATE'] = pd.to_datetime(data_o['TDATE']).dt.date
    data['TDATE'] = pd.to_datetime(data['TDATE']).dt.date

    contracts = data[['CODE']].drop_duplicates()
    contracts['keep'] = contracts['CODE'].apply(lambda x: False if 'y' in x.lower() else True)
    contracts = contracts[contracts['keep']].sort_values(by='CODE', ascending=False)['CODE'].tolist()

    data = data.pivot(index='TDATE', columns='CODE', values='CLOSE')

    web = Line(
        # init_opts=opts.InitOpts(width="1200px", height="400px")
    ).add_xaxis(
        xaxis_data=data_o['TDATE']
    ).add_yaxis(
        series_name=index_underlying[index_code],
        y_axis=(data_o['CLOSE'] / data_o['CLOSE'][0]).round(4),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        # is_selected=False,
    )

    data_bucket = {}
    for c in range(min(len(contracts), 4)):
        data_bucket[contracts[c]] = data_o[['TDATE', 'CLOSE']].merge(
            data[contracts[c]].reset_index(),
            on='TDATE', how='left'
        )

        data_bucket[contracts[c]]['basis'] = round(
            (data_bucket[contracts[c]][contracts[c]] - data_bucket[contracts[c]]['CLOSE'])
            / data_bucket[contracts[c]]['CLOSE'] * 100,
            2
        )
        data_bucket[contracts[c]]['basis_chg'] = round(
            (
                data_bucket[contracts[c]][contracts[c]] / data_bucket[contracts[c]][contracts[c]].shift(1)
                - data_bucket[contracts[c]]['CLOSE'] / data_bucket[contracts[c]]['CLOSE'].shift(1)
            ) * 100, 2
        )
        if c == 1:
            selected = True
        else:
            selected = False
        web.add_yaxis(
            series_name=contracts[c][2:6],
            y_axis=(
                    data_bucket[contracts[c]][contracts[c]]
                    / data_bucket[contracts[c]][data_bucket[contracts[c]][contracts[c]] > 0][contracts[c]].tolist()[0]
            ).round(4),
            label_opts=opts.LabelOpts(is_show=False),
            yaxis_index=0,
            is_selected=selected,
        )

    web.extend_axis(
        yaxis=opts.AxisOpts(
            name='基差',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            position="right",
            # interval=5,
            min_='dataMin',
            max_='dataMax',
        )
    ).extend_axis(
        yaxis=opts.AxisOpts(
            name='基差变化',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            position="right",
            offset=80,
            min_='dataMin',
            max_='dataMax',
            # interval=5
        )
    ).set_global_opts(
        title_opts=opts.TitleOpts(
            title=data_o['TDATE'][len(data_o) - 1]
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        # toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            min_='dataMin',
            max_='dataMax',
        ),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=zoom_left, range_end=zoom_right),
            # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
            # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
            opts.DataZoomOpts(type_="inside")
        ],
        legend_opts=opts.LegendOpts(
            pos_top="7%",
            pos_left='10%',
            pos_right='10%'
        )
    )

    web2 = Line().add_xaxis(
        xaxis_data=data_o['TDATE']
    )
    web3 = Bar().add_xaxis(
        xaxis_data=data_o['TDATE']
    )
    for c in range(min(len(contracts), 4)):
        if c == 1:
            selected = True
        else:
            selected = False
        web2.add_yaxis(
            series_name=contracts[c][2:6] + '基差',
            y_axis=data_bucket[contracts[c]]['basis'].tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            yaxis_index=1,
            is_selected=False,
        )

        web3.add_yaxis(
            series_name=contracts[c][2:6] + '变化',
            y_axis=data_bucket[contracts[c]]['basis_chg'].tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            yaxis_index=2,
            is_selected=selected,
            # areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        )

    web.overlap(web2).overlap(web3)

    grid = (
        Grid(init_opts=opts.InitOpts(
            width=str(grid_width) + "px", height=str(grid_height) + "px")
        ).add(
            web, grid_opts=opts.GridOpts(
                pos_right=str(chart_pos_right) + "%",
                pos_left=str(chart_pos_left) + "%",
                pos_top='25%',
            ),
            is_control_axis_index=True
        )
    )
    return grid


def fut_sec_stats_wind(
        start_date=datetime(2010, 1, 1).date(), end_date=datetime.now().date(),
        db_path=path_hb['daily'], grid_width=1200, grid_height=600, key='amount', freq=None, to_excel=False
):
    com_data = wind_com_fut_sec_index(start_date=start_date, end_date=end_date, db_path=db_path, key=key, decimal=1)
    index_data = wind_fin_fut_index(start_date=start_date, end_date=end_date, db_path=db_path, key=key, decimal=1)
    data = com_data.merge(index_data, on='t_date')
    columns = data.columns.tolist()
    columns.pop(columns.index('t_date'))

    data = data.set_index(pd.to_datetime(data['t_date']))
    x_axis = data['t_date']
    if freq is not None:
        x_axis = data['t_date'].resample(freq).last()
        data = data.resample(freq).mean()

    if to_excel:
        data.index = pd.to_datetime(data.index).date.tolist()
        return data

    if key.lower() == 'oi_amount':
        name = '期货持仓额(日均)'
        decimal = 100000000
        unit_str = '亿元'
    elif key.lower() == 'volume':
        name = '期货成交量(日均)'
        decimal = 10000
        unit_str = '万手'
    elif key.lower() == 'oi':
        name = '期货持仓量(日均)'
        decimal = 10000
        unit_str = '万手'
    else:
        name = '期货成交额(日均)'
        decimal = 100000000
        unit_str = '亿元'

    web = Line().add_xaxis(xaxis_data=x_axis)

    for i in columns:
        web.add_yaxis(
            series_name=i,
            y_axis=(data[i] / decimal).round(2).tolist(),
            stack='总量',
            label_opts=opts.LabelOpts(is_show=False),
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        )

    web.set_global_opts(
        title_opts=opts.TitleOpts(title=name),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axislabel_opts=opts.LabelOpts(formatter="{value} " + unit_str),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        datazoom_opts=[
            opts.DataZoomOpts(
                range_start=0,
                range_end=100,
                # is_show=False,
                type_="inside",
                # xaxis_index=[0, 1],
            ),
            opts.DataZoomOpts(
            #     is_show=True,
            #     xaxis_index=[0, 1],
            #     type_="slider",
            #     pos_top="90%",
            #     range_start=98,
            #     range_end=100,
            ),
        ],
        legend_opts=opts.LegendOpts(
            orient="vertical",
            type_='scroll',
            pos_top="10%",
            pos_left='77%',
            pos_right='5%',
            pos_bottom="5%",
        )
    )
    # web2.set_global_opts(
    #     legend_opts=opts.LegendOpts(
    #         pos_top="7%",
    #         pos_left='10%',
    #         pos_right='20%'
    #     )
    # )
    grid = (
        Grid(
            init_opts=opts.InitOpts(
                width=str(grid_width) + "px",
                height=str(grid_height) + "px"
            ),
        ).add(
            web, grid_opts=opts.GridOpts(
                pos_right="25%",
                pos_left="8%",
                pos_top="10%",
                pos_bottom="15%"
                # pos_bottom='50%'
            ),
            # is_control_axis_index=True
        # ).add(
        #     web2, grid_opts=opts.GridOpts(
        #         pos_right="20%",
        #         pos_left="10%",
        #         pos_top='55%',
        #         pos_bottom='15%'
        #     ),
        )
    )

    return grid


def fin_fut_stats(product, start_date=None, end_date=None, grid_width=1200, grid_height=600, to_excel=False):
    if start_date is None:
        start_date = datetime(2010, 1, 1).date()
    if end_date is None:
        end_date = datetime.now().date()

    fut_data = fin_fut_daily_k_by_contracts(
        contract_list=HSJY_VIRTUAL_CONTRACT['FINANCE'][product].values(),
        start_date=start_date,
        end_date=end_date
    )
    transaction_data = pd.DataFrame(fut_data['data'])
    transaction_data['TRADINGDAY'] = pd.to_datetime(transaction_data['TRADINGDAY']).dt.date.tolist()
    transaction_data = transaction_data.groupby(by='TRADINGDAY').sum()[
        ['TurnoverVolume'.upper(), 'TurnoverValue'.upper(), 'OpenInterest'.upper()]
    ].reset_index()
    if to_excel:
        return transaction_data

    web = Line(
        # init_opts=opts.InitOpts(width="1200px", height="400px")
    ).add_xaxis(
        xaxis_data=transaction_data['TRADINGDAY'].tolist()
    ).add_yaxis(
        series_name='成交量',
        y_axis=list(transaction_data['TurnoverVolume'.upper()].values / 10000),
        linestyle_opts=opts.LineStyleOpts(
            # color="red",
            width=1,
            # type_="dashed"
        ),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0
    ).extend_axis(
        yaxis=opts.AxisOpts(
            name='持仓量',
            axislabel_opts=opts.LabelOpts(formatter="{value} 万手"),
            position="right",
            # interval=5
        )
    ).extend_axis(
        yaxis=opts.AxisOpts(
            name='成交额',
            axislabel_opts=opts.LabelOpts(formatter="{value} 亿元"),
            position="right",
            offset=80
            # interval=5
        )
    ).set_global_opts(
        title_opts=opts.TitleOpts(
            title=product + ' ' + transaction_data['TRADINGDAY'][len(transaction_data) - 1].strftime('%Y-%m-%d')
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        # toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} 万手")),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=100),
            # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
            # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
            opts.DataZoomOpts(type_="inside")
        ]
    )

    web2 = Line().add_xaxis(
        xaxis_data=transaction_data['TRADINGDAY'].tolist()
    ).add_yaxis(
        series_name='持仓量',
        y_axis=list(transaction_data['OpenInterest'.upper()].values / 10000),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=1
    )

    web3 = Line().add_xaxis(
        xaxis_data=transaction_data['TRADINGDAY'].tolist()
    ).add_yaxis(
        series_name='成交额',
        y_axis=list(transaction_data['TurnoverValue'.upper()].values / 100000000),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=2
    )

    web.overlap(web2).overlap(web3)

    grid = (
        Grid(init_opts=opts.InitOpts(
            width=str(grid_width) + "px", height=str(grid_height) + "px")
        ).add(
            web, grid_opts=opts.GridOpts(pos_right="20%", pos_left="10%"),
            is_control_axis_index=True
        )
    )

    return grid


def funds_return_stats(
        funds, end_date, lookback_year, grid_width=1200, grid_height=600, pos_top=20, interval=0.5,
        dtype='', fillna=False, freq='w',
        db_path=path_hb['work'], cal_path=path_hb['daily']
):
    date_end = end_date
    date_start = date_end - timedelta(days=365 * lookback_year)
    table = 'fund_list'

    fund_list = pd.read_sql_query(
        'select * from ' + table + ' where `name` in ' + str(tuple(funds)), create_engine(db_path)
    )

    if dtype.lower() != 'alpha':
        funds_data = load_funds_data(
            fund_list=fund_list,
            first_date=date_start,
            end_date=date_end,
            fillna=fillna,
            db_path=db_path,
            cal_db_path=cal_path,
            freq=freq
        )
    else:
        funds_data = load_funds_alpha(
            fund_list=fund_list,
            first_date=date_start,
            end_date=date_end,
            fillna=fillna,
            db_path=db_path,
            cal_db_path=cal_path,
            freq=freq
        )

    ret_df = ret(data_df=funds_data)
    ret_data = ret_df[funds]
    ret_values = np.reshape(ret_data.values, (1, ret_data.values.shape[0] * ret_data.values.shape[1]))
    ret_values = ret_values[~np.isnan(ret_values)] * 100
    ret_floor = np.floor(min(ret_values)) - 1
    ret_ceil = np.ceil(max(ret_values))
    ret_space = np.linspace(start=ret_floor, stop=ret_ceil, num=int((ret_ceil - ret_floor) / interval + 1))
    dist_df = pd.DataFrame({'zone': ret_space})
    dist_df['label'] = dist_df['zone'].apply(lambda x: str(x) + '% ~ ' + str(x + interval) + '%')
    for i in funds:
        dist_df[i] = 0
        for j in range(1, len(ret_df)):
            fund_ret = ret_df[i][j] * 100
            if np.isnan(fund_ret):
                continue
            fund_ret_index = sum(ret_space <= fund_ret) - 1

            dist_df.loc[fund_ret_index, i] += 1

    web = Bar(
    ).add_xaxis(
        xaxis_data=dist_df['label'].tolist()
    )
    for i in range(len(funds)):
        f_name = funds[i]
        if i == 0:
            sel = True
        else:
            sel = False
        web.add_yaxis(
            series_name=f_name,
            y_axis=dist_df[f_name].tolist(),
            stack='总量',
            label_opts=opts.LabelOpts(is_show=False),
            is_selected=sel,
            # areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        )

    web.set_global_opts(
        title_opts=opts.TitleOpts(
            title='近' + str(lookback_year) + '年产品周收益分布（平均周收益：' + str(np.mean(ret_values).round(2))
                  + '%）' + funds_data['t_date'].tolist()[-1].strftime('%Y-%m-%d')
        ),
        tooltip_opts=opts.TooltipOpts(
            # trigger="axis", axis_pointer_type="cross"
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        # datazoom_opts=[
        #     opts.DataZoomOpts(
        #         range_start=0,
        #         range_end=100,
        #         # is_show=False,
        #         type_="inside",
        #         # xaxis_index=[0, 1],
        #     ),
        #     opts.DataZoomOpts(
        #         #     is_show=True,
        #         #     xaxis_index=[0, 1],
        #         #     type_="slider",
        #         #     pos_top="90%",
        #         #     range_start=98,
        #         #     range_end=100,
        #     ),
        # ],
        legend_opts=opts.LegendOpts(
            pos_top="7%",
            pos_left='5%',
            pos_right='5%'
        )
    )
    # web2.set_global_opts(
    #     legend_opts=opts.LegendOpts(
    #         pos_top="7%",
    #         pos_left='10%',
    #         pos_right='20%'
    #     )
    # )
    grid = (
        Grid(
            init_opts=opts.InitOpts(
                width=str(grid_width) + "px",
                height=str(grid_height) + "px"
            ),
        ).add(
            web, grid_opts=opts.GridOpts(
                pos_right="10%",
                pos_left="10%",
                pos_top=str(pos_top) + '%',
                # pos_bottom='50%'
            ),
            # is_control_axis_index=True
            # ).add(
            #     web2, grid_opts=opts.GridOpts(
            #         pos_right="20%",
            #         pos_left="10%",
            #         pos_top='55%',
            #         pos_bottom='15%'
            #     ),
        )
    )
    return grid


def com_fut_amt(start_date=None, end_date=None, grid_width=1200, grid_height=600):
    data = pd.DataFrame(fut_com_amount_by_ex(start_date=start_date, end_date=end_date)['data'])
    data['ENDDATE'] = pd.to_datetime(data['ENDDATE']).dt.date.tolist()
    data['SUM(TURNOVER)'] = data['SUM(TURNOVER)'] / 100000000
    data.loc[
        data['ENDDATE'] < datetime(2020, 1, 1).date(), 'SUM(TURNOVER)'
    ] = data.loc[
                data['ENDDATE'] < datetime(2020, 1, 1).date(), 'SUM(TURNOVER)'
            ] / 2
    # ex_list = data['EXCHANGE'].drop_duplicates().tolist()
    # calendar = data[['ENDDATE']].drop_duplicates().reset_index(drop=True)
    # calendar['ENDDATE'] = pd.to_datetime(calendar['ENDDATE']).dt.date.tolist()

    web = Line(
    ).add_xaxis(
        xaxis_data=data['ENDDATE'].tolist()
    )
    web.add_yaxis(
        series_name='AMOUNT',
        y_axis=data['SUM(TURNOVER)'].tolist(),
        # stack='总量',
        label_opts=opts.LabelOpts(is_show=False),
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
    )

    # for i in ex_list:
    #     data_e = data[['ENDDATE', 'TURNOVER']].groupby(by='ENDDATE').sum().reset_index()
    #     data_e['TURNOVER'] = data_e['TURNOVER'] / 100000000
    #
    #     web.add_yaxis(
    #         series_name=exchange_dict[i],
    #         y_axis=data_e['TURNOVER'].tolist(),
    #         stack='总量',
    #         label_opts=opts.LabelOpts(is_show=False),
    #         areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
    #     )

    web.set_global_opts(
        title_opts=opts.TitleOpts(title="每日期货成交额(亿元) " + data['ENDDATE'].tolist()[-1].strftime('%Y-%m-%d')),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axislabel_opts=opts.LabelOpts(formatter="{value} 亿元"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        datazoom_opts=[
            opts.DataZoomOpts(
                range_start=0,
                range_end=100,
                # is_show=False,
                type_="inside",
                # xaxis_index=[0, 1],
            ),
            opts.DataZoomOpts(
                #     is_show=True,
                #     xaxis_index=[0, 1],
                #     type_="slider",
                #     pos_top="90%",
                #     range_start=98,
                #     range_end=100,
            ),
        ],
        legend_opts=opts.LegendOpts(
            pos_top="7%",
            pos_left='10%',
            pos_right='10%'
        )
    )
    # web2.set_global_opts(
    #     legend_opts=opts.LegendOpts(
    #         pos_top="7%",
    #         pos_left='10%',
    #         pos_right='20%'
    #     )
    # )
    grid = (
        Grid(
            init_opts=opts.InitOpts(
                width=str(grid_width) + "px",
                height=str(grid_height) + "px"
            ),
        ).add(
            web, grid_opts=opts.GridOpts(
                pos_right="20%",
                pos_left="10%",
                pos_top='20%',
                # pos_bottom='50%'
            ),
            # is_control_axis_index=True
            # ).add(
            #     web2, grid_opts=opts.GridOpts(
            #         pos_right="20%",
            #         pos_left="10%",
            #         pos_top='55%',
            #         pos_bottom='15%'
            #     ),
        )
    )

    return grid


# def chart_ret_with_index(
#         funds, end_date, lookback_year, grid_width=1200, grid_height=600, interval=0.5,
#         dtype='', fillna=False, freq='w',
#         db_path=path_hb['work'], cal_path=path_hb['daily'], *kwargs
# )


def volatility_stats(data, data_name, width=1200, height=600):
    vol_cone, vol_rolling = rolling_volatility(data=data)

    axis_cross = opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")

    web = Line(
        init_opts=opts.InitOpts(width=str(width) + "px", height=str(height) + "px")
    ).add_xaxis(
        xaxis_data=vol_rolling['t_date'].tolist()
    ).add_yaxis(
        series_name=data_name,
        y_axis=vol_rolling['close'].tolist(),
        label_opts=opts.LabelOpts(is_show=False),
        yaxis_index=0,
        is_selected=False
    ).set_series_opts(
        areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
        label_opts=opts.LabelOpts(is_show=False),
    ).extend_axis(
        yaxis=opts.AxisOpts(
            # name='波动率',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            # position="right",
            # interval=5,
            min_='dataMin',
        )
    ).set_global_opts(
        title_opts=opts.TitleOpts(
            title=vol_rolling['t_date'][0].strftime('%Y/%m/%d')
                  + '~'
                  + vol_rolling['t_date'][len(vol_rolling) - 1].strftime('%Y/%m/%d')
            ,
            # pos_right="5%"
        ),
        tooltip_opts=axis_cross,
        legend_opts=opts.LegendOpts(
            pos_top="6%",
            # pos_right='40%'
        ),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=100),
            # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
            # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
            opts.DataZoomOpts(type_="inside")
        ],
        yaxis_opts=opts.AxisOpts(
            # axislabel_opts=opts.LabelOpts(formatter="{value}"),
            min_='dataMin',
        ),
    )

    web_vol = Line().add_xaxis(
        xaxis_data=vol_rolling['t_date'].tolist()
    )
    for i in vol_rolling.columns:
        if '日' not in i:
            continue
        web_vol.add_yaxis(
            series_name=i,
            y_axis=vol_rolling[i].round(2).tolist(),
            # symbol="emptyCircle",
            # is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
            # is_selected=all_selected,
            yaxis_index=1,
        )

    web.overlap(web_vol)

    return web


def factor_index(
        start_date, end_date, factor, params, sql_path, table, freq='', factor_end='', show_end='日', axis_cross=None
):
    web = None
    index_data = None
    if axis_cross:
        axis_cross = opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")

    for window_days in params:
        index_name = factor + str(window_days) + factor_end
        index_data = pd.read_sql_query(
            'select * from ' + table
            + ' where TDATE<=' + end_date.strftime('%Y%m%d')
            + ' and TDATE>=' + start_date.strftime('%Y%m%d')
            + ' and `FACTOR`=\'' + index_name + '\' order by `TDATE`',
            sql_path
        )
        if freq.upper() in ['W', 'M']:
            index_data = index_data.set_index(pd.to_datetime(index_data['TDATE'])).resample(freq.upper()).last()
            index_data = index_data[index_data['CLOSE'] >= 0]
        if web is None:
            web = Line(
                # init_opts=opts.InitOpts(width="1200px", height="400px")
            ).add_xaxis(
                xaxis_data=index_data['TDATE'].tolist()
            )
        web.add_yaxis(
            series_name=str(window_days) + show_end,
            y_axis=list((index_data['CLOSE'] / index_data['CLOSE'][0]).round(4).values),
            label_opts=opts.LabelOpts(is_show=False),
            # yaxis_index=0
        )

    web.set_global_opts(
        title_opts=opts.TitleOpts(
            title=index_data['TDATE'].tolist()[-1]
        ),
        tooltip_opts=axis_cross,
        # toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        yaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            min_='dataMin',
        ),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=100),
            # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
            # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
            opts.DataZoomOpts(type_="inside")
        ],
        legend_opts=opts.LegendOpts(
            pos_top="7%",
            pos_left='5%',
            pos_right='5%'
        )
    )

    grid = (
        Grid(init_opts=opts.InitOpts(
            width="630px", height="400px")
        ).add(
            web,
            grid_opts=opts.GridOpts(
                pos_right="0%",
                pos_left="10%",
                pos_top="20%",
            ),
            is_control_axis_index=True
        )
    )
    return grid


def market_win(start_date, end_date, freq='D', table='index_win', sql_path=path_hb['daily']):
    index_win_data = pd.read_sql_query(
        'select * from ' + table + ' where TDATE<=' + end_date.strftime('%Y%m%d')
        + ' and TDATE>=' + start_date.strftime('%Y%m%d')
        + ' and FREQ=\'' + freq + '\'',
        sql_path
    )

    web = Bar(
        init_opts=opts.InitOpts(width="1200px", height="400px")
    ).add_xaxis(
        xaxis_data=index_win_data['TDATE'].tolist()
    )

    def t000905(x):
        if x == '000905':
            return True
        else:
            return False

    col = ['Q1', 'Q25', 'MEDIAN', 'Q75', 'Q99']
    c = Boxplot()
    c.add_xaxis(index_win_data['TDATE'].tolist())
    c.add_yaxis(
        series_name="个股涨跌分散度",
        # y_axis=c.prepare_data(ret_df_new[funds].values.tolist()),
        y_axis=index_win_data[col].round(2).values.tolist(),
        yaxis_index=1,
        tooltip_opts=opts.TooltipOpts(
            formatter=JsCode(
                """function(param) { return [
                            param.name,
                            '99分位：' + param.data[5],
                            '75分位：' + param.data[4],
                            '中位数：' + param.data[3],
                            '25分位：' + param.data[2],
                            '1分位：' + param.data[1],
                        ].join('<br/>') }"""
            )
        ),
    )

    web.extend_axis(
        yaxis=opts.AxisOpts(
            name='涨跌分散度',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            position="right",
            # interval=5,
            min_=index_win_data[col].round(2).min().min(),
            max_=index_win_data[col].round(2).max().max(),
        )
    ).extend_axis(
        yaxis=opts.AxisOpts(
            name='指数涨跌幅',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            position="right",
            offset=80,
            # interval=5,
            min_=index_win_data[col].round(2).min().min(),
            max_=index_win_data[col].round(2).max().max(),
        )
    )

    index_r = Bar().add_xaxis(
        xaxis_data=index_win_data['TDATE'].tolist()
    )

    for i in ['000300', '000905', '000852']:
        # print(i)
        web.add_yaxis(
            series_name='跑赢' + i,
            y_axis=(index_win_data[i + 'w'] / index_win_data['STKN'] * 100).round(2).tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            yaxis_index=0,
            is_selected=t000905(i),
        )
        index_r.add_yaxis(
            series_name=i,
            y_axis=index_win_data[i].round(2).tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            yaxis_index=2,
            is_selected=t000905(i),
        )

    web.set_global_opts(
        title_opts=opts.TitleOpts(
            title=index_win_data['TDATE'].tolist()[0].strftime('%Y/%m/%d')
                  + ' ~ ' + index_win_data['TDATE'].tolist()[-1].strftime('%Y/%m/%d')
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        # toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        yaxis_opts=opts.AxisOpts(
            name='跑赢指数个股占比',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            min_=0,
            max_=100,
        ),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=100),
            # opts.DataZoomOpts(pos_left="5%", xaxis_index=0),
            # opts.DataZoomOpts(pos_right="5%", xaxis_index=1),
            opts.DataZoomOpts(type_="inside")
        ],
        legend_opts=opts.LegendOpts(
            pos_top="7%",
            # pos_left='10%',
            # pos_right='10%'
        )
    )

    return web.overlap(index_r).overlap(c)


def gzb_ts_max_positions(data, n=5):
    data['绝对市值占净值'] = data['市值占净值'].abs()
    data_cal = data.sort_values(by=['日期']).groupby('日期').sum().round(2)[['市值占净值', '绝对市值占净值']].rename(
        columns={
            '市值占净值': '净头寸%',
            '绝对市值占净值': '总头寸%',
        }
    ).reset_index()
    data_sort = data.sort_values(by='绝对市值占净值', ascending=False).groupby('日期', as_index=False)
    for i in range(n):
        df_i = data_sort.nth(i).sort_values(by='日期')[['日期', '科目名称', '市值占净值']].rename(
            columns={
                '科目名称': '第' + str(i + 1) + '大',
                '市值占净值': '' + str(i + 1) + '占净值%',
            }
        ).round(2).replace('合约', '', regex=True)
        data_cal = data_cal.merge(df_i, on='日期', how='left')
    table = Table()

    headers = data_cal.columns.tolist()
    rows = data_cal.values.tolist()
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(
            title=data['基金名称'][0], subtitle="时序前" + str(n) + "大持仓"
        )
    )
    return table


def gzb_ts_positions(data, width=800, height=600):
    data_d = data[0]
    data_d['绝对占比'] = data_d['市值占净值'].abs()
    data_value = data_d.groupby(['日期'], as_index=False)['绝对占比'].sum().rename(columns={'绝对占比': '总比'})
    data_value_by_sector = data_d.groupby(['日期', '板块'], as_index=False)['绝对占比'].sum()
    data_value_by_sector = data_value_by_sector.merge(data_value, on='日期', how='left')
    data_value_by_sector['相对占比'] = data_value_by_sector['绝对占比'] / data_value_by_sector['总比'] * 100

    data_value_net_by_sector = data_d.groupby(['日期', '板块'], as_index=False)['市值占净值'].sum()

    sectors = data_d['板块'].drop_duplicates().tolist()
    web = Bar().add_xaxis(data_value['日期'].tolist())
    web2 = Bar().add_xaxis(data_value['日期'].tolist())
    web3 = Bar().add_xaxis(data_value['日期'].tolist())
    for i in sectors:
        abs_p = data_value_by_sector[data_value_net_by_sector['板块'] == i][['日期', '绝对占比']]
        abs_p = data_value[['日期']].merge(abs_p, on='日期', how='left')

        rel_p = data_value_by_sector[data_value_net_by_sector['板块'] == i][['日期', '相对占比']]
        rel_p = data_value[['日期']].merge(rel_p, on='日期', how='left')

        net_p = data_value_net_by_sector[data_value_net_by_sector['板块'] == i][['日期', '市值占净值']]
        net_p = data_value[['日期']].merge(net_p, on='日期', how='left')

        web.add_yaxis(
            i,
            abs_p['绝对占比'].round(2).tolist(),
            stack='stack1',
        )
        web2.add_yaxis(
            i,
            rel_p['相对占比'].round(2).tolist(),
            stack='stack2',
        )
        web3.add_yaxis(
            i,
            net_p['市值占净值'].round(2).tolist(),
            stack='stack3',
        )

    web.set_series_opts(
        label_opts=opts.LabelOpts(is_show=False)
    ).set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False),
        yaxis_opts=opts.AxisOpts(
            name='总市值敞口',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            # min_='dataMin',
            # max_='dataMax',
        ),
    )

    web3.set_series_opts(
        label_opts=opts.LabelOpts(is_show=False)
    ).set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False),
        yaxis_opts=opts.AxisOpts(
            name='净市值敞口',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            min_='dataMin',
            max_='dataMax',
        ),
    )

    # return web2
    web2.set_series_opts(
        label_opts=opts.LabelOpts(is_show=False)
    ).set_global_opts(
        title_opts=opts.TitleOpts(title=data_d['基金名称'][0] + " 持仓分布"),
        legend_opts=opts.LegendOpts(
            orient="vertical",
            pos_top="5%",
            # pos_left='2%',
            pos_right='2%',
            type_='scroll',
        ),
        yaxis_opts=opts.AxisOpts(
            name='总市值占比',
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            # min_='dataMin',
            max_=100,
        ),
        datazoom_opts=[
            opts.DataZoomOpts(xaxis_index=[0, 0], range_start=0, range_end=100),
            opts.DataZoomOpts(xaxis_index=[0, 1], range_start=0, range_end=100, type_="inside"),
            opts.DataZoomOpts(xaxis_index=[0, 2], range_start=0, range_end=100, type_="inside")
        ],
    )
    # return web2
    web_aum = Bar().add_xaxis(
        xaxis_data=data[1]['日期'].tolist()
    ).add_yaxis(
        series_name='产品规模（万元）',
        y_axis=data[1]['市值'].div(10000).round().tolist(),
        # symbol="emptyCircle",
        # is_symbol_show=False,
        label_opts=opts.LabelOpts(is_show=False),
        # is_selected=all_selected,
        # yaxis_index=1,
        ).set_global_opts(
        # title_opts=opts.TitleOpts(title='产品规模'),
        legend_opts=opts.LegendOpts(
            # orient="vertical",
            # pos_top="5%",
            # pos_left='2%',
            # pos_right='2%',
            # type_='scroll',
            is_show=False
        ),
        yaxis_opts=opts.AxisOpts(
            name='产品规模',
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            # min_='dataMin',
            # max_=100,
        ),
    )
    # web2.overlap(web_aum)

    grid = (
        Grid(
            init_opts=opts.InitOpts(
                width=str(width) + "px",
                height=str(height) + "px"
            )
        ).add(
            web2,
            grid_opts=opts.GridOpts(
                pos_right="25%",
                pos_left="8%",
                pos_top="10%",
                pos_bottom="70%"
            ),
            # is_control_axis_index=True
        ).add(
            web,
            grid_opts=opts.GridOpts(
                pos_right="25%",
                pos_left="8%",
                pos_top="38%",
                pos_bottom="50%"
            ),
            # is_control_axis_index=True
        ).add(
            web3,
            grid_opts=opts.GridOpts(
                pos_right="25%",
                pos_left="8%",
                pos_top="58%",
                pos_bottom="30%"
            ),
            # is_control_axis_index=True
        ).add(
            web_aum,
            grid_opts=opts.GridOpts(
                pos_right="25%",
                pos_left="8%",
                pos_top="78%",
                # pos_bottom=""
            ),
            # is_control_axis_index=True
        )
    )

    return grid


def gzb_xs_position(data, width=800, height=600):
    # data = data[0]
    date = data['日期'][len(data) - 1]
    name = data['基金名称'][0]
    data = data[data['日期'] == date].reset_index(drop=True)
    data['绝对占比'] = data['市值占净值'].abs()
    data_value_by_sector = data.groupby(['板块'], as_index=False)['绝对占比'].sum().rename(
        columns={'绝对占比': '板块市值占比'}
    )
    data = data.merge(data_value_by_sector, on='板块', how='left')
    data = data.sort_values(by=['板块市值占比', '绝对占比'], ascending=False)
    data['科目名称'] = data['科目名称'].apply(lambda x: x + ' 空' if data[data['科目名称'] == x]['市值占净值'].tolist()[0] < 0 else x)
    inner_data = data[['板块', '板块市值占比']].drop_duplicates().reset_index(drop=True)
    inner_data_pair = [
        list(z) for z in zip(inner_data['板块'].tolist(), inner_data['板块市值占比'].round(2).tolist())
    ]

    outer_data = data[['科目名称', '绝对占比']].sort_values(by=['绝对占比'], ascending=False).reset_index(drop=True)
    outer_data_pair = [
        list(z) for z in zip(outer_data['科目名称'].tolist(), outer_data['绝对占比'].round(2).tolist())
    ]

    web = Pie(
        init_opts=opts.InitOpts(
            width=str(width) + "px",
            height=str(height) + "px"
        )
    ).add(
        series_name="板块占比",
        data_pair=inner_data_pair,
        radius=[0, "60%"],
        center=["25%", "50%"],
        label_opts=opts.LabelOpts(
            position="inner",
            # formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
            # background_color="#eee",
            # border_color="#aaa",
            # border_width=1,
            # border_radius=4,
            # rich={
            #     "a": {"color": "#999", "lineHeight": 22, "align": "center"},
            #     "abg": {
            #         "backgroundColor": "#e3e3e3",
            #         "width": "100%",
            #         "align": "right",
            #         "height": 22,
            #         "borderRadius": [4, 4, 0, 0],
            #     },
            #     "hr": {
            #         "borderColor": "#aaa",
            #         "width": "100%",
            #         "borderWidth": 0.5,
            #         "height": 0,
            #     },
            #     "b": {"fontSize": 12, "lineHeight": 33},
            #     "per": {
            #         "color": "#eee",
            #         "backgroundColor": "#334455",
            #         "padding": [2, 4],
            #         "borderRadius": 2,
            #     },
            # },
        )
    ).add(
        series_name="品种占比",
        radius=[0, "30%"],
        center=["75%", "50%"],
        data_pair=outer_data_pair,
        label_opts=opts.LabelOpts(
            position="outside",
            # formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
            # background_color="#eee",
            # border_color="#aaa",
            # border_width=1,
            # border_radius=4,
            # rich={
            #     "a": {"color": "#999", "lineHeight": 22, "align": "center"},
            #     "abg": {
            #         "backgroundColor": "#e3e3e3",
            #         "width": "100%",
            #         "align": "right",
            #         "height": 22,
            #         "borderRadius": [4, 4, 0, 0],
            #     },
            #     "hr": {
            #         "borderColor": "#aaa",
            #         "width": "100%",
            #         "borderWidth": 0.5,
            #         "height": 0,
            #     },
            #     "b": {"fontSize": 16, "lineHeight": 33},
            #     "per": {
            #         "color": "#eee",
            #         "backgroundColor": "#334455",
            #         "padding": [2, 4],
            #         "borderRadius": 2,
            #     },
            # },
        ),
    ).set_global_opts(
        title_opts=opts.TitleOpts(
            title=name + ' ' + date.strftime('%Y/%m/%d') + " 持仓分布，品种数量：" + str(
                len(data.groupby('品种').count())
            )
        ),
        legend_opts=opts.LegendOpts(
            is_show=False,
            pos_left="left",
            orient="vertical"
        )
    ).set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        )
    )

    return web

