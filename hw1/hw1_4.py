import pandas as pd
import numpy as np
from statsmodels.stats.weightstats import ztest
import scipy.stats as st

print("ok")

def check_intervals_intersect(first_ci, second_ci):   
    first_ci_inter = st.t.interval(alpha=0.95, df=len(first_ci) - 1, loc=np.mean(first_ci), scale=st.sem(first_ci))
    second_ci_inter = st.t.interval(alpha=0.95, df=len(second_ci) - 1, loc=np.mean(second_ci),scale=st.sem(second_ci))
    if first_ci_inter[1] < second_ci_inter[0] or first_ci_inter[0] > second_ci_inter[1]:
        are_intersect = False
    else:
        are_intersect = True
    return are_intersect

def check_dge_with_ci(first_table, second_table):
    ci_test_results = []
    for i in range(np.shape(first_table)[1]):
        ci_test_results.append(check_intervals_intersect(first_table.iloc[:, [i]], second_table.iloc[:, [i]]))
    return ci_test_results

def check_dge_with_ztest(first_table, second_table):
    z_test_results = []
    for i in range(np.shape(first_table)[1]):
        z_test_results.append(ztest(first_table.iloc[:, [i]], second_table.iloc[:, [i]])[1]<0.05)
    return z_test_results

def check_dge_with_ztest_p_values(first_table, second_table):
    z_test_p_values = []
    for i in range(np.shape(first_table)[1]):
        z_test_p_values.append(ztest(first_table.iloc[:, [i]], second_table.iloc[:, [i]])[1])
    return z_test_p_values

def count_mean_diff(first_table, second_table):
    mean_diff = []
    for i in range(np.shape(first_table)[1]):
        mean_diff.append(np.mean(np.array(first_table.iloc[:, [i]])) - np.mean(np.array(second_table.iloc[:, [i]])))
    return mean_diff


first_cell_type_expressions_path = input()
second_cell_type_expressions_path = input()
save_results_table = input()

expression_data_first_cell = pd.read_csv(first_cell_type_expressions_path, index_col=0)
expression_data_second_cell = pd.read_csv(second_cell_type_expressions_path, index_col=0)


ci_test_results = check_dge_with_ci(expression_data_first_cell, expression_data_second_cell)
z_test_results = check_dge_with_ztest(expression_data_first_cell, expression_data_second_cell)
z_test_p_values = check_dge_with_ztest_p_values(expression_data_first_cell, expression_data_second_cell)
mean_diff = count_mean_diff(expression_data_first_cell, expression_data_second_cell)


results = {
    "ci_test_results": ci_test_results,
    "z_test_results": z_test_results,
    "z_test_p_values": z_test_p_values,
    "mean_diff": mean_diff
}

results = pd.DataFrame(results)
results.head()
results.to_csv(save_results_table)
