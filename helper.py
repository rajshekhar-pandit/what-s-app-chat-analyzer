from urlextract import URLExtract
import emoji 
import pandas as pd

def fetch_emoji(text):
    emojis = []

    for char in text:
        if emoji.is_emoji(char):  # Check if character is an emoji
            emojis.append(char)

    return emojis

def fetch_stats(selected_user,df):
    
    if selected_user !='overall':
        df=df[df['User'] == selected_user]
    
    num_messages = df.shape[0]
    words=[]
    media_msgs=0
    urls=[]
    extractor = URLExtract()
    emoji_freq = {} 

    for message in df['Message']:
        text = message
        urls+=extractor.find_urls(text)
        if(message=="<Media omitted>"):
            media_msgs+=1
        else:
            words.extend(message.split())
        
        temp_emoji = fetch_emoji(text)
        
        for emj in temp_emoji:
            if emj in emoji_freq:
                emoji_freq[emj] += 1  # Increment count if emoji already exists
            else:
                emoji_freq[emj] = 1 
    
    return num_messages,len(words),media_msgs,len(urls),words,df,emoji_freq
    
def most_busy_users(df):
    freq = df['User'].value_counts().head()
    freq_percentage = (freq / df.shape[0]) * 100
    # Convert the Series to a DataFrame
    freq_df = freq_percentage.reset_index()
    # Rename the columns
    freq_df.columns = ['User', 'Percentage']
    return freq_df,freq

def quarterly_time_line(selected_user, df):
    if selected_user != 'overall':
        df = df[df['User'] == selected_user]
    
    # Add a column for 'Quarter' based on 'Month_num'
    df['Quarter'] = df['Month_no.'].apply(lambda x: (x - 1) // 3 + 1)

    # Group by 'Year' and 'Quarter' and count the number of messages
    timeline = df.groupby(['Year', 'Quarter']).count()['Message'].reset_index()

    # Initialize an empty list to store the 'time' values (for quarters)
    time = []
    
    # Iterate over the timeline DataFrame to create 'Quarter-Year' labels
    for i in range(timeline.shape[0]):
        time.append("Q" + str(timeline['Quarter'][i]) + "-" + str(timeline['Year'][i]))

    timeline['time'] = time
    return timeline

def week_activity_map(selected_user,df):
    if(selected_user!="overall"):
        df=df[df['User']==selected_user]
    
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if(selected_user!="overall"):
        df=df[df['User']==selected_user]
    
    return df['Month'].value_counts()
    
def hourly_heat_map(selected_user,df):
    if(selected_user!="overall"):
        df=df[df['User']==selected_user]

    df_grouped = df.groupby(['day_name', 'Hour']).size().reset_index(name='activity_count')
    all_hours = range(24)

    pivot_table = df_grouped.pivot_table(index='day_name', columns='Hour' , values='activity_count', fill_value=0)
   
    # Sort the days in a meaningful order
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_table = pivot_table.reindex(days_order).fillna(0)
    all_hours = range(24)  # All hours from 0 to 23
    pivot_table = pivot_table.reindex(columns=all_hours, fill_value=0)
    
    return pivot_table
