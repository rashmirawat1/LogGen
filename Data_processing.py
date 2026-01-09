import pandas as pd
import random
import logging
import string
import numpy as np
import matplotlib.pyplot as plt

def generate_log_entry():
    """
    Generate log entries as Timestamp Log_level Actions User
    """
    timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    log_level = random.choice(["INFO", "DEBUG", "WARNING", "ERRORS"])
    actions = random.choice(["Login", "Logout", "Download", "Data Request", "Errors", "File Upload"])
    user = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) #Generate users of 5 character 
    return f"{timestamp} - {log_level} - {actions} - Users : {user}"

#function to write logs to a file
def write_logs_to_file(log_filename , num_entries=100):
    """
    write the specified number of logs into the given file format 
    """
    try:
        with open(log_filename , 'w') as file:
            for _ in range(num_entries):
                log = generate_log_entry()
                file.write(log + '\n')
        print(f"Logs have been successfully written to {log_filename}")
    except Exception as e:
        logging.error(f"Error in writing logs to file: {e}")
        print("Error occured while writing the logs to our file!!")

#functions to read the log file and process it 
def read_and_process_logs(log_filename= "generate_log.txt"):
    """
    Load and process the logs files and generate 
    """
    try:
        #read the log file into python dataframe and split it by ' - ' separator
        df = pd.read_csv(log_filename, sep=' - ', header=None, names=["Timestamp", "Log_level", "Action", "Users"], engine='python')
        
        #clean spaces around timestamp
        df['Timestamp']=  df['Timestamp'].str.strip()
        
        #converts the timestamp column to datetime 
        df['Timestamp']= pd.to_datetime(df['Timestamp'], errors ="coerce")
        
        #drop rows with the invalid timestamp
        df = df.dropna(subset=['Timestamp'])

        if df.empty :
            print("No valid data is found after the timestamp conversion")
        else:
            print("Data after the timestamp conversion: ")
            print(df.head())

        #set the timestamp column as the index for timestamp based calculation 
        df.set_index('Timestamp', inplace=True)

        return df
    except Exception as e:
        print(f"Error in reading and process logs: {e}")
        return None

#function to perform basics stastical analysys using pandas and numpy 
def analyze_data(df):
    """
    perform basics analyses like counting log level and actions and computing basic statics  
    """
    try:
        if df is None or df.empty:
            print("No data available for analysis")
            return None, None
        #count the occurence of each log level
        log_level_count = df['Log_level'].value_counts()

        #counts the occurance of each actions level
        actions_count = df['Action'].value_counts()

        log_count = len(df)     #total number of logs
        unique_users = df['Users'].nunique()    #total number of unique users 
        logs_per_day = df.resample('D').size()  #number of logs per day

        #Average actions per day
        average_logs_per_day = logs_per_day.mean()

        #max logs per day
        max_logs_per_day = logs_per_day.max()

        #Display summary statics
        print("\nLog level counts:\n", log_level_count)
        print("\nActions counts:\n", actions_count)
        print(f"Total number of logs: {log_count}")
        print(f"Unique number of users: {unique_users}")
        print(f"Number of logs per day: {logs_per_day}")
        print(f"Average logs per day: {average_logs_per_day:.2f}")
        print(f"Maximum logs per day: {max_logs_per_day}")

        #create a dictionary to display the analysys result in a single formatt
        stats = {
            "log_level_counts" : log_level_count ,
            "actions_counts" : actions_count ,
            "total_number_of_logs" : log_count ,
            "unique_number_of_users" : unique_users ,
            "number_of_logs_per_day" : logs_per_day ,
            "average_logs_per_day" : average_logs_per_day ,
            "maximum_logs_per_day" : max_logs_per_day
        }
        return stats
    except Exception as e:
        print(f"Error in analyzing the data: {e}")
        return None
    
#functions to visualize trends over time using matplotlib
def visualize_trends(df):
    """
    Visualize data trends over time using matplotlib
    """
    try:
        logs_by_day = df.resample('D').size()

        #plotting log frequency over time using matplotlib
        plt.figure(figsize=(10,5))
        plt.plot(logs_by_day.index , logs_by_day.values , marker ='o', linestyle='-', color='b')

        #customixe the plot
        plt.title("Log frequency over time")
        plt.xlabel("Date")
        plt.ylabel("Number of logs")
        plt.xticks(rotation=45)
        plt.grid(True)

        #show the plot
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error in visualizing trends: {e}")
        
log_filename = "generate_log.txt"
#step 1
write_logs_to_file(log_filename, num_entries=250)
#step 2
df_logs = read_and_process_logs(log_filename)
#step 3
if df_logs is not None:
    stats = analyze_data(df_logs)
    #step 4
    visualize_trends(df_logs)









        








