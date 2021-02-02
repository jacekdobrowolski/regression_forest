import matplotlib.pyplot as plt

import random_forest
import preparedata


df = preparedata.load()
delayed_df = preparedata.delay(df, 2)
forest_result = list()
naive_result = list()

iterations = 10
x_axis = range(10, 130, 20)
for x in x_axis:
    random_forest.tree.config.create_config(
        min_split_size=x,
        number_of_predictors_to_draw=4)
    random_forest.forest.config.create_config(
        data_size_for_tree=140,
        number_of_trees=50)

    naive_err_sum, forest_err_sum, test_data_count = preparedata.test(
        delayed_df,
        iterations)

    naive_result.append(naive_err_sum/(iterations*test_data_count)*100)
    forest_result.append(forest_err_sum/(iterations*test_data_count)*100)

plt.plot(x_axis, forest_result, label="forest")
plt.plot(x_axis, naive_result, label="naive")
plt.xlabel('Rozmiar liścia')
plt.ylabel('Średni błąd względny')
plt.title('Wpływ rozmiaru liścia')
plt.legend()
plt.show()
