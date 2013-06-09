import os.path
import re
import torndb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
import thread
import app.spot
import app.auth
import app.music
import time
import wsgiref.handlers
from tornado.options import define, options
import tornado.wsgi
from wsgiref.simple_server import make_server
import sys
import csv

DEV = True


if DEV is True:
    MYSQL_HOST = "remixed-dev.ctcjjejttofu.us-east-1.rds.amazonaws.com:3306"
    MYSQL_USER_NAME = sys.argv[1]
    MYSQL_PASSWORD = sys.argv[2]
    DATABASE = "remixed"
    SPOTIFY_USER = "RemixedApp"
    SPOTIFY_PASSWORD = sys.argv[3]
else:
    file = open('.remixed-prod-conf')

    if file is not None:
        args = file.read().split(',')
        
        MYSQL_HOST = args[0]
        MYSQL_USER_NAME = args[1]
        MYSQL_PASSWORD = args[2]
        DATABASE = "remixed"
        SPOTIFY_USER = "RemixedApp"
        SPOTIFY_PASSWORD = args[3]

define("mysql_host", default=MYSQL_HOST, help="database host")
define("mysql_database", default=DATABASE, help="")
define("mysql_user", default=MYSQL_USER_NAME, help="")
define("mysql_password", default=MYSQL_PASSWORD, help="")


from spotify import ArtistBrowser, Link, ToplistBrowser, SpotifyError
from spotify.manager import (
    SpotifySessionManager, SpotifyPlaylistManager, SpotifyContainerManager)

class SpotifyDriver(SpotifySessionManager):
    appkey_file = os.path.join(os.path.dirname(__file__), 'spotify_appkey.key')

    def __init__(self, *a, **kw):
        SpotifySessionManager.__init__(self, *a, **kw)
        print "Logging in, please wait..."

    # This needs a timeout
    def wait(self, obj, timeout=3):
        start = time.time()
        while not obj.is_loaded():
            self.session.process_events()

        return True

    def logged_in(self, session, error):
        if error:
            print error
            return

        print "Logged into Spotify!"


class Remixed(tornado.web.Application):
  def __init__(self):
    handlers = [
        (r"/", app.spot.HomeHandler),
        (r"/cpl", app.spot.CheckPlayList),
        (r"/playlist", app.spot.GetSpotifyTracks),
        (r"/find", app.music.FindSongHandler),
        (r"/crunch", app.music.Crunch),
        (r"/login", app.auth.LoginHandler),
        (r"/logout", app.auth.LogoutHandler)

    ]

    settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="!NEEDSTOBEMORERANDOM?",
            debug=True
        )

    
    tornado.web.Application.__init__(self, handlers, **settings)


    self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

    print "Connected to DB"

    self.sp = SpotifyDriver(SPOTIFY_USER, SPOTIFY_PASSWORD, True)
    
    thread.start_new_thread(self.sp.connect, ())

tornado.options.parse_command_line()
http_server = tornado.httpserver.HTTPServer(Remixed())
http_server.listen(8889)
tornado.ioloop.IOLoop.instance().start()

print "Server Started"

