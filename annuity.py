import pandas as pd

periods_per_year_map = {
    'Monatlich': 12,
    'Quartalsweise': 4,
    'Halbjährlich': 2,
    'Jährlich': 1
}


def calc_monthly_annuity(principal, nom_intr, duration, periods_per_year):
    total_periods = duration * periods_per_year
    periodic_interest = nom_intr / periods_per_year

    annuity = principal * ((periodic_interest * pow(1 + periodic_interest, total_periods)) /
                           (pow(1 + periodic_interest, total_periods) - 1))

    return annuity


def calc_repayment_plan(principal, nom_intr, duration, spec_repay, period):
    df = pd.DataFrame()
    residual_debt = principal
    nom_intr_fac = nom_intr / 100
    periods_per_year = periods_per_year_map[period]
    tot_periods = duration * periods_per_year
    annuity = calc_monthly_annuity(principal, nom_intr_fac, duration, periods_per_year)

    for j in range(1, tot_periods + 1):
        interest_amt = residual_debt * nom_intr_fac / periods_per_year
        redemption = residual_debt if residual_debt < annuity else annuity - interest_amt

        initial_debt = residual_debt
        cur_year = ((j - 1) // periods_per_year) + 1
        if j % periods_per_year == 0 and initial_debt > 0:
            cur_repay = min(spec_repay, residual_debt - redemption)
        else:
            cur_repay = 0

        residual_debt = residual_debt - redemption - cur_repay
        df = pd.concat([df, pd.DataFrame(
            [{period: j, 'Jahr': cur_year, 'Anfangsschuld': initial_debt, 'Restschuld': residual_debt,
              'Zinsen': interest_amt, 'Tilgung': redemption, 'Annuität': annuity, 'Sondertilgung': cur_repay,
              }])], ignore_index=True)

    df = df[[period, 'Jahr', 'Anfangsschuld', 'Restschuld', 'Zinsen', 'Tilgung', 'Annuität', 'Sondertilgung']]
    for i in ['Anfangsschuld', 'Zinsen', 'Tilgung', 'Annuität', 'Restschuld']:
        df[i] = df[i].apply(lambda x: round(x, 2))

    df.set_index(period, inplace=True)
    return df
