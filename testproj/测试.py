import pandas as pd

# import data
df1 = pd.read_excel('十大股东文件1-测试.xlsx')

def classify_PO(info):
    if info == "国有法人" or info == "国家" or info == "国有法人、境外法人":
        return '国有法人持股比例'
    else:
        return '其他持股比例'
    
df1['其他持股比例'].fillna(0, inplace=True)
df1['国有法人持股比例'].fillna(0, inplace=True)

df1['是否民营股东'] = df1['股东性质'].apply(classify_PO)
df1 = df1.groupby(['统计截止日期', '证券代码', '是否民营股东'])['持股比例(%)'].sum().reset_index()
df1 = df1.pivot_table(index=['统计截止日期', '证券代码'], columns='是否民营股东', values='持股比例(%)').reset_index()
df1['民营指数'] = df1['其他持股比例'] / df1['国有法人持股比例']
df1['民营指数'].fillna(100, inplace=True)
def classify_MY(index):
    if index >= 1:
        return '民营企业'
    else:
        return '非民营企业'
df1['是否民营企业'] = df1['民营指数'].apply(classify_MY)
print(df1.head())
df1.to_excel('证券1-测试.xlsx', index=False)