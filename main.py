
if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    import time

    df = pd.read_csv('alpha24_step15Stud.csv')

    df['temp'] = df['temp'].apply(lambda x: x.replace(',','.')).astype('float64')
    df['Ts'] = df['Ts'].apply(lambda x: x.replace(',','.')).astype('float64')
    df.rename(columns={"czas(min)": "time", "alpha": "compressor", "temp": 'ambient_temp', "Ts": 'refrigerator_temp'}, inplace=True)
    df.set_index('time', inplace=True)

    delay = 2
    frames = [df.shift(-t) for t in range(delay)]
    # small_df = df.iloc[:40]
    delayed_df = pd.concat(frames, axis=1).dropna()

    import random_forest
    from random_forest.tree import Tree
    from random_forest.forest import Forest

    random_forest.tree.config.create_config(min_split_size=5, number_of_predictors_to_draw=3)
    random_forest.forest.config.create_config(data_size_for_tree=50, number_of_trees=200)

    start = time.perf_counter()
    forest = Forest(delayed_df)
    finish = time.perf_counter()
    print(f"Forest created in {finish-start} second(s)")

    print(f"Out of bag data size {forest.out_of_bag.shape[0]}")
    prediction_err_sum = 0
    actual_value = 0
    naive_err_sum = 0
    for test_data in forest.out_of_bag.values:
        actual_value = test_data[-1]
        prediction_err_sum += abs(forest.predict(test_data[:-1]) - actual_value)/actual_value
        naive_err_sum =+ abs(test_data[-4] - actual_value)/actual_value

    out_of_bag_size = forest.out_of_bag.shape[0]
    print(f"Out of bag relative error {abs(prediction_err_sum/out_of_bag_size)*100}%")
    print(f"Naive relative error {abs(naive_err_sum)/out_of_bag_size*100}%")