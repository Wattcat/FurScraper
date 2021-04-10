# this was to test webscraping.
# Program contains way to many returns and spaghetti code
# This scrapes all users who follow an account - Wattcat 2021-04-10
from bs4 import BeautifulSoup
import requests
import os


def furScraper(select, username):
    privateexeption = "The owner of this page has elected to make it available to registered users only."
    users = []
    pos = 0
    while True:
        url = 'https://www.furaffinity.net/watchlist/{}/{}/{}/?'.format(
            select, username, pos)
        currentpage = requests.get(url)  # för hämtning av url
        soup = BeautifulSoup(currentpage.content,
                             'html.parser')  # sorts with bs4
        # Check if profile is private
        private = soup.find_all('p', {"class": "link-override"})
        # This is to check if a profile is private
        if privateexeption in str(private):
            print("This profile is set to private for non logged in users.")
            break
        betterdivs = soup.find_all('a', href=True)
        print("Found users in:", url)
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


def selection():
    # Why not use refer to them as followers?
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


def listwriter():
    username = input("Enter a non private Username:\n")
    mypath = os.path.join(os.getcwd(), input("Please enter output file name:\n(Note: Will output in current working folder) \n"))
    select = selection()
    # Both selection
    if select == "both":
        followers = furScraper("to", username)
        if followers == None:
            return listwriter()
        following = furScraper("by", username)
        users = (followers + ["\nAll {} is watching".format(username)] + following)
    else:
        users = furScraper(select, username)
        if users == None:
            return listwriter()

    with open(mypath, 'a') as a_writer:
        for s in users:
            a_writer.write(str(s) + "\n")
        a_writer.close
        return "Done"


print(listwriter())
