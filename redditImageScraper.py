
import praw
import re
import requests
import os
import concurrent.futures
from dotenv import dotenv_values


class redditImageScraper:
    def __init__(self, sub):
        config = dotenv_values(".env")
        self.sub = sub
        self.extension = ['jpeg', 'jpg', 'png']
        self.reddit = praw.Reddit(client_id=config["C_ID"],
                                  client_secret=config["C_SECRET"],
                                  password=config["PASSWORD"],
                                  user_agent=config["UA"],
                                  username=config["USERNAME"])

    def writeFile(self, link):
        name = re.search('(?s:.*)\w/(.*)', link)
        name = name.group(1)
        request = requests.get(link)
        if not os.path.isfile(name):
            with open(name, 'wb') as f:
                f.write(request.content)

    def start(self, sort):
        subreddit = self.reddit.subreddit(self.sub)
        if sort == "hot":
            submissions = subreddit.hot()
        if sort == "new":
            submissions = subreddit.new()
        if sort == "controversial":
            submissions = subreddit.controversial()
        if sort == "rising":
            submissions = subreddit.rising()
        if sort == "top":
            submissions = subreddit.top()
        if sort == "gilded":
            submissions = subreddit.gilded()
        imageLinks = []
        print("[+] Fetching image links")
        try:
            for submission in submissions:
                if submission.url[-3:] in self.extension or submission.url[-4:] in self.extension:
                    imageLinks.append(submission.url)
        except Exception as e:
            exit("[!] " + self.sub + " does not exist")

        print("[+] Found {} in {}".format(len(imageLinks), sort))
        limit = str(input("[+] Download ['all'/limit]: "))
        while True:
            try:
                if limit == "all" or int(limit) >= len(imageLinks):
                    l = len(imageLinks)
                    break
                else:
                    l = int(limit)
                    break
            except:
                print("[!] Please enter a valid input ('all' to download all images)")
        print(
            "[+] Downloading {} images from {} using {} sort".format(l, self.sub, sort))
        imageLinks = imageLinks[:l]
        path = './scraped/' + self.sub
        if not os.path.exists(path):
            os.mkdir(path)
        os.chdir(path)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.writeFile, imageLinks)
        print("[+] Download complete. Check ", path)


subreddit = str(input("[+] Select the name of the subreddit to scrape: "))

sort = ["controversial", "gilded", "hot", "new", "rising", "top"]
print("[+] How to sort submission?")
print("- controversial: 0\n- gilded: 1\n- hot: 2\n- new: 3\n- rising: 4\n- top: 5")
while True:
    s = int(input("[+] Please choose a number (0->5): "))
    if s >= 0 and s <= 5:
        break
scraper = redditImageScraper(subreddit)
scraper.start(sort[s])
