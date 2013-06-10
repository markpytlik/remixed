import app.base
import urllib2
import re
import json
import tornado
import tornado.auth
import time
from app.helper import Helper

from spotify import ArtistBrowser, Link, ToplistBrowser, SpotifyError
from spotify.manager import (
    SpotifySessionManager, SpotifyPlaylistManager, SpotifyContainerManager)


class HomeHandler(app.base.BaseHandler):
    def get(self):
        self.render("index.html")
	
class CheckPlayList(app.base.BaseHandler):
	def check_xsrf_cookie(self):
		pass

	def post(self):
		try:
			track_data = json.loads(self.request.body)
		except:
			return self.resp({'tracks' : None, 'message' : "Missing JSON body"}, False)

		uri = Helper.urltouri(track_data['link'])
		
		if uri is None:
			return self.resp({'tracks' : None, 'message' : 'Invalid Spotify URL'}, False)

		return self.resp({}, True)

class GetSpotifyTracks(app.base.BaseHandler):
	def check_xsrf_cookie(self):
		pass

	def post(self):
		user = self.get_current_user()

		if user is None:
			return self.resp({'message' : "please login, you will be redirected to login page...", "next" : "/login"}, False)

		try:
			track_data = json.loads(self.request.body)
		except:
			return self.resp({'tracks' : None, 'message' : "Missing JSON body"}, False)

		uri = Helper.urltouri(track_data['link'])
		
		if uri is None:
			return self.resp({'tracks' : None, 'message' : 'Invalid Spotify URL'}, False)

		playlist_link = Link.from_string(uri)
		playlist = playlist_link.as_playlist()

		tracks = []
		index = 0
		if self.sp.wait(playlist) is None:
		    print "Failed to load playlist."
		else:	
			pl = self.db.get("SELECT * FROM Playlist WHERE spotify_id = %s", playlist_link.__str__())
			if pl is None:
				pl_id = self.db.execute_lastrowid("INSERT into Playlist (spotify_id, name, User_id) VALUES (%s, %s, %s)", 
					playlist_link.__str__(), str(playlist.name()), str(user.id))
			else:
				pl_id = pl.id

			for index, track in enumerate(playlist):
				if self.sp.wait(track) is not None:
					try:
						tracks.append({'title' : track.name(), 
										'album' : track.album().name(), 
										'artist' : track.artists()[0].name(), 
										'index' : index, 
										'valid' : True, 
										'id' : str(Link.from_track(track)),
										'pl_id' : str(pl_id)})
					except:
						tracks.append({'valid' : False})
				else:
					tracks.append({'valid' : False})

				index += 1
				
		return self.resp({'playlist_title' : playlist.name(), 'tracks' : tracks}, True)

			