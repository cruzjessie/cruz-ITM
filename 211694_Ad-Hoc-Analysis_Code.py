#!/usr/bin/env python
# coding: utf-8

# In[1]:


#my favorite and sure starting point because there's rarely ever an error
#importing packages and the transaction file with data

import pandas as pd
import matplotlib.pyplot as plt
import json
import calendar

file = '/Users/jessie/transaction-data-adhoc-analysis.json'
lt = pd.read_json(file)


# In[2]:


# to complete the necessary data, a transaction month column is added because lola tamis requests breakdowns per month

def date(x):
    month = int(x[6:len(x)-3])
    m = calendar.month_name[month]
    return m

lt['transaction_month'] = lt['transaction_date'].apply(date).astype(pd.api.types.CategoricalDtype(categories=['January','February','March','April','May','June']))


# In[3]:


# lola tamis said she prefers if the data had one “line item” per row, so to accomplish this, at this point we are splitting up the transaction items
# using explode to transfer each item into its own row

lt['transaction_items'] = lt['transaction_items'].str.split(";")
lt_final = lt.explode('transaction_items',False)


# In[4]:


lt
# just for viewing in comparison to original file with 9 columns
# at this point we can see that there are now 10 columns after adding transaction month column
# the transaction items are also now split up 


# In[5]:


lt_final
# just for viewing
# at this point we can see that the line items are now in different rows as per lola tamis' request because of the explode function
# this data frame is now what we will be using moving forward


# In[6]:


# adding quantity column which will help in computing total prices
def quant_items(x):
    charset = [
        *[str(i) for i in range(10)]
    ]
    x = ''.join([i for i in x if i in charset])
    return int(x[-1])

lt_final['quantity_per_item'] = lt_final['transaction_items'].apply(quant_items)


# In[7]:


# cleaning up the item name 
def item(x):
    item_edited = x.split(",")[1]
    return (item_edited)

lt_final['transaction_items'] = lt_final['transaction_items'].apply(item)


# In[8]:


# computing for the price per item
price_list = {'Beef Chicharon': list(lt_final.loc[(lt_final.transaction_items == 'Beef Chicharon')].min(numeric_only=True))[0], 
              'Nutrional Milk':list(lt_final.loc[(lt_final.transaction_items == 'Nutrional Milk')].min(numeric_only=True))[0],
              'Gummy Vitamins': list(lt_final.loc[(lt_final.transaction_items == 'Gummy Vitamins')].min(numeric_only=True))[0],
              'Gummy Worms':list(lt_final.loc[(lt_final.transaction_items == 'Gummy Worms')].min(numeric_only=True))[0],
              'Kimchi and Seaweed':list(lt_final.loc[(lt_final.transaction_items == 'Kimchi and Seaweed')].min(numeric_only=True))[0],
              'Yummy Vegetables':list(lt_final.loc[(lt_final.transaction_items == 'Yummy Vegetables')].min(numeric_only=True))[0],
              'Orange Beans':list(lt_final.loc[(lt_final.transaction_items == 'Orange Beans')].min(numeric_only=True))[0]}


# In[9]:


# adding column of price per item 
def price_per_item(x):
    final_price_list = {'Beef Chicharon': 1299, 'Nutrional Milk': 1990, 'Gummy Vitamins': 1500, 'Gummy Worms': 150, 'Kimchi and Seaweed': 799, 'Yummy Vegetables': 500,'Orange Beans': 199}
    return final_price_list[x]
    
lt_final['price_per_item'] = lt_final['transaction_items'].apply(price_per_item)


# In[10]:


# computing for total prices by multiplying quantity per item to price per item 
lt_final['total_price_per_item'] = lt_final['quantity_per_item'] * lt_final['price_per_item']

# ordering the columns properly
lt_final = lt_final[['name','transaction_items','price_per_item','quantity_per_item','total_price_per_item','transaction_value','transaction_month','transaction_date']]


# In[11]:


lt_final
# this is the cleaned transaction data with all relevant information


# In[12]:


# creating the breakdown of the count of each item sold per month in a pivot table
count_of_items_sold_per_month = pd.pivot_table(lt_final, index='transaction_month', columns='transaction_items',values='quantity_per_item',aggfunc=sum)


# In[13]:


#graphing the pivot table of the count of each item sold per month to help analysis
a=count_of_items_sold_per_month.plot.line(figsize=(10,7.5))
a.set_xlabel('months')
a.set_ylabel('count')
a.set_title('counts of items purchased per month')


# In[14]:


count_of_items_sold_per_month=count_of_items_sold_per_month.transpose()

count_of_items_sold_per_month
#second of two pivot tables


# In[15]:


# creating the breakdown of the total sale value per item per month in a pivot table
sale_value_per_item_per_month = pd.pivot_table(lt_final, index='transaction_month', columns='transaction_items',values='total_price_per_item',aggfunc='sum')


# In[16]:


#graphing the pivot table of the total sale value per item per month to help analysis
a=sale_value_per_item_per_month.plot.bar(figsize=(10,7.5))
a.set_xlabel('months')
a.set_ylabel('revenue value')
a.set_title('sale value of items per month')


# In[17]:


sale_value_per_item_per_month=sale_value_per_item_per_month.transpose()

sale_value_per_item_per_month
#second of two pivot tables


# In[18]:


lt['bin']=1
# this is the bin column from the very first file 


# In[19]:


bin_value = pd.pivot_table(lt,index='name',columns='transaction_month',values='bin',aggfunc='count',margins=True)


# In[20]:


# repeater table containing months and the number of customers from the current month who also purchased in the previous month

repeater = {'January':0, 
            'February':len(bin_value[(bin_value.January >= 1) & (bin_value.February >= 1)])-1,
            'March':len(bin_value[(bin_value.February >= 1) & (bin_value.March >= 1)])-1,
            'April':len(bin_value[(bin_value.March >= 1) & (bin_value.April >= 1)])-1,
            'May': len(bin_value[(bin_value.April >= 1) & (bin_value.May >= 1)])-1,
            'June': len(bin_value[(bin_value.May >= 1) & (bin_value.June >= 1)])-1}


# In[21]:


repeater
# just for viewing


# In[22]:


# inactive table containing months and the number of customers in the total set of transactions up to and including the current month who have purchase history but do not have a purchase for the current month
inactive = {'January':0, 
            'February':len(bin_value[(bin_value.January >= 0) & (bin_value.February == 0)])-len(bin_value[(bin_value.January == 0) & (bin_value.February == 0)]),
            'March':len(bin_value[(bin_value.January >= 0) & (bin_value.February >= 0) & (bin_value.March == 0)])-len(bin_value[(bin_value.January == 0) & (bin_value.February == 0) & (bin_value.March == 0)]),
            'April':len(bin_value[(bin_value.January >= 0) & (bin_value.February >= 0) & (bin_value.March >= 0) & (bin_value.April == 0)]) - len(bin_value[(bin_value.January == 0) & (bin_value.February == 0) & (bin_value.March == 0) & (bin_value.April == 0)]),
            'May': len(bin_value[(bin_value.January >= 0) & (bin_value.February >= 0) & (bin_value.March >= 0) & (bin_value.April >= 0) & (bin_value.May == 0)]) - len(bin_value[(bin_value.January == 0) & (bin_value.February == 0) & (bin_value.March == 0) & (bin_value.April == 0) & (bin_value.May == 0)]),
            'June': len(bin_value[(bin_value.January >= 0) & (bin_value.February >= 0) & (bin_value.March >= 0) & (bin_value.April >= 0) & (bin_value.May >= 0) & (bin_value.June == 0)])-- len(bin_value[(bin_value.January == 0) & (bin_value.February == 0) & (bin_value.March == 0) & (bin_value.April == 0) & (bin_value.May == 0) & (bin_value.June == 0)])}


# In[23]:


inactive
# just for viewing


# In[24]:


# engaged table containing months and he number of customers in the total set of transactions up to and including the current month who have consistently purchased every single month
engaged = {'January':len(bin_value[bin_value.January >= 1])-1, 
            'February':len(bin_value[(bin_value.January >= 1) & (bin_value.February >= 1)])-1,
            'March':len(bin_value[(bin_value.January >= 1) & (bin_value.February >= 1) & (bin_value.March >= 1)])-1,
            'April':len(bin_value[(bin_value.January >= 1) & (bin_value.February >= 1) & (bin_value.March >= 1) & (bin_value.April >= 1)])-1,
            'May': len(bin_value[(bin_value.January >= 1) & (bin_value.February >= 1) & (bin_value.March >= 1) & (bin_value.April >= 1) & (bin_value.May >= 1)])-1,
            'June': len(bin_value[(bin_value.January >= 1) & (bin_value.February >= 1) & (bin_value.March >= 1) & (bin_value.April >= 1) & (bin_value.May >= 1) & (bin_value.June >= 1)])-1}


# In[25]:


engaged
# just for viewing


# In[26]:


# additional first table given other useful activity metrics as requested by lola tamis
# first table containing months and the number of customers that purchased for the first time in 2022

first = {'January':len(bin_value[bin_value.January >= 1]),
        'February':len(bin_value[(bin_value.January == 0) & (bin_value.February >= 1)]),
        'March':len(bin_value[(bin_value.January == 0) & (bin_value.February == 0) & (bin_value.March >= 1)]),
        'April':len(bin_value[(bin_value.January == 0) & (bin_value.February == 0) & (bin_value.March == 0) & (bin_value.April >= 1)]),
        'May': len(bin_value[(bin_value.January == 0) & (bin_value.February == 0) & (bin_value.March == 0) & (bin_value.April == 0) & (bin_value.May >= 1)]),
        'June': len(bin_value[(bin_value.January == 0) & (bin_value.February == 0) & (bin_value.March == 0) & (bin_value.April == 0) &(bin_value.May == 0) & (bin_value.June >= 1)])}


# In[27]:


first
#just for viewing


# In[28]:


# putting the data collected for repeater, inactive and engaged in one table or data frame together, along with the additional data for first timers

table_data ={'repeater':repeater,
        'inactive':inactive,
        'engaged':engaged,
        'first timers':first}

final_table = pd.DataFrame.from_dict(table_data, orient ='index') 


# In[29]:


final_table
# this is the final table containing customer activity data

