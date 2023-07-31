
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df = pd.read_excel(r'C:\Users\nitro 5\Desktop\NMIMS-Hiten\Data Wrangling\Project\Word_Population.xlsx')

df.head()


# # Droping columns which are not required and renaming few

df.rename({'Country/Territory' : 'Country',
           '2022 Population' : '2022',
           '2020 Population' : '2020',
           '2015 Population' : '2015',
           '2010 Population' : '2010',
           '2000 Population' : '2000',
           '1990 Population' : '1990',
           '1980 Population' : '1980',
           '1970 Population' : '1970'}, inplace=True, axis=1)
new_df = df.drop(['CCA3','Capital'], axis=1)
new_df

# # Checking for null values


df.isnull().sum()

# # Description of dataset

new_df.describe()

new_df.nunique(axis=0)


# # World Population Trend
plt.figure(figsize = (10, 5))
trend = new_df.iloc[:,3:11].sum()[::-1]
sns.lineplot(x=trend.index, y=trend.values, marker="o")
plt.xticks(rotation=45)
plt.ylabel("Population")
plt.title("World Population Trend (1970-2022)")
plt.show()


# # Number of countries in each continet
plt.figure(figsize = (10, 5))
sns.barplot(x = 'Continent', y = 'NumberOfCountries',
            data=new_df.groupby(['Continent'])['Country'].count().reset_index(name = 'NumberOfCountries'))
plt.ylabel('Number Of Countries', size=15)
plt.xlabel('Continent ', size=15)
plt.title('Number of countries in each continet', size=15)
plt.show()


# # Population in each continent
continent_df = new_df.groupby(by='Continent').sum()
plt.subplot(221)
continent_df['2022'].plot(kind = 'pie', figsize=(20,10), shadow=True, autopct='%1.1f%%')

plt.subplot(222)
continent_df['2015'].plot(kind = 'pie', figsize=(20,10), shadow=True, autopct='%1.1f%%')

plt.subplot(223)
continent_df['2010'].plot(kind = 'pie', figsize=(20,10), shadow=True, autopct='%1.1f%%')

plt.subplot(224)
continent_df['2000'].plot(kind = 'pie', figsize=(20,10), shadow=True, autopct='%1.1f%%')


# # Growth rate in each continent
plt.figure(figsize = (10,5))
list_of_years = ['1970','1980','1990','2000','2010','2015','2020','2022']

df_continent_population = new_df.groupby(['Continent'])[list_of_years].sum().reset_index()
df_continent_population = df_continent_population.melt(id_vars=['Continent'],
                                                       var_name='Poulation Year', value_name='Population')

plt.figure(figsize = (10,5))
sns.lineplot(data=df_continent_population, x='Poulation Year', y='Population', hue='Continent')
plt.xticks(rotation=45, fontsize = 'medium')
plt.xlabel('Poulation Year', size=15)
plt.ylabel('Population', size=15)
plt.show()


# # Growth of all countries over the years
pop = df.melt(id_vars=['Country'], value_vars=['2020', '2010', '2000', '1990', '1980', '1970'], var_name='Year', value_name='Population')
pop = pop.sort_values('Year')
fig = px.choropleth(pop, 
              locations = 'Country',
              color="Population", 
              template='plotly_dark',
              animation_frame="Year",
              color_continuous_scale='Viridis',
              locationmode='country names',
              title = 'Growth Rate(Year 1970-2020)',
              height=600
             )
fig.show()


# # Countries with highest growth rate
growth_top_10 = new_df.sort_values(by='Growth Rate',ascending=False).head(10)
growth_top_10

fig= plt.subplots(figsize=(12,8))
plt.barh(growth_top_10['Country'],growth_top_10['Growth Rate'],log=True)
plt.gca().invert_yaxis()
plt.xticks(rotation=0, fontsize = 'large')
plt.xlabel('Country', size=15)
plt.ylabel('Growth Rate', size=15)
plt.title('Top 10 Countries with Highest Growth Rate')
plt.show()


fig= plt.subplots(figsize=(12,8))

plt.plot(growth_top_10['Country'],growth_top_10['Growth Rate'],marker='o')
plt.xticks(rotation=0, fontsize = 'large')
plt.xlabel('Country', size=15)
plt.ylabel('Growth Rate', size=15)
plt.title('Top 10 Countries with Highest Growth Rate')
plt.show()


# # Population Decade-By-Decade Percent Change ¶

pop_diff = df.groupby('Continent')[['1970','1980', '1990', '2000', '2010', '2020']].sum().sort_values(by='Continent').reset_index()

pop_diff.head(7)

# finding the population decade-by-decade percent change

pop_diff['70s'] = pop_diff['1970']/pop_diff['1980']*100
pop_diff['80s'] = pop_diff['1980']/pop_diff['1990']*100
pop_diff['90s'] = pop_diff['1990']/pop_diff['2000']*100
pop_diff['00s'] = pop_diff['2000']/pop_diff['2010']*100
pop_diff['10s'] = pop_diff['2010']/pop_diff['2020']*100
pop_diff['20s'] = pop_diff['2010']/pop_diff['2020']*100

pop_diff.head(7)


# creating dataframe for decade-by-decade

decade_diff = pop_diff.groupby('Continent')[['70s','80s', '90s', '00s', '10s']].sum().sort_values(by='Continent').reset_index()

decade_diff

plt.figure(figsize = (10,5))
asian_countries = new_df[(new_df.Continent == 'Asia') &  (new_df.Rank <20)]
sns.barplot(x=asian_countries['Country'],y=asian_countries['2022'])

plt.tight_layout()
plt.show()



