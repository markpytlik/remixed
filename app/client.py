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

                cr_pl_resp = sesh.request(**cr_pl_params)


    @staticmethod
    def find_song(user, track, db):
        
        if user is None:
            return False
        else:
            sesh = requests.Session()
            url = 'https://play.google.com/music/services/search'

            track_title = Helper.clean(track['title'])
            track_artist = Helper.clean(track['artist'])
            track_album = Helper.clean(track['album'])
            track_id = track['id']
            pl_id = track['pl_id']
            track_index = track['index']

            search_term = track_title + " - " + track_artist
            
            cr_pl_params = dict()
            cr_pl_params['url'] = url
            cr_pl_params['method'] = 'POST'
            cr_pl_params['data'] = '[["",1],["' + search_term + '",1]]'
            cr_pl_params['headers'] = {'Authorization' : 'GoogleLogin auth='+ user.auth}
            cr_pl_params['params'] = { 'u' : 0, 'xt' :  user.xt, 'format' : 'jsarray' }

            all_access_song_id = None

            match = db.get('SELECT * FROM remixed.Match where spotify_id = %s', str(track['id']))

            # We have a match cached?
            if match is not None:
                print "Using cached match"
                all_access_song_id = match.access_id
            else: # No match, let's hit Google
                try:
                    cr_pl_resp = sesh.request(**cr_pl_params)

                    valid = False
                    # Oh dear god no!
                    try:
                        full_result = cr_pl_resp.text
                        
                        index_of_care = full_result.find(']\n]\n]')

                        slim_result =full_result[:index_of_care + 2]

                        clean_result = re.sub(',+', ',', slim_result) + ']]]]'

                        ret = json.loads(clean_result)
                        
                        ret = ret[1][0]
                    except:
                        ret = dict()
                        ret[0] = None
                        pass
                except:
                    ret = dict()
                    ret[0] = None
                    pass

                # Did we find a match?
                if ret[0] is not None and track is not None:
                    # Yes, log both the songs, set a match
                    
                    access_id = ret[0][0]

                    spotify = db.execute("INSERT into remixed.SpotifySong (platform_id, artist, title, album) VALUES (%s, %s, %s, %s)", 
                            track['id'], track_artist, track_title, track_album)

                    access = db.execute("INSERT into remixed.AccessSong (platform_id, title, artist, album) VALUES (%s, %s, %s, %s)", 
                            access_id, "", "", "")

                    match = db.execute_lastrowid("INSERT into remixed.Match (spotify_id, access_id) VALUES (%s, %s)", 
                        track['id'], access_id)

                    db.execute("INSERT into remixed.Playlist_has_Match (playlist_id, match_id) VALUES (%s, %s)", pl_id, match)

                    all_access_song_id = access_id

                # we still didn't
                else:
                    pass

            # Build the output

            id_out = {
                'google' : all_access_song_id,
                'spotify' : track_id
            }

            meta = {
                'index' : track_index,
                'artist' : track_artist,
                'title' : track_title,
                'album' : track_album
            }

            return Helper.resp({   
                    'valid' : True if (all_access_song_id is not None) else False,             
                    'ids' : id_out,
                    'meta' : meta
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
                          
            return Helper.resp({"playlist" : json, 'message' : "Playlist " + name + " was created!"})