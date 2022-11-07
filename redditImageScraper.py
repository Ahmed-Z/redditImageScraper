
import praw
import re
import requests
import os
import concurrent.futures
from flask import Flask, render_template, request   


class redditImageScraper:
    def __init__(self, data):
        self.sub = data["subreddit"]
        self.sort = data["sort"].lower()
        self.extension = ['jpeg', 'jpg', 'png']
        self.reddit = praw.Reddit(client_id=data["client_username"],
                                  client_secret=data["client_secret"],
                                  password=data["reddit_password"],
                                  user_agent = "Mozilla/5.0 (Linux; ; )AppleWebKit/ (KHTML, like Gecko) Chrome/Mobile Safari/",
                                  username=data["reddit_username"])
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

        for submission in submissions:
            if submission.url[-3:] in self.extension or submission.url[-4:] in self.extension:
                imageLinks.append(submission.url)
        return imageLinks


app = Flask(__name__,template_folder='./templates')

# GLOBALS
pics = []
subreddit = ''

@app.route('/')
def index():
    download_button = "hidden"
    return render_template('./index.html',pics=pics,download_button=download_button)


@app.route('/submit', methods=['POST'])
def submit():
    global pics, subreddit
    data = request.form.to_dict()
    subreddit = data["subreddit"]
    scraper = redditImageScraper(data)
    try:
        imagelinks = scraper.start()
    except Exception as e:
        error="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative ml-8 mr-8"
        return render_template('./index.html',pics=pics,error=error,exception=e,download_button="hidden")

    pics = imagelinks
    info = "flex items-center bg-blue-500 text-white text-sm font-bold px-4 py-3 ml-8 mr-8"
    message = "Found " + str(len(imagelinks)) + " images."
    download_button = "flex-shrink-0 bottom-0 right-0 bg-teal-500 hover:bg-teal-700 border-teal-500 hover:border-teal-700 mt-8 text-sm border-4 text-white py-1 px-2 rounded"    
    return render_template('./index.html',pics=pics,download_button=download_button,info=info,message=message)

@app.route('/download', methods=['POST'])
def download():
    global pics
    def writeFile(link):
        name = re.search('(?s:.*)\w/(.*)', link)
        name = name.group(1)
        request = requests.get(link)
        if not os.path.isfile(name):
            with open(name, 'wb') as f:
                f.write(request.content)

    path = os.path.join("scraped",subreddit)
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(writeFile, pics)
    download_button = "hidden"
    info = "flex items-center bg-blue-500 text-white text-sm font-bold px-4 py-3 ml-8 mr-8"
    message = str(len(pics)) + " images downloaded successfully in ." + path
    return render_template('./index.html',pics=pics,download_button=download_button,d_info=info,d_message=message)
app.run()


