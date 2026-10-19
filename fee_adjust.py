"""Offline Fermi executed-notional accounting. Python standard library only."""
import argparse
import json
from decimal import Decimal
from pathlib import Path


def number(value, name, nonnegative=False):
    if isinstance(value, bool):
        raise ValueError(name + ' must be numeric')
    try:
        x = Decimal(str(value))
    except Exception as exc:
        raise ValueError(name + ' must be numeric') from exc
    if not x.is_finite() or (nonnegative and x < 0):
        raise ValueError(name + ' must be finite and within range')
    return x


def adjustment(maker, taker):
    return number(maker, 'maker', True)*Decimal('0.0003') - number(taker, 'taker', True)*Decimal('0.0006')


def adjust_run(run):
    if run.get('fermi_trading_fees_included') is not False:
        raise ValueError('explicit fermi_trading_fees_included=false required')
    if run.get('notional_basis') != 'executed_price_times_base_quantity_usd':
        raise ValueError('executed notional required; margin/venue volume is invalid')
    maker = number(run['maker_notional_usd'], 'maker', True)
    taker = number(run['taker_notional_usd'], 'taker', True)
    base = number(run['base_marked_pnl_usd'], 'base PnL')
    capital = number(run['test_capital_usd'], 'capital', True)
    days = number(run['duration_days'], 'days', True)
    if capital == 0 or days == 0:
        raise ValueError('positive capital and duration required')
    delta = adjustment(maker, taker)
    return dict(run_id=run['run_id'], status=run['status'],
                base_marked_pnl_usd=float(base), maker_notional_usd=float(maker),
                taker_notional_usd=float(taker), maker_rebate_usd=float(maker*Decimal('0.0003')),
                taker_fee_usd=float(taker*Decimal('0.0006')), fee_adjustment_usd=float(delta),
                adjusted_marked_pnl_usd=float(base+delta), fermi_trading_fees_included=True,
                test_capital_simple_annualized_pct=float((base+delta)/capital/days*365*100),
                funded_vault_apr=None, adjusted_max_drawdown_usd=None,
                terminal_closeout_included=False)


def executed_volumes(fills):
    """Fermi fills only; LP is_taker flag, not counterparty taker-flow tag."""
    maker = taker = Decimal(0)
    for f in fills:
        if f.get('venue') != 'fermi' or type(f.get('is_taker')) is not bool:
            raise ValueError('explicit Fermi venue and boolean LP is_taker required')
        px,qty = number(f['price'],'price',True),number(f['size'],'size',True)
        if px == 0 or qty == 0:
            raise ValueError('executions require positive price and quantity')
        if f['is_taker']: taker += px*qty
        else: maker += px*qty
    return maker,taker


def adjusted_curve(points):
    """Sampled drawdown using cumulative fills as of each timestamp; include t=0.

    Post-hoc fee adjustment does not change quotes, risk halts or fill sequence.
    """
    out,peak,dd,last_t,last_m,last_k = [],None,Decimal(0),None,Decimal(0),Decimal(0)
    for p in points:
        t=number(p['t'],'timestamp')
        m=number(p['cumulative_maker_notional_usd'],'maker',True)
        k=number(p['cumulative_taker_notional_usd'],'taker',True)
        if (last_t is not None and t <= last_t) or m < last_m or k < last_k:
            raise ValueError('timestamps must increase and notionals must be cumulative')
        if last_t is None and (m or k):
            raise ValueError('initial point must precede fills')
        eq=number(p['base_equity_usd'],'equity')+adjustment(m,k)
        peak=eq if peak is None else max(peak,eq)
        dd=max(dd,peak-eq)
        out.append(dict(t=float(t),adjusted_equity_usd=float(eq)))
        last_t,last_m,last_k=t,m,k
    if not out: raise ValueError('equity points required')
    return out,float(dd)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input',type=Path)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    result=[adjust_run(r) for r in json.loads(args.input.read_text())]
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')

if __name__ == '__main__': main()
