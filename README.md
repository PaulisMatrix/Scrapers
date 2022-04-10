This is a dictionary bot created for displaying the meaning of a word when called by a specific command on the mentioned subreddit on Reddit website.

For creating this bot I have used the following:
1. PRAW (Python Reddit API Wrapper)
2. requests
3. Beautiful soup for webscrapping 
4. schedule for scheduling the bot
5. re for regex matching and much more...



The syntax for triggering the bot is :
shashi explain <your word> or !define <your word>

I have implemented two word lookups.
First is the call to the oxford dictionary api and if the word is not found there then
second lookup is the urban dictionary which I have scrapped using beautiful soup.

The bot returns the defintion,type of the word(noun/pronoun/adjective/verb) and an example 
on a successful lookup else "Not found" message incase word is not found.

Example trigger call :
shashi exlpain mitigation or !explain mitigation

Response:
According to the Oxford dictionary:

Your Word: mitigation.

Word Type: noun.

Meaning: the action of reducing the severity,seriousness, or painfulness of something.

Example: the identification and mitigation of pollution.
