[English](README.md) · [简体中文](README.zh-CN.md)

![A-share Equity Index Research](.github/cover.svg)

# A-share Equity Index Research

<!-- futures-desk-v3 -->
## Research desk v2.0

New: an offline **English/Chinese** desk with historical vintages, explicit sessions, comparable basis/curves, seasonal evidence, Decimal fee/margin capacity and gap stress. [Data contract](docs/desk-data-contract.md) · [Research playbook](references/research-playbook.md) · [Capacity assumptions](docs/desk-risk-model.md).

```bash
python scripts/run_desk.py run --config examples/desk-demo/equity-index/config.json --out output --lang en
```

Both report languages are emitted on every run. The original command and frozen Chinese demonstrations below remain available. Download the self-contained Skill ZIP from [releases](https://github.com/Serennity007/a-share-index-research-skill/releases). Basic commands need only Python 3.10+.


Check index performance and constituent-sample breadth separately, including large/small-cap comparisons and missing coverage.

[Futures research workbench](https://github.com/Serennity007/taotao-futures-research) · [Agent Skill](SKILL.md) · [Language coverage](docs/LANGUAGES.md) · MIT

## Run an offline exercise

Python 3.10+ is required. The scripts use only the standard library.

```bash
git clone https://github.com/Serennity007/a-share-index-research-skill.git
cd a-share-index-research-skill
python scripts/run_research.py --config examples/workbench.json --out output
```

Open the printed `REPORT.html` path. You can also inspect the committed [Markdown report](examples/workbench/REPORT.md) or download the [HTML report](examples/workbench/REPORT.html).

The supplied CSV files are synthetic; dates label the exercise. They test calculations and workflow, not a historical trading record. Legacy research reports and reference material retain Chinese text; this source release provides English and Chinese entry guides, not an application language switch.

## Check the numbers

The four-index fixture starts at 100. CSI 300 ends at 102 and CSI 1000 at 104: returns of 2% and 4%, a 2-percentage-point gap. The relative-ratio change is about 1.9608%.

The breadth fixture contains 6 observations against a declared universe of 10: 60% coverage, with 3 advancing, 2 declining and 1 unchanged. The advance fraction is 50% of included observations; four constituents are missing.

IF, IH, IC and IM correspond to CSI 300, SSE 50, CSI 500 and CSI 1000 respectively. Fixtures are synthetic spot-index and constituent data; actual futures research also needs the contract month and contemporaneous spot observations.

See the [method](references/method.md) for assumptions and additional evidence to check.

## Use your own data

Copy `examples/workbench.json`, then set the instrument, cutoff and file paths. For imported observations, set `data_kind` to `imported_observations` and record a source name and retrieval time for every file. [Fields and configuration](references/workbench.md) also document the original standalone calculation commands.

CSV paths are resolved relative to the configuration file. When running from another directory, use absolute script and configuration paths.

## Save and review runs

Each run creates `output/run-…/`: `REPORT.md` contains the narrative, `bundle.json` the calculation details, and `inputs/` the actual files used. Rerun a saved snapshot in this repository:

```bash
python scripts/run_research.py --config /path/to/previous-run/config.snapshot.json --out output
```

The same inputs should reproduce the calculations. Keep the old run, create a separate run with new data and compare whether the stated conditions occurred. See the [report template](references/report-template.md).

## Use as an Agent Skill

Copy the whole repository to your agent's skill directory, keeping the folder name `a-share-index-research-skill`. State the data paths, instrument, cutoff and desired response language:

```text
Use $a-share-index-research-skill with the supplied data, instrument and cutoff.
Run the calculations, distinguish observations from missing evidence,
save the report and explain the results in English.
```

The original Skill instructions remain in Chinese. The response language request does not automatically translate script-generated artifacts.

## Verification and sources

```bash
python -m unittest discover -s tests -v
```

Tests cover calculations, cutoff handling and file I/O. Real-world source identity, units and historical versions still require review. [Official source entry points](references/sources.md) are provided.

The OHLC helper derives from the author's [quant research collection](https://github.com/Serennity007/awesome-stock-quant-skills/tree/67156b0aa4860894a8cdbc66b797db535531fe59/my-skills/gold-cross-asset-research); this repository includes its own code and tests.

Research and learning only; calculations and synthetic examples do not establish trading performance. Original code is distributed under [MIT](LICENSE).
