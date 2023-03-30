import re
import pandas as pd

with open('./README.md','r',encoding='utf-8')as f:
    full_text = f.read()

name_ls = re.findall(r'#{3,5} (.*?)\n\n接口', full_text,re.S)
name_new_ls = []
for name in name_ls:
    if '#' in name:
        result = name.split("#")[-1]
    else:
        result = name.strip().replace("*","")
    name_new_ls.append(result)
method_ls = [x.strip() for x in re.findall(r'接口:(.*?)\n?\n\n描述', full_text,re.S)]
method_new_ls = []
for method in method_ls:
    if '(' in method:
        result = ''
        for j in method:
            if j== '(':
                break
            result+=j
    else:
        result = method
    method_new_ls.append(result)
dic = {
    'describe':name_new_ls,
    'method':method_new_ls
}
df = pd.DataFrame(dic)
df.to_excel('info.xlsx')