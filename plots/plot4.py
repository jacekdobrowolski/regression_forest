import matplotlib.pyplot as plt

import random_forest
import preparedata


if __name__ == '__main__':
    df = preparedata.load()
    delayed_df = preparedata.delay(df, 2)
    forest_result = list()
    naive_result = list()

    iterations = 10
    x_axis = range(10, 500, 50)
    for x in x_axis:
        random_forest.tree.config.create_config(
            min_split_size=30,
            number_of_predictors_to_draw=5)
        random_forest.forest.config.create_config(
            data_size_for_tree=x,
            number_of_trees=50)

        naive_err_sum, forest_err_sum, test_data_count = preparedata.test(
            delayed_df,
            iterations)

        naive_result.append(naive_err_sum/(iterations*test_data_count)*100)
        forest_result.append(forest_err_sum/(iterations*test_data_count)*100)

    plt.plot(x_axis, forest_result, label="forest")
    plt.plot(x_axis, naive_result, label="naive")
    plt.xlabel('Ilość danych do budowy drzew')
    plt.ylabel('Średni błąd względny')
    plt.title('Wpływ ilości danych w drzewe')
    plt.legend()
    plt.show()
