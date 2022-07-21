# Market Watch

Hey I'm [Mercer@Zhihu](https://www.zhihu.com/people/daleige). 

为了更方便地分享我在知乎写作时用到的数据，以及让更多的人可以加入到经济分析的活动中来，增加合作的可能性，我开通了这个GitHub项目。如果你有兴趣加入，对项目作出贡献，或者单纯为了获取相关数据，请在知乎私信我。

在项目的初始阶段，我会以搭建数据源与数据面板为主，并按类别分别搭建各自的模块：

### 宏观经济数据（`macro-watch`）
- [Bureau of Labor Statistics](https://www.bls.gov/bls/newsrels.htm#major)：就业、通胀等数据
- [Bureau of Economic Analysis](https://www.bea.gov/data)：产出与居民收入核算(NIPA)
- [Federael Reserve Board Flow of Funds](https://www.federalreserve.gov/releases/z1)：美国经济参与者们资产负债表的全貌

### 美联储数据（`fed-watch`）
- Federal Reserve Board Tables: 
  - H.4.1：M1货币供给渠道与央行资产负债表信息
  - H.6：广义货币供给
  - H.8：商业银行资产负债表
  - H.15：利率
  - G.19：消费者信贷，见专栏文章[【数据拾遗：消费者信贷】](https://zhuanlan.zhihu.com/p/526754098)
- [NY Fed Database](https://www.newyorkfed.org/markets/data-hub)
  - 各类短期利率
  - 资产负债表SOMA数据
  - 公开市场操作数据
  - Primary Dealers 数据
- FRED：圣路易斯联储的数据库，以Python库[`fredapi`](https://github.com/mortada/fredapi)为基础，主要作为搭建其他数据库与分析的快捷通道
  
### 美国财政部数据 (`treasury-watch`)
- [Treasury Direct Auction Announcement, Data & Results](https://www.treasurydirect.gov/instit/annceresult/annceresult.htm)：美债拍卖的细节数据，见专栏文章[【数据拾遗：美债拍卖细节】](https://zhuanlan.zhihu.com/p/514668515)
- [Investor Class Auction Allotments](https://home.treasury.gov/data/investor-class-auction-allotments)：美债拍卖的总结数据，见专栏文章[【数据拾遗：美债拍卖数据2】](https://zhuanlan.zhihu.com/p/516037009)
- [Daily Treasury Statement](https://fiscal.treasury.gov/reports-statements/dts/index.html)：包含最详尽的美国财政收支高频数据
- [Monthly Treasury Statement](https://fiscal.treasury.gov/reports-statements/mts/#:~:text=The%20Monthly%20Treasury%20Statement%20summarizes,Budget%20of%20the%20U.S.%20Government.&text=The%20MTS%20presents%20a%20summary,Surplus%20or%20deficit)：DTS的月度总结

### 利率数据（`rates-watch`）
- [Interest Rate Statistics](https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics)：官方的利率曲线数据，包含名义国债收益率曲线，真实收益率（五年以上），国库券利率等，见专栏文章[【数据拾遗：美债官方利率数据】](https://www.zhihu.com/column/c_1509153964662263808)
- [NY Fed Repo Reference Rates](https://www.newyorkfed.org/markets/data-hub)：纽约联储发布的回购利率指数，详见[【漫谈缩表：美国的回购市场】](https://zhuanlan.zhihu.com/p/463721684)

### 大宗商品与期货数据（`futures-watch`）

- [CFTC](https://www.cftc.gov/MarketReports/index.htm)

### [World Bank Data](https://data.worldbank.org/)
- [World Development Indicators](https://datatopics.worldbank.org/world-development-indicators/)
- [Debt Statistics](https://www.worldbank.org/en/programs/debt-statistics/statistics)
- [DataBank](https://databank.worldbank.org/home.aspx)
- [API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structure)
