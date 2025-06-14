import pandas as pd
import os 
import matplotlib.pyplot as plt

#Merging all Months Data
'''
files=[file for file in os.listdir('SalesAnalysis\Sales_Data')]

all_months_data=pd.DataFrame()

for file in files:
    df=pd.read_csv(r"SalesAnalysis/Sales_Data/"+file)
    all_months_data=pd.concat([all_months_data,df])

all_months_data.to_csv("all_data.csv",index=False)
       
'''
#Reading all the Data from One csv file

all_data=pd.read_csv('all_data.csv')
print(all_data.shape)

#Drop NaN rows

nan_df=all_data[all_data.isna().any(axis=1)]
print(nan_df.head())

all_data=all_data.dropna(how='all')
print(all_data.shape)

#Drop Columns where Months are Wrong 'Or'

all_data=all_data[all_data['Order Date'].str[0:2] != 'Or']
print(all_data.shape)

#Make Quantity and Price Column in Integer and Float

all_data['Quantity Ordered']=pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each']=pd.to_numeric(all_data['Price Each'])

#Add Months Column

all_data['Month']=all_data['Order Date'].str[0:2]
all_data['Month']=all_data['Month'].astype('int32')
print(all_data.head())
print(all_data.shape)

#Add Sales Column

all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']
print(all_data.head())

#Add city Column

def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_data['City']=all_data['Purchase Address'].apply(lambda x:f"{get_city(x)} ({get_state(x)})")
print(all_data.head())
                                                    

#Best Month for sales and How much was earned

res=all_data.groupby('Month').sum()
#print(res)
months=range(1,13)
plt.bar(months,res['Sales'])
plt.xlabel('Month Number')
plt.ylabel('Sales in USD')
plt.xticks(months)
plt.show()

#What City sold the most product

res2=all_data.groupby('City').sum()

cities=[city for city ,df in all_data.groupby('City')]

plt.bar(cities,res2['Sales'])
plt.xticks(cities,rotation='vertical',size=8)
plt.xlabel('Cities Name')
plt.ylabel('Sales in USD')
plt.show()


#what time should we display ads to maximize likelihood of customers buying product
'''
all_data['Order Date']=pd.to_datetime(all_data['Order Date'])

all_data['Hour']=all_data['Order Date'].dt.hour
print(all_data.head())
all_data['Minute']=all_data['Order Date'].dt.minute
print(all_data.head())

print(all_data.groupby(['Hour']).count())
hours=[hour for hour,df in all_data.groupby('Hour')]

plt.plot(hours,all_data.groupby(['Hour']).count())
plt.xlabel('Hour')
plt.ylabel('No of Orders')
plt.grid()
plt.show()
'''
#what Products are most often sold together

from itertools import combinations
from collections import Counter

df=all_data[all_data['Order ID'].duplicated(keep=False)]

df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x:','.join(x))

df=df[['Order ID','Grouped']].drop_duplicates()

print(df.head())

count=Counter()

for row in df['Grouped']:
    row_list=row.split(',')
    count.update(Counter(combinations(row_list,2)))

for key,value in count.most_common(10):
    print(key,value)

#what product sold the most
#why do you think it sold the most

product_group=all_data.groupby('Product')
quantity_ordered=product_group.sum()['Quantity Ordered']

products=[product for product,df in product_group]

prices=all_data[['Product','Price Each','Quantity Ordered']].groupby('Product').mean()['Price Each']

fig,ax1=plt.subplots()

ax2=ax1.twinx()
ax1.bar(products,quantity_ordered,color='g')
ax2.plot(products,prices,'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered',color='g')
ax2.set_ylabel('Price ($)',color='b')
ax1.set_xticklabels(products,rotation='vertical',size=8)

plt.show()



