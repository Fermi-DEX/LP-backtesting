import unittest
from fee_adjust import adjustment, adjust_run, executed_volumes, adjusted_curve
class Fees(unittest.TestCase):
    def row(self):
        return dict(run_id='synthetic',status='synthetic_test',fermi_trading_fees_included=False,
                    notional_basis='executed_price_times_base_quantity_usd',maker_notional_usd=1000000,
                    taker_notional_usd=100000,base_marked_pnl_usd=150,test_capital_usd=100000,duration_days=1)
    def test_rates(self): self.assertEqual(adjustment(1000000,100000),240)
    def test_no_protocol_revenue_or_hedge_double_count(self):
        r=adjust_run(self.row())
        self.assertEqual(r['adjusted_marked_pnl_usd'],390)
        self.assertEqual(r['maker_rebate_usd'],300)
        self.assertEqual(r['taker_fee_usd'],60)
        self.assertAlmostEqual(r['test_capital_simple_annualized_pct'],142.35)
        self.assertIsNone(r['funded_vault_apr'])
    def test_double_application_rejected(self):
        r=self.row(); r['fermi_trading_fees_included']=True
        with self.assertRaises(ValueError): adjust_run(r)
    def test_margin_rejected(self):
        r=self.row(); r['notional_basis']='margin'
        with self.assertRaises(ValueError): adjust_run(r)
    def test_missing_volume_rejected(self):
        r=self.row(); del r['maker_notional_usd']
        with self.assertRaises(KeyError): adjust_run(r)
    def test_invalid_numbers(self):
        for n in [-1,float('nan'),float('inf'),True]:
            with self.assertRaises(ValueError): adjustment(n,0)
    def test_execution_notional_and_role(self):
        self.assertEqual(executed_volumes([dict(venue='fermi',price=200,size=5,is_taker=False),
                         dict(venue='fermi',price=100,size=2,is_taker=True)]),(1000,200))
    def test_external_hedge_rejected(self):
        with self.assertRaises(ValueError): executed_volumes([dict(venue='phoenix',price=1,size=1,is_taker=True)])
    def test_unknown_role_rejected(self):
        with self.assertRaises(ValueError): executed_volumes([dict(venue='fermi',price=1,size=1,is_taker='false')])
    def test_fee_adjusted_drawdown(self):
        points=[dict(t=0,base_equity_usd=1000,cumulative_maker_notional_usd=0,cumulative_taker_notional_usd=0),
                dict(t=1,base_equity_usd=1100,cumulative_maker_notional_usd=100000,cumulative_taker_notional_usd=0),
                dict(t=2,base_equity_usd=1000,cumulative_maker_notional_usd=100000,cumulative_taker_notional_usd=100000)]
        curve,dd=adjusted_curve(points)
        self.assertEqual(curve[-1]['adjusted_equity_usd'],970)
        self.assertEqual(dd,160)
    def test_bad_curve_rejected(self):
        with self.assertRaises(ValueError): adjusted_curve([])
    def test_zero_duration_rejected(self):
        r=self.row(); r['duration_days']=0
        with self.assertRaises(ValueError): adjust_run(r)
if __name__ == '__main__': unittest.main()
