import pandas as pd
from random_forest.forest import Forest


def load():
    df = pd.read_csv('refrigerator_temp_time_series.csv')
    df['temp'] = df['temp'].apply(lambda x: x.replace(',', '.')).astype(
        'float64')
    df['Ts'] = df['Ts'].apply(lambda x: x.replace(',', '.')).astype('float64')
    df.rename(
        columns={
            "czas(min)": "time",
            "alpha": "compressor",
            "temp": 'ambient_temp',
            "Ts": 'refrigerator_temp'},
        inplace=True)
    df.set_index('time', inplace=True)
    return df


def delay(df, delay):
    frames = [df.shift(-t) for t in range(delay)]
    frames.append(df.iloc[:, -1:].diff().shift(-delay))
    delayed_df = pd.concat(frames, axis=1).dropna()
    return delayed_df


def test(df, iterations, data_to_test='fresh_data'):
    prediction_err_sum = 0
    naive_err_sum = 0
    for _ in range(iterations):

        fresh_data = df.sample(df.shape[0]//10)
        training_data = df[~df.index.isin(fresh_data.index)]

        forest = Forest(training_data)

        if data_to_test == 'test_data':
            test_data = fresh_data
        else:
            test_data = training_data

        for test in test_data.values:
            previous_temp = test[-2]
            actual_value = previous_temp + test[-1]
            prediction_err_sum += abs(
                (forest.predict(test[:-1]) + previous_temp - actual_value) /
                actual_value if actual_value else 0)
            naive_err_sum += abs((previous_temp - actual_value) /
                                 actual_value if actual_value else 0)
    return naive_err_sum, prediction_err_sum, test_data.shape[0]