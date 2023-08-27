import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import subprocess        
    

def git_push(remote_repo, branch="main"):
    try:
        # Adding the file to the staging area
        subprocess.run(["git", "add", "."], check=True)

        # Committing the changes
        commit_message = f"Add update"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Pushing the changes to the remote repository
        subprocess.run(["git", "push", remote_repo, branch], check=False)
        print("File successfully pushed to the remote repository.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {str(e)}")
        print(
            "Please make sure you have configured your Git credentials and have the necessary permissions."
        )


hour = int(datetime.now().strftime('%H'))

url = 'https://www.benzinpreis.de/aktuell/super_e5/deutschland/baden-wuerttemberg/karlsruhe/landkreis_heidelberg/heidelberg'

response = requests.get(
    url,
    headers={
        "Accept-Language":
        "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Accept-Encoding":
        "gzip, deflate",
        "Upgrade-Insecure-Requests":
        "1",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    })
soup = BeautifulSoup(response.text, "lxml")

prices_list = soup.find_all('td', 'center')
prices = [i.text for i in prices_list]

with open('test.csv', 'a+') as tempLog:
    csv.writer(tempLog).writerow([
        f"Kategorie (Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        prices[0], prices[1], prices[2]
    ])
    csv.writer(tempLog).writerow(
        ["Günstigster Preis:", prices[3], prices[4], prices[5]])
    csv.writer(tempLog).writerow(
        ["Teuerster Preis:", prices[6], prices[7], prices[8]])
    csv.writer(tempLog).writerow(
        ["Durchschnittspreis:", prices[9], prices[10], prices[11]])

with open('guenstigster_preis.csv', 'a+') as tempLog:
    csv.writer(tempLog).writerow([
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", prices[3],
        prices[4], prices[5]
    ])
with open('teuerster_preis.csv', 'a+') as tempLog:
    csv.writer(tempLog).writerow([
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", prices[6],
        prices[7], prices[8]
    ])
with open('durchschnitts_preis.csv', 'a+') as tempLog:
    csv.writer(tempLog).writerow([
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", prices[9],
        prices[10], prices[11]
    ])


with open("git_log.txt", "r") as f:
    todays_day = datetime.today().day
    if todays_day == 1:
        if f.read() == "False":
            remote_repo = "origin"
            branch = "main"  # Change this to your branch name if different
            git_push(remote_repo, branch)
            with open("git_log.txt", "w") as file:
                file.write("True")
    else:
        with open("git_log.txt", "w") as file:
            file.write("False")        