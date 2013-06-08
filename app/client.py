import cookielib
import re
import urllib
import urllib2
import json
import requests
import re
import sys
from app.helper import Helper

class GoogleClient():
    #{"playlistId":"a2532e45-8cd5-4b07-a0da-6216243a151d","songRefs":[{"id":"Trwioibhrokwtlwhusbvi4ie64u","type":2}],"sessionId":"61j8ml3efqb2"}

    @staticmethod 
    def create_then_add(user, playlist, tracks, db):
        if user is None:
            return False
        else:
            pl = GoogleClient.create_pl(user, playlist, db)


            if pl['success'] == True:
                sesh = requests.Session()
                url = 'https://play.google.com/music/services/addtoplaylist'

                cr_pl_params = dict()
                cr_pl_params['url'] = url
                cr_pl_params['method'] = 'POST'
                cr_pl_params['data'] = { 'json' : '{"playlistId" : "'+pl['playlist']['id']+'", "songRefs" : '+json.dumps(tracks)+'}' }
                cr_pl_params['headers'] = {'Authorization' : 'GoogleLogin auth='+ user.auth}
                cr_pl_params['params'] = { 'u' : 0, 'xt' :  user.xt }

            
            #print "*"+track_title+"*"

                cr_pl_resp = sesh.request(**cr_pl_params)

              #  print cr_pl_resp.text


    @staticmethod
    def find_song(user, track, db):
        #print user
        if user is None:
            return False
        else:
            sesh = requests.Session()
            url = 'https://play.google.com/music/services/search'

            track_title = Helper.clean(track['title'])
            track_artist = Helper.clean(track['artist'])
            track_album = Helper.clean(track['album'])

            search_term = track_title + " - " + track_artist
            
            #print search_term

            cr_pl_params = dict()
            cr_pl_params['url'] = url
            cr_pl_params['method'] = 'POST'
            cr_pl_params['data'] = '[["",1],["' + search_term + '",1]]'
            cr_pl_params['headers'] = {'Authorization' : 'GoogleLogin auth='+ user.auth}
            cr_pl_params['params'] = { 'u' : 0, 'xt' :  user.xt, 'format' : 'jsarray' }

            
            print "*"+track_title+"*"

            try:
                cr_pl_resp = sesh.request(**cr_pl_params)

                valid = False
                # Oh dear god no!
                try:
                    full_result = cr_pl_resp.text
                    
                    #print "*",full_result,"*"

                    index_of_care = full_result.find(']\n]\n]')

                    slim_result =full_result[:index_of_care + 2]

                    clean_result = re.sub(',+', ',', slim_result) + ']]]]'

                    print clean_result

                    ret = json.loads(clean_result)
                    
                    ret = ret[1][0]

                   # print ret
                except:
                    ret = dict()
                    ret[0] = None
                    pass
                    #return Helper.general_success()
                    #return Helper.resp({'message' :     }, False)
                    #return Helper.app_resp({'success' : False})
                    #return {'success' : False}

               # print ret
                #print ret[1][0]
            except:
                ret = dict()
                ret[0] = None
                pass

            return Helper.resp({                    
                    'google': ret[0],
                    'spotify': track,
                    'index' : track['index'],
                    'confidence' : 100
            })
          
    @staticmethod
    def create_pl(user, name, db):
        if user is None:
            return False
        else:
            sesh = requests.Session()
            url = 'https://play.google.com/music/services/addplaylist'
            cr_pl_params = dict()
            cr_pl_params['url'] = url
            cr_pl_params['method'] = 'POST'
            cr_pl_params['data'] =  {'json': '{"title": "' + name + '"}'}
            cr_pl_params['headers'] = {'Authorization' : 'GoogleLogin auth='+ user.auth}
            cr_pl_params['params'] = { 'u' : 0, 'xt' :  user.xt }

            cr_pl_resp = sesh.request(**cr_pl_params)

            json = cr_pl_resp.json()

            if json['title'] is None or json['id'] is None:
                return Helper.resp({'message' : "Unable to create playlist " + name}, False)
                #return Helper.general_success()
                #return {'success' : False}
            
            return Helper.resp({"playlist" : json, 'message' : "Playlist " + name + " was created!"})