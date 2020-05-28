import os
import sys
import json
import random
import requests

class Functions:
    """ Set of useful functions that will help us get the job done :) """
    def __init__(self, url=None):
        self.url = url

    def _send_requests(self, url):
        """ Send requests and return the json response object """
        header = self._get_headers()
        response = requests.get(url, headers=header)
        self._raise_for_error(response)
        return response
    

    def _raise_for_error(self, r):
        """ Print error if requests was not completed
            r: response object from requests """

        try:
            r.raise_for_status
        except Exception as e:
            print(str(r))
            sys.exit(0)

    
    def _get_headers(self):
        """ Generates random headers from header file """
        try:
            file = "./headers.json"
            with open(file) as f:
                headers = json.load(f)    
            return random.randrange(headers)
        
        except:
            return {"User-Agent": "Mozila/5.0"}


    def _download_contents(self, url, file_name=None, location=None):
        """ Download the parse files
        url: the photo or video url which is to be downloaded 
        file_name: name of the file
        location: Directory to download the file  """

        contents = self._send_requests(url).content
        if not file_name:
            file_name = "/".split(url)[-1]
        if not location:
            location = f"./Download_File"
        if not os.path.exists(location):
            os.makedirs(location)
        
        path = os.path.join(location, file_name)        
        
        with open(path, "wb") as f:
            f.write(contents)

