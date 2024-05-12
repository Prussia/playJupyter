import pandas as pd
from scipy.stats import ttest_1samp

# import data
df = pd.read_excel('quarterly_returns.xlsx')

# 数据预处理：确保年份为整数
df['年份'] = df['年份'].astype(int)

# 过滤出2014到2023年的数据
df_filtered = df[(df['年份'] >= 2014) & (df['年份'] <= 2023)]

# 查看 DataFrame 中每列的数据类型
print(df_filtered.dtypes)

# 重新调整季度的映射
quarter_mapping = {
    4: '1-4',  # 代表第一季度
    8: '5-8',  # 代表第二季度
    12: '9-12'  # 代表第三季度
}

# 初始化结果存储
results = []

# 分组和进行 t 检验
for group in df_filtered['分组'].unique():
    for year in range(2014, 2024):
        for quarter_key, quarter_str in quarter_mapping.items():
            # 对应年份和季度的数据
            data = df[(df['分组'] == group) &
                      (df['年份'] == year) &
                      (df['季度'] == quarter_key)]
            print(f"Checking group {group}, year {year}, quarter {quarter_str}: {len(data)} records found")

            if not data.empty:
                t_stat, p_val = ttest_1samp(data['加权回报率'], 0)
                results.append({
                    '分组': group,
                    '年份': year,
                    '季度': quarter_str,
                    't统计量': t_stat,
                    'p值': p_val
                })


# 创建结果DataFrame
results_df = pd.DataFrame(results)
print(results_df)



