if __name__ == '__main__':
    import sys
    sys.path.append('E:\\codes\\hbshare')
    from hbshare.quant.CChen.data.wind_data import WindApi
    import pandas as pd
    from datetime import datetime, timedelta
    from hbshare.quant.CChen.db_const import sql_write_path_hb, sql_user_hb as sql_user
    from hbshare.quant.CChen.cta_factor.hsjy_to_local import hsjy_mr_wz

    load_end_date = datetime.now() - timedelta(days=1)

    daily_path = sql_write_path_hb['daily']

    t1 = datetime.now()
    wind_api = WindApi()
    sector_df = pd.read_csv('fut_sec_wind.csv')
    fut_index_df = pd.read_csv('fut_index_wind.csv')
    edb_list = pd.read_csv('wind_edb.csv')
    codes_df = pd.DataFrame()
    for i in range(len(sector_df)):
        sector = wind_api.api.wset(
            "sectorconstituent",
            "date=" + datetime.now().strftime('%Y-%m-%d')
            + ";sectorid=" + str(sector_df['id'][i]) + ";field=wind_code,sec_name"
        )
        data_df = pd.DataFrame({'code': sector.Data[0]})
        codes_df = pd.concat([codes_df, data_df])
    codes_df['product'] = codes_df['code'].apply(
        lambda x: x.replace('FI.WI', '') if 'AP' not in x.upper() else x.replace('LFI.WI', '')
    )
    fut_index_df = pd.concat([fut_index_df, codes_df])
    fut_index_df = fut_index_df.reset_index(drop=True)

    # Wind 股指期货日线行情
    wind_api.to_sql_stk_index_fut(
        db_path=daily_path,
        table='futures_wind',
        sql_info=sql_user,
        end_date=load_end_date,
        database='daily_data'
    )

    # Wind 南华指数日线行情
    wind_api.to_sql_fut_index(
        db_path=daily_path,
        table='fut_index_wind',
        sql_info=sql_user,
        end_date=load_end_date,
        database='daily_data',
        code_df=pd.read_csv('nh_index_wind.csv', encoding='gbk')
    )

    # Wind 万得商品指数日线行情
    wind_api.to_sql_fut_index(
        db_path=daily_path,
        table='fut_index_wind',
        sql_info=sql_user,
        end_date=load_end_date,
        database='daily_data',
        code_df=fut_index_df,
    )
    hsjy_mr_wz(
        db_path=daily_path,
        sql_info=sql_user,
    )

    print(datetime.now() - t1)
