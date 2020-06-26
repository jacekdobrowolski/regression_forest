import random_forest
from preparedata import *


if __name__ == '__main__':
    df = load()
    delayed_df = delay(df, 2)
    forest_result = list()
    naive_result = list()

    iterations = 10
    x_axis = range(10, 100, 10)
    for x in x_axis:
        random_forest.tree.config.create_config(min_split_size=10, number_of_predictors_to_draw=5)
        random_forest.forest.config.create_config(data_size_for_tree=140, number_of_trees=x)

        naive_err_sum, forest_err_sum, test_data_count = test(delayed_df, iterations)

        naive_result.append(naive_err_sum/(iterations*test_data_count)*100)
        forest_result.append(forest_err_sum/(iterations*test_data_count)*100)

    import matplotlib.pyplot as plt

    plt.plot(x_axis, forest_result, label="forest")
    plt.plot(x_axis, naive_result, label="naive")
    plt.xlabel('Ilość drzew')
    plt.ylabel('Średni błąd względny')
    plt.title('Wpływ ilości drzew')
    plt.legend()
    plt.show()