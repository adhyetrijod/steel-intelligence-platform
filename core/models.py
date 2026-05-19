# core/models.py
# ═══════════════════════════════════════════════════════════════
# ISFIP — Integrated Steel Financial Intelligence Platform
# Financial Models Engine
# Inspired by: Bain & Company Steel Sector Cost Pressure Reports
#              McKinsey Global Steel Index Methodology
# ═══════════════════════════════════════════════════════════════

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import linprog, brentq
import warnings
warnings.filterwarnings('ignore')


class SteelFinancialEngine:
    """
    Enterprise financial modeling engine for integrated steel producers.
    
    Covers all CFO/Strategy-level analyses:
    1. Monte Carlo EBITDA simulation
    2. DCF / NPV / IRR capital analysis  
    3. Commodity Value at Risk (VaR)
    4. Linear Programming procurement optimizer
    5. Bear/Base/Bull scenario P&L
    6. Working Capital / Cash Conversion Cycle
    7. Break-Even & Operating Leverage
    
    Research basis:
    - Bain & Company: "Steel Sector Under Pressure" (2024)
    - World Bank Commodity Markets Outlook
    - WSA Steel Statistical Yearbook
    """

    # ─── Model 1: Monte Carlo ─────────────────────────────────────────────────
    @staticmethod
    def monte_carlo_ebitda(
        revenue: float,
        coal_cost: float,
        ore_cost: float,
        fixed_costs: float,
        units: float,
        n_simulations: int = 10_000,
        coal_vol: float = 0.18,
        ore_vol: float = 0.15,
        demand_vol: float = 0.08,
        commodity_correlation: float = 0.45
    ) -> dict:
        """
        Simulates EBITDA distribution across market scenarios.
        
        Key assumption: Coal-Ore correlation = 0.45 (empirical, 2015-2024).
        Both driven by Chinese demand cycles (Bain 2024 observation).
        """
        np.random.seed(42)

        cov = np.array([
            [coal_vol**2, commodity_correlation * coal_vol * ore_vol],
            [commodity_correlation * coal_vol * ore_vol, ore_vol**2]
        ])
        shocks = np.random.multivariate_normal([0, 0], cov, n_simulations)

        sim_coal  = coal_cost * np.exp(shocks[:, 0])
        sim_ore   = ore_cost  * np.exp(shocks[:, 1])
        sim_units = units * (1 + np.random.normal(0, demand_vol, n_simulations))
        sim_units = np.clip(sim_units, units * 0.5, units * 1.5)

        avg_price = revenue / units
        sim_rev   = sim_units * avg_price
        sim_var   = (sim_coal + sim_ore) * sim_units
        sim_ebitda= sim_rev - sim_var - fixed_costs
        sim_margin= (sim_ebitda / sim_rev) * 100

        var_95  = float(np.percentile(sim_ebitda, 5))
        cvar_95 = float(sim_ebitda[sim_ebitda <= var_95].mean())

        return {
            'ebitda_dist':    sim_ebitda.tolist(),
            'margin_dist':    sim_margin.tolist(),
            'mean_ebitda':    float(sim_ebitda.mean()),
            'median_ebitda':  float(np.median(sim_ebitda)),
            'std_ebitda':     float(sim_ebitda.std()),
            'var_95':         var_95,
            'cvar_95':        cvar_95,
            'prob_loss_pct':  float((sim_ebitda < 0).mean() * 100),
            'p10':            float(np.percentile(sim_ebitda, 10)),
            'p90':            float(np.percentile(sim_ebitda, 90)),
            'n_sims':         n_simulations
        }

    # ─── Model 2: DCF / NPV / IRR ─────────────────────────────────────────────
    @staticmethod
    def dcf_analysis(
        initial_investment: float,
        annual_ebitda: float,
        growth_rate: float = 0.03,
        wacc: float = 0.10,
        tax_rate: float = 0.25,
        depreciation: float = 50.0,
        capex: float = 30.0,
        delta_wc: float = 10.0,
        terminal_growth: float = 0.025,
        years: int = 10
    ) -> dict:
        """
        Full DCF with terminal value (Gordon Growth).
        Industry standard for steel capex decisions (blast furnace,
        DRI plants, EAF upgrades).
        """
        cashflows, pv_cashflows = [], []

        for t in range(1, years + 1):
            ebitda_t = annual_ebitda * (1 + growth_rate) ** t
            ebit_t   = ebitda_t - depreciation
            nopat_t  = ebit_t * (1 - tax_rate)
            fcff_t   = nopat_t + depreciation - capex - delta_wc
            cashflows.append(round(fcff_t, 2))
            pv_cashflows.append(round(fcff_t / (1 + wacc) ** t, 2))

        terminal_fcff  = cashflows[-1] * (1 + terminal_growth)
        terminal_value = terminal_fcff / (wacc - terminal_growth)
        pv_terminal    = terminal_value / (1 + wacc) ** years

        npv = sum(pv_cashflows) + pv_terminal - initial_investment

        def npv_func(r):
            flows = [-initial_investment] + cashflows
            return sum(cf / (1 + r)**t for t, cf in enumerate(flows))

        try:
            irr = brentq(npv_func, 0.001, 5.0)
        except Exception:
            irr = wacc

        return {
            'npv':            round(npv, 2),
            'irr':            round(irr * 100, 2),
            'payback_years':  round(initial_investment / (annual_ebitda * 0.6), 1),
            'pv_terminal':    round(pv_terminal, 2),
            'pv_cashflows':   round(sum(pv_cashflows), 2),
            'cashflows':      cashflows,
            'pv_annual':      pv_cashflows,
            'years':          list(range(1, years + 1)),
            'decision':       'INVEST' if npv > 0 and irr > wacc else '❌ REJECT'
        }

    # ─── Model 3: Value at Risk ────────────────────────────────────────────────
    @staticmethod
    def commodity_var(
        coal_exposure: float,
        ore_exposure: float,
        coal_vol: float = 0.18,
        ore_vol: float = 0.15,
        correlation: float = 0.45,
        confidence: float = 0.95,
        horizon_days: int = 30
    ) -> dict:
        """Parametric VaR for commodity cost exposure."""
        port_var = (
            (coal_exposure * coal_vol)**2 +
            (ore_exposure  * ore_vol)**2 +
            2 * correlation * coal_exposure * coal_vol * ore_exposure * ore_vol
        )
        port_std    = np.sqrt(port_var)
        daily_std   = port_std / np.sqrt(252)
        horizon_std = daily_std * np.sqrt(horizon_days)
        z           = stats.norm.ppf(confidence)

        return {
            'var_amount':    round(z * horizon_std, 2),
            'cvar_amount':   round(horizon_std * stats.norm.pdf(z) / (1 - confidence), 2),
            'confidence':    f"{int(confidence * 100)}%",
            'horizon_days':  horizon_days,
            'total_exposure':round(coal_exposure + ore_exposure, 2),
            'var_pct':       round((z * horizon_std / (coal_exposure + ore_exposure)) * 100, 2)
        }

    # ─── Model 4: LP Procurement Optimizer ────────────────────────────────────
    @staticmethod
    def optimize_procurement(
        spot_coal: float, fwd3m_coal: float, fwd6m_coal: float,
        spot_ore: float,  fwd3m_ore: float,  fwd6m_ore: float,
        coal_needed: float, ore_needed: float,
        max_fwd_ratio: float = 0.70,
        storage_cost_pct: float = 0.02
    ) -> dict:
        """
        Linear programming: minimize total procurement cost.
        Variables: [coal_spot, coal_3m, coal_6m, ore_spot, ore_3m, ore_6m]
        """
        c = [
            spot_coal,
            fwd3m_coal * (1 + storage_cost_pct * 3/12),
            fwd6m_coal * (1 + storage_cost_pct * 6/12),
            spot_ore,
            fwd3m_ore  * (1 + storage_cost_pct * 3/12),
            fwd6m_ore  * (1 + storage_cost_pct * 6/12)
        ]

        A_eq = [[1,1,1,0,0,0], [0,0,0,1,1,1]]
        b_eq = [coal_needed, ore_needed]
        A_ub = [[0,1,1,0,0,0], [0,0,0,0,1,1]]
        b_ub = [coal_needed * max_fwd_ratio, ore_needed * max_fwd_ratio]

        res = linprog(c, A_ub=A_ub, b_ub=b_ub,
                      A_eq=A_eq, b_eq=b_eq,
                      bounds=[(0, None)]*6, method='highs')

        x = res.x if res.success else [coal_needed,0,0,ore_needed,0,0]
        opt_cost  = float(np.dot(c, x))
        base_cost = spot_coal * coal_needed + spot_ore * ore_needed
        savings   = base_cost - opt_cost

        return {
            'coal_spot':    round(x[0], 0), 'coal_3m': round(x[1], 0), 'coal_6m': round(x[2], 0),
            'ore_spot':     round(x[3], 0), 'ore_3m':  round(x[4], 0), 'ore_6m':  round(x[5], 0),
            'optimal_cost': round(opt_cost, 2),
            'baseline_cost':round(base_cost, 2),
            'savings':      round(savings, 2),
            'savings_pct':  round((savings / base_cost) * 100, 2),
            'success':      res.success
        }

    # ─── Model 5: Scenario P&L ─────────────────────────────────────────────────
    @staticmethod
    def scenario_pl(
        revenue: float, coal_cost: float, ore_cost: float,
        fixed_costs: float, units: float,
        interest: float = 20.0, tax_rate: float = 0.25
    ) -> dict:
        """
        3-scenario full income statement.
        Scenarios calibrated to Bain steel sector stress-test ranges.
        """
        scenarios = {
            'Bear': dict(rev=0.85, coal=1.25, ore=1.20, vol=0.80),
            'Base': dict(rev=1.00, coal=1.00, ore=1.00, vol=1.00),
            'Bull': dict(rev=1.18, coal=0.82, ore=0.85, vol=1.15),
        }
        out = {}
        for name, s in scenarios.items():
            adj_units = units       * s['vol']
            adj_rev   = revenue     * s['rev'] * s['vol']
            adj_coal  = coal_cost   * s['coal']
            adj_ore   = ore_cost    * s['ore']
            var_cost  = (adj_coal + adj_ore) * adj_units
            gross_p   = adj_rev - var_cost
            ebitda    = gross_p - fixed_costs
            depr      = fixed_costs * 0.15
            ebit      = ebitda - depr
            ebt       = ebit - interest
            tax       = max(ebt * tax_rate, 0)
            pat       = ebt - tax

            out[name] = {
                'Revenue':        round(adj_rev, 1),
                'Variable Costs': round(var_cost, 1),
                'Gross Profit':   round(gross_p, 1),
                'Fixed Costs':    round(fixed_costs, 1),
                'EBITDA':         round(ebitda, 1),
                'Depreciation':   round(depr, 1),
                'EBIT':           round(ebit, 1),
                'Interest':       round(interest, 1),
                'EBT':            round(ebt, 1),
                'Tax':            round(tax, 1),
                'PAT':            round(pat, 1),
                'EBITDA Margin':  round((ebitda / adj_rev) * 100, 1) if adj_rev else 0,
                'PAT Margin':     round((pat    / adj_rev) * 100, 1) if adj_rev else 0,
            }
        return out

    # ─── Model 6: Working Capital ──────────────────────────────────────────────
    @staticmethod
    def working_capital(
        revenue: float, cogs: float,
        rec_days: int = 45, pay_days: int = 35, inv_days: int = 60
    ) -> dict:
        dr = revenue / 30
        dc = cogs    / 30
        rec = dr * rec_days
        pay = dc * pay_days
        inv = dc * inv_days
        nwc = rec + inv - pay
        ccc = rec_days + inv_days - pay_days
        opt_pay = dc * (pay_days + 15)
        freed   = nwc - (rec + inv - opt_pay)

        return {
            'receivables': round(rec, 1), 'payables': round(pay, 1),
            'inventory':   round(inv, 1), 'nwc': round(nwc, 1),
            'ccc':         ccc,           'freed': round(freed, 1),
            'rec_days': rec_days, 'pay_days': pay_days, 'inv_days': inv_days
        }

    # ─── Model 7: Break-Even & Operating Leverage ─────────────────────────────
    @staticmethod
    def breakeven(
        fixed_costs: float,
        price_per_unit: float,
        variable_cost_per_unit: float,
        current_units: float
    ) -> dict:
        cm    = price_per_unit - variable_cost_per_unit
        cm_r  = cm / price_per_unit
        bep_u = fixed_costs / cm
        bep_r = fixed_costs / cm_r
        mos_u = current_units - bep_u
        mos_r = mos_u / current_units * 100
        dol   = (current_units * cm) / (current_units * cm - fixed_costs)

        return {
            'bep_units':   round(bep_u, 0),
            'bep_revenue': round(bep_r, 1),
            'cm':          round(cm, 4),
            'cm_ratio':    round(cm_r * 100, 1),
            'mos_units':   round(mos_u, 0),
            'mos_pct':     round(mos_r, 1),
            'dol':         round(dol, 2),
        }
        