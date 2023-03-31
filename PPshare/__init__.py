"""
获取上海银行间同业拆放利率（Shibor）
贷款基础利率（LPR）
"""
from PPshare.stock.macro.shibor import (shibor, LPR)
"""
获取中国银行同业间拆借市场数据（chinbor）
伦敦银行同业间拆借市场数据（Libor）
香港银行同业间拆借市场数据（hibor）
欧洲银行同业间拆借市场数据（euribor）
新加坡银行同业间拆借市场数据（sibor）
"""
from PPshare.stock.macro.bor import (get_chinbor, get_euribor,
                                            get_hibor, get_libor, get_sibor)
"""
全球宏观-中国宏观
"""
from PPshare.stock.macro.macro_china import *
"""
金十数据中心-外汇情绪
"""
from PPshare.stock.macro.macro_other import macro_fx_sentiment
"""
金十数据中心-经济指标-欧元区
"""
from PPshare.stock.macro.macro_euro import *
"""
金十数据中心-经济指标-央行利率-主要央行利率
"""
from PPshare.stock.macro.macro_bank import *
"""
中国宏观杠杆率数据
"""
from PPshare.stock.macro.macro_cnbs import macro_cnbs
"""
宏观-加拿大
"""
from PPshare.stock.macro.macro_canada import *
"""
宏观-澳大利亚
"""
from PPshare.stock.macro.macro_australia import *
"""
英国-宏观
"""
from PPshare.stock.macro.macro_uk import *
"""
日本-宏观
"""
from PPshare.stock.macro.macro_japan import *
"""
瑞士-宏观
"""
from PPshare.stock.macro.macro_swiss import *
"""
全球宏观-机构宏观
"""
from PPshare.stock.macro.macro_constitute import *
"""
全球宏观-美国宏观
"""
from PPshare.stock.macro.macro_usa import *
"""
德国-经济指标
"""
from PPshare.stock.macro.macro_germany import *

from PPshare.util.function import get_methods

from PPshare.article.epu import article_epu_index