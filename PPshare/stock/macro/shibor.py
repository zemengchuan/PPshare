import pandas as pd
import datetime
import PPshare.stock.macro.cons as cs


def shibor(mode='data', start_date=None, end_date=datetime.date.today()):
    """
    获取上海银行间同业拆放利率（Shibor）：data
    shibor报价数据：quote
    shibor均值数据：avg
    Parameters
    ------
    start_year:起始年份(%Y-%M-%D)
    end_year:截止年份(%Y-%M-%D)
    Return
    ------
    date:日期
    ON:隔夜拆放利率
    1W:1周拆放利率
    2W:2周拆放利率
    1M:1个月拆放利率
    3M:3个月拆放利率
    6M:6个月拆放利率
    9M:9个月拆放利率
    1Y:1年拆放利率
    """
    url = cs.URL_TYPE['https'] + cs.URL_DIC['shibor'] + cs.URL_PARA[mode]
    if type(end_date) != datetime.date:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    if not start_date:
        start_date = end_date - datetime.timedelta(days=364)
    else:
        if type(start_date) != datetime.date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    df = pd.read_excel(url.format(start_date, end_date))[:-2]
    return df


def LPR(start_date=None, end_date=datetime.date.today()):
    """
    获取贷款基础利率（LPR）
    Parameters
    ------
    start_year:起始年份(%Y-%M-%D)
    end_year:截止年份(%Y-%M-%D)
    Return
    ------
    date:日期
    1Y:1年贷款利率
    5Y:5年贷款利率
    """
    url = cs.URL_TYPE['https'] + cs.URL_DIC['LPR'] + cs.URL_PARA['LPR']
    if type(end_date) != datetime.date:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    if not start_date:
        start_date = end_date - datetime.timedelta(days=364)
    else:
        if type(start_date) != datetime.date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    df = pd.read_excel(url.format(start_date, end_date))[:-2]
    return df


if __name__ == '__main__':
    # print(shibor('data'))
    # print(shibor('queto'))
    # print(shibor('avg'))
    print(shibor(mode='data',end_date='2007-01-01'))
    print(LPR(start_date='2013-10-01',end_date='2014-9-30'))