# CDTweetBot
[![Build Status](https://travis-ci.org/franccesco/CDTweetBot.svg?branch=master)](https://travis-ci.org/franccesco/CDTweetBot)[![Coverage Status](https://coveralls.io/repos/github/franccesco/CDTweetBot/badge.svg?branch=master)](https://coveralls.io/github/franccesco/CDTweetBot?branch=master)

**CDTweetBot** is a custom made twitter-bot that share new blog posts from [CodingDose()](https://codingdose.info/) to Twitter automatically using the [@codingdose](https://twitter.com/codingdose) account.


**Disclaimer: This project is a Work-in-Progress and only works with my Blog, feel free to reuse my code as an example to use it in your projects.**

# Features and TODO
- [x] Handle Twitter Authentication System (OAuth)
- [x] Scrape the blog searching for new blog posts
- [x] SQLite3 integration to store posts and handles posts duplication
- [ ] If a new blog post is identified, then it will share it through twitter
- [ ] Autoreply Direct Messages

# Requirements
- Tweepy
- Python-dotenv
- Requests
- BeautifulSoup4

### Installation with Pipenv (Recommended)
```sh
pipenv install
```
### Installation with Pip

```sh
pip install -r requirements.txt
```

### Installation for development
If you wan't to run tests, coverage and debugging install the development requirements with `pip` or `pipenv`

**Pipenv**
```sh
pipenv install --dev
```
**Pip**
```sh
pip install -r requirements-dev.txt
```
