# redditImageScraper
This program scrapes images from a selected subreddit.

# Installation

`git clone https://github.com/Ahmed-Z/redditImageScraper`<br>
`cd redditImageScraper` <br><br>
After downloading you have to install dependencies:<br>
`pip3 install -r requirements.txt`

# Configuration
1. Go to [App Preferences](https://www.reddit.com/prefs/apps) and click create another app… at the bottom.

2. Fill out the required details, make sure to select script — and click create app.

3. Create a `.env` file with the following configuration

```
C_ID= client_id
C_SECRET= client_secret
PASSWORD= reddit_account_password
UA= user_agent
USERNAME= reddit_user
```
