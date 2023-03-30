from PPshare.stock.macro.eastmoney import *
from PPshare.util.text import paramter_wrong


def get_chinbor(period='ON'):
    """
    获取中国银行同业间拆借市场数据（chinbor）
    Parameters
    ------
    period:{
        'ON':'隔夜',
        '1W':'1周',
        '2W':'2周',
        '3W':'3周',
        '1M':'1月',
        '2M':'2月'
        '3M':'3月',
        '4M':'4月',
        '6M':'6月',
        '9M':'9月',
        '1Y':'1年',
    }
    """
    return get_bor(market_code='002', curr_type='CNY', period=period)


def get_libor(curr_type='USD', period='ON'):
    """
    获取伦敦银行同业间拆借市场数据（Libor）
    Parameters
    ------
    curr_type:{
        'USD':'美元',
        'GBP':'英镑',
        'JPY':'日元',
        'EUR':'欧元'
    }
    period:{
        'ON':'隔夜',
        '1W':'1周',
        '1M':'1月',
        '2M':'2月'
        '3M':'3月',
        '8M':'8月',
    }
    """
    if curr_type not in ['USD', 'GBP', 'JPY', 'EUR']:
        raise Exception(paramter_wrong("curr_type"))
    return get_bor(market_code='003', curr_type=curr_type, period=period)


def get_euribor(period='ON'):
    """
    获取欧洲银行同业间拆借市场数据（eurinbor）
    Parameters
    ------
    period:{
        'ON':'隔夜',
        '1W':'1周',
        '2W':'2周',
        '3W':'3周',
        '1M':'1月',
        '2M':'2月'
        '3M':'3月',
        '4M':'4月',
        '5M':'5月',
        '6M':'6月',
        '7M':'7月',
        '8M':'8月',
        '9M':'9月',
        '10M':'10月',
        '11M':'11月',
        '1Y':'1年',
    }
    """
    return get_bor(market_code='004', curr_type='EUR', period=period)


def get_hibor(curr_type='USD', period='ON'):
    """
    获取香港银行同业间拆借市场数据（hibor）
    Parameters
    ------
    curr_type:{
        'CNH':'人民币',
        'HKD':'港币',
        'USD':'美元'
    }
    period:{
        'ON':'隔夜',
        '1W':'1周',
        '2W':'2周',
        '1M':'1月',
        '2M':'2月'
        '3M':'3月',
        '4M':'4月',
        '6M':'6月',
        '9M':'9月',
        '1Y':'1年',
    }
    """
    if curr_type not in ['CNH', 'HKD', 'USD']:
        raise Exception(paramter_wrong("curr_type"))
    return get_bor(market_code='005', curr_type=curr_type, period=period)


def get_sibor(curr_type='USD', period='1M'):
    """
    获取新加坡银行同业间拆借市场数据（sibor）
    Parameters
    ------
    curr_type：{
        'SGD':'星元',
        'USD':'美元'
    }
    period:{
        '1M':'1月',
        '2M':'2月'
        '3M':'3月',
        '6M':'6月',
        '9M':'9月',
        '1Y':'1年',
    }
    """
    if curr_type not in ['SGD', 'USD']:
        raise Exception(paramter_wrong("curr_type"))
    return get_bor(market_code='006', curr_type=curr_type, period=period)


if __name__ == '__main__':
    # print(get_chinbor(period='1M'))
    # print(get_libor(curr_type='USD', period='1M'))
    # print(get_hibor(curr_type='CNH', period='6M'))
    # print(get_euribor(period='1Y'))
    print(get_sibor(curr_type='USD', period='2M'))
