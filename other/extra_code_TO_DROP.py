'''train_df["totals.transactionRevenue"] = train_df["totals.transactionRevenue"].astype('float')
gdf = train_df.groupby("fullVisitorId")["totals.transactionRevenue"].sum().reset_index()

plt.figure(figsize=(8,6))
plt.scatter(range(gdf.shape[0]), np.sort(np.log1p(gdf["totals.transactionRevenue"].values)))
plt.xlabel('index', fontsize=12)
plt.ylabel('TransactionRevenue', fontsize=12)
plt.show()'''

'''nzi = pd.notnull(train_df["totals.transactionRevenue"]).sum()
nzr = (gdf["totals.transactionRevenue"]>0).sum()
print("Number of instances in train set with non-zero revenue : ", nzi, " and ratio is : ", nzi / train_df.shape[0])
print("Number of unique customers with non-zero revenue : ", nzr, "and the ratio is : ", nzr / gdf.shape[0])'''

'''print("Number of unique visitors in train set : ",train_df.fullVisitorId.nunique(), " out of rows : ",train_df.shape[0])
print("Number of unique visitors in test set : ",test_df.fullVisitorId.nunique(), " out of rows : ",test_df.shape[0])
print("Number of common visitors in train and test set : ",len(set(train_df.fullVisitorId.unique()).intersection(set(test_df.fullVisitorId.unique())) ))'''

'''numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

newdf = df.select_dtypes(include=numerics)'''

# In[46]:


#"transactionRevenue" in train_df


# In[47]:


#print(len(set(train_df.columns)) - len(set(train_df.columns).intersection(set(test_df.columns))))
#print(len(set(test_df.columns)) - len(set(train_df.columns).intersection(set(test_df.columns))))

#set(train_df.columns).difference(set(train_df.columns).intersection(set(test_df.columns)))


# In[48]:

# non più usata
def add_cols(train, test, new_train, new_test, commons):
    for feat in commons:
        train[feat] = new_train[feat]
        test[feat] = new_test[feat]

    return train, test


def weekday_hour(df, column):
    weekday = []
    vect = pd.to_datetime(df[column])

    for x in vect:
        weekday += [x.weekday()]

    df["weekday"] = weekday

    hour = []

    for x in vect:
        hour += [x.hour]

    df["hour"] = hour

    # synth_cols+=["weekday"]
    # synth_cols+=["hour"]

    return df


# train_df = weekday_hour(train_df,"visitStartTime")

# test_df = weekday_hour(test_df,"visitStartTime")

def day_month_year(df, column):
    month = []
    vect = df[column].astype(int)

    for x in vect:
        month += [x // 100 % 100]

    df["month"] = month

    day = []

    for x in vect:
        day += [int(x % 100)]

    df["day"] = day

    year = []

    for x in vect:
        year += [x // 10000]

    df["year"] = year

    # synth_cols+=["month"]
    # synth_cols+=["day"]
    # synth_cols+=["year"]

    return df

# train_df = day_month_year(train_df,"date")

# test_df = day_month_year(test_df,"date")

#non piu usata perchè porta ad una scarsa(ma rapida) convergenza (in termini di accuratezza)


'''params = {
        "objective" : "regression",
        "metric" : "rmse", 
        "num_leaves" : 80,
        "learning_rate" : 0.004,
        "boosting":"rf",
        "feature_fraction":0.5,
        "bagging_freq":0,
        "min_child_samples":20,
        "verbosity" : -1
    }'''

'''params = {
    'num_leaves':100,
    'objective':'regression',
    "metric" : "rmse", 
    'max_depth':-1,
    'learning_rate':0.004,
    "min_child_samples":20,
    "boosting":"rf",
    "feature_fraction":0.99,
    "bagging_freq":20,
    "bagging_fraction":0.99 ,
    #"bin_construct_sample_cnt":200000,
    "bagging_seed": 13
}'''

#sub_df.to_csv("baseline_lgb.csv", index=False)


# In[ ]:


'''fig, ax = plt.subplots(figsize=(12,18))
lgb.plot_importance(model, max_num_features=50, height=0.8, ax=ax)
ax.grid(False)
plt.title("LightGBM - Feature Importance", fontsize=15)
plt.show()'''


# In[ ]:

'''def add_char(x):
    return x+"lol"


train_df.columns = up.mappa(add_char,train_df.columns)
test_df.columns = up.mappa(add_char,test_df.columns)
cat_cols = up.mappa(add_char,cat_cols)
num_cols = up.mappa(add_char,num_cols)'''





