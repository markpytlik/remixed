
# help me 

import re

class Helper():
    @staticmethod
    def json_resp_only(req, data):
        response = data
        req.set_header("Content-type", 'application/javascript')
        req.finish(response)

    @staticmethod
    def resp(data, success = True):
        if data is not None:
            data['success'] = success

        return data

    @staticmethod
    def resp_http(req, data, success = True):
        response = Helper.resp(data, success)
        req.set_header("Content-type", 'application/javascript')
        req.finish(response)

    @staticmethod
    def clean(data):
        #data = data.encode('utf-8', errors='ignore') # Get rid of bad char
        data = re.sub(r'\([^)]*\)', '', data) # Remove anything inside ( )
        data = re.sub(r'\[[^)]*\]', '', data) # Remove anything inside [ ]
        data = re.sub(r'( - ).*', '', data) # Remove anything after a - ie: XYZ - Radio Edit
        return data
        
    @staticmethod
    def urltouri(url):
        m = re.match(r"[https?://[www\.]*?]*?[open|play]*\.spotify\.com/(album|track|user)/([a-zA-Z0-9\.]*)/(playlist)/([a-zA-Z0-9]+)", url)
        if m:
            
            user = m.group(1)
            user_id = m.group(2)
            pl = m.group(3)
            pl_id = m.group(4)
            
            if user != "user" or pl != "playlist":
                return None

            return "spotify:{0}:{1}:{2}:{3}".format(user, user_id, pl, pl_id)
        else:
            return None