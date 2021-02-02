if __name__ == '__main__':
    import time

    import pandas as pd
    import matplotlib. pyplot as plt

    import random_forest.tree
    import random_forest.forest
    from random_forest.forest import Forest

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

    delay = 2
    frames = [df.shift(-t) for t in range(delay)]
    delayed_df = pd.concat(frames, axis=1).dropna()

    to_be_predicted = delayed_df.iloc[:, -2].shift(-1)

    actual_refrigerator_temp = delayed_df.iloc[:, -4].shift(-1)

    final_df = pd.concat([delayed_df, to_be_predicted,
                         actual_refrigerator_temp], axis=1).dropna()

    perrtraining = list()
    perrtest = list()
    naivetest = list()
    naivetraining = list()

    for i in range(10):
        test_data = final_df.sample(1000)
        training_data = final_df[~final_df.index.isin(test_data.index)]
        random_forest.tree.config.create_config(
            min_split_size=10,
            number_of_predictors_to_draw=4)
        random_forest.forest.config.create_config(data_size_for_tree=50,
                                                  number_of_trees=50)

        start = time.perf_counter()
        forest = Forest(training_data.iloc[:, :-1])
        finish = time.perf_counter()
        print(f"Forest created in {finish-start} second(s)")

        actual_value = 0
        naive_err_sum = 0
        prediction_err_sum = 0
        result = list()
        for test in test_data.values:
            previous_temp = test[-6]
            actual_value = test[-1]
            prediction_err_sum += abs(((forest.predict(test[:-2]) +
                                       previous_temp) - actual_value))
            naive_err_sum += abs((previous_temp - actual_value))
            result.append([previous_temp, forest.predict(test[:-2]) +
                           previous_temp, actual_value])

        perrtest.append(prediction_err_sum/test_data.shape[0])
        naivetest.append(naive_err_sum/test_data.shape[0])
        result_df = pd.DataFrame(
            result,
            columns=[
                'previous_temp',
                'forest prediction',
                'actual value'])

        actual_value = 0
        naive_err_sum = 0
        prediction_err_sum = 0
        result = list()
        for test in training_data.values:
            previous_temp = test[-6]
            actual_value = test[-1]
            prediction_err_sum += abs(((forest.predict(test[:-2]) +
                                        previous_temp) - actual_value))
            naive_err_sum += abs((previous_temp - actual_value))
            result.append([previous_temp, forest.predict(test[:-2]) +
                          previous_temp, actual_value])
        perrtraining.append(prediction_err_sum/training_data.shape[0])
        naivetraining.append(naive_err_sum/training_data.shape[0])

    plt.title("training data")
    plt.plot(perrtraining, label='forest training')
    plt.plot(naivetraining, label='naive training')
    plt.plot(perrtest, label="forest test")
    plt.plot(naivetest, label="naive test")
    plt.legend()
    plt.show()
