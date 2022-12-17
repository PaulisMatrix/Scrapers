## Dump of my python scripts

<br>

1.  **Greendeck Crawlers**:

    a. Scraping an e-commerce webiste and storing the scraped details in a mongo db collection.

    b. Used Scrapy framework for the same.

    c. Go through its README for implementation details.

2.  **Reddit Dictionary Bot**:

    a. A simple reddit bot which responds with a meaning of a word requested by the user.

    b. Go through its README for implementation details.

3.  **Steps to run pre-commit hook**:

    a. Install pre-commit: `pip3 install pre-commit`

    b. Setup a sample pre-commit.yaml: `pre-commit sample-config > .pre-commit-config.yaml`

    c. Edit the yaml file for whatever hooks you want to use. Refer following links:

    https://pre-commit.com/

    https://pre-commit.com/hooks.html

    d. Install/Initialize in your repo:

        ❯ pre-commit install
        pre-commit installed at .git/hooks/pre-commit

    e. Make code changes and on every commit, the pre-COMMMIT hook will run.
