"""
Date: 2022/5/25 21:11
Desc: 金十数据中心-经济指标-央行利率-主要央行利率
输出数据格式为 float64
美联储利率决议报告
欧洲央行决议报告
新西兰联储决议报告
中国央行决议报告
瑞士央行决议报告
英国央行决议报告
澳洲联储决议报告
日本央行决议报告
俄罗斯央行决议报告
印度央行决议报告
巴西央行决议报告
"""
import datetime
import time

import pandas as pd
import requests

import PPshare.stock.macro.cons as cs



def get_from_jin10_3(name,attr_id):
    t = time.time()
    headers = cs.HEADERS['3jin10']
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": attr_id,
        "_": str(int(round(t * 1000))),
    }
    big_df = pd.DataFrame()
    while True:
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        if not data_json["data"]["values"]:
            break
        temp_df = pd.DataFrame(data_json["data"]["values"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
        last_date_str = temp_df.iat[-1, 0]
        last_date_str = (
            (
                datetime.datetime.strptime(last_date_str, "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )
            .date()
            .isoformat()
        )
        params.update({"max_date": f"{last_date_str}"})
    big_df["商品"] = name
    big_df.columns = [
        "日期",
        "今值",
        "预测值",
        "前值",
        "商品",
    ]
    big_df = big_df[
        [
            "商品",
            "日期",
            "今值",
            "预测值",
            "前值",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["今值"] = pd.to_numeric(big_df["今值"])
    big_df["预测值"] = pd.to_numeric(big_df["预测值"])
    big_df["前值"] = pd.to_numeric(big_df["前值"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df
    

# 金十数据中心-经济指标-央行利率-主要央行利率-美联储利率决议报告
def macro_bank_usa_interest_rate():
    """
    美联储利率决议报告, 数据区间从 19820927-至今
    :return: 美联储利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    big_df = get_from_jin10_3('美联储利率决议',24)
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-欧洲央行决议报告
def macro_bank_euro_interest_rate():
    """
    欧洲央行决议报告, 数据区间从 19990101-至今
    :return: 欧洲央行决议报告-今值(%)
    :rtype: pandas.Series
    """
    big_df = get_from_jin10_3('欧元区利率决议',21)
    return big_df
    


# 金十数据中心-经济指标-央行利率-主要央行利率-新西兰联储决议报告
def macro_bank_newzealand_interest_rate():
    """
    新西兰联储决议报告, 数据区间从 19990401-至今
    :return: 新西兰联储决议报告-今值(%)
    :rtype: pandas.Series
    """
    big_df = get_from_jin10_3('新西兰利率决议报告',23)
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-中国央行决议报告
def macro_bank_china_interest_rate():
    """
    中国人民银行利率报告, 数据区间从 19910501-至今
    :return: 中国人民银行利率报告-今值(%)
    :rtype: pandas.Series
    """
    big_df = get_from_jin10_3('中国人民银行利率报告',91)
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-瑞士央行决议报告
def macro_bank_switzerland_interest_rate():
    """
    瑞士央行利率决议报告, 数据区间从 20080313-至今
    :return: 瑞士央行利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    big_df = get_from_jin10_3('瑞士央行利率决议报告',25)
    return big_df
    


# 金十数据中心-经济指标-央行利率-主要央行利率-英国央行决议报告
def macro_bank_english_interest_rate():
    """
    英国央行决议报告, 数据区间从 19700101-至今
    :return: 英国央行决议报告-今值(%)
    :rtype: pandas.Series
    """
    big_df = get_from_jin10_3('英国利率决议报告',26)
    return big_df
    


# 金十数据中心-经济指标-央行利率-主要央行利率-澳洲联储决议报告
def macro_bank_australia_interest_rate():
    """
    澳洲联储决议报告, 数据区间从 19800201-至今
    :return: 澳洲联储决议报告-今值(%)
    :rtype: pandas.Series
    """
    big_df = get_from_jin10_3('澳大利亚利率决议报告',27)
    return big_df
    


# 金十数据中心-经济指标-央行利率-主要央行利率-日本央行决议报告
def macro_bank_japan_interest_rate():
    """
    日本利率决议报告, 数据区间从 20080214-至今
    :return: 日本利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    big_df = get_from_jin10_3('日本利率决议报告',22)
    return big_df
    


# 金十数据中心-经济指标-央行利率-主要央行利率-俄罗斯央行决议报告
def macro_bank_russia_interest_rate():
    """
    俄罗斯利率决议报告, 数据区间从 20030601-至今
    :return: 俄罗斯利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    big_df = get_from_jin10_3('俄罗斯利率决议报告',64)
    return big_df
    


# 金十数据中心-经济指标-央行利率-主要央行利率-印度央行决议报告
def macro_bank_india_interest_rate():
    """
    印度利率决议报告, 数据区间从 20000801-至今
    :return: 印度利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    big_df = get_from_jin10_3('印度利率决议报告',68)
    return big_df


# 金十数据中心-经济指标-央行利率-主要央行利率-巴西央行决议报告
def macro_bank_brazil_interest_rate():
    """
    巴西利率决议报告, 数据区间从 20080201-至今
    :return: 巴西利率决议报告-今值(%)
    :rtype: pandas.Series
    """
    big_df = get_from_jin10_3('巴西利率决议报告',55)
    return big_df