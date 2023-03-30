def get_easy_data_1(market_code, curr_type, num, page):
    params = {
        'reportName':
        'RPT_IMP_INTRESTRATEN',
        'columns':
        'REPORT_DATE,REPORT_PERIOD,IR_RATE,CHANGE_RATE,INDICATOR_ID,LATEST_RECORD,MARKET,MARKET_CODE,CURRENCY,CURRENCY_CODE',
        'filter':
        '(MARKET_CODE="{}")(CURRENCY_CODE="{}")(INDICATOR_ID="{}")'.format(
            market_code, curr_type, num),
        'pageNumber':
        page,
        'pageSize':
        '500',
        'sortTypes':
        '-1',
        'sortColumns':
        'REPORT_DATE',
        'p':
        page,
        'pageNo':
        page,
        'pageNum':
        page,
    }
    return params

def get_easy_data_2(reportName,columns):
    params = {
        "columns": columns,
        "pageNumber": "1",
        "pageSize": "200",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "WEB",
        "client": "WEB",
        "reportName": reportName,
        "p": "1",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1669047266881",
    }
    return params

def eastmoney(param_mode=0):
    if param_mode:
        return get_easy_data_1
    else:
        return get_easy_data_2

def jin10(category,attr_id,t):
    params={
        "max_date": "",
        "category": category,
        "attr_id": attr_id,
        "_": str(int(round(t * 1000))),
    }
    return params