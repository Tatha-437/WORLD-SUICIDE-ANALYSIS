# -*- coding: utf-8 -*-
"""Global_Suicide_Rates_Visualization_CAO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R6zLddY_lNpeOi9mAo_zN2DYSfFR1TXu
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np 
import pandas as pd 
import os
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot 
init_notebook_mode(connected=True)
import plotly.graph_objs as go
from wordcloud import WordCloud
from plotly import tools
 
# %pylab inline

dataset = pd.read_csv('master.csv')
worldmap=pd.read_csv("concap.csv")

dataset.head()

# List of Countries in the Dataset
unique_country = dataset['country'].unique()
print(unique_country)

###Let's check for country
alpha = 1.0
plt.figure(figsize=(10,25))
sns.countplot(y='country', data=dataset, alpha=alpha)
plt.title('Data by country')
plt.show()

# Between Genders Male vs Female
plt.figure(figsize=(7,7))
sex = sns.countplot(x='sex',data = dataset)

# Corelation between the Data
plt.figure(figsize=(16,7))
cor = sns.heatmap(dataset.corr(), annot = True)

g = sns.jointplot(dataset.year,dataset.suicides_no, kind="kde", color="#bfa9e0" ,size=7)
plt.savefig('graph.png')

# Visualizing which age of people Suicide the most
plt.figure(figsize=(16,7))
bar_age = sns.barplot(x = 'sex', y = 'suicides_no', hue = 'age',data = dataset)

# Visualizing which Generation of people Suicide the most
plt.figure(figsize=(16,7))
bar_gen = sns.barplot(x = 'sex', y = 'suicides_no', hue = 'generation',data = dataset)

cat_accord_year = sns.catplot('sex','suicides_no',hue='age',col='year',data=dataset,kind='bar',col_wrap=3)

# Finding the year with the highest suicide
df = dataset.reset_index()
df = df.drop(["index"], axis=1)
max_suicide_year = df["year"][0]
max_suicide_year

data = dataset[(dataset['year']== max_suicide_year)]
data_as_99 = data.groupby(["age","sex"]).sum()["suicides_no"].reset_index()
data_as_99

plt.figure(figsize=(10,8))
sns.barplot(x=dataset["sex"], y=dataset["suicides_no"],hue=dataset["age"], palette=sns.color_palette("Set2"))
plt.xlabel('Sex')
plt.ylabel('Suicides')
plt.title('Suicide Rate Sex and Age')
plt.show()

sns.kdeplot(dataset.year, dataset.suicides_no, shade=True, cut=1)
plt.show()

#Visualizing the lineplot to see Suicides numbers according to year with age group
age_5 = dataset.loc[dataset.loc[:, 'age']=='5-14 years',:]
age_15 = dataset.loc[dataset.loc[:, 'age']=='15-24 years',:]
age_25 = dataset.loc[dataset.loc[:, 'age']=='25-34 years',:]
age_35 = dataset.loc[dataset.loc[:, 'age']=='35-54 years',:]
age_55 = dataset.loc[dataset.loc[:, 'age']=='55-74 years',:]
age_75 = dataset.loc[dataset.loc[:, 'age']=='75+ years',:]
plt.figure(figsize=(16,7))
#Now lets plot a line plot
age_5_lp = sns.lineplot(x='year', y='suicides_no', data=age_5)
age_15_lp = sns.lineplot(x='year', y='suicides_no', data=age_15)
age_25_lp = sns.lineplot(x='year', y='suicides_no', data=age_25)
age_35_lp = sns.lineplot(x='year', y='suicides_no', data=age_35)
age_55_lp = sns.lineplot(x='year', y='suicides_no', data=age_55)
age_75_lp = sns.lineplot(x='year', y='suicides_no', data=age_75)

#Now make the legend
leg = plt.legend(['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years'])

#Visualizing a lineplot for a Male & Female population
male_population = dataset.loc[dataset.loc[:, 'sex']=='male',:]
female_population = dataset.loc[dataset.loc[:, 'sex']=='female',:]

# Set figure size
plt.figure(figsize=(16,7))

#Plot the Lineplot
lp_male = sns.lineplot(x = 'year' , y = 'suicides_no' , data = male_population)
lp_female = sns.lineplot(x = 'year' , y = 'suicides_no' , data = female_population)
leg1 = plt.legend(['Males','Females'])

group_dataset=dataset.groupby(['age','sex'])['suicides_no'].sum().unstack()
group_dataset=group_dataset.reset_index().melt(id_vars='age')

group_dataset_female=group_dataset.iloc[:6,:]
group_dataset_male=group_dataset.iloc[6:,:]

group_dataset_female

group_dataset_male

# Visualizing the number of Suicides at diffrent ages by males and females
female_=[175437,208823,506233,16997,430036,221984]
male_=[633105,915089,1945908,35267,1228407,431134]
plot_id = 0
for i,age in enumerate(['15-24 years','25-34 years','35-54 years','5-14 years','55-74 years','75+ years']):
    plot_id += 1
    plt.subplot(3,2,plot_id)
    plt.title(age)
    fig, ax = plt.gcf(), plt.gca()
    sns.barplot(x=['female','male'],y=[female_[i],male_[i]],color='cyan')
    plt.tight_layout()
    fig.set_size_inches(10, 15)
plt.show()

index_population=[]
for age in dataset['age'].unique():
  index_population.append(sum(dataset[dataset['age']==age].population)/len(dataset[dataset['age']==age].population))
    
plt.bar(['15-24 years','35-54 years','75+ years','25-34 years','55-74 years','5-14 years'],index_population,align='center',alpha=0.5)
plt.xticks(rotation=90)
plt.show()

g = sns.lmplot(x="year", y="suicides_no", hue="generation",truncate=True, height=5, data=dataset)
# Use more informative axis labels than are provided by default
g.set_axis_labels("year", "suicides_no")
plt.show()

# Visualizing the pie chart for the Generations vs Suicide count
f,ax=plt.subplots(1,2,figsize=(18,8))
dataset['generation'].value_counts().plot.pie(explode=[0.1,0.1,0.1,0.1,0.1,0.1],autopct='%1.1f%%',ax=ax[0],shadow=True)
ax[0].set_title('generations count')
ax[0].set_ylabel('count')
sns.countplot('generation',data=dataset,ax=ax[1])
ax[1].set_title('generations count')
plt.show()

sns.pairplot(dataset,hue='generation')
plt.show()

sns.pairplot(dataset, hue="sex")
plt.show()

x = dataset.iloc[:, [4, 5]].values
x

from sklearn.cluster import KMeans

wcss = []
for i in range(1, 11):
    km = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
    km.fit(x)
    wcss.append(km.inertia_)
    
plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method', fontsize = 20)
plt.xlabel('suicideno')
plt.ylabel('population')
plt.show()

km = KMeans(n_clusters = 5, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
y_means = km.fit_predict(x)

plt.scatter(x[y_means == 0, 0], x[y_means == 0, 1], s = 100, c = 'pink', label = 'score between 0 and 0.4')
plt.scatter(x[y_means == 1, 0], x[y_means == 1, 1], s = 100, c = 'yellow', label = 'score between 0.4 to 0.9')
plt.scatter(x[y_means == 2, 0], x[y_means == 2, 1], s = 100, c = 'cyan', label = 'score between 0.9 to 1.3')
plt.scatter(x[y_means == 3, 0], x[y_means == 3, 1], s = 100, c = 'magenta', label = 'score betwen 1.3 to 3.0')
plt.scatter(x[y_means == 4, 0], x[y_means == 4, 1], s = 100, c = 'orange', label = 'score more than 3.0')
plt.scatter(km.cluster_centers_[:,0], km.cluster_centers_[:, 1], s = 50, c = 'blue' , label = 'centeroid')

plt.style.use('fivethirtyeight')
plt.title('K Means Clustering', fontsize = 20)
plt.xlabel('population')
plt.ylabel('suicides')
plt.legend()
plt.grid()
plt.show()