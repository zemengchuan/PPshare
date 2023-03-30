import requests
import pandas as pd
import time
import math
import json
import PPshare.stock.macro.cons as cs
from tqdm import tqdm
import PPshare.util.demjson as demjson
from PPshare.stock.macro.func import eastmoney,jin10


def get_from_jin10_1(name,cname,attr_id):
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA[name]
    r = requests.get(
        url.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(r.text[r.text.find("{") : r.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"][cname] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    try:
        temp_df = value_df["今值"]
    except:
        try:
            temp_df = value_df["今值(%)"]
        except:
            temp_df = value_df["今值(亿美元)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = jin10('ec',attr_id,t)
    headers = cs.HEADERS['jin10']
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = pd.concat([temp_df, temp_se])
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.columns = ["date", "value"]
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    temp_df["value"] = pd.to_numeric(temp_df["value"])
    return temp_df

def get_from_jin10_2(name,cname,attr_id):
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA[name]
    res = requests.get(
        url.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"][cname] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    try:
        temp_df = value_df["今值"]
    except:
        try:
            temp_df = value_df["今值(%)"]
        except:
            temp_df = value_df["今值(亿美元)"]
    url = cs.URL_TYPE['https']+cs.URL_DIC['data-jin10']+cs.URL_PARA['list_v2']
    params = jin10('ec',attr_id,t)
    headers = cs.HEADERS['jin10']
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
    temp_df.name = f"china_{name}"
    temp_df = temp_df.astype(float)
    return temp_df

def China_CGPI():
    """
    东方财富-经济数据一览-中国-企业商品价格指数
    :return: 企业商品价格指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = eastmoney(0)
    data = params("RPT_ECONOMY_GOODS_INDEX",cs.REQ_COLUMNS['China_CGPI'])
    r = requests.get(url, params=data)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    del temp_df['REPORT_DATE']
    columns = cs.TABLE_COLUMN['China_CGPI']
    temp_df.columns = columns
    for column in columns[1:]:
        temp_df[column] = pd.to_numeric(temp_df[column], errors="coerce")
    return temp_df

# 外商直接投资数据
def China_FDI():
    """
    东方财富-经济数据一览-中国-外商直接投资数据
    :return: 外商直接投资数据
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = eastmoney(0)
    data = params("RPT_ECONOMY_FDI",cs.REQ_COLUMNS['China_FDI'])
    r = requests.get(url, params=data)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    del temp_df['REPORT_DATE']
    columns = cs.TABLE_COLUMN['China_FDI']
    temp_df.columns = columns
    for column in columns[1:]:
        temp_df[column] = pd.to_numeric(temp_df[column], errors="coerce")
    return temp_df

def China_ISFC():
    """
    商务数据中心-国内贸易-社会融资规模增量统计
    :return: 社会融资规模增量统计
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http']+cs.URL_DIC['mofcom']+cs.URL_PARA['ISFC']
    r = requests.post(url)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    columns = cs.TABLE_COLUMN['China_ISFC_1']
    temp_df.columns = columns
    temp_df = temp_df[cs.TABLE_COLUMN['China_ISFC_2']]
    for column in columns[1:]:
        temp_df[column] = pd.to_numeric(temp_df[column], errors="coerce")
    temp_df.sort_values(["月份"], inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df

# 金十数据中心-经济指标-中国-国民经济运行状况-经济状况-中国GDP年率报告
def China_GDP_yearly():
    """
    金十数据中心-中国 GDP 年率报告, 数据区间从 20110120-至今
    :return: 中国 GDP 年率报告
    :rtype: pandas.DataFrame
    """
    temp_df = get_from_jin10_1("GDP_yoy","中国GDP年率报告",57)
    return temp_df

def China_CPI_monthly():
    """
    中国月度 CPI 数据, 数据区间从 19960201-至今
    :return: 中国月度 CPI 数据
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_1("CPI_mom","中国CPI月率报告",72)
    return temp_df

# 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国CPI年率报告
def China_CPI_yearly():
    """
    中国年度 CPI 数据, 数据区间从 19860201-至今
    :return: 中国年度 CPI 数据
    :rtype: pandas.DataFrame
    """
    temp_df = get_from_jin10_1("CPI_yoy","中国CPI年率报告",56)
    return temp_df

# 金十数据中心-经济指标-中国-国民经济运行状况-物价水平-中国PPI年率报告
def China_PPI_yearly():
    """
    中国年度 PPI 数据, 数据区间从 19950801-至今
    :return: 中国年度PPI数据
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_1("PPI_yoy","中国PPI年率报告",60)
    return temp_df

# 金十数据中心-经济指标-中国-贸易状况-以美元计算出口年率报告
def China_exports_yoy():
    """
    中国以美元计算出口年率报告, 数据区间从19820201-至今
    :return: 中国以美元计算出口年率报告-今值(%)
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_2("exports_yoy","中国以美元计算出口年率报告",66)
    return temp_df

# 金十数据中心-经济指标-中国-贸易状况-以美元计算进口年率
def China_imports_yoy():
    """
    中国以美元计算进口年率报告, 数据区间从 19960201-至今
    :return: 中国以美元计算进口年率报告-今值(%)
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_2("imports_yoy","中国以美元计算进口年率报告",77)
    return temp_df

def China_trade_balance():
    """
    中国以美元计算贸易帐报告, 数据区间从 19810201-至今
    :return: 中国以美元计算贸易帐报告-今值(亿美元)
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_2("trade_balance","中国以美元计算贸易帐报告",61)
    return temp_df

def China_industrial_production_yoy():
    """
    中国规模以上工业增加值年率报告, 数据区间从19900301-至今
    :return: 中国规模以上工业增加值年率报告-今值(%)
    :rtype: pandas.Series
    """
    temp_df = get_from_jin10_2("industrial_production_yoy","中国规模以上工业增加值年率报告",58)
    return temp_df

def China_PMI_yearly():
    """
    中国年度 PMI 数据, 数据区间从20050201-至今
    :return: pandas.Series
    """
    temp_df = get_from_jin10_1("PMI_yoy","中国官方制造业PMI报告",65)
    return temp_df

def China_cx_PMI_yearly():
    """
    中国年度财新PMI数据, 数据区间从 20120120-至今
    :return: pandas.Series
    """
    temp_df = get_from_jin10_1("cx_PMI_yoy","中国财新制造业PMI终值报告",73)
    return temp_df

def China_cx_services_PMI_yearly():
    """
    中国财新服务业PMI报告, 数据区间从 20120405-至今
    :return: pandas.Series
    """
    temp_df = get_from_jin10_1("cx_services_PMI_yoy","中国财新服务业PMI报告",67)
    return temp_df

def China_non_man_PMI():
    """
    中国官方非制造业 PMI, 数据区间从 20160101-至今
    :return: pandas.Series
    """
    temp_df = get_from_jin10_1("non_man_PMI","中国官方非制造业PMI报告",75)
    return temp_df

def China_fx_reserves_yearly():
    """
    中国年度外汇储备数据, 数据区间从 20140115-至今
    :return: pandas.Series
    """
    temp_df = get_from_jin10_1("fx_reserves","中国外汇储备报告",76)
    return temp_df

def China_M2_yearly():
    """
    中国年度 M2 数据, 数据区间从 19980201-至今
    :return: pandas.Series
    """
    temp_df = get_from_jin10_1("M2_yearly","中国M2货币供应年率报告",59)
    return temp_df

def China_daily_energy():
    """
    中国日度沿海六大电库存数据, 数据区间从20160101-至今
    :return: pandas.Series
                 沿海六大电库存      日耗 存煤可用天数
    2016-01-01  1167.60   64.20   18.19
    2016-01-02  1162.90   63.40   18.34
    2016-01-03  1160.80   62.60   18.54
    2016-01-04  1185.30   57.60   20.58
    2016-01-05  1150.20   57.20   20.11
                  ...     ...    ...
    2019-05-17   1639.47   61.71  26.56
    2019-05-21   1591.92   62.67  25.40
    2019-05-22   1578.63   59.54  26.51
    2019-05-24   1671.83   60.65  27.56
    2019-06-21   1786.64   66.57  26.84
    """
    t = time.time()
    url = cs.URL_TYPE['https']+cs.URL_DIC['jin10']+cs.URL_PARA['daily_energy']
    res = requests.get(
        url.format(
            str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)
        )
    )
    json_data = json.loads(res.text[res.text.find("{") : res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["沿海六大电厂库存动态报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df[["沿海六大电库存", "日耗", "存煤可用天数"]]
    temp_df.name = "energy"
    temp_df = temp_df.astype(float)
    return temp_df

def China_rmb():
    """
    中国人民币汇率中间价报告, 数据区间从 20170103-至今
    :return: 中国人民币汇率中间价报告
    :rtype: pandas.DataFrame
    """
    t = time.time()
    params = {"_": t}
    res = requests.get(
        cs.URL_TYPE['https']+cs.URL_DIC['2jin10']+cs.URL_PARA['rmb'],
        params=params,
    )
    json_data = res.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    big_df = pd.DataFrame()
    temp_df.fillna(value="--", inplace=True)
    big_df["美元/人民币_中间价"] = temp_df["美元/人民币"].apply(lambda x: x[0])
    big_df["美元/人民币_涨跌幅"] = temp_df["美元/人民币"].apply(lambda x: x[1])
    big_df["欧元/人民币_中间价"] = temp_df["欧元/人民币"].apply(lambda x: x[0])
    big_df["欧元/人民币_涨跌幅"] = temp_df["欧元/人民币"].apply(lambda x: x[1])
    big_df["100日元/人民币_中间价"] = temp_df["100日元/人民币"].apply(lambda x: x[0])
    big_df["100日元/人民币_涨跌幅"] = temp_df["100日元/人民币"].apply(lambda x: x[1])
    big_df["港元/人民币_中间价"] = temp_df["港元/人民币"].apply(lambda x: x[0])
    big_df["港元/人民币_涨跌幅"] = temp_df["港元/人民币"].apply(lambda x: x[1])
    big_df["英镑/人民币_中间价"] = temp_df["英镑/人民币"].apply(lambda x: x[0])
    big_df["英镑/人民币_涨跌幅"] = temp_df["英镑/人民币"].apply(lambda x: x[1])
    big_df["澳元/人民币_中间价"] = temp_df["澳元/人民币"].apply(lambda x: x[0])
    big_df["澳元/人民币_涨跌幅"] = temp_df["澳元/人民币"].apply(lambda x: x[1])
    big_df["新西兰元/人民币_中间价"] = temp_df["新西兰元/人民币"].apply(lambda x: x[0])
    big_df["新西兰元/人民币_涨跌幅"] = temp_df["新西兰元/人民币"].apply(lambda x: x[1])
    big_df["新加坡元/人民币_中间价"] = temp_df["新加坡元/人民币"].apply(lambda x: x[0])
    big_df["新加坡元/人民币_涨跌幅"] = temp_df["新加坡元/人民币"].apply(lambda x: x[1])
    big_df["瑞郎/人民币_中间价"] = temp_df["瑞郎/人民币"].apply(lambda x: x[0])
    big_df["瑞郎/人民币_涨跌幅"] = temp_df["瑞郎/人民币"].apply(lambda x: x[1])
    big_df["加元/人民币_中间价"] = temp_df["加元/人民币"].apply(lambda x: x[0])
    big_df["加元/人民币_涨跌幅"] = temp_df["加元/人民币"].apply(lambda x: x[1])
    big_df["人民币/马来西亚林吉特_中间价"] = temp_df["人民币/马来西亚林吉特"].apply(lambda x: x[0])
    big_df["人民币/马来西亚林吉特_涨跌幅"] = temp_df["人民币/马来西亚林吉特"].apply(lambda x: x[1])
    big_df["人民币/俄罗斯卢布_中间价"] = temp_df["人民币/俄罗斯卢布"].apply(lambda x: x[0])
    big_df["人民币/俄罗斯卢布_涨跌幅"] = temp_df["人民币/俄罗斯卢布"].apply(lambda x: x[1])
    big_df["人民币/南非兰特_中间价"] = temp_df["人民币/南非兰特"].apply(lambda x: x[0])
    big_df["人民币/南非兰特_涨跌幅"] = temp_df["人民币/南非兰特"].apply(lambda x: x[1])
    big_df["人民币/韩元_中间价"] = temp_df["人民币/韩元"].apply(lambda x: x[0])
    big_df["人民币/韩元_涨跌幅"] = temp_df["人民币/韩元"].apply(lambda x: x[1])
    big_df["人民币/阿联酋迪拉姆_中间价"] = temp_df["人民币/阿联酋迪拉姆"].apply(lambda x: x[0])
    big_df["人民币/阿联酋迪拉姆_涨跌幅"] = temp_df["人民币/阿联酋迪拉姆"].apply(lambda x: x[1])
    big_df["人民币/沙特里亚尔_中间价"] = temp_df["人民币/沙特里亚尔"].apply(lambda x: x[0])
    big_df["人民币/沙特里亚尔_涨跌幅"] = temp_df["人民币/沙特里亚尔"].apply(lambda x: x[1])
    big_df["人民币/匈牙利福林_中间价"] = temp_df["人民币/匈牙利福林"].apply(lambda x: x[0])
    big_df["人民币/匈牙利福林_涨跌幅"] = temp_df["人民币/匈牙利福林"].apply(lambda x: x[1])
    big_df["人民币/波兰兹罗提_中间价"] = temp_df["人民币/波兰兹罗提"].apply(lambda x: x[0])
    big_df["人民币/波兰兹罗提_涨跌幅"] = temp_df["人民币/波兰兹罗提"].apply(lambda x: x[1])
    big_df["人民币/丹麦克朗_中间价"] = temp_df["人民币/丹麦克朗"].apply(lambda x: x[0])
    big_df["人民币/丹麦克朗_涨跌幅"] = temp_df["人民币/丹麦克朗"].apply(lambda x: x[1])
    big_df["人民币/瑞典克朗_中间价"] = temp_df["人民币/瑞典克朗"].apply(lambda x: x[0])
    big_df["人民币/瑞典克朗_涨跌幅"] = temp_df["人民币/瑞典克朗"].apply(lambda x: x[1])
    big_df["人民币/挪威克朗_中间价"] = temp_df["人民币/挪威克朗"].apply(lambda x: x[0])
    big_df["人民币/挪威克朗_涨跌幅"] = temp_df["人民币/挪威克朗"].apply(lambda x: x[1])
    big_df["人民币/土耳其里拉_中间价"] = temp_df["人民币/土耳其里拉"].apply(lambda x: x[0])
    big_df["人民币/土耳其里拉_涨跌幅"] = temp_df["人民币/土耳其里拉"].apply(lambda x: x[1])
    big_df["人民币/墨西哥比索_中间价"] = temp_df["人民币/墨西哥比索"].apply(lambda x: x[0])
    big_df["人民币/墨西哥比索_涨跌幅"] = temp_df["人民币/墨西哥比索"].apply(lambda x: x[1])
    big_df["人民币/泰铢_定价"] = temp_df["人民币/泰铢"].apply(lambda x: x[0])
    big_df["人民币/泰铢_涨跌幅"] = temp_df["人民币/泰铢"].apply(lambda x: x[1])
    big_df = big_df.apply(lambda x: x.replace("-", pd.NA))
    big_df = big_df.apply(lambda x: x.replace([None], pd.NA))
    big_df.sort_index(inplace=True)
    big_df.fillna(0, inplace=True)
    big_df = big_df.astype("float")
    big_df.reset_index(inplace=True)
    big_df.rename(columns={"index": "日期"}, inplace=True)
    return big_df

# 金十数据中心-经济指标-中国-其他-深圳融资融券报告
def China_market_margin_sz():
    """
    深圳融资融券报告, 数据区间从20100331-至今
    :return: pandas.DataFrame
                   融资买入额(元)       融资余额(元)  融券卖出量(股)    融券余量(股)     融券余额(元)  \
    2010-03-31       684569        670796      4000       3900       70895
    2010-04-08      6713260      14467758      2100       3100       56023
    2010-04-09      9357095      19732998      6700       5400      108362
    2010-04-12     10406563      24813027      2200       1000        8100
    2010-04-15     16607172      47980287      4200       5200       97676
                     ...           ...       ...        ...         ...
    2019-12-12  25190412075  423457288662  29769255  209557883  2504593151
    2019-12-13  29636811209  423422868505  32820867  206092170  2509424768
    2019-12-16  39166060634  428851154451  44000215  217123568  2647520178
    2019-12-17  46930557203  433966722200  40492711  220945538  2750371397
    2019-12-18  41043515833  438511398249  39150376  224554586  2761303194
                   融资融券余额(元)
    2010-03-31        741691
    2010-04-08      14523781
    2010-04-09      19841360
    2010-04-12      24821127
    2010-04-15      48077963
                      ...
    2019-12-12  425961881813
    2019-12-13  425932293273
    2019-12-16  431498674629
    2019-12-17  436717093597
    2019-12-18  441272701443
    """
    t = time.time()
    params = {"_": t}
    res = requests.get(
        cs.URL_TYPE['https']+cs.URL_DIC['2jin10']+cs.URL_PARA['market_margin_sz'], params=params
    )
    json_data = res.json()
    temp_df = pd.DataFrame(json_data["values"]).T
    temp_df.columns = ["融资买入额", "融资余额", "融券卖出量", "融券余量", "融券余额", "融资融券余额"]
    temp_df.sort_index(inplace=True)
    temp_df.index = pd.to_datetime(temp_df.index)
    temp_df = temp_df.astype("float")
    return temp_df

def China_au_report():
    """
    上海黄金交易所报告, 数据区间从20100331-至今
    :return: pandas.DataFrame
    """
    t = time.time()
    params = {"_": t}
    url = cs.URL_TYPE['https']+cs.URL_DIC['2jin10']+cs.URL_PARA['au_report']
    res = requests.get(url,params=params)
    json_data = res.json()
    big_df = pd.DataFrame()
    for item in json_data["values"].keys():
        temp_df = pd.DataFrame(json_data["values"][item])
        temp_df["date"] = item
        temp_df.columns = [
            "商品",
            "开盘价",
            "最高价",
            "最低价",
            "收盘价",
            "涨跌",
            "涨跌幅",
            "加权平均价",
            "成交量",
            "成交金额",
            "持仓量",
            "交收方向",
            "交收量",
            "日期",
        ]
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.index = pd.to_datetime(big_df["日期"])
    del big_df["日期"]
    big_df.sort_index(inplace=True)
    return big_df

def China_ctci():
    """
    中国电煤价格指数-全国综合电煤价格指数
    :return: 20140101-至今的所有历史数据
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http']+cs.URL_DIC['ctci']+cs.URL_PARA['ctci']
    r = requests.get(url)
    temp_df = pd.Series(r.json()["data"][0])
    temp_df.index = pd.to_datetime(r.json()["periods"])
    temp_df = temp_df.astype(float)
    return temp_df

def China_ctci_detail():
    """
    2019年11月各价区电煤价格指数
    :return:
    :rtype:
    """
    url = cs.URL_TYPE['http']+cs.URL_DIC['ctci']+cs.URL_PARA['ctci_detail']
    res = requests.get(url)
    data_df = pd.DataFrame(res.json()["data"])
    data_df.index = res.json()["names"]
    data_df.columns = ["-", "环比", "上期", "同比", "本期"]
    temp = data_df[["环比", "上期", "同比", "本期"]]
    temp = temp.astype(float)
    return temp

# 发改委-中国电煤价格指数-历史电煤价格指数
def China_ctci_detail_hist(year="2018"):
    """
    历史电煤价格指数
    :param year: 2014-2019 年
    :type year: str
    :return: 制定年份的中国电煤价格指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http']+cs.URL_DIC['ctci']+cs.URL_PARA['ctci_detail_hist']
    url = "http://59.252.41.60/portal//out/dm/listAll?t=1578299685398"
    params = {
        "CONF_ID": "cebdf627f9c24c22a507e2f2e25e2b43",
        "year": f"{year}",
    }
    res = requests.post(url, data=params)
    data_df = pd.DataFrame(res.json()["data"])
    data_df.columns = res.json()["names"]
    data_df.index = data_df["地区"]
    del data_df["地区"]
    temp_df = data_df
    temp_df = temp_df.astype(float)
    return temp_df

# 中国-新房价指数
def China_new_house_price(city_first: str = "北京", city_second: str = "上海") :
    """
    中国-新房价指数
    :param city_first: 城市; 城市列表见目标网站
    :type city_first: str
    :param city_second: 城市; 城市列表见目标网站
    :type city_second: str
    :return: 新房价指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "reportName": "RPT_ECONOMY_HOUSE_PRICE",
        "columns": "REPORT_DATE,CITY,FIRST_COMHOUSE_SAME,FIRST_COMHOUSE_SEQUENTIAL,FIRST_COMHOUSE_BASE,SECOND_HOUSE_SAME,SECOND_HOUSE_SEQUENTIAL,SECOND_HOUSE_BASE,REPORT_DAY",
        "filter": f'(CITY in ("{city_first}","{city_second}"))',
        "pageNumber": "1",
        "pageSize": "500",
        "sortColumns": "REPORT_DATE,CITY",
        "sortTypes": "-1,-1",
        "source": "WEB",
        "client": "WEB",
        'p': '1',
        'pageNo': '1',
        'pageNum': '1',
        '_': '1669352163467',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "日期",
        "城市",
        "新建商品住宅价格指数-同比",
        "新建商品住宅价格指数-环比",
        "新建商品住宅价格指数-定基",
        "二手住宅价格指数-环比",
        "二手住宅价格指数-同比",
        "二手住宅价格指数-定基",
        "-",
    ]
    temp_df = temp_df[[
        "日期",
        "城市",
        "新建商品住宅价格指数-同比",
        "新建商品住宅价格指数-环比",
        "新建商品住宅价格指数-定基",
        "二手住宅价格指数-环比",
        "二手住宅价格指数-同比",
        "二手住宅价格指数-定基",
    ]]
    temp_df['日期'] = pd.to_datetime(temp_df['日期']).dt.date
    temp_df['新建商品住宅价格指数-同比'] = pd.to_numeric(temp_df['新建商品住宅价格指数-同比'], errors="coerce")
    temp_df['新建商品住宅价格指数-环比'] = pd.to_numeric(temp_df['新建商品住宅价格指数-环比'], errors="coerce")
    temp_df['新建商品住宅价格指数-定基'] = pd.to_numeric(temp_df['新建商品住宅价格指数-定基'], errors="coerce")
    temp_df['二手住宅价格指数-环比'] = pd.to_numeric(temp_df['二手住宅价格指数-环比'], errors="coerce")
    temp_df['二手住宅价格指数-同比'] = pd.to_numeric(temp_df['二手住宅价格指数-同比'], errors="coerce")
    temp_df['二手住宅价格指数-定基'] = pd.to_numeric(temp_df['二手住宅价格指数-定基'], errors="coerce")
    return temp_df

# 中国-企业景气及企业家信心指数
def China_enterprise_boom_index():
    """
    中国-企业景气及企业家信心指数
    :return: 企业景气及企业家信心指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,BOOM_INDEX,FAITH_INDEX,BOOM_INDEX_SAME,BOOM_INDEX_SEQUENTIAL,FAITH_INDEX_SAME,FAITH_INDEX_SEQUENTIAL",
        "pageNumber": "1",
        "pageSize": "500",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_BOOM_INDEX",
        'p': '1',
        'pageNo': '1',
        'pageNum': '1',
        '_': '1669352163467',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "-",
        "季度",
        "企业景气指数-指数",
        "企业家信心指数-指数",
        "企业景气指数-同比",
        "企业景气指数-环比",
        "企业家信心指数-同比",
        "企业家信心指数-环比",
    ]
    temp_df = temp_df[[
        "季度",
        "企业景气指数-指数",
        "企业景气指数-同比",
        "企业景气指数-环比",
        "企业家信心指数-指数",
        "企业家信心指数-同比",
        "企业家信心指数-环比",
    ]]
    temp_df['企业景气指数-指数'] = pd.to_numeric(temp_df['企业景气指数-指数'], errors="coerce")
    temp_df['企业家信心指数-指数'] = pd.to_numeric(temp_df['企业家信心指数-指数'], errors="coerce")
    temp_df['企业景气指数-同比'] = pd.to_numeric(temp_df['企业景气指数-同比'], errors="coerce")
    temp_df['企业景气指数-环比'] = pd.to_numeric(temp_df['企业景气指数-环比'], errors="coerce")
    temp_df['企业家信心指数-同比'] = pd.to_numeric(temp_df['企业家信心指数-同比'], errors="coerce")
    temp_df['企业家信心指数-环比'] = pd.to_numeric(temp_df['企业家信心指数-环比'], errors="coerce")
    return temp_df

# 中国-全国税收收入
def China_national_tax_receipts():
    """
    中国-全国税收收入
    :return: 全国税收收入
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,TAX_INCOME,TAX_INCOME_SAME,TAX_INCOME_SEQUENTIAL",
        "pageNumber": "1",
        "pageSize": "500",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_TAX",
        'p': '1',
        'pageNo': '1',
        'pageNum': '1',
        '_': '1669352163467',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])

    temp_df.columns = ["-", "季度", "税收收入合计", "较上年同期", "季度环比"]
    temp_df = temp_df[[
        "季度", "税收收入合计", "较上年同期", "季度环比"
    ]]

    temp_df["税收收入合计"] = pd.to_numeric(temp_df["税收收入合计"], errors="coerce")
    temp_df["较上年同期"] = pd.to_numeric(temp_df["较上年同期"], errors="coerce")
    temp_df["季度环比"] = pd.to_numeric(temp_df["季度环比"], errors="coerce")
    return temp_df

# 中国-银行理财产品发行数量
def China_bank_financing():
    """
    银行理财产品发行数量
    :return: 银行理财产品发行数量
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "1000",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI01516267")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df["最新值"] = pd.to_numeric(temp_df["最新值"])
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
    temp_df["近3月涨跌幅"] = pd.to_numeric(temp_df["近3月涨跌幅"])
    temp_df["近6月涨跌幅"] = pd.to_numeric(temp_df["近6月涨跌幅"])
    temp_df["近1年涨跌幅"] = pd.to_numeric(temp_df["近1年涨跌幅"])
    temp_df["近2年涨跌幅"] = pd.to_numeric(temp_df["近2年涨跌幅"])
    temp_df["近3年涨跌幅"] = pd.to_numeric(temp_df["近3年涨跌幅"])
    temp_df.sort_values(["日期"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df

def China_insurance_income():
    """
    原保险保费收入
    :return: 原保险保费收入
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "1000",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMM00088870")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df["最新值"] = pd.to_numeric(temp_df["最新值"])
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
    temp_df["近3月涨跌幅"] = pd.to_numeric(temp_df["近3月涨跌幅"])
    temp_df["近6月涨跌幅"] = pd.to_numeric(temp_df["近6月涨跌幅"])
    temp_df["近1年涨跌幅"] = pd.to_numeric(temp_df["近1年涨跌幅"])
    temp_df["近2年涨跌幅"] = pd.to_numeric(temp_df["近2年涨跌幅"])
    temp_df["近3年涨跌幅"] = pd.to_numeric(temp_df["近3年涨跌幅"])
    temp_df.sort_values(["日期"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df

def China_mobile_number():
    """
    手机出货量
    :return: 手机出货量
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "1000",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00225823")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.drop_duplicates(inplace=True)
    temp_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"]).dt.date
    temp_df["最新值"] = pd.to_numeric(temp_df["最新值"])
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
    temp_df["近3月涨跌幅"] = pd.to_numeric(temp_df["近3月涨跌幅"])
    temp_df["近6月涨跌幅"] = pd.to_numeric(temp_df["近6月涨跌幅"])
    temp_df["近1年涨跌幅"] = pd.to_numeric(temp_df["近1年涨跌幅"])
    temp_df["近2年涨跌幅"] = pd.to_numeric(temp_df["近2年涨跌幅"])
    temp_df["近3年涨跌幅"] = pd.to_numeric(temp_df["近3年涨跌幅"])
    temp_df.sort_values(["日期"], inplace=True)
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df

def China_vegetable_basket() :
    """
    菜篮子产品批发价格指数
    :return: 菜篮子产品批发价格指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00009275")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df

def China_agricultural_product():
    """
    农产品批发价格总指数
    :return: 农产品批发价格总指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00009274")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def China_agricultural_index():
    """
    农副指数
    :return: 农副指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00662543")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def China_energy_index():
    """
    能源指数
    :return: 能源指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00662539")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def China_commodity_price_index():
    """
    大宗商品价格
    :return: 大宗商品价格
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00662535")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def Global_sox_index():
    """
    费城半导体指数
    :return: 费城半导体指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00055562")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def China_yw_electronic_index():
    """
    义乌小商品指数-电子元器件
    :return: 义乌小商品指数-电子元器件
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00055551")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def China_construction_index():
    """
    建材指数
    :return: 建材指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00662541")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def China_construction_price_index():
    """
    建材价格指数
    :return: 建材价格指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00237146")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def China_lpi_index():
    """
    物流景气指数
    :return: 物流景气指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00352262")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def China_bdti_index():
    """
    原油运输指数
    :return: 原油运输指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00107668")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def China_bsi_index():
    """
    超灵便型船运价指数
    :return: 超灵便型船运价指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMI00107667")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.drop_duplicates(inplace=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df


def China_new_financial_credit():
    """
    中国-新增信贷数据
    :return: 新增信贷数据
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,RMB_LOAN,RMB_LOAN_SAME,RMB_LOAN_SEQUENTIAL,RMB_LOAN_ACCUMULATE,LOAN_ACCUMULATE_SAME",
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_RMB_LOAN",
        "p": "1",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1669047266881",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])

    temp_df.columns = ["-",
                       "月份",
                       "当月",
                       "当月-同比增长",
                       "当月-环比增长",
                       "累计",
                       "累计-同比增长"
                       ]
    temp_df = temp_df[[
        "月份",
        "当月",
        "当月-同比增长",
        "当月-环比增长",
        "累计",
        "累计-同比增长"
    ]]

    temp_df["当月"] = pd.to_numeric(temp_df["当月"], errors="coerce")
    temp_df["当月-同比增长"] = pd.to_numeric(temp_df["当月-同比增长"], errors="coerce")
    temp_df["当月-环比增长"] = pd.to_numeric(temp_df["当月-环比增长"], errors="coerce")
    temp_df["累计"] = pd.to_numeric(temp_df["累计"], errors="coerce")
    temp_df["累计-同比增长"] = pd.to_numeric(temp_df["累计-同比增长"], errors="coerce")

    return temp_df


def China_fx_gold():
    """
    东方财富-外汇和黄金储备
    :return: 外汇和黄金储备
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "columns": "REPORT_DATE,TIME,GOLD_RESERVES,GOLD_RESERVES_SAME,GOLD_RESERVES_SEQUENTIAL,FOREX,FOREX_SAME,FOREX_SEQUENTIAL",
        "pageNumber": "1",
        "pageSize": "1000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_GOLD_CURRENCY",
        "p": "1",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1660718498421",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "-",
        "月份",
        "黄金储备-数值",
        "黄金储备-同比",
        "黄金储备-环比",
        "国家外汇储备-数值",
        "国家外汇储备-同比",
        "国家外汇储备-环比",
    ]
    temp_df = temp_df[
        [
            "月份",
            "黄金储备-数值",
            "黄金储备-同比",
            "黄金储备-环比",
            "国家外汇储备-数值",
            "国家外汇储备-同比",
            "国家外汇储备-环比",
        ]
    ]
    temp_df["国家外汇储备-数值"] = pd.to_numeric(temp_df["国家外汇储备-数值"])
    temp_df["国家外汇储备-同比"] = pd.to_numeric(temp_df["国家外汇储备-同比"])
    temp_df["国家外汇储备-环比"] = pd.to_numeric(temp_df["国家外汇储备-环比"])
    temp_df["黄金储备-数值"] = pd.to_numeric(temp_df["黄金储备-数值"])
    temp_df["黄金储备-同比"] = pd.to_numeric(temp_df["黄金储备-同比"])
    temp_df["黄金储备-环比"] = pd.to_numeric(temp_df["黄金储备-环比"])
    temp_df.sort_values(["月份"], inplace=True, ignore_index=True)
    return temp_df


def China_stock_market_cap():
    """
    东方财富-全国股票交易统计表
    :return: 全国股票交易统计表
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "reportName": "RPT_ECONOMY_STOCK_STATISTICS",
        "columns": "REPORT_DATE,TIME,TOTAL_SHARES_SH,TOTAL_MARKE_SH,DEAL_AMOUNT_SH,VOLUME_SH,HIGH_INDEX_SH,LOW_INDEX_SH,TOTAL_SZARES_SZ,TOTAL_MARKE_SZ,DEAL_AMOUNT_SZ,VOLUME_SZ,HIGH_INDEX_SZ,LOW_INDEX_SZ",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageNumber": "1",
        "pageSize": "1000",
        "source": "WEB",
        "client": "WEB",
        "_": "1660718498421",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "-",
        "数据日期",
        "发行总股本-上海",
        "市价总值-上海",
        "成交金额-上海",
        "成交量-上海",
        "A股最高综合股价指数-上海",
        "A股最低综合股价指数-上海",
        "发行总股本-深圳",
        "市价总值-深圳",
        "成交金额-深圳",
        "成交量-深圳",
        "A股最高综合股价指数-深圳",
        "A股最低综合股价指数-深圳",
    ]
    temp_df = temp_df[[
        "数据日期",
        "发行总股本-上海",
        "发行总股本-深圳",
        "市价总值-上海",
        "市价总值-深圳",
        "成交金额-上海",
        "成交金额-深圳",
        "成交量-上海",
        "成交量-深圳",
        "A股最高综合股价指数-上海",
        "A股最高综合股价指数-深圳",
        "A股最低综合股价指数-上海",
        "A股最低综合股价指数-深圳",
    ]]
    temp_df["发行总股本-上海"] = pd.to_numeric(temp_df["发行总股本-上海"], errors="coerce")
    temp_df["发行总股本-深圳"] = pd.to_numeric(temp_df["发行总股本-深圳"], errors="coerce")
    temp_df["市价总值-上海"] = pd.to_numeric(temp_df["市价总值-上海"], errors="coerce")
    temp_df["市价总值-深圳"] = pd.to_numeric(temp_df["市价总值-深圳"], errors="coerce")
    temp_df["成交金额-上海"] = pd.to_numeric(temp_df["成交金额-上海"], errors="coerce")
    temp_df["成交金额-深圳"] = pd.to_numeric(temp_df["成交金额-深圳"], errors="coerce")
    temp_df["成交量-上海"] = pd.to_numeric(temp_df["成交量-上海"], errors="coerce")
    temp_df["成交量-深圳"] = pd.to_numeric(temp_df["成交量-深圳"], errors="coerce")
    temp_df["A股最高综合股价指数-上海"] = pd.to_numeric(temp_df["A股最高综合股价指数-上海"], errors="coerce")
    temp_df["A股最高综合股价指数-深圳"] = pd.to_numeric(temp_df["A股最高综合股价指数-深圳"], errors="coerce")
    temp_df["A股最低综合股价指数-上海"] = pd.to_numeric(temp_df["A股最低综合股价指数-上海"], errors="coerce")
    temp_df["A股最低综合股价指数-深圳"] = pd.to_numeric(temp_df["A股最低综合股价指数-深圳"], errors="coerce")
    return temp_df


def China_money_supply():
    """
    东方财富-货币供应量
    :return: 货币供应量
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,BASIC_CURRENCY,BASIC_CURRENCY_SAME,BASIC_CURRENCY_SEQUENTIAL,CURRENCY,CURRENCY_SAME,CURRENCY_SEQUENTIAL,FREE_CASH,FREE_CASH_SAME,FREE_CASH_SEQUENTIAL",
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_CURRENCY_SUPPLY",
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
        "月份",
        "货币和准货币(M2)-数量(亿元)",
        "货币和准货币(M2)-同比增长",
        "货币和准货币(M2)-环比增长",
        "货币(M1)-数量(亿元)",
        "货币(M1)-同比增长",
        "货币(M1)-环比增长",
        "流通中的现金(M0)-数量(亿元)",
        "流通中的现金(M0)-同比增长",
        "流通中的现金(M0)-环比增长",
    ]
    temp_df = temp_df[[
        "月份",
        "货币和准货币(M2)-数量(亿元)",
        "货币和准货币(M2)-同比增长",
        "货币和准货币(M2)-环比增长",
        "货币(M1)-数量(亿元)",
        "货币(M1)-同比增长",
        "货币(M1)-环比增长",
        "流通中的现金(M0)-数量(亿元)",
        "流通中的现金(M0)-同比增长",
        "流通中的现金(M0)-环比增长",
    ]]

    temp_df["货币和准货币(M2)-数量(亿元)"] = pd.to_numeric(temp_df["货币和准货币(M2)-数量(亿元)"])
    temp_df["货币和准货币(M2)-同比增长"] = pd.to_numeric(temp_df["货币和准货币(M2)-同比增长"])
    temp_df["货币和准货币(M2)-环比增长"] = pd.to_numeric(temp_df["货币和准货币(M2)-环比增长"])
    temp_df["货币(M1)-数量(亿元)"] = pd.to_numeric(temp_df["货币(M1)-数量(亿元)"])
    temp_df["货币(M1)-同比增长"] = pd.to_numeric(temp_df["货币(M1)-同比增长"])
    temp_df["货币(M1)-环比增长"] = pd.to_numeric(temp_df["货币(M1)-环比增长"])
    temp_df["流通中的现金(M0)-数量(亿元)"] = pd.to_numeric(temp_df["流通中的现金(M0)-数量(亿元)"])
    temp_df["流通中的现金(M0)-同比增长"] = pd.to_numeric(temp_df["流通中的现金(M0)-同比增长"])
    temp_df["流通中的现金(M0)-环比增长"] = pd.to_numeric(temp_df["流通中的现金(M0)-环比增长"])
    return temp_df


def China_CPI():
    """
    东方财富-中国居民消费价格指数
    :return: 东方财富-中国居民消费价格指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,NATIONAL_SAME,NATIONAL_BASE,NATIONAL_SEQUENTIAL,NATIONAL_ACCUMULATE,CITY_SAME,CITY_BASE,CITY_SEQUENTIAL,CITY_ACCUMULATE,RURAL_SAME,RURAL_BASE,RURAL_SEQUENTIAL,RURAL_ACCUMULATE",
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_CPI",
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
        "月份",
        "全国-同比增长",
        "全国-当月",
        "全国-环比增长",
        "全国-累计",
        "城市-同比增长",
        "城市-当月",
        "城市-环比增长",
        "城市-累计",
        "农村-同比增长",
        "农村-当月",
        "农村-环比增长",
        "农村-累计",
    ]
    temp_df = temp_df[[
        "月份",
        "全国-当月",
        "全国-同比增长",
        "全国-环比增长",
        "全国-累计",
        "城市-当月",
        "城市-同比增长",
        "城市-环比增长",
        "城市-累计",
        "农村-当月",
        "农村-同比增长",
        "农村-环比增长",
        "农村-累计",
    ]]
    temp_df["全国-当月"] = pd.to_numeric(temp_df["全国-当月"], errors="coerce")
    temp_df["全国-同比增长"] = pd.to_numeric(temp_df["全国-同比增长"], errors="coerce")
    temp_df["全国-环比增长"] = pd.to_numeric(temp_df["全国-环比增长"], errors="coerce")
    temp_df["全国-累计"] = pd.to_numeric(temp_df["全国-累计"], errors="coerce")
    temp_df["城市-当月"] = pd.to_numeric(temp_df["城市-当月"], errors="coerce")
    temp_df["城市-同比增长"] = pd.to_numeric(temp_df["城市-同比增长"], errors="coerce")
    temp_df["城市-环比增长"] = pd.to_numeric(temp_df["城市-环比增长"], errors="coerce")
    temp_df["城市-累计"] = pd.to_numeric(temp_df["城市-累计"], errors="coerce")
    temp_df["农村-当月"] = pd.to_numeric(temp_df["农村-当月"], errors="coerce")
    temp_df["农村-同比增长"] = pd.to_numeric(temp_df["农村-同比增长"], errors="coerce")
    temp_df["农村-环比增长"] = pd.to_numeric(temp_df["农村-环比增长"], errors="coerce")
    temp_df["农村-累计"] = pd.to_numeric(temp_df["农村-累计"], errors="coerce")

    return temp_df


def China_GDP():
    """
    东方财富-中国国内生产总值
    :return: 东方财富中国国内生产总值
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,DOMESTICL_PRODUCT_BASE,FIRST_PRODUCT_BASE,SECOND_PRODUCT_BASE,THIRD_PRODUCT_BASE,SUM_SAME,FIRST_SAME,SECOND_SAME,THIRD_SAME",
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_GDP",
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
        "季度",
        "国内生产总值-绝对值",
        "第一产业-绝对值",
        "第二产业-绝对值",
        "第三产业-绝对值",
        "国内生产总值-同比增长",
        "第一产业-同比增长",
        "第二产业-同比增长",
        "第三产业-同比增长",
    ]
    temp_df = temp_df[[
        "季度",
        "国内生产总值-绝对值",
        "国内生产总值-同比增长",
        "第一产业-绝对值",
        "第一产业-同比增长",
        "第二产业-绝对值",
        "第二产业-同比增长",
        "第三产业-绝对值",
        "第三产业-同比增长",
    ]]
    temp_df["国内生产总值-绝对值"] = pd.to_numeric(temp_df["国内生产总值-绝对值"], errors="coerce")
    temp_df["国内生产总值-同比增长"] = pd.to_numeric(temp_df["国内生产总值-同比增长"], errors="coerce")
    temp_df["第一产业-绝对值"] = pd.to_numeric(temp_df["第一产业-绝对值"], errors="coerce")
    temp_df["第一产业-同比增长"] = pd.to_numeric(temp_df["第一产业-同比增长"], errors="coerce")
    temp_df["第二产业-绝对值"] = pd.to_numeric(temp_df["第二产业-绝对值"], errors="coerce")
    temp_df["第二产业-同比增长"] = pd.to_numeric(temp_df["第二产业-同比增长"], errors="coerce")
    temp_df["第三产业-绝对值"] = pd.to_numeric(temp_df["第三产业-绝对值"], errors="coerce")
    temp_df["第三产业-同比增长"] = pd.to_numeric(temp_df["第三产业-同比增长"], errors="coerce")
    return temp_df


def China_PPI():
    """
    东方财富-中国工业品出厂价格指数
    :return: 东方财富中国工业品出厂价格指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,BASE,BASE_SAME,BASE_ACCUMULATE",
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_PPI",
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
        "月份",
        "当月",
        "当月同比增长",
        "累计",
    ]
    temp_df = temp_df[[
        "月份",
        "当月",
        "当月同比增长",
        "累计",
    ]]
    temp_df["当月"] = pd.to_numeric(temp_df["当月"], errors="coerce")
    temp_df["当月同比增长"] = pd.to_numeric(temp_df["当月同比增长"], errors="coerce")
    temp_df["累计"] = pd.to_numeric(temp_df["累计"], errors="coerce")
    return temp_df


def China_PMI():
    """
    东方财富-中国采购经理人指数
    :return: 东方财富中国采购经理人指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,MAKE_INDEX,MAKE_SAME,NMAKE_INDEX,NMAKE_SAME",
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_PMI",
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
        "月份",
        "制造业-指数",
        "制造业-同比增长",
        "非制造业-指数",
        "非制造业-同比增长",
    ]
    temp_df = temp_df[[
        "月份",
        "制造业-指数",
        "制造业-同比增长",
        "非制造业-指数",
        "非制造业-同比增长",
    ]]
    temp_df["制造业-指数"] = pd.to_numeric(temp_df["制造业-指数"], errors="coerce")
    temp_df["制造业-同比增长"] = pd.to_numeric(temp_df["制造业-同比增长"], errors="coerce")
    temp_df["非制造业-指数"] = pd.to_numeric(temp_df["非制造业-指数"], errors="coerce")
    temp_df["非制造业-同比增长"] = pd.to_numeric(temp_df["非制造业-同比增长"], errors="coerce")
    return temp_df


def China_gdzctz():
    """
    东方财富-中国城镇固定资产投资
    :return: 东方财富中国城镇固定资产投资
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,BASE,BASE_SAME,BASE_SEQUENTIAL,BASE_ACCUMULATE",
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_ASSET_INVEST",
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
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "自年初累计",
    ]
    temp_df = temp_df[[
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "自年初累计",
    ]]
    temp_df['当月'] = pd.to_numeric(temp_df['当月'], errors="coerce")
    temp_df['同比增长'] = pd.to_numeric(temp_df['同比增长'], errors="coerce")
    temp_df['环比增长'] = pd.to_numeric(temp_df['环比增长'], errors="coerce")
    temp_df['自年初累计'] = pd.to_numeric(temp_df['自年初累计'], errors="coerce")
    return temp_df


def China_hgjck():
    """
    东方财富-海关进出口增减情况一览表
    :return: 东方财富-海关进出口增减情况一览表
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,EXIT_BASE,IMPORT_BASE,EXIT_BASE_SAME,IMPORT_BASE_SAME,EXIT_BASE_SEQUENTIAL,IMPORT_BASE_SEQUENTIAL,EXIT_ACCUMULATE,IMPORT_ACCUMULATE,EXIT_ACCUMULATE_SAME,IMPORT_ACCUMULATE_SAME",
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_CUSTOMS",
        "p": "1",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1669047266881",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.rename(columns={
        'REPORT_DATE': "-",
        'TIME': "月份",
        'EXIT_BASE': "当月出口额-金额",
        'IMPORT_BASE': "当月进口额-金额",
        'EXIT_BASE_SAME': "当月出口额-同比增长",
        'IMPORT_BASE_SAME': "当月进口额-同比增长",
        'EXIT_BASE_SEQUENTIAL': "当月出口额-环比增长",
        'IMPORT_BASE_SEQUENTIAL': "当月进口额-环比增长",
        'EXIT_ACCUMULATE': "累计出口额-金额",
        'IMPORT_ACCUMULATE': "累计进口额-金额",
        'EXIT_ACCUMULATE_SAME': "累计出口额-同比增长",
        'IMPORT_ACCUMULATE_SAME': "累计进口额-同比增长",
    }, inplace=True)
    temp_df = temp_df[[
        "月份",
        "当月出口额-金额",
        "当月出口额-同比增长",
        "当月出口额-环比增长",
        "当月进口额-金额",
        "当月进口额-同比增长",
        "当月进口额-环比增长",
        "累计出口额-金额",
        "累计出口额-同比增长",
        "累计进口额-金额",
        "累计进口额-同比增长",
    ]]
    temp_df["当月出口额-金额"] = pd.to_numeric(temp_df["当月出口额-金额"], errors="coerce")
    temp_df["当月出口额-同比增长"] = pd.to_numeric(temp_df["当月出口额-同比增长"], errors="coerce")
    temp_df["当月出口额-环比增长"] = pd.to_numeric(temp_df["当月出口额-环比增长"], errors="coerce")
    temp_df["当月进口额-金额"] = pd.to_numeric(temp_df["当月进口额-金额"], errors="coerce")
    temp_df["当月进口额-同比增长"] = pd.to_numeric(temp_df["当月进口额-同比增长"], errors="coerce")
    temp_df["当月进口额-环比增长"] = pd.to_numeric(temp_df["当月进口额-环比增长"], errors="coerce")
    temp_df["累计出口额-金额"] = pd.to_numeric(temp_df["累计出口额-金额"], errors="coerce")
    temp_df["累计出口额-同比增长"] = pd.to_numeric(temp_df["累计出口额-同比增长"], errors="coerce")
    temp_df["累计进口额-金额"] = pd.to_numeric(temp_df["累计进口额-金额"], errors="coerce")
    temp_df["累计进口额-同比增长"] = pd.to_numeric(temp_df["累计进口额-同比增长"], errors="coerce")
    return temp_df


def China_czsr():
    """
    东方财富-财政收入
    :return: 东方财富-财政收入
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,BASE,BASE_SAME,BASE_SEQUENTIAL,BASE_ACCUMULATE,ACCUMULATE_SAME",
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_INCOME",
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
        "月份",
        "当月",
        "当月-同比增长",
        "当月-环比增长",
        "累计",
        "累计-同比增长",
    ]
    temp_df = temp_df[[
        "月份",
        "当月",
        "当月-同比增长",
        "当月-环比增长",
        "累计",
        "累计-同比增长",
    ]]
    temp_df['当月'] = pd.to_numeric(temp_df['当月'], errors="coerce")
    temp_df['当月-同比增长'] = pd.to_numeric(temp_df['当月-同比增长'], errors="coerce")
    temp_df['当月-环比增长'] = pd.to_numeric(temp_df['当月-环比增长'], errors="coerce")
    temp_df['累计'] = pd.to_numeric(temp_df['累计'], errors="coerce")
    temp_df['累计-同比增长'] = pd.to_numeric(temp_df['累计-同比增长'], errors="coerce")

    return temp_df


def China_whxd():
    """
    东方财富-外汇贷款数据
    :return: 东方财富-外汇贷款数据
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,BASE,BASE_SAME,BASE_SEQUENTIAL,BASE_ACCUMULATE",
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_FOREX_LOAN",
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
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "累计",
    ]
    temp_df = temp_df[[
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "累计",
    ]]
    temp_df['当月'] = pd.to_numeric(temp_df['当月'], errors="coerce")
    temp_df['同比增长'] = pd.to_numeric(temp_df['同比增长'], errors="coerce")
    temp_df['环比增长'] = pd.to_numeric(temp_df['环比增长'], errors="coerce")
    temp_df['累计'] = pd.to_numeric(temp_df['累计'], errors="coerce")
    return temp_df

def China_wbck():
    """
    东方财富-本外币存款
    :return: 东方财富-本外币存款
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,BASE,BASE_SAME,BASE_SEQUENTIAL,BASE_ACCUMULATE",
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_FOREX_DEPOSIT",
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
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "累计",
    ]
    temp_df = temp_df[[
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "累计",
    ]]
    temp_df['当月'] = pd.to_numeric(temp_df['当月'], errors="coerce")
    temp_df['同比增长'] = pd.to_numeric(temp_df['同比增长'], errors="coerce")
    temp_df['环比增长'] = pd.to_numeric(temp_df['环比增长'], errors="coerce")
    temp_df['累计'] = pd.to_numeric(temp_df['累计'], errors="coerce")

    return temp_df

def China_xfzxx():
    """
    东方财富网-经济数据一览-消费者信心指数
    :return: 消费者信心指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,TIME,CONSUMERS_FAITH_INDEX,FAITH_INDEX_SAME,FAITH_INDEX_SEQUENTIAL,CONSUMERS_ASTIS_INDEX,ASTIS_INDEX_SAME,ASTIS_INDEX_SEQUENTIAL,CONSUMERS_EXPECT_INDEX,EXPECT_INDEX_SAME,EXPECT_INDEX_SEQUENTIAL",
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_FAITH_INDEX",
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
        "月份",
        "消费者信心指数-指数值",
        "消费者信心指数-同比增长",
        "消费者信心指数-环比增长",
        "消费者满意指数-指数值",
        "消费者满意指数-同比增长",
        "消费者满意指数-环比增长",
        "消费者预期指数-指数值",
        "消费者预期指数-同比增长",
        "消费者预期指数-环比增长",
    ]
    temp_df = temp_df[[
        "月份",
        "消费者信心指数-指数值",
        "消费者信心指数-同比增长",
        "消费者信心指数-环比增长",
        "消费者满意指数-指数值",
        "消费者满意指数-同比增长",
        "消费者满意指数-环比增长",
        "消费者预期指数-指数值",
        "消费者预期指数-同比增长",
        "消费者预期指数-环比增长",
    ]]

    temp_df["消费者信心指数-指数值"] = pd.to_numeric(temp_df["消费者信心指数-指数值"], errors="coerce")
    temp_df["消费者信心指数-同比增长"] = pd.to_numeric(temp_df["消费者信心指数-同比增长"], errors="coerce")
    temp_df["消费者信心指数-环比增长"] = pd.to_numeric(temp_df["消费者信心指数-环比增长"], errors="coerce")
    temp_df["消费者满意指数-指数值"] = pd.to_numeric(temp_df["消费者满意指数-指数值"], errors="coerce")
    temp_df["消费者满意指数-同比增长"] = pd.to_numeric(temp_df["消费者满意指数-同比增长"], errors="coerce")
    temp_df["消费者满意指数-环比增长"] = pd.to_numeric(temp_df["消费者满意指数-环比增长"], errors="coerce")
    temp_df["消费者预期指数-指数值"] = pd.to_numeric(temp_df["消费者满意指数-指数值"], errors="coerce")
    temp_df["消费者预期指数-同比增长"] = pd.to_numeric(temp_df["消费者预期指数-同比增长"], errors="coerce")
    temp_df["消费者预期指数-环比增长"] = pd.to_numeric(temp_df["消费者预期指数-环比增长"], errors="coerce")
    return temp_df

def China_reserve_requirement_ratio():
    """
    存款准备金率
    :return: 存款准备金率
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    params = {
        "columns": "REPORT_DATE,PUBLISH_DATE,TRADE_DATE,INTEREST_RATE_BB,INTEREST_RATE_BA,CHANGE_RATE_B,INTEREST_RATE_SB,INTEREST_RATE_SA,CHANGE_RATE_S,NEXT_SH_RATE,NEXT_SZ_RATE,REMARK",
        "pageNumber": "1",
        "pageSize": "2000",
        "sortColumns": "PUBLISH_DATE,TRADE_DATE",
        "sortTypes": "-1,-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_DEPOSIT_RESERVE",
        "p": "1",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1669047266881",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = ["-",
                       "公布时间",
                       "生效时间",
                       "大型金融机构-调整前",
                       "大型金融机构-调整后",
                       "大型金融机构-调整幅度",
                       "中小金融机构-调整前",
                       "中小金融机构-调整后",
                       "中小金融机构-调整幅度",
                       "消息公布次日指数涨跌-上证",
                       "消息公布次日指数涨跌-深证",
                       "备注",
                       ]
    temp_df = temp_df[[
        "公布时间",
        "生效时间",
        "大型金融机构-调整前",
        "大型金融机构-调整后",
        "大型金融机构-调整幅度",
        "中小金融机构-调整前",
        "中小金融机构-调整后",
        "中小金融机构-调整幅度",
        "消息公布次日指数涨跌-上证",
        "消息公布次日指数涨跌-深证",
        "备注",
    ]]
    temp_df['大型金融机构-调整前'] = pd.to_numeric(temp_df['大型金融机构-调整前'], errors="coerce")
    temp_df['大型金融机构-调整后'] = pd.to_numeric(temp_df['大型金融机构-调整后'], errors="coerce")
    temp_df['大型金融机构-调整幅度'] = pd.to_numeric(temp_df['大型金融机构-调整幅度'], errors="coerce")
    temp_df['大型金融机构-调整前'] = pd.to_numeric(temp_df['大型金融机构-调整前'], errors="coerce")
    temp_df['大型金融机构-调整后'] = pd.to_numeric(temp_df['大型金融机构-调整后'], errors="coerce")
    temp_df['大型金融机构-调整幅度'] = pd.to_numeric(temp_df['大型金融机构-调整幅度'], errors="coerce")
    temp_df['消息公布次日指数涨跌-上证'] = pd.to_numeric(temp_df['消息公布次日指数涨跌-上证'], errors="coerce")
    temp_df['消息公布次日指数涨跌-深证'] = pd.to_numeric(temp_df['消息公布次日指数涨跌-深证'], errors="coerce")
    temp_df['消息公布次日指数涨跌-深证'] = pd.to_numeric(temp_df['消息公布次日指数涨跌-深证'], errors="coerce")
    return temp_df

def China_consumer_goods_retail():
    """
    东方财富-经济数据-社会消费品零售总额
    :return: 社会消费品零售总额
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "columns": "REPORT_DATE,TIME,RETAIL_TOTAL,RETAIL_TOTAL_SAME,RETAIL_TOTAL_SEQUENTIAL,RETAIL_TOTAL_ACCUMULATE,RETAIL_ACCUMULATE_SAME",
        "pageNumber": "1",
        "pageSize": "1000",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": "RPT_ECONOMY_TOTAL_RETAIL",
        "p": "1",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1660718498421",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["result"]["data"])
    temp_df.columns = [
        "-",
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "累计",
        "累计-同比增长",
    ]
    temp_df = temp_df[[
        "月份",
        "当月",
        "同比增长",
        "环比增长",
        "累计",
        "累计-同比增长",
    ]]
    temp_df["当月"] = pd.to_numeric(temp_df["当月"], errors="coerce")
    temp_df["同比增长"] = pd.to_numeric(temp_df["同比增长"], errors="coerce")
    temp_df["环比增长"] = pd.to_numeric(temp_df["环比增长"], errors="coerce")
    temp_df["累计"] = pd.to_numeric(temp_df["累计"], errors="coerce")
    temp_df["累计-同比增长"] = pd.to_numeric(temp_df["累计-同比增长"], errors="coerce")
    return temp_df

def China_society_electricity():
    """
    新浪财经-中国宏观经济数据-全社会用电分类情况表
    :return: 全社会用电分类情况表
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['sina']+cs.URL_PARA['society_electricity']
    params = {
        "cate": "industry",
        "event": "6",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601557771972",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in range(1, page_num):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)

    big_df.columns = [
        "统计时间",
        "全社会用电量",
        "全社会用电量同比",
        "各行业用电量合计",
        "各行业用电量合计同比",
        "第一产业用电量",
        "第一产业用电量同比",
        "第二产业用电量",
        "第二产业用电量同比",
        "第三产业用电量",
        "第三产业用电量同比",
        "城乡居民生活用电量合计",
        "城乡居民生活用电量合计同比",
        "城镇居民用电量",
        "城镇居民用电量同比",
        "乡村居民用电量",
        "乡村居民用电量同比",
    ]
    return big_df

def China_society_traffic_volume():
    """
    新浪财经-中国宏观经济数据-全社会客货运输量
    :return: 全社会客货运输量
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['sina']+cs.URL_PARA['society_traffic_volume']
    params = {
        "cate": "industry",
        "event": "10",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601557771972",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"]["非累计"])
    for i in tqdm(range(1, page_num), leave=False):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"]["非累计"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df

def China_postal_telecommunicational():
    """
    新浪财经-中国宏观经济数据-邮电业务基本情况
    :return: 邮电业务基本情况
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['sina']+cs.URL_PARA['postal_telecommunicational']
    params = {
        "cate": "industry",
        "event": "11",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"]["非累计"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"]["非累计"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    for item in big_df.columns[1:]:
        big_df[item] = pd.to_numeric(big_df[item], errors="coerce")
    return big_df

def China_international_tourism_fx():
    """
    新浪财经-中国宏观经济数据-国际旅游外汇收入构成
    :return: 国际旅游外汇收入构成
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['sina']+cs.URL_PARA['international_tourism_fx']
    params = {
        "cate": "industry",
        "event": "15",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df

def China_passenger_load_factor():
    """
    新浪财经-中国宏观经济数据-民航客座率及载运率
    :return: 民航客座率及载运率
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['sina']+cs.URL_PARA['passenger_load_factor']
    params = {
        "cate": "industry",
        "event": "20",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df

def China_freight_index():
    """
    新浪财经-中国宏观经济数据-航贸运价指数
    :return: 航贸运价指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http']+cs.URL_DIC['sina']+cs.URL_PARA['freight_index']
    params = {
        "cate": "industry",
        "event": "22",
        "from": "0",
        "num": 5000,
        "condition": "",
    }
    r = requests.get(url, params=params)
    columns_list = r.content.decode("gbk").split("\n")[2].split(", ")
    columns_list = [item.strip() for item in columns_list]
    content_list = r.content.decode("gbk").split("\n")[3:]
    big_df = (
        pd.DataFrame([item.split(", ") for item in content_list], columns=columns_list)
        .dropna(axis=1, how="all")
        .dropna(axis=0)
        .iloc[:, :-1]
    )
    big_df["波罗的海好望角型船运价指数BCI"] = pd.to_numeric(big_df["波罗的海好望角型船运价指数BCI"])
    big_df["灵便型船综合运价指数BHMI"] = pd.to_numeric(big_df["灵便型船综合运价指数BHMI"])
    big_df["波罗的海超级大灵便型船BSI指数"] = pd.to_numeric(big_df["波罗的海超级大灵便型船BSI指数"])
    big_df["波罗的海综合运价指数BDI"] = pd.to_numeric(big_df["波罗的海综合运价指数BDI"])
    big_df["HRCI国际集装箱租船指数"] = pd.to_numeric(big_df["HRCI国际集装箱租船指数"])
    big_df["油轮运价指数成品油运价指数BCTI"] = pd.to_numeric(big_df["油轮运价指数成品油运价指数BCTI"])
    big_df["油轮运价指数原油运价指数BDTI"] = pd.to_numeric(big_df["油轮运价指数原油运价指数BDTI"])
    return big_df

def China_central_bank_balance():
    """
    新浪财经-中国宏观经济数据-央行货币当局资产负债
    :return: 央行货币当局资产负债
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http']+cs.URL_DIC['sina']+cs.URL_PARA['central_bank_balance']
    params = {
        "cate": "fininfo",
        "event": "8",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df

def China_insurance():
    """
    新浪财经-中国宏观经济数据-保险业经营情况
    :return: 保险业经营情况
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http']+cs.URL_DIC['sina']+cs.URL_PARA['insurance']
    params = {
        "cate": "fininfo",
        "event": "19",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df

def China_supply_of_money():
    """
    新浪财经-中国宏观经济数据-货币供应量
    :return: 货币供应量
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http']+cs.URL_DIC['sina']+cs.URL_PARA['supply_of_money']
    params = {
        "cate": "fininfo",
        "event": "1",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df

def China_swap_rate(
    start_date: str = "20221027", end_date: str = "20221127"
):
    """
    FR007利率互换曲线历史数据; 只能获取近一年的数据
    :param start_date: 开始日期, 开始和结束日期不得超过一个月
    :type start_date: str
    :param end_date: 结束日期, 开始和结束日期不得超过一个月
    :type end_date: str
    :return: FR007利率互换曲线历史数据
    :rtype: pandas.DataFrame
    """
    start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = cs.URL_TYPE['https']+cs.URL_DIC['chinamoney']+cs.URL_PARA['swap_rate']
    params = {
        "cfgItemType": "72",
        "interestRateType": "0",
        "startDate": start_date,
        "endDate": end_date,
        "bidAskType": "",
        "lang": "CN",
        "quoteTime": "全部",
        "pageSize": "5000",
        "pageNum": "1",
    }
    headers = cs.HEADERS['chinamoney']
    r = requests.post(url, data=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    temp_df.columns = [
        "日期",
        "_",
        "_",
        "时刻",
        "_",
        "_",
        "_",
        "_",
        "_",
        "价格类型",
        "_",
        "曲线名称",
        "_",
        "_",
        "_",
        "_",
        "data",
    ]
    price_df = pd.DataFrame([item for item in temp_df["data"]])
    price_df.columns = [
        "1M",
        "3M",
        "6M",
        "9M",
        "1Y",
        "2Y",
        "3Y",
        "4Y",
        "5Y",
        "7Y",
        "10Y",
    ]
    big_df = pd.concat([temp_df, price_df], axis=1)
    big_df = big_df[
        [
            "日期",
            "曲线名称",
            "时刻",
            "价格类型",
            "1M",
            "3M",
            "6M",
            "9M",
            "1Y",
            "2Y",
            "3Y",
            "4Y",
            "5Y",
            "7Y",
            "10Y",
        ]
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["1M"] = pd.to_numeric(big_df["1M"], errors="coerce")
    big_df["3M"] = pd.to_numeric(big_df["3M"], errors="coerce")
    big_df["6M"] = pd.to_numeric(big_df["6M"], errors="coerce")
    big_df["9M"] = pd.to_numeric(big_df["9M"], errors="coerce")
    big_df["1Y"] = pd.to_numeric(big_df["1Y"], errors="coerce")
    big_df["2Y"] = pd.to_numeric(big_df["2Y"], errors="coerce")
    big_df["3Y"] = pd.to_numeric(big_df["3Y"], errors="coerce")
    big_df["4Y"] = pd.to_numeric(big_df["4Y"], errors="coerce")
    big_df["5Y"] = pd.to_numeric(big_df["5Y"], errors="coerce")
    big_df["7Y"] = pd.to_numeric(big_df["7Y"], errors="coerce")
    big_df["10Y"] = pd.to_numeric(big_df["10Y"], errors="coerce")
    return big_df

def China_foreign_exchange_gold():
    """
    央行黄金和外汇储备
    :return: 央行黄金和外汇储备
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http']+cs.URL_DIC['sina']+cs.URL_PARA['foreign_exchange_gold']
    params = {
        "cate": "fininfo",
        "event": "5",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df

def China_retail_price_index():
    """
    商品零售价格指数
    :return: 商品零售价格指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['http']+cs.URL_DIC['sina']+cs.URL_PARA['retail_price_index']
    params = {
        "cate": "price",
        "event": "12",
        "from": "0",
        "num": "31",
        "condition": "",
        "_": "1601624495046",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -3])
    page_num = math.ceil(int(data_json["count"]) / 31)
    big_df = pd.DataFrame(data_json["data"])
    for i in tqdm(range(1, page_num)):
        params.update({"from": i * 31})
        r = requests.get(url, params=params)
        data_text = r.text
        data_json = demjson.decode(data_text[data_text.find("{") : -3])
        temp_df = pd.DataFrame(data_json["data"])
        big_df = big_df.append(temp_df, ignore_index=True)
    big_df.columns = [item[1] for item in data_json["config"]["all"]]
    return big_df

def China_real_estate():
    """
    国房景气指数
    :return: 国房景气指数
    :rtype: pandas.DataFrame
    """
    url = cs.URL_TYPE['https']+cs.URL_DIC['eastmoney']+cs.URL_PARA['eastmoney']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    params = {
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "pageSize": "1000",
        "pageNumber": "1",
        "reportName": "RPT_INDUSTRY_INDEX",
        "columns": "REPORT_DATE,INDICATOR_VALUE,CHANGE_RATE,CHANGERATE_3M,CHANGERATE_6M,CHANGERATE_1Y,CHANGERATE_2Y,CHANGERATE_3Y",
        "filter": '(INDICATOR_ID="EMM00121987")',
        "source": "WEB",
        "client": "WEB",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_page + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.columns = [
        "日期",
        "最新值",
        "涨跌幅",
        "近3月涨跌幅",
        "近6月涨跌幅",
        "近1年涨跌幅",
        "近2年涨跌幅",
        "近3年涨跌幅",
    ]
    big_df["日期"] = pd.to_datetime(big_df["日期"]).dt.date
    big_df["最新值"] = pd.to_numeric(big_df["最新值"])
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["近3月涨跌幅"] = pd.to_numeric(big_df["近3月涨跌幅"])
    big_df["近6月涨跌幅"] = pd.to_numeric(big_df["近6月涨跌幅"])
    big_df["近1年涨跌幅"] = pd.to_numeric(big_df["近1年涨跌幅"])
    big_df["近2年涨跌幅"] = pd.to_numeric(big_df["近2年涨跌幅"])
    big_df["近3年涨跌幅"] = pd.to_numeric(big_df["近3年涨跌幅"])
    big_df.sort_values(["日期"], inplace=True)
    big_df.drop_duplicates(inplace=True)
    big_df.reset_index(inplace=True, drop=True)
    return big_df