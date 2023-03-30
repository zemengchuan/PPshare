"""
Date: 2022/11/27 20:30
Desc: 东方财富-经济数据-加拿大
"""
import pandas as pd
import requests
import PPshare.stock.macro.cons as cs

def get_from_eastmoney(INDICATOR_ID):
    url = cs.URL_TYPE['https'] + cs.URL_DIC['eastmoney'] + cs.URL_PARA[
        'eastmoney']
    params = {
        "reportName": "RPT_ECONOMICVALUE_CA",
        "columns": "ALL",
        "filter": f'(INDICATOR_ID="{INDICATOR_ID}")',
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "p": "1",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1669047266881",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "-",
        "-",
        "-",
        "-",
        "时间",
        "-",
        "发布日期",
        "现值",
        "前值",
    ]
    temp_df = temp_df[[
        "时间",
        "前值",
        "现值",
        "发布日期",
    ]]
    temp_df["前值"] = pd.to_numeric(temp_df["前值"], errors="coerce")
    temp_df["现值"] = pd.to_numeric(temp_df["现值"], errors="coerce")
    temp_df['发布日期'] = pd.to_datetime(temp_df['发布日期']).dt.date
    return temp_df
    

# 新屋开工
def macro_canada_new_house_rate():
    """
    东方财富-经济数据-加拿大-新屋开工
    :return: 新屋开工
    :rtype: pandas.DataFrame
    """
    temp_df = get_from_eastmoney("EMG00342247")
    return temp_df

# 失业率
def macro_canada_unemployment_rate():
    """
    东方财富-经济数据-加拿大-失业率
    :return: 失业率
    :rtype: pandas.DataFrame
    """
    temp_df = get_from_eastmoney("EMG00157746")
    return temp_df


# 贸易帐
def macro_canada_trade():
    """
    东方财富-经济数据-加拿大-贸易帐
    :return: 贸易帐
    :rtype: pandas.DataFrame
    """
    temp_df = get_from_eastmoney("EMG00102022")
    return temp_df


# 零售销售月率
def macro_canada_retail_rate_monthly():
    """
    东方财富-经济数据-加拿大-零售销售月率
    :return: 零售销售月率
    :rtype: pandas.DataFrame
    """
    temp_df = get_from_eastmoney("EMG01337094")
    return temp_df


# 央行公布利率决议
def macro_canada_bank_rate():
    """
    东方财富-经济数据-加拿大-央行公布利率决议
    :return: 央行公布利率决议
    :rtype: pandas.DataFrame
    """
    temp_df = get_from_eastmoney("EMG00342248")
    return temp_df


# 核心消费者物价指数年率
def macro_canada_core_cpi_yearly():
    """
    东方财富-经济数据-加拿大-核心消费者物价指数年率
    :return: 核心消费者物价指数年率
    :rtype: pandas.DataFrame
    """
    temp_df = get_from_eastmoney("EMG00102030")
    return temp_df
    


# 核心消费者物价指数月率
def macro_canada_core_cpi_monthly():
    """
    东方财富-经济数据-加拿大-核心消费者物价指数月率
    :return: 核心消费者物价指数月率
    :rtype: pandas.DataFrame
    """
    temp_df = get_from_eastmoney("EMG00102044")
    return temp_df


# 消费者物价指数年率
def macro_canada_cpi_yearly():
    """
    东方财富-经济数据-加拿大-消费者物价指数年率
    :return: 消费者物价指数年率
    :rtype: pandas.DataFrame
    """
    temp_df = get_from_eastmoney("EMG00102029")
    return temp_df



# 消费者物价指数月率
def macro_canada_cpi_monthly():
    """
    东方财富-经济数据-加拿大-消费者物价指数月率
    :return: 消费者物价指数月率
    :rtype: pandas.DataFrame
    """
    temp_df = get_from_eastmoney("EMG00158719")
    return temp_df
    

# GDP 月率
def macro_canada_gdp_monthly():
    """
    东方财富-经济数据-加拿大-GDP 月率
    :return: GDP 月率
    :rtype: pandas.DataFrame
    """
    temp_df = get_from_eastmoney("EMG00159259")
    return temp_df

    

if __name__ == '__main__':
    print(macro_canada_gdp_monthly())