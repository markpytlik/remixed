
from app.client import GoogleClient
import app.base
import json

from app.helper import Helper as Helper

class Crunch(app.base.BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self):
        data = json.loads(self.request.body)
        ret = GoogleClient.create_then_add(self.get_current_user(), data['playlist_title'], data['tracks'], self.db)
        return self.resp({'message' : "Import done!"}, True)
            
class FindSongHandler(app.base.BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def post(self):
        track = json.loads(self.request.body)

        if track is None:
            return self.resp({"message" : track['message']}, False)

        match = GoogleClient.find_song(self.get_current_user(), track, self.db)

        if match['success'] == True:
            return self.resp({'match' : match})
        else:
            return self.resp({"message" : match['message']}, False)