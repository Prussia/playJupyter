import pandas as pd

# import data
df = pd.read_excel('计算.xlsx')

df['季度'] = pd.cut(df['月份'], bins=[0, 4, 8, 12], labels=['4', '8', '12'], right=False)

# 自定义函数计算复合回报率
def compound_return(x):
    return (1 + x).prod() - 1

# 使用自定义函数计算每个季度的复合回报率
quarterly_returns = df.groupby(['年份', '分组', '季度'])['加权回报率'].apply(compound_return).reset_index()

# 将'Quarter'列的值替换为对应的月份
quarterly_returns['月份'] = quarterly_returns['季度'].replace({'4': '1-4', '8': '5-8', '12': '9-12'})


# 输出结果
quarterly_returns.to_excel('quarterly_returns.xlsx', index=False)