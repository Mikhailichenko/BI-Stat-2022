import pandas as pd
import numpy as np
from statsmodels.stats.weightstats import ztest
from statsmodels.stats.multitest import multipletests
import scipy.stats as st


def check_intervals_intersect(first_ci, second_ci):   
    first_ci_inter = st.t.interval(alpha=0.95, df=len(first_ci) - 1, loc=np.mean(first_ci), scale=st.sem(first_ci))
    second_ci_inter = st.t.interval(alpha=0.95, df=len(second_ci) - 1, loc=np.mean(second_ci),scale=st.sem(second_ci))
    are_intersect = not(first_ci_inter[1] < second_ci_inter[0] or first_ci_inter[0] > second_ci_inter[1])
    return are_intersect

def check_dge_with_ci(first_table, second_table):
    ci_test_results = []
    for i in range(np.shape(first_table)[1]):
        ci_test_results.append(check_intervals_intersect(first_table.iloc[:, [i]], second_table.iloc[:, [i]]))
    return ci_test_results

def check_dge_with_ztest(first_table, second_table):
    z_test_results = []
    for i in range(np.shape(first_table)[1]):
        z_test_results.append(float(ztest(first_table.iloc[:, [i]], second_table.iloc[:, [i]])[1])<0.05)
    return z_test_results

def check_dge_with_ztest_p_values(first_table, second_table):
    z_test_p_values = []
    for i in range(np.shape(first_table)[1]):
        z_test_p_values.append(float(ztest(first_table.iloc[:, [i]], second_table.iloc[:, [i]])[1]))
    return z_test_p_values

def count_mean_diff(first_table, second_table):
    mean_diff = []
    for i in range(np.shape(first_table)[1]):
        mean_diff.append(np.mean(np.array(first_table.iloc[:, [i]])) - np.mean(np.array(second_table.iloc[:, [i]])))
    return mean_diff

def correct_p_values(p_values, met, a=0.05):
    p_values_corrected = multipletests(p_values, alpha=a, method=met)
    return p_values_corrected

first_cell_type_expressions_path = input("Enter the path to the file with data on expression in the cell of the first type \n")
second_cell_type_expressions_path = input("Enter the path to the file with data on expression in the cell of the second type \n")
save_results_table = input("Enter the path to the file where the table with the results will be saved \n")

expression_data_first_cell = pd.read_csv(first_cell_type_expressions_path, index_col=0)
expression_data_second_cell = pd.read_csv(second_cell_type_expressions_path, index_col=0)


ci_test_results = check_dge_with_ci(expression_data_first_cell, expression_data_second_cell)
z_test_results = check_dge_with_ztest(expression_data_first_cell, expression_data_second_cell)
z_test_p_values = check_dge_with_ztest_p_values(expression_data_first_cell, expression_data_second_cell)
mean_diff = count_mean_diff(expression_data_first_cell, expression_data_second_cell)
met = input("Enter a method of correction for multiple comparisons \n bonferroni, sidak, holm-sidak, holm, simes-hochberg, hommel, fdr_bh, fdr_by, fdr_tsbh or fdr_tsbky \n")
if met != "":
    z_test_p_values_corrected = correct_p_values(z_test_p_values, met)

results = {
    "Gene": expression_data_first_cell.columns,
    "ci_test_results": ci_test_results,
    "z_test_results": z_test_results,
    "z_test_p_values": z_test_p_values,
    "mean_diff": mean_diff
}

if met != "":
    results[f"z_test_corrected_{met}"] = z_test_p_values_corrected[0]
    results[f"z_test_p_values_corrected_{met}"] = z_test_p_values_corrected[1]

results = pd.DataFrame(results)
results.head()
results.to_csv(save_results_table)