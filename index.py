import pandas as pd
import re


def convert_two_digit_year(date_str):
    # Parse the date string
    date_obj = pd.to_datetime(date_str, format='mixed')
    return date_obj

def process_chat_data(data):
    # Regular expression pattern to extract date, time, user, and message
    pattern = r'(\d{2}/\d{2}/\d{2,4}, \d{1,2}:\d{2}\s?[ap]m) - ([^:]+): (.*)'
   
    # Extracting data from the text
    matches = re.findall(pattern, data)
   
    # Creating the DataFrame
    df = pd.DataFrame(matches, columns=['Date and Time', 'User', 'Message'])

    # Clean the 'Date and Time' column to remove non-breaking spaces and other issues
    df['Date and Time'] = df['Date and Time'].str.replace('\u202f', ' ', regex=False).str.strip()
    
    # Convert 'Date and Time' column to datetime
    df['Date and Time'] = df['Date and Time'].apply(convert_two_digit_year)

    # Now you can access month and year properties
    df['Month_no.'] = df['Date and Time'].dt.month
    df['Year'] = df['Date and Time'].dt.year
    df['Day'] = df['Date and Time'].dt.day
    df['Hour'] = df['Date and Time'].dt.hour
    df['day_name']=df['Date and Time'].dt.day_name()
    df['Month'] =df['Date and Time'].dt.month_name()
    df['minute']=df['Date and Time'].dt.minute
  
    return df
