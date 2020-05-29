from instagram import Instagram
from arguments import args
import requests
import json
import os

def dump_json(obj, username, file_name):
    file_name += '.json'
    location = str(username)
    if not os.path.exists(location):
        os.makedirs(location)

    with open(f'./{location}/{file_name}', 'w') as f:
        json.dump(obj, f)

def download(url, username, file_name):
    location = str(username)
    if not os.path.exists(location):
        os.makedirs(location)
    is_exist = os.path.join(os.getcwd(), username, file_name)
    if not os.path.exists(is_exist):
        r = requests.get(url)
        with open(f'./{location}/{file_name}', 'wb') as f:
            for chunk in r.iter_content(1000):
                f.write(chunk)
        print(f"{file_name} downloaded succesfully!")
    else:
        print(f"{file_name} already exists")
        
url = args.url
tags = args.tag
detail = args.detail  
photos = args.photos
videos = args.videos
username = args.username

if username:
    account = Instagram(account=username)
    if detail:
        data, file_name = account.save_details()
        dump_json(data, file_name)

    if photos:
        print(f"Getting {username} photos!!")
        for contents in account.contents.get_all_contents():
            for content in contents:
                if content['type'] == 'photo':
                    if detail:
                        dump_json(content, content['id'])
                    download(content['download_url'], username, content['file_name'])
        

    
    elif videos:
        print(f"Getting {username} videos!!")
        for contents in account.contents.get_all_contents():
            for content in contents:
                if content['type'] == 'video':
                    if detail:
                        dump_json(content, content['id'])
                    download(content['download_url'], username, content['file_name'])
                
    else:
        for contents in account.contents.get_all_contents():
            for content in contents:
                if detail:
                    dump_json(content, content['id'])
                download(content['download_url'], username, content['file_name'])
            

elif url:
    post = Instagram(url=url)
    post.download_single_post()

else:
    os.system("python main.py --help")


            