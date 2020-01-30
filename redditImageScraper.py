
import praw,re,requests,os
import concurrent.futures
from auth import *

class redditImageScraper:
    def __init__(self,sub,limit):
        self.sub = sub
        self.limit = limit
        self.reddit = praw.Reddit(client_id = c_id,
                     client_secret = c_secret,
                     password = password,
                     user_agent='testyscript',
                     username = username)

    def writeFile(self, link):
        name = re.search('(?s:.*)\w/(.*)',link)
        name = name.group(1)
        request = requests.get(link)
        if not os.path.isfile(name):  
            with open(name,'wb') as f:
                f.write(request.content)

    def start(self):
        subreddit = self.reddit.subreddit(self.sub)
        hot_submission = subreddit.hot()
        imageLinks = []
        try:
            for submission in hot_submission:
                if not submission.stickied and submission.url.endswith('jpg'):
                    imageLinks.append(submission.url)
        except Exception as e:
            print(e)
            exit(self.sub + " does not exist")

        imageLinks = imageLinks[:self.limit]
        path = './scraped'
        if not os.path.exists(path):
            os.mkdir(path)
        os.chdir(path)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.writeFile, imageLinks)

scraper = redditImageScraper("cats",10)
scraper.start()