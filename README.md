# Market Watch

你好，我是[Mercer@Zhihu](https://www.zhihu.com/people/daleige). 

为了更方便地分享我在知乎写作时用到的数据，以及让更多的人可以加入到经济分析的活动中来，增加合作的可能性，我开通了这个GitHub项目。特别希望可以为经管类学生和研究员提供便捷的获取数据的渠道。

在项目的初始阶段，我会以搭建数据源与数据面板为主，并按类别分别搭建各自的模块。如果你有兴趣加入，请在知乎私信我。合作的方式有：
- 发现数据源，总结背景知识
- 搭建数据库代码
- 基于market-watch数据发布应用类分析，优质内容可以发表在知乎market-watch专栏
- 搭建数据与分析的可视化应用

## 数据源汇总

### 宏观经济数据（`macro-watch`）
- [美国劳工部](https://www.bls.gov/bls/newsrels.htm#major)：就业、通胀等数据
- [美国经济分析局](https://www.bea.gov/data)：产出与居民收入核算(NIPA)
- [美联储Flow of Funds](https://www.federalreserve.gov/releases/z1)：美国经济参与者们资产负债表的全貌

### 美联储数据（`fed-watch`）
- 美联储数据表: 
  - H.4.1：M1货币供给渠道与央行资产负债表信息
  - H.6：广义货币供给
  - H.8：商业银行资产负债表
  - H.15：利率
  - G.19：消费者信贷，见专栏文章[【数据拾遗：消费者信贷】](https://zhuanlan.zhihu.com/p/526754098)
- [美联储纽约分行数据库](https://www.newyorkfed.org/markets/data-hub)
  - 各类短期利率
  - 资产负债表SOMA数据
  - 公开市场操作数据
  - 大型券商持仓与融资数据
- [美联储圣路易斯分行数据库(FRED)](https://fred.stlouisfed.org/)，以Python库[`fredapi`](https://github.com/mortada/fredapi)为基础，主要作为搭建其他数据库与分析的快捷通道
  
### 美国财政部数据 (`treasury-watch`)
- [美债拍卖细节](https://www.treasurydirect.gov/instit/annceresult/annceresult.htm)：见专栏文章[【数据拾遗：美债拍卖细节】](https://zhuanlan.zhihu.com/p/514668515)
- [美债拍卖的投资者分布数据](https://home.treasury.gov/data/investor-class-auction-allotments)：见专栏文章[【数据拾遗：美债拍卖数据2】](https://zhuanlan.zhihu.com/p/516037009)
- [美国财政收支日频数据](https://fiscal.treasury.gov/reports-statements/dts/index.html)
- [财政收支月度总结](https://fiscal.treasury.gov/reports-statements/mts/#:~:text=The%20Monthly%20Treasury%20Statement%20summarizes,Budget%20of%20the%20U.S.%20Government.&text=The%20MTS%20presents%20a%20summary,Surplus%20or%20deficit)

### 利率数据（`rates-watch`）
- [财政部利率曲线](https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics)：包含名义国债收益率曲线，真实收益率（五年以上），国库券利率等，见专栏文章[【数据拾遗：美债官方利率数据】](https://www.zhihu.com/column/c_1509153964662263808)
- [纽约联储回购利率指数](https://www.newyorkfed.org/markets/data-hub)：详见[【漫谈缩表：美国的回购市场】](https://zhuanlan.zhihu.com/p/463721684)

### 大宗商品与期货数据（`futures-watch`）

- [CFTC](https://www.cftc.gov/MarketReports/index.htm)

### [世界银行数据库](https://data.worldbank.org/)
- [World Development Indicators](https://datatopics.worldbank.org/world-development-indicators/)
- [Debt Statistics](https://www.worldbank.org/en/programs/debt-statistics/statistics)
- [DataBank](https://databank.worldbank.org/home.aspx)
- [API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structure)
