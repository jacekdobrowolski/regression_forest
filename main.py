
if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    import time

    df = pd.read_csv('alpha24_step15Stud.csv')

    df['temp'] = df['temp'].apply(lambda x: x.replace(',','.')).astype('float64')
    df['Ts'] = df['Ts'].apply(lambda x: x.replace(',','.')).astype('float64')
    df.rename(columns={"czas(min)": "time", "alpha": "compressor", "temp": 'ambient_temp', "Ts": 'refrigerator_temp'}, inplace=True)
    df.set_index('time', inplace=True)



    delay = 4
    frames = [df.shift(-t) for t in range(delay)]
    # small_df = df.iloc[:40]
    delayed_df = pd.concat(frames, axis=1).dropna()



    import random_forest
    from random_forest.tree import Tree
    from random_forest.forest import Forest

    random_forest.tree.config.create_config(min_split_size=15, number_of_predictors_to_draw=5)
    
    random_forest.forest.forest_config.data_size_for_tree = 150
    random_forest.forest.forest_config.number_of_trees = 100


    start = time.perf_counter()
    forest = Forest(delayed_df)
    finish = time.perf_counter()
    print(f"Forest created in {finish-start} second(s)")

    print(forest.out_of_bag.shape)
    test = forest.out_of_bag.iloc[0].values

    print(test)
    print(forest.predict(test))