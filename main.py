from arguments import args
from instagram import Instagram
from os import system as sys

url = args.url
tags = args.tag
detail = args.detail  
photos = args.photos
videos = args.videos
username = args.username

if username:
    account = Instagram(account=username)

elif url:
    post = Instagram(url=url)
    post.download_single_post()

else:
    sys("python main.py --help")