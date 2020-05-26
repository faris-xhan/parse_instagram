# parse_instagram

An Instagram script that will let you parse the PUBLIC INSTAGRAM USER DATA i.e Information, Photos etc. without giving your credentials.

![Python 3.6+](https://img.shields.io/badge/Python-3.6+-3776ab.svg?maxAge=2592000)

## Overview

I wrote this to access Instagram's API without giving your password it is an easy to use script and you can use this in your project.
I am not an expert and this is one of the project that I'm working one during my learning journey. :) 
It is not complete yet I'm still working on it but you can use it. The following features are available at the moment.

## Features
- Get public information of the user in json format 
- Download instagram user profile photo 
- Generate a generator which will let you iterate over all the public instagram posts
( MORE FEATURES WILL BE ADDED SOON )

## Usage

```python

from instagram import Instagram
account = Instagram("account")
accounts.download_profile()
contents = Instagram.contents.get_all()
next(contents)

```
An [``Instagram Instance``] will contain the following information
- id 
- profile
- username
- followers ( total followers )
- followed ( total user following )
- biography ( account caption )
- is_private 
- is_varified  
- external_url
- business_category
- is_business_account
- [``contents``]
  It is and instance of Contents class which after at the moment it contains an method [``get_all_contents()``] which will return a generator that will iterate over all the media contents of the user and return a json response containing information about that content 
  
## Support

Feel free to submit an issue report or pull request.

