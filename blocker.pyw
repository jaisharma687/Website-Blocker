import time
import datetime as dt

# IP address of the local machine
ip_localmachine = "127.0.0.1"

# List of websites to block
website_list = ["www.reddit.com", "reddit.com", "www.instagram.com", "instagram.com"]

# Path to the hosts file
hosts_path = "C:\Windows\System32\drivers\etc\hosts"

# Define start and end times for working hours
start_time = "09:00:00"
end_time = "18:00:00"

# Infinite loop to check the time and block/unblock websites
while True:
    # Get the current time
    now = dt.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)

    # If current time is within working hours
    if start_time <= current_time and current_time <= end_time:
        print("Working hours")
        with open(hosts_path, "r+") as file:
            content = file.read()
            for website in website_list:
                if not website in content:
                    file.write(ip_localmachine + " " + website + "\n")
    else:
        print("Non-working hours")
        with open(hosts_path, "r+") as file:
            content = file.readlines()
            file.seek(0)  # Reset file pointer to the beginning
            for line in content:
                if not any(website in line for website in website_list):
                    file.write(line)  # Write back lines that don't contain blocked websites
            file.truncate()  # Truncate the file to remove leftover content

    # Sleep for 10 seconds before re-checking
    time.sleep(10)
