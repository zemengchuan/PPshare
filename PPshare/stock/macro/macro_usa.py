"""
Date: 2022/11/27 19:08
Desc: 金十数据中心-经济指标-美国
"""
import json
import time
import PPshare.stock.macro.cons as cs
import pandas as pd
import requests


# urls-usa
JS_USA_INTEREST_RATE_URL = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['INTEREST_RATE']
JS_USA_NON_FARM_URL = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['NON_FARM']
JS_USA_UNEMPLOYMENT_RATE_URL = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['UNEMPLOYMENT_RATE']
JS_USA_EIA_CRUDE_URL = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['EIA_CRUDE']
JS_USA_INITIAL_JOBLESS_URL = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['INITIAL_JOBLESS']
JS_USA_CORE_PCE_PRICE_URL = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['CORE_PCE_PRICE']
JS_USA_CPI_MONTHLY_URL = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['CPI_MONTHLY']
JS_USA_LMCI_URL = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['LMCI']
JS_USA_ADP_NONFARM_URL = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['ADP_NONFARM']
JS_USA_GDP_MONTHLY_URL = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['GDP_MONTHLY']
JS_USA_EIA_CRUDE_PRODUCE_URL = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['EIA_CRUDE_PRODUCE']



# 东方财富-美国-未决房屋销售月率
def macro_usa_phs():
    """
    东方财富-经济数据一览-美国-未决房屋销售月率
    :return: 未决房屋销售月率
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "reportName": "RPT_ECONOMICVALUE_USA",
        "columns": "ALL",
        "filter": '(INDICATOR_ID="EMG00342249")',
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
        "时间",
        "-",
        "发布日期",
        "现值",
        "前值",
    ]
    temp_df = temp_df[
        [
            "时间",
            "前值",
            "现值",
            "发布日期",
        ]
    ]
    temp_df["前值"] = pd.to_numeric(temp_df["前值"], errors="coerce")
    temp_df["现值"] = pd.to_numeric(temp_df["现值"], errors="coerce")
    temp_df["发布日期"] = pd.to_datetime(temp_df["发布日期"]).dt.date
    return temp_df


# 金十数据中心-经济指标-美国-经济状况-美国GDP
def macro_usa_gdp_monthly() :
    """
    金十数据-美国国内生产总值(GDP)报告, 数据区间从 20080228-至今
    :return: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_USA_GDP_MONTHLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国国内生产总值(GDP)"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]

    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "53",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "gdp"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-物价水平-美国CPI月率报告
def macro_usa_cpi_monthly() :
    """
    美国CPI月率报告, 数据区间从19700101-至今
    :return: 美国CPI月率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_USA_CPI_MONTHLY_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国居民消费价格指数(CPI)(月环比)"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "9",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "cpi_monthly"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-物价水平-美国核心CPI月率报告
def macro_usa_core_cpi_monthly() :
    """
    美国核心CPI月率报告, 数据区间从19700101-至今
    :return: 美国核心CPI月率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['core_cpi_monthly']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国核心CPI月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "6",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_core_cpi"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-物价水平-美国个人支出月率报告
def macro_usa_personal_spending() :
    """
    美国个人支出月率报告, 数据区间从19700101-至今
    :return: 美国个人支出月率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['personal_spending']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国个人支出月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "35",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_personal_spending"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-物价水平-美国零售销售月率报告
def macro_usa_retail_sales() :
    """
    美国零售销售月率报告, 数据区间从19920301-至今
    :return: 美国零售销售月率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_retail_sales']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国零售销售月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "39",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_retail_sales"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-物价水平-美国进口物价指数报告
def macro_usa_import_price() :
    """
    美国进口物价指数报告, 数据区间从19890201-至今
    :return: 美国进口物价指数报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['import_price']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国进口物价指数"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "18",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_import_price"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-物价水平-美国出口价格指数报告
def macro_usa_export_price() :
    """
    美国出口价格指数报告, 数据区间从19890201-至今
    :return: 美国出口价格指数报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['export_price']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国出口价格指数"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "79",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_export_price"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-劳动力市场-LMCI
def macro_usa_lmci() :
    """
    美联储劳动力市场状况指数报告, 数据区间从20141006-至今
    :return: 美联储劳动力市场状况指数报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_USA_LMCI_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美联储劳动力市场状况指数"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "93",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "lmci"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-劳动力市场-失业率-美国失业率报告
def macro_usa_unemployment_rate() :
    """
    美国失业率报告, 数据区间从19700101-至今
    :return: 获取美国失业率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_USA_UNEMPLOYMENT_RATE_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国失业率"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "category": "ec",
        "attr_id": "47",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df = temp_df.astype("float")
    temp_df.name = "unemployment_rate"
    return temp_df


# 金十数据中心-经济指标-美国-劳动力市场-失业率-美国挑战者企业裁员人数报告
def macro_usa_job_cuts() :
    """
    美国挑战者企业裁员人数报告, 数据区间从19940201-至今
    :return: 美国挑战者企业裁员人数报告-今值(万人)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_job_cuts']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国挑战者企业裁员人数报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万人)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "category": "ec",
        "attr_id": "78",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df = temp_df.astype("float")
    temp_df.name = "usa_job_cuts"
    return temp_df


# 金十数据中心-经济指标-美国-劳动力市场-就业人口-美国非农就业人数报告
def macro_usa_non_farm() :
    """
    美国非农就业人数报告, 数据区间从19700102-至今
    :return: 美国非农就业人数报告-今值(万人)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_USA_NON_FARM_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国非农就业人数"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万人)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "category": "ec",
        "attr_id": "33",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df = temp_df.astype("float")
    temp_df.name = "non_farm"
    return temp_df


# 金十数据中心-经济指标-美国-劳动力市场-就业人口-美国ADP就业人数报告
def macro_usa_adp_employment() :
    """
    美国ADP就业人数报告, 数据区间从20010601-至今
    :return: 美国ADP就业人数报告-今值(万人)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_USA_ADP_NONFARM_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国ADP就业人数(万人)"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万人)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "category": "ec",
        "attr_id": "1",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df = temp_df.astype("float")
    temp_df.name = "adp"
    return temp_df


# 金十数据中心-经济指标-美国-劳动力市场-消费者收入与支出-美国核心PCE物价指数年率报告
def macro_usa_core_pce_price() :
    """
    美国核心PCE物价指数年率报告, 数据区间从19700101-至今
    :return: 美国核心PCE物价指数年率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    res = requests.get(
        JS_USA_CORE_PCE_PRICE_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国核心PCE物价指数年率"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "category": "ec",
        "attr_id": "80",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df = temp_df.astype("float")
    temp_df.name = "core_pce_price"
    return temp_df


# 金十数据中心-经济指标-美国-劳动力市场-消费者收入与支出-美国实际个人消费支出季率初值报告
def macro_usa_real_consumer_spending() :
    """
    美国实际个人消费支出季率初值报告, 数据区间从20131107-至今
    :return: 美国实际个人消费支出季率初值报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['real_consumer_spending']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国实际个人消费支出季率初值报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "category": "ec",
        "attr_id": "81",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df = temp_df.astype("float")
    temp_df.name = "usa_real_consumer_spending"
    return temp_df


# 金十数据中心-经济指标-美国-贸易状况-美国贸易帐报告
def macro_usa_trade_balance() :
    """
    美国贸易帐报告, 数据区间从19700101-至今
    :return: 美国贸易帐报告-今值(亿美元)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_trade_balance']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国贸易帐报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(亿美元)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "category": "ec",
        "attr_id": "42",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df = temp_df.astype("float")
    temp_df.name = "usa_trade_balance"
    return temp_df


# 金十数据中心-经济指标-美国-贸易状况-美国经常帐报告
def macro_usa_current_account() :
    """
    美国经常帐报告, 数据区间从20080317-至今
    :return: 美国经常帐报告-今值(亿美元)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_current_account']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国经常账报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(亿美元)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "category": "ec",
        "attr_id": "12",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df = temp_df.astype("float")
    temp_df.name = "usa_current_account"
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-制造业-贝克休斯钻井报告
def macro_usa_rig_count() :
    """
    贝克休斯钻井报告, 数据区间从20080317-至今
    :return: 贝克休斯钻井报告-当周
    :rtype: pandas.Series
    """
    t = time.time()
    params = {"_": t}
    url = cs.URL_TYPE['https']+cs.URL_DIC['2jin10']+cs.URL_PARA['rig_count']
    res = requests.get(
        url, params=params
    )
    temp_df = pd.DataFrame(res.json().get("values")).T
    big_df = pd.DataFrame()
    big_df["钻井总数_钻井数"] = temp_df["钻井总数"].apply(lambda x: x[0])
    big_df["钻井总数_变化"] = temp_df["钻井总数"].apply(lambda x: x[1])
    big_df["美国石油钻井_钻井数"] = temp_df["美国石油钻井"].apply(lambda x: x[0])
    big_df["美国石油钻井_变化"] = temp_df["美国石油钻井"].apply(lambda x: x[1])
    big_df["混合钻井_钻井数"] = temp_df["混合钻井"].apply(lambda x: x[0])
    big_df["混合钻井_变化"] = temp_df["混合钻井"].apply(lambda x: x[1])
    big_df["美国天然气钻井_钻井数"] = temp_df["美国天然气钻井"].apply(lambda x: x[0])
    big_df["美国天然气钻井_变化"] = temp_df["美国天然气钻井"].apply(lambda x: x[1])
    big_df = big_df.astype("float")
    return big_df




# 金十数据中心-经济指标-美国-产业指标-制造业-美国生产者物价指数(PPI)报告
def macro_usa_ppi() :
    """
    美国生产者物价指数(PPI)报告, 数据区间从20080226-至今
    :return: 美国生产者物价指数(PPI)报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_ppi']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国生产者物价指数(PPI)报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "37",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_ppi"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-制造业-美国核心生产者物价指数(PPI)报告
def macro_usa_core_ppi() :
    """
    美国核心生产者物价指数(PPI)报告, 数据区间从20080318-至今
    :return: 美国核心生产者物价指数(PPI)报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_core_ppi']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国核心生产者物价指数(PPI)报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "7",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_core_ppi"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-制造业-美国API原油库存报告
def macro_usa_api_crude_stock() :
    """
    美国API原油库存报告, 数据区间从20120328-至今
    :return: 美国API原油库存报告-今值(万桶)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_api_crude_stock']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国API原油库存报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万桶)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "69",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_api_crude_stock"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-制造业-美国Markit制造业PMI初值报告
def macro_usa_pmi() -> pd.Series:
    """
    美国Markit制造业PMI初值报告, 数据区间从20120601-至今
    :return: 美国Markit制造业PMI初值报告-今值
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_pmi']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国Markit制造业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "74",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_pmi"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-制造业-美国ISM制造业PMI报告
def macro_usa_ism_pmi() :
    """
    美国ISM制造业PMI报告, 数据区间从19700101-至今
    :return: 美国ISM制造业PMI报告-今值
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_ism_pmi']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国ISM制造业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "28",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_ism_pmi"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-工业-美国工业产出月率报告
def macro_usa_industrial_production() :
    """
    美国工业产出月率报告, 数据区间从19700101-至今
    :return: 美国工业产出月率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_industrial_production']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国工业产出月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "20",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_industrial_production"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-工业-美国耐用品订单月率报告
def macro_usa_durable_goods_orders() :
    """
    美国耐用品订单月率报告, 数据区间从20080227-至今
    :return: 美国耐用品订单月率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_durable_goods_orders']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国耐用品订单月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "13",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_durable_goods_orders"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-工业-美国工厂订单月率报告
def macro_usa_factory_orders() :
    """
    美国工厂订单月率报告, 数据区间从19920401-至今
    :return: 美国工厂订单月率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_factory_orders']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国工厂订单月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "16",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_factory_orders"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-服务业-美国Markit服务业PMI初值报告
def macro_usa_services_pmi() :
    """
    美国Markit服务业PMI初值报告, 数据区间从20120701-至今
    :return: 美国Markit服务业PMI初值报告-今值
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_services_pmi']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国Markit服务业PMI初值报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "89",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_services_pmi"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-服务业-美国商业库存月率报告
def macro_usa_business_inventories() :
    """
    美国商业库存月率报告, 数据区间从19920301-至今
    https://datacenter.jin10.com/reportType/dc_usa_business_inventories
    https://cdn.jin10.com/dc/reports/dc_usa_business_inventories_all.js?v=1578744618
    :return: 美国商业库存月率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_business_inventories']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国商业库存月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "4",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_business_inventories"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-服务业-美国ISM非制造业PMI报告
def macro_usa_ism_non_pmi() :
    """
    美国ISM非制造业PMI报告, 数据区间从19970801-至今
    :return: 美国ISM非制造业PMI报告-今值
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_ism_non_pmi']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国ISM非制造业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "29",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_ism_non_pmi"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-房地产-美国NAHB房产市场指数报告
def macro_usa_nahb_house_market_index() :
    """
    美国NAHB房产市场指数报告, 数据区间从19850201-至今
    :return: 美国NAHB房产市场指数报告-今值
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_nahb_house_market_index']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国NAHB房产市场指数报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "31",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_nahb_house_market_index"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-房地产-美国新屋开工总数年化报告
def macro_usa_house_starts() :
    """
    美国新屋开工总数年化报告, 数据区间从19700101-至今
    :return: 美国新屋开工总数年化报告-今值(万户)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_house_starts']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国新屋开工总数年化报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万户)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "17",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_house_starts"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-房地产-美国新屋销售总数年化报告
def macro_usa_new_home_sales() :
    """
    美国新屋销售总数年化报告, 数据区间从19700101-至今
    :return: 美国新屋销售总数年化报告-今值(万户)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_new_home_sales']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国新屋销售总数年化报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万户)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "32",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_new_home_sales"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-房地产-美国营建许可总数报告
def macro_usa_building_permits() :
    """
    美国营建许可总数报告, 数据区间从20080220-至今
    :return: 美国营建许可总数报告-今值(万户)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_building_permits']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国营建许可总数报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万户)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "3",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_building_permits"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-房地产-美国成屋销售总数年化报告
def macro_usa_exist_home_sales() :
    """
    美国成屋销售总数年化报告, 数据区间从19700101-至今
    :return: 美国成屋销售总数年化报告-今值(万户)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_exist_home_sales']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国成屋销售总数年化报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万户)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "15",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_exist_home_sales"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-房地产-美国FHFA房价指数月率报告
def macro_usa_house_price_index() :
    """
    美国FHFA房价指数月率报告, 数据区间从19910301-至今
    :return: 美国FHFA房价指数月率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_house_price_index']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国FHFA房价指数月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "51",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_house_price_index"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-房地产-美国S&P/CS20座大城市房价指数年率报告
def macro_usa_spcs20() :
    """
    美国S&P/CS20座大城市房价指数年率报告, 数据区间从20010201-至今
    :return: 美国S&P/CS20座大城市房价指数年率报告-今值(%)
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_spcs20']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国S&P/CS20座大城市房价指数年率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "52",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", keep="last", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_spcs20"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-美国-产业指标-房地产-美国成屋签约销售指数月率报告
def macro_usa_pending_home_sales() :
    """
    美国成屋签约销售指数月率报告, 数据区间从20010301-至今
    :return: 美国成屋签约销售指数月率报告
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_pending_home_sales']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国成屋签约销售指数月率报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(%)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "34",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", keep="last", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_pending_home_sales"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-美国-领先指标-美国谘商会消费者信心指数报告
def macro_usa_cb_consumer_confidence() :
    """
    金十数据中心-经济指标-美国-领先指标-美国谘商会消费者信心指数报告, 数据区间从 19700101-至今
    :return: 美国谘商会消费者信心指数报告-今值
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_cb_consumer_confidence']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国谘商会消费者信心指数报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]

    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "5",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", keep="last", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "cb_consumer_confidence"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-美国-领先指标-美国NFIB小型企业信心指数报告
def macro_usa_nfib_small_business() :
    """
    美国NFIB小型企业信心指数报告, 数据区间从19750201-至今
    :return: 美国NFIB小型企业信心指数报告-今值
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_nfib_small_business']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国NFIB小型企业信心指数报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "63",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", keep="last", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "nfib_small_business"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-美国-领先指标-美国密歇根大学消费者信心指数初值报告
def macro_usa_michigan_consumer_sentiment() :
    """
    美国密歇根大学消费者信心指数初值报告, 数据区间从19700301-至今
    :return: 美国密歇根大学消费者信心指数初值报告-今值
    :rtype: pandas.Series
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['usa_michigan_consumer_sentiment']
    res = requests.get(
        url.format(str(int(round(t * 1000))), str(int(round(t * 1000)) + 90))
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国密歇根大学消费者信心指数初值报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "50",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", keep="last", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "michigan_consumer_sentiment"
    temp_df = temp_df.astype(float)
    return temp_df


# 金十数据中心-经济指标-美国-其他-美国EIA原油库存报告
def macro_usa_eia_crude_rate() :
    """
    美国EIA原油库存报告, 数据区间从19950801-至今
    :return: pandas.Series
    1982-09-01   -262.6
    1982-10-01       -8
    1982-11-01    -41.3
    1982-12-01    -87.6
    1983-01-01     51.3
                  ...
    2019-10-02      310
    2019-10-09    292.7
    2019-10-16        0
    2019-10-17    928.1
    2019-10-23        0
    """
    t = time.time()
    res = requests.get(
        JS_USA_EIA_CRUDE_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国EIA原油库存(万桶)"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万桶)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "10",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "eia_crude_rate"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-其他-美国初请失业金人数报告
def macro_usa_initial_jobless() :
    """
    美国初请失业金人数报告, 数据区间从19700101-至今
    :return: pandas.Series
    1970-01-01    22.1087
    1970-02-01    24.9318
    1970-03-01      25.85
    1970-04-01    26.8682
    1970-05-01    33.1591
                   ...
    2019-09-26       21.5
    2019-10-03         22
    2019-10-10         21
    2019-10-17       21.4
    2019-10-24          0
    """
    t = time.time()
    res = requests.get(
        JS_USA_INITIAL_JOBLESS_URL.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国初请失业金人数(万人)"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值(万人)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "44",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "initial_jobless"
    temp_df = temp_df.astype("float")
    return temp_df


# 金十数据中心-经济指标-美国-其他-美国原油产量报告
def macro_usa_crude_inner() :
    """
    美国原油产量报告, 数据区间从19830107-至今
    :return: pandas.Series
    1983-01-07     863.40
    1983-01-14     863.40
    1983-01-21     863.40
    1983-01-28     863.40
    1983-02-04     866.00
                   ...
    2019-09-20    1250.00
    2019-09-27    1240.00
    2019-10-04    1260.00
    2019-10-11    1260.00
    2019-10-18    1260.00
    """
    t = time.time()
    params = {"_": t}
    url = cs.URL_TYPE['https']+cs.URL_DIC['2jin10']+cs.URL_PARA['usa_crude_inner']
    res = requests.get(
        url, params=params
    )
    temp_df = pd.DataFrame(res.json().get("values")).T
    big_df = pd.DataFrame()
    big_df["美国国内原油总量_产量"] = temp_df["美国国内原油总量"].apply(lambda x: x[0])
    big_df["美国国内原油总量_变化"] = temp_df["美国国内原油总量"].apply(lambda x: x[1])
    big_df["美国本土48州原油产量_产量"] = temp_df["美国本土48州原油产量"].apply(lambda x: x[0])
    big_df["美国本土48州原油产量_变化"] = temp_df["美国本土48州原油产量"].apply(lambda x: x[1])
    big_df["美国阿拉斯加州原油产量_产量"] = temp_df["美国阿拉斯加州原油产量"].apply(lambda x: x[0])
    big_df["美国阿拉斯加州原油产量_变化"] = temp_df["美国阿拉斯加州原油产量"].apply(lambda x: x[1])
    big_df = big_df.astype("float")
    return big_df


# 金十数据中心-美国商品期货交易委员会CFTC外汇类非商业持仓报告
def macro_usa_cftc_nc_holding() :
    """
    美国商品期货交易委员会CFTC外汇类非商业持仓报告, 数据区间从 19830107-至今
    :return: pandas.DataFrame
    """
    t = time.time()
    params = {"_": str(int(round(t * 1000)))}
    url = cs.URL_TYPE['https']+cs.URL_DIC['2jin10']+cs.URL_PARA['usa_cftc_nc_holding']
    r = requests.get(
        url, params=params
    )
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df.fillna("[0, 0, 0]", inplace=True)
    big_df = pd.DataFrame()
    for item in temp_df.columns:
        for i in range(3):
            inner_temp_df = temp_df.loc[:, item].apply(lambda x: eval(str(x))[i])
            inner_temp_df.name = inner_temp_df.name + "-" + json_data["keys"][i]["name"]
            big_df = pd.concat([big_df, inner_temp_df], axis=1)
    big_df.sort_index(inplace=True)
    return big_df


# 金十数据中心-美国商品期货交易委员会CFTC商品类非商业持仓报告
def macro_usa_cftc_c_holding() :
    """
    美国商品期货交易委员会CFTC商品类非商业持仓报告, 数据区间从 19830107-至今
    :return: pandas.DataFrame
    """
    t = time.time()
    params = {"_": str(int(round(t * 1000)))}
    url = cs.URL_TYPE['https']+cs.URL_DIC['2jin10']+cs.URL_PARA['usa_cftc_c_holding']
    r = requests.get(
        url, params=params
    )
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df.fillna("[0, 0, 0]", inplace=True)
    big_df = pd.DataFrame()
    for item in temp_df.columns:
        for i in range(3):
            inner_temp_df = temp_df.loc[:, item].apply(lambda x: eval(str(x))[i])
            inner_temp_df.name = inner_temp_df.name + "-" + json_data["keys"][i]["name"]
            big_df = pd.concat([big_df, inner_temp_df], axis=1)
    big_df.sort_index(inplace=True)
    return big_df


# 金十数据中心-美国商品期货交易委员会CFTC外汇类商业持仓报告
def macro_usa_cftc_merchant_currency_holding() :
    """
    美国商品期货交易委员会CFTC外汇类商业持仓报告, 数据区间从 19860115-至今
    :return: pandas.DataFrame
    """
    t = time.time()
    params = {"_": str(int(round(t * 1000)))}
    url = cs.URL_TYPE['https']+cs.URL_DIC['2jin10']+cs.URL_PARA['usa_cftc_merchant_currency_holding']
    r = requests.get(
        url, params=params
    )
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df.fillna("[0, 0, 0]", inplace=True)
    big_df = pd.DataFrame()
    for item in temp_df.columns:
        for i in range(3):
            inner_temp_df = temp_df.loc[:, item].apply(lambda x: eval(str(x))[i])
            inner_temp_df.name = inner_temp_df.name + "-" + json_data["keys"][i]["name"]
            big_df = pd.concat([big_df, inner_temp_df], axis=1)
    big_df.sort_index(inplace=True)
    return big_df


# 金十数据中心-美国商品期货交易委员会CFTC商品类商业持仓报告
def macro_usa_cftc_merchant_goods_holding() :
    """
    美国商品期货交易委员会CFTC商品类商业持仓报告, 数据区间从 19860115-至今
    :return: 美国商品期货交易委员会CFTC商品类商业持仓报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {"_": str(int(round(t * 1000)))}
    url = cs.URL_TYPE['https']+cs.URL_DIC['2jin10']+cs.URL_PARA['usa_cftc_merchant_goods_holding']
    r = requests.get(
        url, params=params
    )
    json_data = r.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df.fillna("[0, 0, 0]", inplace=True)
    big_df = pd.DataFrame()
    for item in temp_df.columns:
        for i in range(3):
            inner_temp_df = temp_df.loc[:, item].apply(lambda x: eval(str(x))[i])
            inner_temp_df.name = inner_temp_df.name + "-" + json_data["keys"][i]["name"]
            big_df = pd.concat([big_df, inner_temp_df], axis=1)
    big_df.sort_index(inplace=True)
    return big_df



if __name__ == "__main__":
    # 东方财富-经济指标-美国-未决房屋销售月率
    macro_usa_phs_df = macro_usa_phs()
    print(macro_usa_phs_df)

    # 金十数据中心-经济指标-美国-经济状况-美国GDP
    # macro_usa_gdp_monthly_df = macro_usa_gdp_monthly()
    # print(macro_usa_gdp_monthly_df)
    # 金十数据中心-经济指标-美国-物价水平-美国CPI月率报告
    # macro_usa_cpi_monthly_df = macro_usa_cpi_monthly()
    # print(macro_usa_cpi_monthly_df)
    # 金十数据中心-经济指标-美国-物价水平-美国核心CPI月率报告
    macro_usa_core_cpi_monthly_df = macro_usa_core_cpi_monthly()
    print(macro_usa_core_cpi_monthly_df)
    # 金十数据中心-经济指标-美国-物价水平-美国个人支出月率报告
    macro_usa_personal_spending_df = macro_usa_personal_spending()
    print(macro_usa_personal_spending_df)
    # 金十数据中心-经济指标-美国-物价水平-美国零售销售月率报告
    macro_usa_retail_sales_df = macro_usa_retail_sales()
    print(macro_usa_retail_sales_df)
    # 金十数据中心-经济指标-美国-物价水平-美国进口物价指数报告
    macro_usa_import_price_df = macro_usa_import_price()
    print(macro_usa_import_price_df)
    # 金十数据中心-经济指标-美国-物价水平-美国出口价格指数报告
    macro_usa_export_price_df = macro_usa_export_price()
    print(macro_usa_export_price_df)
    # 金十数据中心-经济指标-美国-劳动力市场-LMCI
    macro_usa_lmci_df = macro_usa_lmci()
    print(macro_usa_lmci_df)
    # 金十数据中心-经济指标-美国-劳动力市场-失业率-美国失业率报告
    macro_usa_unemployment_rate_df = macro_usa_unemployment_rate()
    print(macro_usa_unemployment_rate_df)
    # 金十数据中心-经济指标-美国-劳动力市场-失业率-美国挑战者企业裁员人数报告
    macro_usa_job_cuts_df = macro_usa_job_cuts()
    print(macro_usa_job_cuts_df)
    # 金十数据中心-经济指标-美国-劳动力市场-就业人口-美国非农就业人数报告
    macro_usa_non_farm_df = macro_usa_non_farm()
    print(macro_usa_non_farm_df)
    # 金十数据中心-经济指标-美国-劳动力市场-就业人口-美国ADP就业人数报告
    macro_usa_adp_employment_df = macro_usa_adp_employment()
    print(macro_usa_adp_employment_df)
    # 金十数据中心-经济指标-美国-劳动力市场-消费者收入与支出-美国核心PCE物价指数年率报告
    macro_usa_core_pce_price_df = macro_usa_core_pce_price()
    print(macro_usa_core_pce_price_df)
    # 金十数据中心-经济指标-美国-劳动力市场-消费者收入与支出-美国实际个人消费支出季率初值报告
    macro_usa_real_consumer_spending_df = macro_usa_real_consumer_spending()
    print(macro_usa_real_consumer_spending_df)
    # 金十数据中心-经济指标-美国-贸易状况-美国贸易帐报告
    macro_usa_trade_balance_df = macro_usa_trade_balance()
    print(macro_usa_trade_balance_df)
    # 金十数据中心-经济指标-美国-贸易状况-美国经常帐报告
    macro_usa_current_account_df = macro_usa_current_account()
    print(macro_usa_current_account_df)
    # 金十数据中心-经济指标-美国-产业指标-制造业-贝克休斯钻井报告
    macro_usa_rig_count_df = macro_usa_rig_count()
    print(macro_usa_rig_count_df)
    # 金十数据中心-经济指标-美国-产业指标-制造业-美国个人支出月率报告
    # 金十数据中心-经济指标-美国-产业指标-制造业-美国生产者物价指数(PPI)报告
    macro_usa_ppi_df = macro_usa_ppi()
    print(macro_usa_ppi_df)
    # 金十数据中心-经济指标-美国-产业指标-制造业-美国核心生产者物价指数(PPI)报告
    macro_usa_core_ppi_df = macro_usa_core_ppi()
    print(macro_usa_core_ppi_df)
    # 金十数据中心-经济指标-美国-产业指标-制造业-美国API原油库存报告
    macro_usa_api_crude_stock_df = macro_usa_api_crude_stock()
    print(macro_usa_api_crude_stock_df)
    # 金十数据中心-经济指标-美国-产业指标-制造业-美国Markit制造业PMI初值报告
    macro_usa_pmi_df = macro_usa_pmi()
    print(macro_usa_pmi_df)
    # 金十数据中心-经济指标-美国-产业指标-制造业-美国ISM制造业PMI报告
    macro_usa_ism_pmi_df = macro_usa_ism_pmi()
    print(macro_usa_ism_pmi_df)
    # 金十数据中心-经济指标-美国-产业指标-房地产-美国NAHB房产市场指数报告
    macro_usa_nahb_house_market_index_df = macro_usa_nahb_house_market_index()
    print(macro_usa_nahb_house_market_index_df)
    # 金十数据中心-经济指标-美国-产业指标-房地产-美国新屋开工总数年化报告
    macro_usa_house_starts_df = macro_usa_house_starts()
    print(macro_usa_house_starts_df)
    # 金十数据中心-经济指标-美国-产业指标-房地产-美国新屋销售总数年化报告
    macro_usa_new_home_sales_df = macro_usa_new_home_sales()
    print(macro_usa_new_home_sales_df)
    # 金十数据中心-经济指标-美国-产业指标-房地产-美国营建许可总数报告
    macro_usa_building_permits_df = macro_usa_building_permits()
    print(macro_usa_building_permits_df)
    # 金十数据中心-经济指标-美国-产业指标-房地产-美国成屋销售总数年化报告
    macro_usa_exist_home_sales_df = macro_usa_exist_home_sales()
    print(macro_usa_exist_home_sales_df)
    # 金十数据中心-经济指标-美国-产业指标-房地产-美国FHFA房价指数月率报告
    macro_usa_house_price_index_df = macro_usa_house_price_index()
    print(macro_usa_house_price_index_df)
    # 金十数据中心-经济指标-美国-产业指标-房地产-美国S&P/CS20座大城市房价指数年率报告
    macro_usa_spcs20_df = macro_usa_spcs20()
    print(macro_usa_spcs20_df)
    # 金十数据中心-经济指标-美国-产业指标-房地产-美国成屋签约销售指数月率报告
    macro_usa_pending_home_sales_df = macro_usa_pending_home_sales()
    print(macro_usa_pending_home_sales_df)
    # 金十数据中心-经济指标-美国-领先指标-美国谘商会消费者信心指数报告
    macro_usa_cb_consumer_confidence_df = macro_usa_cb_consumer_confidence()
    print(macro_usa_cb_consumer_confidence_df)
    # 金十数据中心-经济指标-美国-领先指标-美国NFIB小型企业信心指数报告
    macro_usa_nfib_small_business_df = macro_usa_nfib_small_business()
    print(macro_usa_nfib_small_business_df)
    # 金十数据中心-经济指标-美国-领先指标-美国密歇根大学消费者信心指数初值报告
    macro_usa_michigan_consumer_sentiment_df = macro_usa_michigan_consumer_sentiment()
    print(macro_usa_michigan_consumer_sentiment_df)

    # 金十数据中心-经济指标-美国-其他-美国EIA原油库存报告
    macro_usa_eia_crude_rate_df = macro_usa_eia_crude_rate()
    print(macro_usa_eia_crude_rate_df)

    # 金十数据中心-经济指标-美国-其他-美国初请失业金人数报告
    macro_usa_initial_jobless_df = macro_usa_initial_jobless()
    print(macro_usa_initial_jobless_df)

    # 金十数据中心-经济指标-美国-其他-美国原油产量报告
    macro_usa_crude_inner_df = macro_usa_crude_inner()
    print(macro_usa_crude_inner_df)

    # 金十数据中心-美国商品期货交易委员会CFTC外汇类非商业持仓报告
    macro_usa_cftc_nc_holding_df = macro_usa_cftc_nc_holding()
    print(macro_usa_cftc_nc_holding_df)
    # 金十数据中心-美国商品期货交易委员会CFTC商品类非商业持仓报告
    macro_usa_cftc_c_holding_df = macro_usa_cftc_c_holding()
    print(macro_usa_cftc_c_holding_df)
    # 金十数据中心-美国商品期货交易委员会CFTC外汇类商业持仓报告
    macro_usa_cftc_merchant_currency_holding_df = (
        macro_usa_cftc_merchant_currency_holding()
    )
    print(macro_usa_cftc_merchant_currency_holding_df)
    # 金十数据中心-美国商品期货交易委员会CFTC商品类商业持仓报告
    macro_usa_cftc_merchant_goods_holding_df = macro_usa_cftc_merchant_goods_holding()
    print(macro_usa_cftc_merchant_goods_holding_df)
