import re
from functools import lru_cache
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import PPshare.energy.cons as cs
from PPshare.util import demjson


@lru_cache()
def energy_carbon_domestic(symbol="湖北"):
    """
    碳交易网-行情信息
    :param symbol: choice of {'湖北', '上海', '北京', '重庆', '广东', '天津', '深圳', '福建'}
    :type symbol: str
    :return: 行情信息
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http'] + cs.URL_DIC['tanjiaoyi'] + cs.URL_PARA[
        'KDataController']
    params = {
        "lcnK": "53f75bfcefff58e4046ccfa42171636c",
        "brand": "TAN",
        "_": "1626773022063",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("(") + 1:-1])
    temp_df = pd.DataFrame(data_json[symbol])
    temp_df.columns = [
        "成交价",
        "_",
        "成交量",
        "地点",
        "成交额",
        "日期",
        "_",
    ]
    temp_df = temp_df[[
        "日期",
        "成交价",
        "成交量",
        "成交额",
        "地点",
    ]]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df["成交价"] = pd.to_numeric(temp_df["成交价"])
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"])
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
    return temp_df


@lru_cache()
def energy_carbon_bj():
    """
    北京市碳排放权电子交易平台-北京市碳排放权公开交易行情
    :return: 北京市碳排放权公开交易行情
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http'] + cs.URL_DIC['bjets'] + cs.URL_PARA['article']
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    total_page = (soup.find("table").find("script").string.split("=")
                  [-1].strip().strip(";").strip('"'))
    temp_df = pd.DataFrame()
    for i in tqdm(
            range(1,
                  int(total_page) + 1),
            desc="Please wait for a moment",
            leave=False,
    ):
        if i == 1:
            i = ""
        url = f"{url}?{i}"
        r = requests.get(url)
        r.encoding = "utf-8"
        df = pd.read_html(r.text)[0]
        temp_df = pd.concat([temp_df, df], ignore_index=True)
    temp_df.columns = ["日期", "成交量", "成交均价", "成交额"]
    temp_df["成交单位"] = (temp_df["成交额"].str.split(
        "(", expand=True).iloc[:, 1].str.split(
            "）", expand=True).iloc[:, 0].str.split(")", expand=True).iloc[:,
                                                                          0])
    temp_df["成交额"] = (temp_df["成交额"].str.split(
        "(", expand=True).iloc[:, 0].str.split("（", expand=True).iloc[:, 0])
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"])
    temp_df["成交均价"] = pd.to_numeric(temp_df["成交均价"])
    temp_df["成交额"] = temp_df["成交额"].str.replace(",", "")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df.sort_values("日期", inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


@lru_cache()
def energy_carbon_sz():
    """
    深圳碳排放交易所-国内碳情
    :return: 国内碳情每日行情数据
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http'] + cs.URL_DIC['cerx'] + cs.URL_PARA['dailynewsCN']
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    page_num = int(
        soup.find(attrs={
            "class": "pagebar"
        }).find_all("option")[-1].text)
    big_df = pd.read_html(r.text, header=0)[0]
    for page in tqdm(range(2, page_num + 1),
                     desc="Please wait for a moment",
                     leave=False):
        url = f"{cs.URL_TYPE['http']+cs.URL_DIC['cerx']}dailynewsCN/index_{page}.htm"
        r = requests.get(url)
        temp_df = pd.read_html(r.text, header=0)[0]
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df["交易日期"] = pd.to_datetime(big_df["交易日期"]).dt.date
    big_df["开盘价"] = pd.to_numeric(big_df["开盘价"])
    big_df["最高价"] = pd.to_numeric(big_df["最高价"])
    big_df["最低价"] = pd.to_numeric(big_df["最低价"])
    big_df["成交均价"] = pd.to_numeric(big_df["成交均价"])
    big_df["收盘价"] = pd.to_numeric(big_df["收盘价"])
    big_df["成交量"] = pd.to_numeric(big_df["成交量"])
    big_df["成交额"] = pd.to_numeric(big_df["成交额"])
    big_df.sort_values("交易日期", inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


@lru_cache()
def energy_carbon_eu():
    """
    深圳碳排放交易所-国际碳情
    :return: 国际碳情每日行情数据
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http'] + cs.URL_DIC['cerx'] + cs.URL_PARA[
        'dailynewsOuter']
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    page_num = int(
        soup.find(attrs={
            "class": "pagebar"
        }).find_all("option")[-1].text)
    big_df = pd.read_html(r.text, header=0)[0]
    for page in tqdm(range(2, page_num + 1),
                     desc="Please wait for a moment",
                     leave=False):
        url = f"{cs.URL_TYPE['http']+cs.URL_DIC['cerx']}dailynewsOuter/index_{page}.htm"
        r = requests.get(url)
        temp_df = pd.read_html(r.text, header=0)[0]
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df["交易日期"] = pd.to_datetime(big_df["交易日期"]).dt.date
    big_df["开盘价"] = pd.to_numeric(big_df["开盘价"])
    big_df["最高价"] = pd.to_numeric(big_df["最高价"])
    big_df["最低价"] = pd.to_numeric(big_df["最低价"])
    big_df["成交均价"] = pd.to_numeric(big_df["成交均价"])
    big_df["收盘价"] = pd.to_numeric(big_df["收盘价"])
    big_df["成交量"] = pd.to_numeric(big_df["成交量"])
    big_df["成交额"] = pd.to_numeric(big_df["成交额"])
    big_df.sort_values("交易日期", inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


@lru_cache()
def energy_carbon_hb():
    """
    湖北碳排放权交易中心-现货交易数据-配额-每日概况
    :return: 现货交易数据-配额-每日概况行情数据
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http'] + cs.URL_DIC['hbets'] + cs.URL_PARA['list']
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    page_string = (soup.find("div", attrs={
        "class": "page"
    }).find_all("span")[-1].text)
    page_num = int(re.findall(r"\d+", page_string)[-1])
    columns = [
        item.text for item in soup.find("ul", attrs={
            "class": "title"
        }).find_all("li")
    ]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, page_num + 1),
                     desc="Please wait for a moment",
                     leave=False):
        params = {"page": page}
        r = requests.get(url, params=params)
        soup = BeautifulSoup(r.text, "lxml")
        page_node = [
            item for item in soup.find(attrs={
                "class": "future_table"
            }).find_all(attrs={"class": "cont"})
        ]
        temp_list = []
        for item in page_node:
            temp_inner_list = []
            for inner_item in item.find_all("li"):
                temp_inner_list.append(inner_item.text)
            temp_list.append(temp_inner_list)
        temp_df = pd.DataFrame(temp_list)
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.columns = columns
    big_df["交易品种"] = big_df["交易品种"].str.strip()
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新"] = pd.to_numeric(big_df["最新"])
    big_df["涨跌幅"] = big_df["涨跌幅"].str.strip("%").str.strip()
    big_df["涨跌幅"] = big_df["涨跌幅"].str.strip("%")
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["最高"] = big_df["最高"].str.replace("--", "")
    big_df["最高"] = pd.to_numeric(big_df["最高"])
    big_df["最低"] = big_df["最低"].str.replace("--", "")
    big_df["最低"] = pd.to_numeric(big_df["最低"])
    big_df["成交量"] = big_df["成交量"].str.replace("--", "")
    big_df["成交量"] = pd.to_numeric(big_df["成交量"])
    big_df["成交额"] = big_df["成交额"].str.replace("--", "")
    big_df["成交额"] = pd.to_numeric(big_df["成交额"])
    big_df["昨收盘价"] = big_df["昨收盘价"].str.replace("--", "")
    big_df["昨收盘价"] = pd.to_numeric(big_df["昨收盘价"])
    big_df.dropna(subset=["最新"], inplace=True)
    big_df.sort_values("日期", inplace=True)
    big_df = big_df[[
        "日期", "交易品种", "最新", "涨跌幅", "最高", "最低", "成交量", "成交额", "昨收盘价"
    ]]
    big_df.reset_index(inplace=True, drop=True)
    return big_df


@lru_cache()
def energy_carbon_gz():
    """
    广州碳排放权交易中心-行情信息
    :return: 行情信息数据
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http'] + cs.URL_DIC['ets'] + cs.URL_PARA['carbon']
    params = {
        "Top": "1",
        "beginTime": "2010-01-01",
        "endTime": "2030-09-12",
    }
    r = requests.get(url, params=params)
    temp_df = pd.read_html(r.text, header=0)[1]
    temp_df.columns = [
        "日期",
        "品种",
        "开盘价",
        "收盘价",
        "最高价",
        "最低价",
        "涨跌",
        "涨跌幅",
        "成交数量",
        "成交金额",
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], format="%Y%m%d").dt.date
    temp_df["开盘价"] = pd.to_numeric(temp_df["开盘价"])
    temp_df["收盘价"] = pd.to_numeric(temp_df["收盘价"])
    temp_df["最高价"] = pd.to_numeric(temp_df["最高价"])
    temp_df["最低价"] = pd.to_numeric(temp_df["最低价"])
    temp_df["涨跌"] = pd.to_numeric(temp_df["涨跌"])
    temp_df["涨跌幅"] = temp_df["涨跌幅"].str.strip("%")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
    temp_df["成交数量"] = pd.to_numeric(temp_df["成交数量"])
    temp_df["成交金额"] = pd.to_numeric(temp_df["成交金额"])
    temp_df.sort_values("日期", inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df


if __name__ == "__main__":
    # energy_carbon_domestic_df = energy_carbon_domestic(symbol="湖北")
    # print(energy_carbon_domestic_df)

    # energy_carbon_domestic_df = energy_carbon_domestic(symbol="深圳")
    # print(energy_carbon_domestic_df)

    energy_carbon_bj_df = energy_carbon_bj()
    print(energy_carbon_bj_df)

    # 出错了，删掉
    # energy_carbon_sz_df = energy_carbon_sz()
    # print(energy_carbon_sz_df)

    # 出错了，删掉
    # energy_carbon_eu_df = energy_carbon_eu()
    # print(energy_carbon_eu_df)

    # energy_carbon_hb_df = energy_carbon_hb()
    # print(energy_carbon_hb_df)

    # energy_carbon_gz_df = energy_carbon_gz()
    # print(energy_carbon_gz_df)