# this was to test webscraping.
# Program contains way to many returns and spaghetti code
# This scrapes all users who follow an account - Wattcat 2021-04-10
from bs4 import BeautifulSoup
import requests
import os

# Checks if supplied username is valid. Otherwise returns false
def isValid(username):
    isValidUser = True
    privateexeption = ["The owner of this page has elected to make it available to registered users only.",
                       "Provided username not found in the database."]
    url = "https://www.furaffinity.net/watchlist/to/{}/".format(username)
    currentpage = requests.get(url)
    soup = BeautifulSoup(currentpage.content, 'html.parser')  # sorts with bs4
    private = soup.find_all('div', {"class": "section-body alignleft"})
    # This is to check if a profile is private or non existent
    if privateexeption[0] in str(private) or privateexeption[1] in str(private):
        isValidUser = False
    return isValidUser


# Returns a list of unique user accounts
def pageScraper(select, username):
    users = []
    pos = 0
    while True:
        url = 'https://www.furaffinity.net/watchlist/{}/{}/{}/?'.format(
            select, username, pos)
        currentpage = requests.get(url)
        soup = BeautifulSoup(currentpage.content,
                             'html.parser')  # sorts with bs4
        betterdivs = soup.find_all('a', href=True)
        print("scraping users at page:", url)
        try:  # this is to catch out of range errors
            contentlist = str(betterdivs).split("</a>")
            for i in range(len(contentlist)):
                scrapedusername = contentlist[i].split(">")[1]  # Usernames
                if scrapedusername not in users:
                    users.append(scrapedusername)

        except Exception as e:
            # print(e)
            pass

            if (len(str(soup)) < 4500):
                print("End of the line!")
                return users
                break
            pos += 1

# This is used by UI for user selection
def selector():
    selection = input(
        "Select mode:\n1. Get what user is Watching \n2. Get Watchers/followers \n3. Get both \n")
    selection = selection.strip()
    if selection == "1":
        return "by"
    elif selection == "2":
        return "to"
    elif selection == "3":
        return "both"
    else:
        print("Please enter a valid number")
        selection()

# used for writing everything to a file
def writer(path, lists):
    with open(path, 'a') as a_writer:
        for s in lists:
            a_writer.write(str(s) + "\n")
        a_writer.close
        return "Done"

# simple user interface in terminal
def UI():
    username = input("Enter a non private Username:\n")
    if isValid(username) == True:
        mypath = os.path.join(os.getcwd(), input(
            "Please enter output file name:\n(Note: Will output in current working folder) \n"))
        selected = selector()
        if selected == "both":
            followers = pageScraper("to", username)
            following = pageScraper("by", username)
            users = (
                followers + ["\nAll {} is watching".format(username)] + following)
        else:
            users = pageScraper(selected, username)
        writer(mypath, users)
    else:
        print("Error username is not valid")
        return UI()

UI()
