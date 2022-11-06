
import praw
import re
import requests
import os
import concurrent.futures
from flask import Flask, render_template, request   
# from dotenv import dotenv_values


class redditImageScraper:
    def __init__(self, data):
        self.sub = data["subreddit"]
        self.sort = data["sort"].lower()
        self.extension = ['jpeg', 'jpg', 'png']
        self.reddit = praw.Reddit(client_id=data["client_username"],
                                  client_secret=data["client_secret"],
                                  password=data["reddit_password"],
                                  user_agent = "whatever",
                                  username=data["reddit_username"])

    def writeFile(self, link):
        name = re.search('(?s:.*)\w/(.*)', link)
        name = name.group(1)
        request = requests.get(link)
        if not os.path.isfile(name):
            with open(name, 'wb') as f:
                f.write(request.content)

    def start(self):
        subreddit = self.reddit.subreddit(self.sub)
        if self.sort == "hot":
            submissions = subreddit.hot()
        if self.sort == "new":
            submissions = subreddit.new()
        if self.sort == "controversial":
            submissions = subreddit.controversial()
        if self.sort == "rising":
            submissions = subreddit.rising()
        if self.sort == "top":
            submissions = subreddit.top()
        if self.sort == "gilded":
            submissions = subreddit.gilded()
        imageLinks = []
        print("[+] Fetching image links")

        for submission in submissions:
            if submission.url[-3:] in self.extension or submission.url[-4:] in self.extension:
                imageLinks.append(submission.url)

        return imageLinks
        print("[+] Found {} in {}".format(len(imageLinks), self.sort))
        # limit = str(input("[+] Download ['all'/limit]: "))
        limit = 99
        
        print(
            "[+] Downloading {} images from {} using {} sort".format(limit, self.sub, self.sort))
        imageLinks = imageLinks[:limit]
        path = './scraped/' + self.sub
        if not os.path.exists(path):
            os.mkdir(path)
        os.chdir(path)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.writeFile, imageLinks)
        print("[+] Download complete. Check ", path)


# subreddit = str(input("[+] Select the name of the subreddit to scrape: "))

# sort = ["controversial", "gilded", "hot", "new", "rising", "top"]
# print("[+] How to sort submission?")
# print("- controversial: 0\n- gilded: 1\n- hot: 2\n- new: 3\n- rising: 4\n- top: 5")
# while True:
#     s = int(input("[+] Please choose a number (0->5): "))
#     if s >= 0 and s <= 5:
#         break

app = Flask(__name__,template_folder='./templates')
pics = []
@app.route('/')
def index():
    return render_template('./index.html',pics=pics)


@app.route('/submit', methods=['POST'])
def submit():
    global pics
    print(request.form.to_dict())
    data = request.form.to_dict()
    scraper = redditImageScraper(data)
    imagelinks = scraper.start()
    pics = imagelinks    
    return render_template('./index.html',pics=pics)

app.run()


#scraper.start(sort[s])
