# The entire code
import re
import os
import schedule
import requests
import json
import sys
import pdb
import praw
import sys
import logging
import random
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime, timedelta

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
        # print(replied_to)
        if (now - timestamp) > timedelta(seconds=45):
            replied_to.pop(author)
            logging.info("%s can now request more words" % author)


def reply_random(comment, responses):
    reply_string = random.choice(responses).encode("utf8")
    comment.upvote()
    comment.reply(reply_string)
    logging.info("Replied to u/%s with %s" % (comment.author, reply_string))


def check_inbox():
    # print("Checking inbox....\n")
    for user_reply in reddit.inbox.unread(limit=None):
        if isinstance(user_reply, praw.models.Comment):
            print(user_reply.author)
            if re.search("good", user_reply.body.lower(), re.IGNORECASE):
                reply_random(user_reply, happy_responses)
            elif re.search("bad", user_reply.body.lower(), re.IGNORECASE):
                reply_random(user_reply, sad_responses)
        user_reply.mark_read()
    # print("Handled Replies\n")


def search_comment(comment):
    comment_body = comment.body.lower()
    word = comment_body[comment_body.find("shashi explain") :].split(" ")[
        2
    ]  # the word after shashi explain
    print(f"Searching for {word}")
    try:
        user_word, user_meaning, user_example = word_lookup1(word)  # call oxford api
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
        comment.reply(reply_string)
        replied_to[comment.author] = datetime.now()
    except Exception as oxford_exception:
        print(oxford_exception)
        user_meaning, user_example = word_lookup2(word)  # search in the urban dict
        if (
            user_meaning == "Definition Not Found"
            and user_example == "Example Not Found"
        ):
            print("Word Not Found\n")
            comment.reply(f"{word} Not Found!")
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
            comment.reply(reply_string)
            replied_to[comment.author] = datetime.now()


def word_lookup1(word_id):
    # import pdb; pdb.set_trace()
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


def lineBreaks(defin):
    string = ""
    ignore = False
    for x in range(0, len(defin) - 4):
        if defin[x] == "<":
            ignore = True
        if ignore == False:
            string += defin[x]
        if (
            defin[x] + defin[x + 1] + defin[x + 2] + defin[x + 3] + defin[x + 4]
            == "<br/>"
        ):
            string += "\n"
        if defin[x] == ">":
            ignore = False
    return string


def word_lookup2(word):
    website = "https://www.urbandictionary.com/define.php?term=" + word

    try:
        source = requests.get(website).text
        soup = BeautifulSoup(source, "lxml")
        section = soup.find("div", class_="def-panel")
        definition = section.find("div", class_="meaning")
        example = section.find("div", class_="example")
        string1 = lineBreaks(str(definition))
        string2 = lineBreaks(str(example))
        return string1.strip(), string2.strip()
    except AttributeError as KE:
        print(KE)
        return "Definition Not Found", "Example Not Found"


schedule.every(5).seconds.do(check_inbox)  # check inbox every 30 seconds
schedule.every(5).seconds.do(restrict_user_spam)  # to avoid spamming

# comment_stream=reddit.subreddit("GumTest").stream.comments
subreddit = reddit.subreddit("GumTest")

print("Starting the stream loop...\n")

while True:
    try:
        for comment in subreddit.stream.comments(skip_existing=True):
            # print(comment.body,comment.author)
            schedule.run_pending()
            if comment.author not in replied_to:
                if "shashi explain" in comment.body.lower():
                    comment.upvote()
                    # print(comment.body)
                    search_comment(comment)
    except praw.exceptions.APIException as e:
        logging.warn(str(e))
        logging.warn("Rate Limit Exceeded. Sleeping for a minute.")
        time.sleep(60)
    except KeyboardInterrupt:
        print("User interrupted the script\n")
        sys.exit()
    except Exception as e:
        logging.exception(e)
        logging.error("Any miscellanous error,Sleeping for 10 seconds")
        time.sleep(10)
