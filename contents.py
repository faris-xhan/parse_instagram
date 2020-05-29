from functions import Functions

class Contents(Functions):
    """ A class to download or save media contents details """

    def __init__(self, account_id=None, url=None):
        """ Intialize the content class and create a content object """
        self.account_id = account_id
        self.url = url
        self.end_cursor = ""          
    
    def get_all_contents(self):
        """  Get all the contents from the server 
            limit: max content to return ( 0 >= limit < 50 )"""
        self.has_next_page = True
        
        while self.has_next_page:
            contents = self._send_query_request()
            for content in contents:
                yield self._parse_content_details(content['node'])

    def download_single_post(self):
        """ Download the single post from given url """
        response = self._send_requests(self.url).json()
        detail = self._parse_content_details(response['graphql']['shortcode_media'])
        file_name = detail['id']
        download_url = detail['download_url']
        self._download_contents(download_url, file_name=file_name)

    def _parse_content_details(self, content):
        """ parse one content detail at a time and send them back 
            json_content: content Json Response """
        if content['__typename'] == 'GraphSidecar':
            return self._parse_graph_side_car(content)

        elif content['__typename'] == 'GraphImage':
            return self._parse_graph_image(content)

        elif content['__typename'] == 'GraphVideo':
            return self._parse_graph_video(content)
    
    def _parse_graph_image(self, img_obj):
        """ Parse the detail of the GraphImage object 
            img_obj: JSON data of the image object """
        data = {}
        data['type'] = 'photo'
        data['id'] = img_obj['id']
        data['file_name'] = data['id'] + '.jpg'
        data['download_url'] = img_obj['display_url']
        try:
            data['comments'] = img_obj['edge_media_to_comment']['count']
        except:
            data['comments'] = None
        data['caption'] = img_obj['edge_media_to_caption']['edges'][0]['node']['text']
        data['timestamp'] = img_obj['taken_at_timestamp']
        data['location'] = img_obj['location']

        return [data]

    def _parse_graph_video(self, vid_obj):
        """ Parse the graph video object 
            vid_obj: JSON data of the object """
        data = {}
        data['type'] = 'video'
        data['id'] = vid_obj['id']
        data['file_name'] = data['id'] + '.mp4'
        data['download_url'] = vid_obj['video_url']
        data['caption'] = vid_obj['edge_media_to_caption']['edges'][0]['node']['text']
        data['timestamp'] = vid_obj['taken_at_timestamp']
        data['location'] = vid_obj['location']
        try:
            data['comments'] = vid_obj['edge_media_to_comment']['count']
        except:
            data['comments'] = None

        return [data]


    def _parse_graph_side_car(self, side_car_obj):
        """ Parse the graph side car object (Instagram posts that have multiple photos init) 
            side_car_obj: JSON data of the object """
        all_contents = []
        for content in side_car_obj['edge_sidecar_to_children']['edges']:
            content = content['node']
            data = {}
            if content['__typename'] == 'GraphImage':
                data['type'] = 'photo'
                data['download_url'] = content['display_url']
                data['file_name'] = content['id'] + '.jpg'

            elif content['__typename'] == 'GraphVidoe':
                data['type'] = 'video'
                data['download_url'] = content['video_url']
                data['file_name'] = content['id'] + '.mp4'

            try:
                data['comments'] = side_car_obj['edge_media_to_comment']['count']
            except:
                pass
        
            data['id'] = content['id']
            data['location'] = side_car_obj['location']
            data['timestamp'] = side_car_obj['taken_at_timestamp']
            
            all_contents.append(data)
        return all_contents


    def _send_query_request(self):
        """ Send and Prase the query requests and return all of contents """

        self.p_url = self._generate_query(limit=50)
        self.response = self._send_requests(self.p_url).json()
        
        self.total_post = self.response['data']['user']['edge_owner_to_timeline_media']['count']
        self.has_next_page = self.response['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        self.end_cursor = self.response['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        self.contents = self.response['data']['user']['edge_owner_to_timeline_media']['edges']
        return self.contents

    
    def _generate_query(self, limit=20):
        """ Generates the query to get the contents data
            limit: Number of contents to return (0 <= limit > 50) 
            query_hash: this is a special instagram hash for requesting contents """

        query_hash = "44efc15d3c13342d02df0b5a9fa3d33f"
        self.variables = { "id": str(self.account_id),
                          "first": str(limit), 
                         "after": str(self.end_cursor) }

        query = f"https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables={self.variables}"
        
        return query.replace("'", '"') # For some reason json contents of variables 
                                      # with single quotes wasn't a valid json data for instagram api
    
    def __repr__(self):
        return f"< CONTENTS OBJECT >"
