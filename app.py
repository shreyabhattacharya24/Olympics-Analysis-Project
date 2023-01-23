import streamlit as st
import pandas as pd
import plotly.express as px
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
st.sidebar.title('Olympics Analysis')
st.sidebar.image('olympicslogo.png')
user_menu = st.sidebar.radio('Select an option',('Medal Tally','Overall Analysis','Country-wise Analysis','Athelete-wise Analysis'))
df=preprocessor.preprocess()
#st.dataframe(df)

if user_menu=='Medal Tally':
    st.sidebar.header('Medal Tally')

    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox('Select Year', years)
    selected_country= st.sidebar.selectbox('Select Country', country)
    new_df=helper.fetch_medal_tally(df,selected_year,selected_country)
    if (selected_year=='Overall') & (selected_country=='Overall'):
        st.title('Overall Tally')
    if (selected_year != 'Overall') & (selected_country == 'Overall'):
        st.title('Tally in year '+str(selected_year))
    if (selected_year=='Overall') & (selected_country!='Overall'):
        st.title('Overall Tally along the years of '+selected_country)
    if (selected_year!='Overall') & (selected_country!='Overall'):
        st.title('Tally of '+selected_country+ ' in year '+ str(selected_year))

    st.table(new_df)


if user_menu=='Overall Analysis':

    editions=df['Year'].unique().shape[0]
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    st.title('Top Statistics')
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('editions')
        st.title(editions)

    with col2:
        st.header('cities')
        st.title(cities)

    with col3:
        st.header('sports')
        st.title(sports)
    with col1:
        st.header('events')
        st.title(events)

    with col2:
        st.header('athletes')
        st.title(athletes)

    with col3:
        st.header('nations')
        st.title(nations)


    st.title('Total participating nations over the years')
    nation_by_year=helper.participation_data_over_time(df,'region')
    fig = px.line(nation_by_year, x='Years', y='region')
    st.plotly_chart(fig)

    st.title('Total events organized over the years')
    events_by_year = helper.participation_data_over_time(df, 'Event')
    fig = px.line(events_by_year, x='Years', y='Event')
    st.plotly_chart(fig)

    st.title('Athelets over the years')
    events_by_year = helper.participation_data_over_time(df, 'Name')
    fig = px.line(events_by_year, x='Years', y='Name')
    st.plotly_chart(fig)

    st.title('No. of events over time (every sport)')
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int))
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select a sport',sport_list)

    x=helper.most_successful_athlete(df,selected_sport)

    st.table(x)

if user_menu =='Country-wise Analysis':

    country = df['region'].dropna().unique().tolist()
    country.sort()
    selected_country=st.sidebar.selectbox('Select Country', country)
    yearwise_medal_df=helper.yearwise_medal_tally(df,selected_country)
    st.title(selected_country+' Medal Analysis')
    fig = px.line(yearwise_medal_df, x='Year', y='Medal')

    st.plotly_chart(fig)


    pt=helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.title(selected_country + ' Analysis heatmap')
    st.pyplot(fig)

    st.title('Top 10 Athletes of '+selected_country)
    x=helper.most_successful_athlete_in_country(df,selected_country)
    st.table(x)

if user_menu=='Athelete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x = athlete_df['Age'].dropna()
    x1 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    st.title('Age wise Performance')
    fig = ff.create_distplot([x, x1, x2, x3], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=500)
    st.plotly_chart(fig)

    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    st.title('Sport wise Weight-Height Distribution')
    sport_chosen=st.selectbox('Choose a sport',sport_list)

    fig,ax=plt.subplots(figsize=(20,20))
    temp=helper.weight_height(df,sport_chosen)
    ax=sns.scatterplot(temp['Weight'],temp['Height'],hue=temp['Medal'],style=temp['Sex'],s=60)
    st.pyplot(fig)

    st.title('Men vs Women distribution')
    final=helper.men_vs_women(df)
    fig, ax = plt.subplots()
    fig=px.line(final,x="Year",y=["Male","Female"])
    fig.update_layout(autosize=False, width=1000, height=500)
    st.plotly_chart(fig)
