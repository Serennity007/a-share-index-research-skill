---
name: a-share-index-research-skill
description: 分析 A 股主要指数的多周期结构、成分样本宽度、成交集中度与大小盘风格，区分沪深300/上证50/中证500/中证1000及 IF/IH/IC/IM。用于股指研究，不替代个股选股或期货执行。
license: MIT
metadata:
  author: Serennity007
  version: "1.1.0"
---

# 大 A 股指研究 Skill

指数涨了，市场是否一起涨？把权重表现、成分股宽度、成交集中度和大小盘风格拆开，避免只看一根指数 K 线。

## 工作方式

1. 明确研究现货指数、ETF 还是股指期货。IF 对应沪深300、IH 上证50、IC 中证500、IM 中证1000；代码、月份、价格口径分开。
2. 用使用者指定周期研究指数结构；用同一市场日期、明确成分范围的快照研究上涨家数、等权表现、行业和成交集中度。
3. 需要样本宽度时读取 `references/domain-data.md`。缺失成分保留覆盖率，不能把部分样本说成全市场；等权样本收益不能冒充官方加权指数涨幅。
4. 对比大盘/小盘、权重/等权和行业的相对强弱；比较需要同一起止时点、调整口径与历史成分，防止幸存者偏差。
5. 分别输出趋势、扩散程度、风格与证据缺口。讨论期货时另查基差、到期和成本；样本宽度不能直接生成仓位或对冲订单。

## 按任务读取

- 解释驱动、拆解情景或审核观点时，读 [研究方法](references/method.md)。
- 导入数据或解释指标时，读 [文件与时间契约](references/data-contract.md)。
- 运行领域工具前读 [领域数据与计算](references/domain-data.md)。
- 写研究报告和复盘时，读 [记录字段](references/report-template.md)。
- 核查外部口径时，使用 [官方来源入口](references/sources.md)，记录实际访问日期。

## 研究工作台

完整研究时先读 [工作台与高级数据](references/workbench.md)。使用者给了数据就核对来源、口径和截止时间，运行本地报告；只有问题没有当前数据时，给缺口清单和情景框架。

```bash
python scripts/run_research.py --config examples/workbench.json --out output
```

报告同时输出 HTML、Markdown、JSON，冻结输入并提供可重跑配置。保留陈旧数据、证据冲突、样本缺失和未就绪指标；不把工具生成的报告视为人工核验结论。若讨论当日计划，区分观察条件、确认条件、失效条件和下次检查事件；复盘追加记录，不改写原计划。

## 单项离线计算

在仓库根目录运行；其他目录运行时将脚本、输入和输出替换成对应绝对路径。

```bash
python scripts/analyze_structure.py --csv examples/bars.csv --instrument A_INDEX_SYNTHETIC --timeframe H4 --as-of 2024-01-09T00:00:00+00:00 --data-kind synthetic --support 100 --out output/structure.json
```

附带数据全部为构造样例。更换真实数据后使用 `--data-kind imported_observations` 并填写来源，不因为标签变化而宣称实测收益。未提供当前数据时可以给研究框架和明确缺口，不能编造即时行情。

保留当时可知信息；未公布数据、未来 K 线不能进入历史结论。工具只做描述计算，不提供已验证的胜率、收益或自动执行。
