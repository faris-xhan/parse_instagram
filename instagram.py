import re
from functions import Functions
from contents import Contents

class Instagram(Functions):
    def __init__(self, account=None, url=None):
        """ Initialize the Instagram class and add the account name """
        self.account = account
        self.post = url
        
        if self.account:
            self.account = account
            self.parse_detail()
            if not self.is_private:
                self.contents = Contents(self.id)
            else:
                self.contents = "Sorry, account is private !!"
        elif self.post:
            self.url = self._generate_single_post_url(url)
            self.post = Contents(url=self.url).post()

    def parse_detail(self):
        """ Parse account details from instagram """
        self.url = f"https://www.instagram.com/{self.account}/?__a=1" 
        response = self._send_requests(self.url).json()        
        response = response['graphql']['user']

        self.id = response['id']
        self.profile = response['profile_pic_url_hd']
        self.username = response['username']
        self.follower = response['edge_followed_by']['count']
        self.followed = response['edge_follow']['count']
        self.full_name = response['full_name']
        self.biography = response['biography']
        self.is_private = response['is_private']
        self.is_varified = response['is_verified']
        self.external_url = response['external_url']        
        self.business_category = response['business_category_name']
        self.is_business_account = response['is_business_account']

    def get_contents(self):
        """ Return a content object which can parse media contents of that account """
        return Contents(self.id)
    
    def download_profile(self):
        """ Download User Profile """
        self._download_contents(url=self.profile, file_name="profile.jpg")
    
    def _generate_single_post_url(self, url):
        """ parse account name 
            url: the given instagram account url """        
        try:
            regex = re.compile(r"(https://www)?instagram.com/p/(\w+)/.*")
            post_id = regex.search(url)[2]
            return f"https://www.instagram.com/p/{post_id}/?__a=1"
        
        except:
            return None


    def __repr__(self):
        return f"< Instagram {self.account} >"
