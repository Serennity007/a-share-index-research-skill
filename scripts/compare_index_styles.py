#!/usr/bin/env python3
"""Compare cash-index price levels at common dates, without claiming total returns or futures P&L."""
import argparse
from datetime import date
from pathlib import Path
from market_io import timestamp, number, records, provenance, emit, kind

INDICES={'HS300','SSE50','CSI500','CSI1000'}


def analyze(raw, as_of, data_kind):
    cutoff=timestamp(as_of)
    panel,seen,excluded={},set(),0
    for row in records(raw,['index','observation_date','available_at','close','return_type']):
        available=timestamp(row['available_at'])
        if available>cutoff:
            excluded+=1
            continue
        name=row['index']
        day=date.fromisoformat(row['observation_date'])
        if name not in INDICES or row['return_type']!='price':
            raise ValueError('use supported cash indices with consistent price-return levels')
        if day>available.date() or (name,day) in seen:
            raise ValueError('invalid availability date or duplicate index/date')
        seen.add((name,day))
        panel.setdefault(day,{})[name]={'close':number(row['close'],positive=True),'available_at':available.isoformat()}
    complete=sorted(day for day,values in panel.items() if set(values)==INDICES)
    if len(complete)<2:
        raise ValueError('need two common complete dates for all four indices; no forward filling')
    first,last=complete[0],complete[-1]
    returns={name:panel[last][name]['close']/panel[first][name]['close']-1 for name in sorted(INDICES)}
    pairs=[]
    for numerator,denominator in [('CSI1000','HS300'),('CSI500','HS300'),('SSE50','HS300')]:
        relative=(1+returns[numerator])/(1+returns[denominator])-1
        pairs.append({'numerator':numerator,'denominator':denominator,'relative_ratio_change':relative,
                      'return_difference_pp':100*(returns[numerator]-returns[denominator])})
    return {'schema_version':1,'data_kind':kind(data_kind),'as_of_utc':cutoff.isoformat(),
            'start_date':first.isoformat(),'end_date':last.isoformat(),'complete_dates':len(complete),
            'incomplete_dates':len(panel)-len(complete),'excluded_unavailable_rows':excluded,
            'price_returns':returns,'relative_strength':pairs,
            'ranked_by_price_return':sorted(returns,key=lambda name:(-returns[name],name)),
            'observations':{day.isoformat():panel[day] for day in (first,last)},
            'end_date_age_days':(cutoff.date()-last).days,'source_sha256':provenance(raw),
            'scope':'Common-window cash-index price comparison, not total return, factor attribution or hedge execution.',
            'limitations':['Index identity, methodology versions and provider observations must be independently verified',
                           'Four index returns do not prove sector breadth or explain a style move causally',
                           'No ETF tracking, futures basis, dividend reinvestment or transaction costs']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv',type=Path,required=True)
    parser.add_argument('--as-of',required=True)
    parser.add_argument('--data-kind',choices=('synthetic','imported_observations'),required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    try:
        emit(analyze(args.csv.read_bytes(),args.as_of,args.data_kind),args.out,[args.csv])
    except (ValueError,OSError,KeyError) as exc:
        parser.exit(2,f'ERROR: {exc}\n')
    print('Saved four-index style comparison.')


if __name__=='__main__':
    main()
