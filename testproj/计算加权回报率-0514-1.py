# %% [markdown]
# ### Definition

# %%
! pip install ydata-profiling
! pip install numpy==1.22.4

# %%
import pandas as pd
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta


# %%
# import data
df1_1 = pd.read_excel('证券2.xlsx', engine='openpyxl')
df1_2 = pd.read_excel('证券1.xlsx', engine='openpyxl')
df1_3 = pd.concat([df1_1, df1_2], ignore_index=True)
df1 = df1_3[df1_3['民营指数'] >= 1]


# %%
df2 = pd.read_excel('TRD_Mnth.xlsx', engine='openpyxl')
#df3 = pd.read_excel('TRD_Mnth.xlsx', engine='openpyxl')

# %%
df3 = df2.copy()

# %%
df2.info()

# %%
df1.dtypes

# %%
df1['统计日期'] = pd.to_datetime(df1['统计截止日期'])
df2['统计日期'] = pd.to_datetime(df2['交易月份'])
df3['统计日期'] = pd.to_datetime(df3['交易月份'])

# %% [markdown]
# ### df1_sorted

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
df1_sorted

# %%
# add a new column in the df1
df1["分组"] = ""



# %%
df1

# %%
df1_copy = df1.copy()
len(df1_copy.index) 
df1_copy


# %% [markdown]
# ### Dataset df1_group
# 对公司进行分组 按照季度进行调仓

# %%

df1_group = pd.DataFrame()

df1_year_keymonth_size = 0

# 对公司进行分组 按照季度进行调仓
for year in df1['统计日期'].dt.year.unique():
    print('****** loop *******')
    print(year)
    
    
    for key, key_month in report_months.items():
        print('*****loop 季度*****')
        print(key)
        print(key_month)
         
        df1_year_keymonth = df1.loc[(df1['统计日期'].dt.year == year ) & (df1['统计日期'].dt.month == key_month)]
        
        df1_year_keymonth['分组'] = pd.qcut(df1_year_keymonth['其他持股比例'], 5, labels=False, duplicates='drop')
        
        df1_year_keymonth.info()
        
        df1_year_keymonth_size += len(df1_year_keymonth.index) 
        
        df1_group = df1_group.append(df1_year_keymonth, ignore_index=True)
        
        
df1_group

# %%
df1_year_keymonth_size

# %%
df1_group

#df1_group.to_excel('加权权重分组.xlsx',index=False)



# %% [markdown]
# ### Dataset df2_market_value
# 
# 进行加权平均计算月度回报率（分组过后+加权之后）
# 
# 匹配时间节点上的公司市值
# 
# 匹配相应时间段的月度回报率数据
# 

# %%
# 进行加权平均计算月度回报率（分组过后+加权之后）
# 匹配时间节点上的公司市值
# 匹配相应时间段的月度回报率数据

df2_market_value = pd.DataFrame()
# loop years
for year in df2['统计日期'].dt.year.unique():
    print('*************')
    print(year)
    current_year_data = df2[df2['统计日期'].dt.year == year] # type: ignore
    print(current_year_data.head())
    
    # loop 季报 调仓时候的市值 
    for key, key_month in report_months.items():
        print('**********')
        print(key)
        print(key_month*4/3)
        current_year_df_monthly = current_year_data[current_year_data['统计日期'].dt.month == key_month*4/3]
        #print(current_year_df_monthly.info())
        #计算权重
    
        df2_market_value = df2_market_value.append(current_year_df_monthly, ignore_index=True)
        

# %%
df2_market_value.reset_index()
df1_group.reset_index()


# %%
df2_market_value

# df2_market_value.to_excel('个股市值统计.xlsx',index=False)
# df2_market_value

# %%
df2_market_value

# %%

# 假设你的DataFrame叫df，日期列叫'最新统计日期'
# 我们假设年份和日不变，只是月份改变了
df2_market_value['new_month'] = (df2_market_value['统计日期'].dt.month *3/4).astype(int)
df2_market_value['new_year'] = df2_market_value['统计日期'].dt.year
df2_market_value['new_day'] = 30  # 假设每月的第一天
df2_market_value
# 构建新的日期字符串
#df2_market_value['新统计日期'] = pd.to_datetime(df2_market_value[['new_year', 'new_month', 'new_day']])



# %%


# 假设 new_year 和 new_month 已经定义
df2_market_value['最新统计日期'] = pd.to_datetime(df2_market_value['new_year'].astype(str) + '-' + df2_market_value['new_month'].astype(str) + '-01')
df2_market_value['最新统计日期'] = df2_market_value['最新统计日期'] + pd.offsets.MonthEnd()

# %%
# df2_market_value['新统计日期'] = pd.to_datetime(df2_market_value[['new_year', 'new_month', 'new_day']])


# df2_market_value['最新统计日期'] = pd.to_datetime({
#     'year': df2_market_value['new_year'],
#     'month': df2_market_value['new_month'],
#     'day': df2_market_value['new_day']
# })

# %%
df2_market_value.drop(columns=['new_year', 'new_month', 'new_day'], inplace=True)
df2_market_value


# %%
# 设置join column
df1_group['最新统计日期'] = df1_group['统计日期']

df1_group['证券代码'] = df1_group['证券代码'].astype(str)
df1_group['最新统计日期'] = pd.to_datetime(df1_group['最新统计日期'])

df2_market_value['证券代码'] = df2_market_value['证券代码'].astype(str)
df2_market_value['最新统计日期'] = pd.to_datetime(df2_market_value['最新统计日期'])

# %%
df2_market_value.info()


# %%
df1_group.info()

# %% [markdown]
# ### df1_merged_group
# 
# merge df1_group, df2_market_value

# %%

df1_merged_group = pd.merge(df1_group, df2_market_value, on=['证券代码','最新统计日期'],how='inner')
df1_merged_group


# %%
df1_merged_group_0 = df1_merged_group[df1_merged_group['分组'] == 0]


# %%
df1_merged_group_0.tail()


# %%

# df1_merged_group_0_sum = df1_merged_group_0.groupby(by=["最新统计日期"]).sum()
# df1_merged_group_0_sum

# %% [markdown]
# ### 个股 市值权重 in group and date
# 
# 根据df1 group， 进行个股权重计算

# %%
# # 取个股 市值 by date / 组内市值总和
# # save in a new dataframe
# # ['证券代码'] ['个股市值'] ['个股组内权重']
def getDF_stock_weight_group(df1_merged_group, df1_merged_group_sum):
    df_stock_weight_group = pd.DataFrame(columns=['证券代码', '个股市值', '个股组内权重', '最新统计日期'] )
    
    for index, row in df1_merged_group.iterrows():
        # print(row['证券代码'])
        # print(row['个股市值'])
        # print(row['最新统计日期'])
        # print('group market value')
        group_row = df1_merged_group_sum[df1_merged_group_sum.index == row['最新统计日期']]
        # print(group_row['个股市值'])
        
        stock_weight = row['个股市值'] / group_row['个股市值'].item()   
        
        # print('stock_weight=======')
        # print(stock_weight)
        
        data = {'证券代码': row['证券代码'], '个股市值': row['个股市值'], '个股组内权重':stock_weight, '最新统计日期': row['最新统计日期'].to_pydatetime()}
        # print(data)
    
        df_stock_weight_group = df_stock_weight_group.append(data, ignore_index=True)
    
    return df_stock_weight_group


# %%

def getDF_stock_weight_group_by_number(index, df1_merged_group):
    
    df1_merged_group = df1_merged_group[df1_merged_group['分组'] == index]
    
    #sum
    df1_merged_group_sum = df1_merged_group.groupby(by=["最新统计日期"]).sum()
    
    df_stock_weight_group = getDF_stock_weight_group(df1_merged_group, df1_merged_group_sum)   
    
    return df_stock_weight_group

# %%

df_stock_weight_group0 = getDF_stock_weight_group_by_number(0, df1_merged_group)
df_stock_weight_group0

# %%
df_stock_weight_group1 = getDF_stock_weight_group_by_number(1, df1_merged_group)
df_stock_weight_group1

# %%
df_stock_weight_group2 = getDF_stock_weight_group_by_number(2, df1_merged_group)
df_stock_weight_group2

# %%
df_stock_weight_group3 = getDF_stock_weight_group_by_number(3, df1_merged_group)
df_stock_weight_group3

# %%
df_stock_weight_group4 = getDF_stock_weight_group_by_number(4, df1_merged_group)
df_stock_weight_group4

# %%
# sum_a = df_stock_weight_group4['个股组内权重'].sum()

# sum_a

# %% [markdown]
# # Dataset 月度回报率

# %% [markdown]
# ### Description
# 
# trd_month as datasource
# 
# 每个 个股 交易时间 
# 
# 每个个股 在每个季度的权重  in df_stock_weight_groupN
# 
# 个股组内权重 at timestamp （xxxx-03, xxxx-06, xxxx-09）
# 
# 个股组内权重 * 4个月 个股月度回报率 （最新统计日期）
# 
# 
# a new dataframe - seucrity code, datetime, weighted stock monthly return
# 
# weighted stock monthly return = weight (3 kinds) *  monthly return (12 months)
# 

# %%
df3['DATE'] = df3['统计日期'].dt.date

df3['统计日期-4'] = df3['DATE'] - relativedelta(months = 4)
df3.info


# %%
df3.head()

# %% [markdown]
# # Comment

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


