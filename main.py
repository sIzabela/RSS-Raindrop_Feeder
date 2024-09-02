import feedparser
import json
import os
from datetime import datetime
from raindropio import API, Raindrop
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Raindrop.io settings
RAINDROP_TOKEN = os.getenv('RAINDROP_TOKEN')

# RSS file list reader
with open(os.getenv('CSV_FILE'), 'r') as file:
  
    # Return a reader object which will iterate over lines in the given csvfile 
    data = file.read() 
  
    # Convert string to list 
    RSS_FEEDS = data.split()

# File with last run time
LAST_RUN_FILE = os.getenv('LAST_RUN_FILE')

# Logs to file with last run time config
log_folder = os.getenv('LOG_FOLDER')
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Set up logging
log_filename = os.path.join(log_folder, f'rss_raindrop_{datetime.now().strftime("%Y%m%d")}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load time of the last startup
def load_last_run():
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_last_run(last_run):
    try:
        with open(LAST_RUN_FILE, 'w') as file:
            json.dump(last_run, file)
        logger.info("The time of the last startup was recorded.")
    except Exception as e:
        logger.error(f"Error when saving the time of the last startup: {e}")


def fetch_new_articles(feed_url, last_run_time):
    feed = feedparser.parse(feed_url)
    new_articles = []
    for entry in feed.entries:
        published_time = datetime(*entry.published_parsed[:6])
        if published_time > last_run_time:
            new_articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': published_time,
                'thumbnail': entry.media_thumbnail[0]['url'] if 'media_thumbnail' in entry else None
            })
    return new_articles

def add_to_raindrop(api, articles):
    for article in articles:
        response = Raindrop.create(
            api,
            link=article['link'],
            title=article['title'],
            tags=[os.getenv('TAGS')],
            cover=article['thumbnail']
        )
        logger.info(f"Added article: {article['title']} - {response}")

def main():
    last_run = load_last_run()
    last_run_time = datetime.fromisoformat(last_run.get('last_run_time', '1970-01-01T00:00:00'))

    api = API(RAINDROP_TOKEN)
    all_new_articles = []

    for feed_url in RSS_FEEDS:
        new_articles = fetch_new_articles(feed_url, last_run_time)
        all_new_articles.extend(new_articles)

    # Show new articles
    for article in all_new_articles:
        print(f"New article: {article['title']} - {article['link']}")

    if all_new_articles:
        add_to_raindrop(api, all_new_articles)
    else:
        print("No new articles found.")
        logger.info("No new articles found.")

    last_run['last_run_time'] = datetime.now().isoformat()
    save_last_run(last_run)

if __name__ == '__main__':
    main()
