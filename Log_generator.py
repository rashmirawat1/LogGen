import random
import string
import time
import logging

#setting up logging for error handlling
logging.basicConfig(filename="log_generator_errors.log", level=logging.ERROR)

#list the level of logs 
LOG_LEVEL = ["INFO", "DEBUG", "WARNING", "ERRORS"]

#list of possible actions 
ACTIONS = ["Login", "Logout", "Download", "Data Request", "Errors", "File Upload"]

#functions to generate random string for logs
def generate_random_string(length=10):
    """
    Generates a random string of given length default length is 10
    """
    try:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    except Exception as e:
        logging.error(f"Errors in generating random string: {e}")
        return "ERROR"

#function to generate a random log entry    
def generate_log_entry():
    """
    Generate log entry with this format: TIMESTAMP LOG_LEVEL ACTIONS USER:USER_NAME/ID PASSWORD
    """
    try:
        log_level = random.choice(LOG_LEVEL)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        actions = random.choice(ACTIONS)
        user = generate_random_string(8)
        log_entry = f"{timestamp} - {log_level} - {actions} - User: {user}"
        return log_entry
    except Exception as e:
        logging.error(f"Errors in generating Log Entry: {e}")
        return "ERROR"

#functions to write logs to the files 
def write_logs_to_file(log_filename, num_entries=100):
    """
        write the specified number of logs to the given file 
    """
    try:
        with open(log_filename, 'w') as file:
            for _ in range(num_entries):
                log = generate_log_entry()
                if log != "ERROR":
                    file.write(log + "\n")
        print(f"Logs have been successfully written to {log_filename}")
    except Exception as e:
        logging.error(f"Errors in writing logs to the file: {e}")
        print("Errors generated while writing logs to the file")

#Generate any number of logs by calling functions 
write_logs_to_file('generate_log.txt', num_entries=150)
