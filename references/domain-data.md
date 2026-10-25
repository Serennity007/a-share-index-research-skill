# 成分样本宽度

`scripts/analyze_breadth.py` 接受 `code,close,previous_close,turnover_cny,sector,observed_at`。

- code 为唯一六位代码，输入 CSV 不把它转换成整数；六位编码并不等于已核验证券身份。样例代码和行业分组仅是占位，不代表真实证券数据。
- close/previous_close 为正，必须采用可比较的口径；拆股、分红、停牌等由数据提供者解释。这里计算 close/previous_close−1。
- turnover_cny 为人民币元且非负；sector 是使用者提供的分类，不能将不同行业版本无说明混合。
- observed_at 带时区且不晚于截止时刻；包含的数据必须来自同一个北京时间市场日期。工具报告异步时间跨度。
- `--universe` 声明样本范围；`--expected-count` 声明当时完整成分数。工具仅校验行数，不独立核实成员名单和历史成分。

coverage=实际行数/声明行数；advance_fraction 以实际包含行数作分母。sample_equal_weight_return 是样本等权均值，**不是官方指数涨跌幅**。top5_turnover_share 是成交额最大的五只占样本总成交额，零总额时为 null。

构造示例是 6/10 的不完整样本：上涨3、下跌2、平1，等权收益约1.6667%，成交额1000元，前五名占比90%。声明总数10仅为展示缺失处理，不代表任何真实指数的成分数。
