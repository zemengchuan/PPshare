import pandas as pd
import PPshare.article.cons as cs


def article_epu_index(index="China"):
    """
    经济政策不确定性指数
    :param index: 指定的国家名称, e.g. “China”
    :type index: str
    :return: 指定 index 的数据
    :rtype: pandas.DataFrame
    """
    if index == "China New":
        index = "China"
    if index == "USA":
        index = "US"
    if index == "Hong Kong":
        index = "HK"
        epu_df = pd.read_excel(cs.URL_TYPE['http'] + cs.URL_DIC['policy'] +
                               cs.URL_PARA['EPU_Data'].format(index),
                               engine="openpyxl")
        return epu_df
    if index in ["Germany", "France", "Italy"]:  # 欧洲
        index = "Europe"
    if index == "South Korea":
        index = "Korea"
    if index == "Spain New":
        index = "Spain"
    if index in [
            "Ireland", "Chile", "Colombia", "Netherlands", "Singapore",
            "Sweden"
    ]:
        epu_df = pd.read_excel(cs.URL_TYPE['http'] + cs.URL_DIC['policy'] +
                               cs.URL_PARA['Uncertainty'].format(index),
                               engine="openpyxl")
        return epu_df
    if index == "Greece":
        epu_df = pd.read_excel(cs.URL_TYPE['http'] + cs.URL_DIC['policy'] +
                               cs.URL_PARA['FKT'].format(index),
                               engine="openpyxl")
        return epu_df
    url = cs.URL_TYPE['http'] + cs.URL_DIC['policy'] + cs.URL_PARA[
        'Default'].format(index)
    epu_df = pd.read_csv(url)
    return epu_df


if __name__ == "__main__":
    article_epu_index_df = article_epu_index(index="Greece")
    print(article_epu_index_df)