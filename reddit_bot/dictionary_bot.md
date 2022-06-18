### This is a dictionary bot created for displaying the meaning of a word when called by a specific command on the mentioned subreddit on Reddit website.


* For creating this bot I have used the following:
    
    1. PRAW (Python Reddit API Wrapper)
    2. requests
    3. Beautiful soup for webscrapping 
    4. schedule for scheduling the bot
    5. re for regex matching and much more...

<br>

* The syntax for triggering the bot is :
`shashi explain <your word>` or `!define <your word>`

* Implementation details:


1. I have implemented two word lookups.
    
    a. First is the call to the oxford dictionary api and if the word is not found there then

    b. Second lookup is the urban dictionary which I have scrapped using beautiful soup.

2.  The bot returns the following:
    a. The defintion

    b. Type of the word(noun/pronoun/adjective/verb)
    
    c. Example on a successful lookup else "<word> Not found!!" message incase word is not found.

3.  Example trigger call :

    `shashi explain mitigation` or `!explain mitigation`

    Oxford Response:

        According to the Oxford dictionary:

        Your Word: mitigation.

        Word Type: noun.

        Meaning: the action of reducing the severity,seriousness, or painfulness of something.

        Example: the identification and mitigation of pollution.

    `shashi explain shashi` or `!explain shashi`

    Urban dictionary Response:

        According to Urban dictionary:

        Word: shashi.

        Meaning: The word "shashi " is used to describe th most handsomest man you'll ever see. Shashi is someone who is kind spiritted smart and someone who loves to go out with dark blonde hair girls.

        Example:  I wish I was a shashi!!
                  I need to be a shashi!!
        