import pandas as pd


def calc_monthly_annuity(principal, nom_intr, rdmp_intr):
    interest = nom_intr / 100
    redemption = rdmp_intr / 100
    return round(principal * (interest + redemption) / 12, 2)


def calc_repayment_plan(principal, nom_intr, rdmp_intr, spec_repay_amt, spec_repay_period, tot_months):
    df = pd.DataFrame()
    residual_debt = principal
    nom_intr_fac = nom_intr / 100
    annuity = calc_monthly_annuity(principal, nom_intr, rdmp_intr)

    for j in range(1, tot_months + 1):
        interest_amt = residual_debt * nom_intr_fac / 12
        redemption = residual_debt if residual_debt < annuity else annuity - interest_amt

        initial_debt = residual_debt
        cur_year = ((j - 1) // 12) + 1
        if j % 12 == 0 and initial_debt > 0 and cur_year > spec_repay_period:
            cur_repay = spec_repay_amt
        else:
            cur_repay = 0
        residual_debt = residual_debt - redemption - cur_repay
        df = pd.concat([df, pd.DataFrame([{'Monat': j, 'Jahr': cur_year, 'Anfangsschuld': initial_debt,
                                           'Zinsen': interest_amt, 'Tilgung': redemption, 'Sondertilgung': cur_repay,
                                           'Restschuld': residual_debt}])], ignore_index=True)

    df = df[['Monat', 'Jahr', 'Anfangsschuld', 'Zinsen', 'Tilgung', 'Sondertilgung', 'Restschuld']]
    for i in ['Anfangsschuld', 'Zinsen', 'Tilgung', 'Restschuld']:
        df[i] = df[i].apply(lambda x: round(x, 2))
    df.set_index('Monat', inplace=True)
    return df
