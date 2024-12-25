from flask import Flask, render_template, request, redirect, url_for
import time
import datetime as dt

app = Flask(__name__)

ip_localmachine = "127.0.0.1"

# Hosts file path for Windows (change path if you're using Linux/Mac)
hosts_path = "C:\\Windows\\System32\\drivers\\etc\\hosts"

def block_websites(website_list):
    with open(hosts_path, "r+") as file:
        content = file.read()
        for website in website_list:
            if website not in content:
                file.write(ip_localmachine + " " + website + "\n")

def unblock_websites(website_list):
    with open(hosts_path, "r+") as file:
        content = file.readlines()
        file.seek(0)
        for line in content:
            if not any(website in line for website in website_list):
                file.write(line)
        file.truncate()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        websites = request.form.get("websites")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        website_list = [website.strip() for website in websites.split(",")]
        return redirect(url_for("manage_blocking", websites=websites, start_time=start_time, end_time=end_time))
    return render_template("index.html")

@app.route("/manage_blocking")
def manage_blocking():
    websites = request.args.get("websites")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    website_list = [website.strip() for website in websites.split(",")]
    now = dt.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Current Time: {current_time}")
    if start_time <= current_time <= end_time:
        print("Working hours: Blocking websites...")
        block_websites(website_list)
        message = "Websites are successfully blocked."
    else:
        print("Non-working hours: Unblocking websites...")
        unblock_websites(website_list)
        message = "Websites are successfully unblocked."
    return render_template("acknowledgment.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
