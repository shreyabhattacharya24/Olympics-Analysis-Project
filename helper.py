import numpy as np
def medal_tally(df):
    # correct data
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
        ['Gold', 'Silver', 'Bronze'], ascending=[False, False, False]).reset_index()
    medal_tally['Total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    medal_tally['Gold']=medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['Total'] = medal_tally['Total'].astype(int)

    return medal_tally

#Returns sorted list of Year and Countries present in df
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

#no. of medals won by i/p country in i/p year
def fetch_medal_tally(df, year, country):
    #all players won in a team are recorded as medal winner. So we will remove duplicates 1st to keep single record onlu
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if (year == 'Overall') & (country == 'Overall'):
        temp_df = medal_tally
    if (year == 'Overall') & (country != 'Overall'):
        flag = 1
        temp_df = medal_tally[medal_tally['region'] == country]
    if (year != 'Overall') & (country == 'Overall'):
        temp_df = medal_tally[medal_tally['Year'] == int(year)]
    if (year != 'Overall') & (country != 'Overall'):
        temp_df = medal_tally[(medal_tally['region'] == country) & (medal_tally['Year'] == int(year))]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=False).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
            ['Gold', 'Silver', 'Bronze'], ascending=[False, False, False]).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    x['Total'] = x['Total'].astype(int)

    return x


#no. of nations/events/athletes participating every year
def participation_data_over_time(df,country):
    nations_by_year = df.drop_duplicates(['Year', country])['Year'].value_counts().reset_index().rename(
        columns={'index': 'Years', 'Year': country})
    return nations_by_year

#most sucessfull athlete in a sport
def most_successful_athlete(df,sport):
    temp=df.dropna(subset=['Medal'])
    if sport!='Overall':
        temp=temp[temp['Sport']==sport]
    x= temp['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    return x

#Total medals won by a country every year
def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

#Total medals won in evry sport by a country every year
def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    new_df=new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return new_df

#To 10 athletes of a country
def most_successful_athlete_in_country(df,country):
    temp=df.dropna(subset=['Medal'])
    if country!='Overall':
        temp=temp[temp['region']==country]
    x= temp['Name'].value_counts().reset_index().head(10).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    return x

#return df with all athletes in a sport
def weight_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport!='Overall':
         temp = athlete_df[athlete_df['Sport'] == sport]
         return temp
    else:
        return df

#return total men and female participating in a year
def men_vs_women(df):
    male = df[df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    female = df[df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = male.merge(female, on='Year', how='left')
    final = final.fillna(0).astype(int)
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    return final