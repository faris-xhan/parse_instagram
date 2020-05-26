from send_requests import Requests

class Contents(Requests):
    """ A class to download or save media contents details """

    def __init__(self, account_id):
        """ Intialize the content class and create a content object """
        self.account_id = account_id
        self.end_cursor = ""          
    
    def get_all_contents(self):
        """  Get all the contents from the server 
            limit: max content to return ( 0 >= limit < 50 )"""
        self.has_next_page = True
        
        while self.has_next_page:
            contents = self._send_query_request()
            for content in contents:
                yield self._parse_content_details(content['node'])


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
        content = ['Photos']
        data['id'] = img_obj['id']
        data['url'] = img_obj['display_url']
        data['comments'] = img_obj['edge_media_to_comment']['count']
        # data['caption'] = img_obj['edge_media_to_caption']['edges']['0']['node']['text']
        data['timestamp'] = img_obj['taken_at_timestamp']
        data['location'] = img_obj['location']

        return data

    def _parse_graph_video(self, vid_obj):
        """ Parse the graph video object 
            vid_obj: JSON data of the object """
        data = {}
        data['content'] = 'Video'
        data['id'] = vid_obj['id']
        data['display_url'] = vid_obj['display_url']
        data['video_url'] = vid_obj['video_url']
        # data['caption'] = vid_obj['edge_media_to_caption']['edges']['0']['node']['text']
        data['timestamp'] = vid_obj['taken_at_timestamp']
        data['location'] = vid_obj['location']
        data['comments'] = vid_obj['edge_media_to_comment']['count']

        return data


    def _parse_graph_side_car(self, side_car_obj):
        """ Parse the graph side car object (Instagram posts that have multiple photos init) 
            side_car_obj: JSON data of the object """
        data = {}
        data['contents'] = []
        data['id'] = side_car_obj['id']
        data['display_url'] = side_car_obj['display_url']
        # data['caption'] = side_car_obj['edge_media_to_caption']['edges']['0']['node']['text
        data['timestamp'] = side_car_obj['taken_at_timestamp']
        data['location'] = side_car_obj['location']
        data['comments'] = side_car_obj['edge_media_to_comment']['count']
        
        for content in side_car_obj['edge_sidecar_to_children']['edges']:
            content = content['node']
            node = {}
            node['type'] = content['__typename']
            node['id'] = content['id']
            node['display_url'] = content['display_url']
            if node['type'] == 'GraphVideo':
                node['video_url'] = content['video_url']

            data['contents'].append(node)
        
        return data


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
        return f"< Contents Object -> id = {self.account_id} >"
