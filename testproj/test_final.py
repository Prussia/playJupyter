import pandas as pd
from scipy.stats import ttest_1samp


# import data
df = pd.read_csv('quarterly_returns.csv')

# 数据预处理：确保年份为整数
df['年份'] = df['年份'].astype(int)

# 过滤出2015到2023年的数据
df_filtered = df[(df['年份'] >= 2015) & (df['年份'] <= 2023)]

# 查看 DataFrame 中每列的数据类型
print(df_filtered.dtypes)

# 在筛选好之后，开始做数组
group1_df = df_filtered.loc[(df_filtered['分组'] == 0)] 
array1 = group1_df[["加权回报率"]].to_numpy()

group2_df = df_filtered.loc[(df_filtered['分组'] == 1)] 
array2 = group2_df[["加权回报率"]].to_numpy()

group3_df = df_filtered.loc[(df_filtered['分组'] == 2)] 
array3 = group3_df[["加权回报率"]].to_numpy()

group4_df = df_filtered.loc[(df_filtered['分组'] == 3)] 
array4 = group4_df[["加权回报率"]].to_numpy()

group5_df = df_filtered.loc[(df_filtered['分组'] == 4)] 
array5 = group5_df[["加权回报率"]].to_numpy()

# array5 - array1
array6 = array5 - array1

# 重新调整季度的映射
quarter_mapping = {
    4: '1-4',  # 代表第一季度
    8: '5-8',  # 代表第二季度
    12: '9-12'  # 代表第三季度
}

# 初始化结果存储
results = []

# 开始进行t检验
print(array1)
t_stat1, p_val1 = ttest_1samp(array1, 0)
print(t_stat1[0])
print(p_val1[0])


print(array2)
t_stat2, p_val2 = ttest_1samp(array2, 0)
print(t_stat2[0])
print(p_val2[0])

print(array3)
t_stat3, p_val3 = ttest_1samp(array3, 0)
print(t_stat3[0])
print(p_val3[0])

print(array4)
t_stat4, p_val4 = ttest_1samp(array4, 0)
print(t_stat4[0])
print(p_val4[0])

print(array5)
t_stat5, p_val5 = ttest_1samp(array5, 0)
print(t_stat5[0])
print(p_val5[0])

print(array6)
t_stat6, p_val6 = ttest_1samp(array6, 0)
print(t_stat6[0])
print(p_val6[0])




