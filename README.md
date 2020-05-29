# parse_instagram

An instagram script that will let you download a single are all the instagram photos of a public account without loging in.

![Python 3.6+](https://img.shields.io/badge/Python-3.6+-3776ab.svg?maxAge=2592000)

## Overview

I wrote this script to download Instagram images. You can download a single post by just giving the url of the post and you can also download the public photos of the user by giving the username.


## Features

- Download all the *posts* along with their information.
- Download all the *photos only* along with their information.
- Download all the *videos only* along with their information.
- Download a single post by giving the url of the post.
- Download instagram user profile photo 


## Usage

```bash

usage: main.py [-h] [-u USERNAME] [--url URL] [-t TAG] [-d] [-p] [-v]

Scrape Instagram!

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Instagram username
  --url URL             Download single post from given url
  -t TAG, --tag TAG     Download posts containing only this tags
  -d, --detail          Save posts along with their information
  -p, --photos          Download photos only
  -v, --videos          Download videos only

```
To download photos, videos or posts along with their details give the optional parameter [```-d or --detail```]

## Support

Feel free to submit an issue report or pull request.
