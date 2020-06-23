
if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    import time
    import matplotlib. pyplot as plt

    df = pd.read_csv('alpha24_step15Stud.csv')

    df['temp'] = df['temp'].apply(lambda x: x.replace(',','.')).astype('float64')
    df['Ts'] = df['Ts'].apply(lambda x: x.replace(',','.')).astype('float64')
    df.rename(columns={"czas(min)": "time", "alpha": "compressor", "temp": 'ambient_temp', "Ts": 'refrigerator_temp'}, inplace=True)
    df.set_index('time', inplace=True)


    df["ambient_refrigerator_diff"] = df["ambient_temp"] - df["refrigerator_temp"]
    df_diff = df.diff().rename(columns={"refrigerator_temp": "refrigerator_temp_diff", "ambient_temp": "ambient_temp_diff"}).loc[:, ["refrigerator_temp_diff","ambient_temp_diff"]]
    frames = [df, df_diff]
    df = pd.concat(frames, axis=1).dropna()
    df.describe()

    delay = 1
    frames = [df.shift(-t) for t in range(delay)]
    # small_df = df.iloc[:40]
    delayed_df = pd.concat(frames, axis=1).dropna()

    to_be_predicted = delayed_df.iloc[:,-2].shift(-1)

    actual_refrigerator_temp = delayed_df.iloc[:,-4].shift(-1)

    final_df = pd.concat([delayed_df, to_be_predicted, actual_refrigerator_temp], axis=1).dropna()

    # training_data = final_df.iloc[:-100, :]
    # test_data = final_df.iloc[-100:, :]

    test_data = final_df.sample(100)
    training_data = final_df[~final_df.index.isin(test_data.index)]
            

    import random_forest.tree
    import random_forest.forest

    random_forest.tree.config.create_config(min_split_size=10, number_of_predictors_to_draw=6)
    random_forest.forest.config.create_config(data_size_for_tree=100, number_of_trees=100)

    from random_forest.tree import Tree
    from random_forest.forest import Forest

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
        prediction_err_sum += abs(((forest.predict(test[:-2]) + previous_temp) - actual_value))
        naive_err_sum += abs((previous_temp - actual_value))
        result.append([previous_temp, forest.predict(test[:-2]) + previous_temp, actual_value])
    # out_of_bag_size = forest.out_of_bag.shape[0]
    print("test data:")
    print(f"Forest mean error {(prediction_err_sum/test_data.shape[0])}%")
    print(f"Naive mean error {(naive_err_sum/test_data.shape[0])}%")
    result_df = pd.DataFrame(result, columns=['previous_temp', 'forest prediction', 'actual value'])
    

    # import matplotlib.pyplot as plt
    # plt.plot((result_df.iloc[:,-2] - result_df.iloc[:,-1]))
    # plt.plot((result_df.iloc[:,0] - result_df.iloc[:,-1]))
    # plt.show()

    actual_value = 0
    naive_err_sum = 0
    prediction_err_sum = 0
    result = list()
    for test in training_data.values:
        previous_temp = test[-6]
        actual_value = test[-1]
        prediction_err_sum += abs(((forest.predict(test[:-2]) + previous_temp) - actual_value))
        naive_err_sum += abs((previous_temp - actual_value))
        result.append([previous_temp, forest.predict(test[:-2]) + previous_temp, actual_value])
    # out_of_bag_size = forest.out_of_bag.shape[0]
    print("training data:")
    print(f"Forest mean error {(prediction_err_sum/training_data.shape[0])}%")
    print(f"Naive mean error {(naive_err_sum/training_data.shape[0])}%")

    actual_value = 0
    naive_err_sum = 0
    prediction_err_sum = 0
    result_123 = list()
    for test in training_data.values:
        previous_temp = test[-6]
        actual_value = test[-1]
        abs(((forest.predict(test[:-2]) + previous_temp) - actual_value))
        naive_err_sum += abs((previous_temp - actual_value))
        result_123.append(forest.predict(test[:-2]))
    # out_of_bag_size = forest.out_of_bag.shape[0]
    print("training data:")
    print(f"Forest mean error {(prediction_err_sum/training_data.shape[0])}%")
    print(f"Naive mean error {(naive_err_sum/training_data.shape[0])}%")

    import matplotlib.pyplot as plt
    plt.plot(result_123)
    plt.show()

    print(pd.DataFrame(result_123).describe())
   