# %%
import pandas as pd

# import data
df1_1 = pd.read_excel('证券2.xlsx', engine='openpyxl')
df1_2 = pd.read_excel('证券1.xlsx', engine='openpyxl')
df1_3 = pd.concat([df1_1, df1_2], ignore_index=True)
df1 = df1_3[df1_3['民营指数'] >= 1]
df2 = pd.read_excel('TRD_Mnth.xlsx', engine='openpyxl')


# %%
df1.head()

# %%
df1.dtypes

# %%
df1['统计日期'] = pd.to_datetime(df1['统计截止日期'])
df2['统计日期'] = pd.to_datetime(df2['交易月份'])

# %%
df1_sorted = df1.sort_values(by=['统计日期', '其他持股比例'], ascending=[True, False])
df1_sorted

# %%
# grouped_returns = pd.DataFrame()

# # 9 三季报
# # 3 一季报
# # 6 半年报
# periods = {
#     9: (1, 4),
#     3: (5, 8),
#     6: (9, 12)
# }


# %%
report_months = {
    'third': 9,
    'first': 3,
    'half': 6
}
    

# %%
df1

# %%

# 对公司进行分组 按照季度进行调仓
for year in df1['统计日期'].dt.year.unique():
    print('*************')
    print(year)
    current_year_data = df1[df1['统计日期'].dt.year == year] # type: ignore
    print(current_year_data.head())
    
    
    for key, key_month in report_months.items():
        print('**********')
        print(key)
        print(key_month)
        current_year_df_monthly = current_year_data[current_year_data['统计日期'].dt.month == key_month]
        print(current_year_df_monthly.head())
        current_year_df_monthly['分组'] = pd.qcut(current_year_df_monthly['其他持股比例'], 5, labels=False, duplicates='drop')
        print("********current_year_df_monthly.head************")
        print(current_year_df_monthly.head(10))
        
        # combine append current_year_df_monthly 
       
        
        df1_group = pd.concat([df1_group,current_year_df_monthly], ignore_index=True)
        print('*************df1_group*******************')
        print(df1_group)
        
        
        
        
        
    

# %%
df1_group.head(5000)

# %%
# 匹配时间节点上的 公司市值
df2


# %%
# join df1_group and df2

#df1_group.set_index('证券代码').join(df2.set_index('证券代码'), on=['证券代码'], lsuffix='_group', rsuffix='_df2')

#df1_group.set_index(['统计日期','证券代码']).join(df2.set_index(['统计日期','证券代码']), on=['统计日期','证券代码'],how = 'outer', lsuffix='_group', rsuffix='_df2')

df1_group_join  = df1_group.set_index(['证券代码']).join(df2.set_index(['证券代码']), on=['证券代码'],how = 'inner', lsuffix='_group', rsuffix='_df2')

df1_group_join.reset_index()


# %%
df1_group_join.dtypes
df1_group_join['统计日期_group']



# %%
#df1_final = df1_group_join[df1_group_join['统计日期_group'].dt.date == df1_group_join['统计日期_group'].dt.date]

numpy.datetime_as_string(t, unit='D')
df1_group_join['统计日期_group_string'] = 

df1_final = df1_group_join.loc[df1_group_join['统计日期_group'].dt.date == df1_group_join['统计日期_df2'].dt.date]

# %%
df1_final

# %%


# %%


# %%


# %%


# %%
# 月度回报率数据

# %%

# for month, (start_month, end_month) in periods.items():
#     # 筛选出分组月份的数据
#     df1_monthly = df1_sorted[df1_sorted['统计日期'].dt.month == month]

#     # 对每一年的数据进行操作
#     for year in df1_monthly['统计日期'].dt.year.unique():
#         # 获取当前年份和上一年的数据
#         current_year_data = df1_monthly[df1_monthly['统计日期'].dt.year == year]
#         previous_year_data = df1_monthly[df1_monthly['统计日期'].dt.year == year - 1]

#         # 对当前年份的数据进行分组
#         current_year_data['分组'] = pd.qcut(current_year_data['其他持股比例'], 5, labels=False, duplicates='drop')

#         # 遍历每个分组
#         for group in range(5):
#             # 获取上一年同一分组的证券代码
#             previous_group_codes = previous_year_data[previous_year_data['证券代码'].isin(current_year_data[current_year_data['分组'] == group]['证券代码'])]['证券代码']

#             # 计算加权回报率
#             for month in range(start_month, end_month + 1):
#                 # 获取对应月份的数据
#                 df2_monthly = df2[(df2['统计日期'].dt.year == year) & (df2['统计日期'].dt.month == month)]

#                 # 筛选出属于当前分组的股票
#                 df2_group = df2_monthly[df2_monthly['证券代码'].isin(previous_group_codes)]

#                 # 计算加权回报率
#                 total_market_value = df2_group['个股市值'].sum()
#                 df2_group['加权回报率'] = df2_group['个股市值'] / total_market_value * df2_group['个股月回报率']
#                 weighted_return = df2_group['加权回报率'].sum()

#                 # 将结果存储到grouped_returns中
#                 new_data = pd.DataFrame({
#                     '年份': [year],
#                     '月份': [month],
#                     '分组': [group],
#                     '加权回报率': [weighted_return]
#                 })

#                 grouped_returns = pd.concat([grouped_returns, new_data], ignore_index=True)
# print(grouped_returns.head())
# grouped_returns.to_excel('计算.xlsx', index=False)


