"""
Date: 2022/11/3 15:08
Desc: 金十数据中心-经济指标-欧元区
金十数据中心-经济指标-欧元区-国民经济运行状况-经济状况
金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平
金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场
金十数据中心-经济指标-欧元区-贸易状况
金十数据中心-经济指标-欧元区-产业指标
金十数据中心-经济指标-欧元区-领先指标
"""
import time

import pandas as pd
import requests
from tqdm import tqdm

import PPshare.stock.macro.cons as cs

# 金十数据中心-经济指标-欧元区-国民经济运行状况
# 金十数据中心-经济指标-欧元区-国民经济运行状况-经济状况
# 金十数据中心-经济指标-欧元区-国民经济运行状况-经济状况-欧元区季度GDP年率报告
def get_from_jin10_5(attr_id, name):
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['jin10_5']
    params = {"category": "ec", "attr_id": attr_id, "_": "1667473128417"}
    headers = cs.HEADERS['4jin10']
    r = requests.get(url, headers=headers, params=params)
    data_json = r.json()
    date_list = data_json["data"]
    date_point_list = [item for num, item in enumerate(date_list) if num % 20 == 0]
    big_df = pd.DataFrame()
    for date in tqdm(date_point_list, leave=False):
        url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
        params = {
            "max_date": f"{date}",
            "category": "ec",
            "attr_id": attr_id,
            "_": "1667475232449",
        }
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "x-app-id": "rU6QIu7JHe2gOUeR",
            "x-csrf-token": "x-csrf-token",
            "x-version": "1.0.0",
        }
        r = requests.get(url, headers=headers, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(
            data_json["data"]["values"],
            columns=[item["name"] for item in data_json["data"]["keys"]],
        )
        big_df = pd.concat([big_df, temp_df], ignore_index=True)

    big_df["商品"] = name

    big_df = big_df[["商品", "日期", "今值", "预测值", "前值"]]
    big_df["今值"] = pd.to_numeric(big_df["今值"])
    big_df["预测值"] = pd.to_numeric(big_df["预测值"])
    big_df["前值"] = pd.to_numeric(big_df["前值"])
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df.sort_values(["日期"], ignore_index=True, inplace=True)
    return big_df

def macro_euro_gdp_yoy() :
    """
    欧元区季度 GDP 年率报告, 数据区间从 20131114-至今
    :return: 欧元区季度 GDP 年率报告
    :rtype: pandas.DataFrame
    """
    temp_df = get_from_jin10_5(83, '欧元区季度GDP年率')
    return temp_df


# 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区CPI月率报告
def macro_euro_cpi_mom():
    """
    欧元区 CPI 月率报告, 数据区间从 19900301-至今
    :return: 欧元区CPI月率报告
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_5(84, '欧元区CPI月率')
    return temp_df


# 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区CPI年率报告
def macro_euro_cpi_yoy():
    """
    欧元区CPI年率报告, 数据区间从19910201-至今
    :return: 欧元区CPI年率报告-今值(%)
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_5(8, '欧元区CPI月率')
    return temp_df


# 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区PPI月率报告
def macro_euro_ppi_mom():
    """
    欧元区PPI月率报告, 数据区间从19810301-至今
    :return: 欧元区PPI月率报告-今值(%)
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_5(36, '欧元区PPI月率')
    return temp_df


# 金十数据中心-经济指标-欧元区-国民经济运行状况-物价水平-欧元区零售销售月率报告
def macro_euro_retail_sales_mom():
    """
    欧元区零售销售月率报告, 数据区间从20000301-至今
    :return: 欧元区零售销售月率报告-今值(%)
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_5(38, '欧元区零售销售月率')
    return temp_df


# 金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场-欧元区季调后就业人数季率报告
def macro_euro_employment_change_qoq():
    """
    欧元区季调后就业人数季率报告, 数据区间从20083017-至今
    :return: 欧元区季调后就业人数季率报告-今值(%)
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_5(14, '欧元区季调后就业人数季率')
    return temp_df


# 金十数据中心-经济指标-欧元区-国民经济运行状况-劳动力市场-欧元区失业率报告
def macro_euro_unemployment_rate_mom():
    """
    欧元区失业率报告, 数据区间从19980501-至今
    :return: 欧元区失业率报告-今值(%)
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_5(46, '欧元区失业率')
    return temp_df

# 金十数据中心-经济指标-欧元区-贸易状况-欧元区未季调贸易帐报告
def macro_euro_trade_balance():
    """
    欧元区未季调贸易帐报告, 数据区间从19990201-至今
    :return: 欧元区未季调贸易帐报告-今值(亿欧元)
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_5(43, '欧元区未季调贸易帐')
    return temp_df


# 金十数据中心-经济指标-欧元区-贸易状况-欧元区经常帐报告
def macro_euro_current_account_mom():
    """
    欧元区经常帐报告, 数据区间从20080221-至今, 前两个值需要去掉
    :return: 欧元区经常帐报告-今值(亿欧元)
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_5(11, '欧元区经常帐')
    return temp_df


# 金十数据中心-经济指标-欧元区-产业指标-欧元区工业产出月率报告
def macro_euro_industrial_production_mom():
    """
    欧元区工业产出月率报告, 数据区间从19910301-至今
    :return: 欧元区工业产出月率报告-今值(%)
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_5(19, '欧元区工业产出月率')
    return temp_df

# 金十数据中心-经济指标-欧元区-产业指标-欧元区制造业PMI初值报告
def macro_euro_manufacturing_pmi():
    """
    欧元区制造业PMI初值报告, 数据区间从20080222-至今
    :return: 欧元区制造业PMI初值报告-今值
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_5(30, '欧元区制造业PMI初值')
    return temp_df


# 金十数据中心-经济指标-欧元区-产业指标-欧元区服务业PMI终值报告
def macro_euro_services_pmi():
    """
    欧元区服务业PMI终值报告, 数据区间从 20080222-至今
    :return: 欧元区服务业PMI终值报告-今值
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_5(41, '欧元区服务业PMI终值')
    return temp_df


# 金十数据中心-经济指标-欧元区-领先指标-欧元区ZEW经济景气指数报告
def macro_euro_zew_economic_sentiment():
    """
    欧元区ZEW经济景气指数报告, 数据区间从20080212-至今
    :return: 欧元区ZEW经济景气指数报告-今值
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_5(48, '欧元区ZEW经济景气指数')
    return temp_df


# 金十数据中心-经济指标-欧元区-领先指标-欧元区Sentix投资者信心指数报告
def macro_euro_sentix_investor_confidence():
    """
    欧元区Sentix投资者信心指数报告, 数据区间从20020801-至今
    :return: 欧元区Sentix投资者信心指数报告-今值
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_5(40, '欧元区Sentix投资者信心指数')
    return temp_df


# 金十数据中心-伦敦金属交易所(LME)-持仓报告
def macro_euro_lme_holding():
    """
    伦敦金属交易所(LME)-持仓报告, 数据区间从 20151022-至今
    https://datacenter.jin10.com/reportType/dc_lme_traders_report
    https://cdn.jin10.com/data_center/reports/lme_position.json?_=1591533934658
    :return: 伦敦金属交易所(LME)-持仓报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {"_": str(int(round(t * 1000)))}
    url = cs.URL_TYPE['https']+cs.URL_DIC['2jin10']+cs.URL_PARA['lme_holding']
    r = requests.get(
        url, params=params
    )
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df.fillna(value="[0, 0, 0]", inplace=True)
    big_df = pd.DataFrame()
    for item in temp_df.columns:
        for i in range(3):
            inner_temp_df = temp_df.loc[:, item].apply(lambda x: eval(str(x))[i])
            inner_temp_df.name = inner_temp_df.name + "-" + json_data["keys"][i]["name"]
            big_df = pd.concat([big_df, inner_temp_df], axis=1)
    big_df.sort_index(inplace=True)
    return big_df


# 金十数据中心-伦敦金属交易所(LME)-库存报告
def macro_euro_lme_stock():
    """
    伦敦金属交易所(LME)-库存报告, 数据区间从 20140702-至今
    https://datacenter.jin10.com/reportType/dc_lme_report
    https://cdn.jin10.com/data_center/reports/lme_stock.json?_=1591535304783
    :return: 伦敦金属交易所(LME)-库存报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {"_": str(int(round(t * 1000)))}
    url = cs.URL_TYPE['https']+cs.URL_DIC['2jin10']+cs.URL_PARA['lme_stock']
    r = requests.get(
        url, params=params
    )
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    big_df = pd.DataFrame()
    for item in temp_df.columns:
        for i in range(3):
            inner_temp_df = temp_df.loc[:, item].apply(lambda x: eval(str(x))[i])
            inner_temp_df.name = inner_temp_df.name + "-" + json_data["keys"][i]["name"]
            big_df = pd.concat([big_df, inner_temp_df], axis=1)
    big_df.sort_index(inplace=True)
    return big_df


if __name__ == "__main__":
    print(macro_euro_lme_stock())
