# A-share index futures / A股股指期货

Use the user's requested instrument, window and language. Do not invent a current contract, data subscription, margin schedule or market observation.

## Evidence to establish before interpretation

Record the dated contract, exchange, quote unit/currency, relevant delivery or index definition, cutoff with offset, observation/publication/availability times, and original source. On a roll, keep both contracts and their overlap explicit; do not splice the move into a return.

## Chain-specific hypotheses and failure conditions

- Use an actual dated futures contract and its exact underlying index. A stock index level is not an executable futures quote.
- Align spot/futures timestamps before basis. Financing, expected dividends and expiry matter; an annualized point discount is not a risk-free expected return.
- Record breadth universe, constituent date, suspension treatment and coverage denominator. Survivorship-biased breadth can reverse an explanation.
- Separate large/small-cap style and industry composition from broad market direction. Do not add total market turnover to overlapping subsets.
- Falsify a broad recovery if index gains rely on a narrowing constituent set. Close-today costs and cash-settlement rules require dated official verification.

## Representative evidence series

- `advancing_fraction`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `index_turnover`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `dividend_estimate`: declare source coverage, native units, publication cadence and revision policy before comparing values.

A missing series is a gap, not zero. Explain which claim it would support or contradict. Use `fundamentals.metric` names that distinguish region, grade and coverage; the engine does not infer these from a short label.

## Practical research delivery

1. Preserve the supplied files and source claims; state whether the evidence is synthetic, retrieved now or an archived vintage.
2. Run `scripts/run_desk.py` for daily observations, vintages, comparable basis/curve, declared processing recipes and hypothetical capacity. Use existing specialist commands where their native macro, breadth, route or curve inputs fit better.
3. Read the quality gates before interpreting numbers. Reject unit/identity contradictions. Describe unavailable calculations rather than hiding them.
4. Write the observed facts first, then the proposed transmission mechanism, the strongest contrary evidence, and the next publication/event that can falsify it. Cite the original source for substantive imported claims.
5. If the user requests a setup, retain their declared trigger, confirmation, invalidation and time limit; do not manufacture historical signals after seeing future data. Separate a scenario from a forecast.
6. If capacity is requested, require the user's budget and effective rule schedule; report stress beyond the stop plan and the model's single-position scope. Do not select risk parameters for the user.

## Next checks

- Check dividend assumptions, expiry and quote synchronization.
- Rebuild breadth with the as-of constituent universe and coverage denominator.
- Confirm open/close/close-today fee schedules with effective dates.

## 中文研究要点

- 使用实际到期期货合约及准确标的指数；股票指数点位不是可成交期货报价。
- 先同步现货与期货时点再算基差；融资、预期分红和到期日影响可比性，年化贴水不是无风险预期收益。
- 广度记录股票池、成分日期、停牌处理和覆盖分母；幸存者偏差可能推翻解释。
- 大小盘风格及行业权重与全市场方向分开；全市场成交额不与重叠子集相加。
- 指数上涨但参与成分持续收窄时，应证伪全面修复叙事；平今费用和现金交割须核对有效官方规则。

- 核对分红假设、到期与报价同步。
- 按当时成分与覆盖分母重建市场广度。
- 确认开仓、平仓、平今费用及其生效日期。

## Review exercises

- A user supplies a continuous contract and asks for a roll-period return: obtain dated contracts/overlap or label the result unavailable; do not reinterpret the continuous code as a deliverable contract.
- An inventory revision was published after the report cutoff: exclude that vintage and retain the previously available observation; show the exclusion count.
- A large calculated premium has asynchronous quotes or different tax/quality scope: block the comparison and identify the precise input needed.
- A user asks for the 'best trade' with no current data: supply conditional research questions and evidence gaps; do not invent a current market or implied confidence score.
- A simulated loss budget fits twelve lots but an adverse gap exceeds it: report both values and state why the stop cannot guarantee that budget.
