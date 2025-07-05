import streamlit as st
import pandas as pd
import index
import helper 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import nltk

from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('stopwords')
st.sidebar.title("whatsapp chat analyzer")
Uploaded_file = st.sidebar.file_uploader("choose a file")
if Uploaded_file is not None:
    bytes_data=Uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    
    df=index.process_chat_data(data)
    
    user_list=df['User'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"overall")
    selected_user=st.sidebar.selectbox("show analysis of user",user_list)
    
    if st.sidebar.button("show Analysis"):
        
        col1, col2, col3, col4 = st.columns(4)
        num_messages,words,media_msgs,urls,ac_words,df,emoji_freq =helper.fetch_stats(selected_user,df)
        columns_to_display = ['User','Message','Date and Time']
        st.dataframe(df[columns_to_display])
        
        with col1:
            st.subheader("Total Messages")
            st.title(num_messages)
        with col2:
            st.subheader("Total Words")
            st.title(words)
        with col3:
            st.subheader("Total media shared")
            st.title(media_msgs)
        with col4:
            st.subheader("Total links shared")
            st.title(urls) 
    # finding most active users
        if selected_user == "overall":
            st.markdown("---")
            st.subheader("👥 Most Active Users")
            new_df, freq = helper.most_busy_users(df)
            
            col1, col2 = st.columns([3, 2])
            with col1:
                fig, ax = plt.subplots(figsize=(10, 8))
                top_5_percentage_sum = new_df['Percentage'].sum()
                remaining_percentage = 100 - top_5_percentage_sum
                df_with_remaining = pd.concat([
                    new_df, 
                    pd.DataFrame([['Others', remaining_percentage]], columns=['User', 'Percentage'])
                ], ignore_index=True)
                
                colors = plt.cm.Pastel1(np.linspace(0, 1, len(df_with_remaining)))
                wedges, texts, autotexts = ax.pie(
                    df_with_remaining['Percentage'], 
                    labels=df_with_remaining['User'], 
                    autopct='%1.1f%%',
                    colors=colors,
                    startangle=90,
                    pctdistance=0.85
                )
                
                centre_circle = plt.Circle((0, 0), 0.70, fc='white')
                fig.gca().add_artist(centre_circle)
                
                ax.axis('equal')
                plt.title("Message count Distribution", fontsize=16, fontweight='bold', pad=20)
                st.pyplot(fig)
            
            with col2:
                st.dataframe(freq) 

        col1 = st.container()
        with col1:
            stop_words = set(stopwords.words('english'))
            filtered_words = [word for word in ac_words if word.lower() not in stop_words]
            removed_words= [word for word in ac_words if word.lower()  in stop_words] 
            text = ' '.join(filtered_words)  
            st.markdown("---")
            st.subheader("📝 Word Cloud")
            if len(text)>=1:
                # Generate the word cloud
                wordcloud = WordCloud(width=800, height=400, background_color='black').generate(text)
                # Create a figure for the word cloud
                fig, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation='bilinear')
                st.pyplot(fig)

        col1 = st.container()
        with col1:
            if(len(emoji_freq) > 4):
                sorted_emojis = sorted(emoji_freq.items(), key=lambda x: x[1], reverse=True)[:5]
                labels = ['One', 'Two', 'Three', 'Four', 'Five']
                _, counts = zip(*sorted_emojis)
                # Plot the bar graph
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(labels, counts, color='blue')
                ax.set_title("Top 5 Most Used Emojis", fontsize=16)
                ax.set_ylabel("Frequency", fontsize=12)
                plt.tight_layout()
                # Streamlit layout
                st.subheader("Emoji Frequency Analysis")
                st.pyplot(fig)
                emoji_table = pd.DataFrame({
                'Label': ['One', 'Two', 'Three', 'Four', 'Five'],
                'Emoji': [emoji for emoji, _ in sorted_emojis],
                'Frequency': [count for _, count in sorted_emojis]
                })
                st.markdown("### Emoji Mapping Table")
                st.table(emoji_table)

        # timeline plot 
        timeline=helper.quarterly_time_line(selected_user,df)
        col1 = st.container()
        if(timeline.shape[0]>0):
            with col1:
                st.subheader("quarterly messages count")
                fig,ax=plt.subplots()
                ax.plot(timeline['time'],timeline['Message'])
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
        
        st.title('Activity map')
        col1,col2=st.columns(2)
        # Most busy day
        with col1:
            st.subheader("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='blue')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        # Most busy month
        with col2:
            st.subheader("Most busy month")
            busy_day=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='orange')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        
        # heat map of activity
        st.subheader('Heat Map of Activity')

        # Create a container for the heatmap
        col1 = st.container()
        with col1:
            # Call the helper function to get the pivot table
            map_df=helper.hourly_heat_map(selected_user,df)

            # Plotting the heatmap using Seaborn and Matplotlib
            fig, ax = plt.subplots(figsize=(12, 7))  # Adjust the figure size if necessary
            sns.heatmap(map_df, cmap="YlGnBu", annot=True, ax=ax)

            # Add labels and title
            ax.set_title("Hourly Activity Frequency Heatmap by Day of Week")
            ax.set_xlabel("Hour of the Day")

            # Display the heatmap in Streamlit
            st.pyplot(fig)




             
