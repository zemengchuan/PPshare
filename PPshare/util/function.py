import PPshare as pp
from fuzzywuzzy import process
import pandas as pd
import os


# 封装用户输入部分的代码
def get_user_input(limit):
    while True:
        num = input('请选择需要调用的函数编号：（不调用则填quit）')
        if num == 'quit':
            return None
        elif num.isdigit() and int(num) < limit:
            return int(num)
        else:
            print("输入不正确，请重新输入")


# 将print语句改为返回值
def get_methods(describe, limit=5):
    # 读取Excel文件
    with pd.ExcelFile(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'info.xlsx')) as xls:
        df = pd.read_excel(xls, 'Sheet1')
    describes = df['describe']
    results = process.extract(describe,
                              describes,
                              scorer=process.fuzz.token_sort_ratio,
                              limit=limit)
    if not results:
        return None
    else:
        methods = []
        result_str = "您希望获取的数据有可能是:\n"
        for result_num in range(len(results)):
            result = results[result_num]
            method = df.loc[df['describe'] == result[0], 'method'].values[0]
            methods.append(method)
            result_str += f"{result_num}\t\"{result[0]}\"，其调用方法为{method}\n"
        print(result_str)
        num = get_user_input(len(results))
        if num is None:
            return None
        else:
            print(f"\n您选择的数据是:“{results[num][0]}”")
            return [eval(f"pp.{methods[num]}")()]


if __name__ == '__main__':
    x = get_methods("商品价格指数")
    print(x)
