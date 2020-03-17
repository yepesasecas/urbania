import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Set the palette and style to be more minimal
sns.set(style='ticks', palette='Set2')

fnames = ['totalArea', 'roofedSurface', 'bedrooms', 'bathrooms', 'halfBathrooms',
            'antiquity', 'parkingSlots', 'priceAmount', 'priceCurrencyId']

# train_df_filter = train_df[train_df.priceAmount > 300000]
# train_df_filter = train_df_filter[train_df_filter.priceAmount < 800000]
# print("\n\n-------------------- BUY -----------------\n\n")
buy_df = pd.read_csv("urbania_buy.csv")
buy_df = buy_df.filter(items=fnames)
buy_df["pricePerMt2"] = buy_df.apply(lambda x: x['priceAmount']/x['roofedSurface'], axis=1)

y = buy_df['priceAmount']
removed_outliers = y.between(y.quantile(.05), y.quantile(.95))
buy_df_filtered = buy_df[removed_outliers]

y = buy_df_filtered['roofedSurface']
removed_outliers = y.between(y.quantile(.05), y.quantile(.95))
buy_df_filtered = buy_df_filtered[removed_outliers]

buy_df_filtered = buy_df_filtered[buy_df.priceCurrencyId.eq(6)]

# Rent Dataframe
rent_df = pd.read_csv("urbania_rent.csv")
rent_df = rent_df.filter(items=fnames)
rent_df["pricePerMt2"] = rent_df.apply(lambda x: x['priceAmount']/x['roofedSurface'], axis=1)

y = rent_df['priceAmount']
removed_outliers = y.between(y.quantile(.05), y.quantile(.95))
rent_df_filtered = rent_df[removed_outliers]

y = rent_df_filtered['roofedSurface']
removed_outliers = y.between(y.quantile(.05), y.quantile(.95))
rent_df_filtered = rent_df_filtered[removed_outliers]

rent_df_filtered = rent_df_filtered[rent_df.priceCurrencyId.eq(6)]

print(buy_df_filtered.head())
print(rent_df_filtered.head())

print(pd.pivot_table(buy_df_filtered, values='pricePerMt2', index=['bedrooms', 'parkingSlots'],
               columns=['bathrooms'], aggfunc=np.mean).round(2))
print(pd.pivot_table(buy_df_filtered, values='pricePerMt2', index=['bedrooms', 'parkingSlots'],
               columns=['bathrooms'], aggfunc='count').round(2))

print(pd.pivot_table(rent_df_filtered, values='pricePerMt2', index=['bedrooms', 'parkingSlots'],
               columns=['bathrooms'], aggfunc=np.mean).round(2))
print(pd.pivot_table(rent_df_filtered, values='pricePerMt2', index=['bedrooms', 'parkingSlots'],
               columns=['bathrooms'], aggfunc='count').round(2))

# print(rent_df_filtered.describe())
#
# # Create the scatter plot
# sns.lmplot(x="roofedSurface", y="priceAmount", data=rent_df_filtered)
# # Remove excess chart lines and ticks for a nicer looking plot
# sns.despine()
#
# plt.show()
# buy_df_filter = buy_df[buy_df.priceCurrencyId.eq(6)]
# print(buy_df_filter.head())
# print(buy_df_filter.describe())
# print(buy_df_filter.info())
# print(buy_df_filter.corr())

#
