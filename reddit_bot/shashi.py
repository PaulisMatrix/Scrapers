# The entire code
import json
import logging
import os
import random
import re
import sys
import time
from datetime import datetime, timedelta

import praw
import requests
import schedule
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from lxml import etree

# to load the env variables
load_dotenv()

happy_responses_filename = "happy_responses.txt"
sad_responses_filename = "sad_responses.txt"

# OXFORD DICTIONARY SETTINGs
app_id = os.getenv("oxford_app_id")
app_key = os.getenv("oxford_app_key")
language = os.getenv("oxford_lang")

# REDDIT SETTINGS
reddit = praw.Reddit(
    client_id=os.getenv("reddit_client_id"),
    client_secret=os.getenv("reddit_client_secret"),
    user_agent=os.getenv("reddit_useragent"),
    username=os.getenv("reddit_username"),
    password=os.getenv("reddit_password"),
)

logging.basicConfig(
    filename="logfile_shashi.log",
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

try:
    with open(happy_responses_filename, encoding="utf8") as f:
        happy_responses = f.read().split("\n")
except FileNotFoundError:
    happy_responses = [":^)"]

try:
    with open(sad_responses_filename, encoding="utf8") as f:
        sad_responses = f.read().split("\n")
except FileNotFoundError:
    sad_responses = [":("]


# dictionary to store author and corresponding timestamp
replied_to = {}


def restrict_user_spam():
    now = datetime.now()
    for author in list(replied_to.keys()):
        timestamp = replied_to[author]
        if (now - timestamp) > timedelta(seconds=45):
            replied_to.pop(author)
            logging.info("%s can now request more words" % author)


def reply_random(comment, responses):
    reply_string = random.choice(responses).encode("utf8")
    comment.upvote()
    comment.reply(body=reply_string)
    logging.info("Replied to u/%s with %s" % (comment.author, reply_string))


def check_inbox():
    for user_reply in reddit.inbox.unread(limit=None):
        if isinstance(user_reply, praw.models.Comment):
            if re.search("good", user_reply.body.lower(), re.IGNORECASE):
                reply_random(user_reply, happy_responses)
            elif re.search("bad", user_reply.body.lower(), re.IGNORECASE):
                reply_random(user_reply, sad_responses)
        user_reply.mark_read()


def search_comment(comment_body):
    if "shashi explain" in comment_body:
        word = comment_body[comment_body.find("shashi explain") :].split(" ")[2]
    else:
        word = comment_body[comment_body.find("!explain") :].split(" ")[1]
    logging.info(f"Searching for {word}")
    try:
        # first lookup oxford api
        user_word, user_meaning, user_example = word_lookup1(word)
        reply_string = (
            "According to Oxford dictionary:\n\n"
            + "**Your Word**: "
            + str(word)
            + "\n\n"
            + "**Word Type**: "
            + str(user_word)
            + "\n\n"
            + "**Meaning**: "
            + str(user_meaning)
            + "\n\n"
        )
        if "not found" not in user_example.lower():
            reply_string += "**Example**: " + str(user_example) + "\n"
        comment.reply(body=reply_string)
        replied_to[comment.author] = datetime.now()
    except Exception as oxford_exception:
        logging.warning(
            f"Oxford didn't find the word. Raised exception {oxford_exception}"
        )
        # second lookup in urban dictionary
        user_meaning, user_example = word_lookup2(word)
        if (
            user_meaning == "Definition Not Found"
            and user_example == "Example Not Found"
        ):
            comment.reply(body=f"{word} Not Found!")
            replied_to[comment.author] = datetime.now()
        else:
            reply_string = "According to Urban dictionary:\n\n"
            if len(user_example) == 0:
                reply_string += (
                    "**Word**: "
                    + str(word)
                    + "\n\n"
                    + "**Meaning**: "
                    + str(user_meaning)
                )
            else:
                reply_string += (
                    "**Word**: "
                    + str(word)
                    + "\n\n"
                    + "**Meaning**: "
                    + str(user_meaning)
                    + "\n\n"
                    + "**Example**: "
                    + str(user_example)
                )
            comment.reply(body=reply_string)
            replied_to[comment.author] = datetime.now()


def word_lookup1(word_id):
    url = (
        "https://od-api.oxforddictionaries.com:443/api/v2/entries/"
        + language
        + "/"
        + word_id.lower()
    )
    r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    json_data = json.loads(r.text)

    word = json_data["results"][0]["lexicalEntries"][0]["lexicalCategory"]["id"]
    meaning = json_data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0][
        "definitions"
    ][0]
    example = json_data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0][
        "examples"
    ][0]["text"]
    return word, meaning, example


def word_lookup2(word):
    website = "https://www.urbandictionary.com/define.php?term=" + word
    try:
        page = requests.get(website).text
        soup = BeautifulSoup(page, "lxml")
        tree = etree.HTML(page)
        word = tree.xpath(
            "/html/body/div/div/main/div/div[4]/section/div[1]/div/div[1]/h1/a/text()"
        )[0]
        definition, example = (
            soup.find("div", class_="break-words meaning mb-4").text,
            soup.find("div", class_="break-words example italic mb-4").text,
        )
        return definition.replace("\r", "\n").strip().replace(
            " '", "'"
        ), example.replace("\r", "\n").strip().replace(" '", "'")

    except Exception as UrbanDictionaryException:
        logging.warning(
            f"Urban Dictionary didn't find the word. Raised exception {UrbanDictionaryException}"
        )
        return "Definition Not Found", "Example Not Found"


# check inbox every 30 seconds
schedule.every(10).seconds.do(check_inbox)
# to avoid spamming
schedule.every(5).seconds.do(restrict_user_spam)

# comment_stream=reddit.subreddit("GumTest").stream.comments
subreddit = reddit.subreddit("GumTest")

logging.info("Starting the stream loop.....")

while True:
    try:
        for comment in subreddit.stream.comments(skip_existing=True):
            schedule.run_pending()
            if comment.author not in replied_to:
                comment_body = comment.body.lower()
                if "shashi explain" in comment_body or "!explain" in comment_body:
                    comment.upvote()
                    search_comment(comment_body)
    except praw.exceptions.APIException as e:
        logging.warning(
            f"Rate Limit Exceeded with exception {str(e)}. Sleeping for a minute."
        )
        time.sleep(60)
    except KeyboardInterrupt:
        print("User interrupted the script\n")
        sys.exit()
    except Exception as e:
        logging.exception(e)
        logging.error("Any miscellanous error,Sleeping for 10 seconds")
        time.sleep(10)
