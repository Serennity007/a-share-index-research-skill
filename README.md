![Research workbench](.github/cover.svg)

# 大 A 股指研究 Skill

指数涨了，市场是否一起涨？把权重表现、成分股宽度、成交集中度和大小盘风格拆开，避免只看一根指数 K 线。

作者：[Serennity007](https://github.com/Serennity007) · [四类研究导航](https://github.com/Serennity007/market-research-skills) · [完整 Skill](SKILL.md) · MIT

## 研究工作台 · v1.1

**Python 3.10+ · 标准库 · 离线运行 · 独立安装**

```bash
python scripts/run_research.py --config examples/workbench.json --out output
```

打开终端打印的 `REPORT.html`：一次完成结构检查、领域计算、高级对照与证据整理，同时保存 Markdown、JSON 和可重跑输入。重复运行使用新目录。

**[先看完整模拟报告](examples/workbench/REPORT.md)** · [计算与来源](examples/workbench/bundle.json) · [工作台与高级数据](references/workbench.md) · [Skill 指令](SKILL.md)

**大 A 股指：共同窗口的风格对照**：对照四个现货指数的共同窗口收益、相对强弱及样本宽度，区分收益差与相对比。

## 能做什么

1. 明确研究现货指数、ETF 还是股指期货。IF 对应沪深300、IH 上证50、IC 中证500、IM 中证1000；代码、月份、价格口径分开。
2. 用使用者指定周期研究指数结构；用同一市场日期、明确成分范围的快照研究上涨家数、等权表现、行业和成交集中度。
3. 需要样本宽度时读取 `references/domain-data.md`。缺失成分保留覆盖率，不能把部分样本说成全市场；等权样本收益不能冒充官方加权指数涨幅。
4. 对比大盘/小盘、权重/等权和行业的相对强弱；比较需要同一起止时点、调整口径与历史成分，防止幸存者偏差。
5. 分别输出趋势、扩散程度、风格与证据缺口。讨论期货时另查基差、到期和成本；样本宽度不能直接生成仓位或对冲订单。

这是可单独使用的研究 Skill：指令、参考、示例和计算脚本都在本仓库内，不依赖其他三个项目。离线脚本使用 Python 3.10+ 标准库，无 API Key。

## 快速体验

```bash
git clone https://github.com/Serennity007/a-share-index-research-skill.git
cd a-share-index-research-skill
python scripts/analyze_structure.py --csv examples/bars.csv --instrument A_INDEX_SYNTHETIC --timeframe H4 --as-of 2024-01-09T00:00:00+00:00 --data-kind synthetic --support 100 --out output/structure.json
python scripts/analyze_breadth.py --csv examples/breadth.csv --as-of 2024-01-09T15:00:00+08:00 --universe DEMO_PARTIAL_UNIVERSE --expected-count 10 --data-kind synthetic --out output/breadth.json
python -m unittest discover -s tests -v
```

输出保存在 `output/`。重复运行请换文件名；脚本拒绝覆盖输入和已有结果。

先看 [输入样例](examples/bars.csv)、[结构计算输出](examples/structure-output.json) 和 [数据约定](references/data-contract.md)。K 线例子是 2024 年时间标签的构造数据，统一使用虚构标的名；归档时间不代表 2024 年曾经做过此分析。末端收复支撑但均线方向仍有分歧，示范如何保留冲突证据。

[领域工具数据规范](references/domain-data.md) · [领域计算输出](examples/domain-output.json)

## 作为 Skill 使用

把本仓库完整复制到使用工具支持的技能目录，保留文件夹名 `a-share-index-research-skill`。例如 Codex 的用户技能目录为 `~/.codex/skills/a-share-index-research-skill`；有图形界面或其他代理时按其技能目录约定安装。

```text
使用 $a-share-index-research-skill，标的是……，截止时间是……，数据来自……。
请核查证据与时效，给出有条件的研究结论、失效条件及复盘检查点。
```

需要当前行情时，使用者提供带来源和时间的文件，或由其已授权的数据工具获取。此仓库不内置行情订阅、账户接入和自动下单。

## 证据与验证范围

计算测试覆盖时间截止、输入校验、指标/领域算术和命令行文件保护。`examples/` 全部是 **synthetic 模拟样例**，用于验证功能；没有宣称真实行情测试、纸面账户收益或实盘盈利。作者的历史观点与证据等级见 [方法说明](references/method.md)。

共同 K 线引擎从作者 [选股与量化技能合集](https://github.com/Serennity007/awesome-stock-quant-skills/tree/67156b0aa4860894a8cdbc66b797db535531fe59/my-skills/gold-cross-asset-research) 的已收盘数据分析器适配而来。各仓库随带自身代码与测试，互不需要联网导入。

[研究与复盘记录模板](references/report-template.md) · [官方来源](references/sources.md)

本地验证（2026-10-25）：**27 项测试通过**，覆盖原有功能、新领域算术、未来信息隔离、输入冻结与重跑、跨目录 CLI 和 HTML 转义。测试数量是可重复执行的行为检查数，不代表研究胜率。
