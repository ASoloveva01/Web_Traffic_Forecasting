from matplotlib import pyplot as plt
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
import itertools
def plot_test(test_set, predictions):

    fig, ax = plt.subplots(figsize=(11,7), facecolor='w')

    ax.plot(test_set, label='Testing Set')
    ax.plot(predictions, label='Forecast')

    ax.set_title("Test vs Forecast", fontsize=15, pad=15)
    ax.set_ylabel("Number of orders", fontsize=12)
    ax.set_xlabel("Date", fontsize=12)

    ax.grid(linestyle=":", color='grey')
    ax.legend()

    plt.show()

def grid_search_sarima(train_set):
    p = range(1, 3)
    d = D = [1]
    q = range(1, 3)
    P = range(0, 2)
    Q = range(0, 2)
    s = 12
    pdq = list(itertools.product(p, d, q))
    PDQ = list(itertools.product(P, D, Q))
    seasonal_pdq = [(x[0], x[1], x[2], s) for x in PDQ]

    # Supress UserWarnings
    warnings.simplefilter('ignore', category=UserWarning)
    # Grid Search
    mse = np.inf
    best_model = None
    for order in pdq:
        for seasonal_order in seasonal_pdq:
            model = SARIMAX(train_set['Views'],
                            order=order,
                            seasonal_order=seasonal_order
                            )
            results = model.fit(disp=0)
            print(f'ARIMA{order}x{seasonal_order} -> AIC: {results.aic}, BIC:{results.bic},  MSE: {results.mse}')
            if mse > results.mse:
                mse = results.mse
                final_model = results
    return final_model

def datetime_features(df_temp):

    df_temp['month'] = df_temp.index.month
    df_temp['year'] = df_temp.index.year
    df_temp['dayofweek'] = df_temp.index.dayofweek
    df_temp['quarter'] = df_temp.index.quarter
    df_temp['dayofmonth'] = df_temp.index.day
    df_temp['weekofyear'] = df_temp.index.weekofyear