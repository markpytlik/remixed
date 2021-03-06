/* App.js - backbone */

var App = (function(){

	var App = function(){
		
	}

	App.prototype.init = function(first_argument) {
		
		this.searchBox      = $('#playlist-link')
		this.loginForm      = $('#login-form')
		this.playlistForm   = $('#playlist-form')
		this.playlistSubmit = $( '#playlist-form-submit' )
		this.progressBar    = $('.playlist-import-progress')
		this.currentSearch  = $('#current-search-text')
		this.currentHit     = $('#current-hit-text')
		this.currentMiss    = $('#current-miss-text')
		this.matchBox       = $('.import-step-2')

		// Bind login button
		this.loginForm.bind('submit', function(e){
			e.preventDefault();

			Remixed.App.login();
		});

		//Bind change event for
		this.searchBox.bind('input', function(e){
			e.preventDefault();

			Remixed.App.verify_playlist();
		});

		// Bind form submission
		this.playlistForm.bind('submit', function(e){
			e.preventDefault();

			Remixed.App.send_playlist();
		});

	};

	App.prototype.verify_playlist = function(){

		var t = this;

		$.ajax({
			'url' : 'cpl',
			'data' : JSON.stringify({
				'link' : this.searchBox.val()
			}),
			type : 'post',
			success : function(d){
				if(d.success){
					t.searchBox.attr('data-valid', "true")
				}
				else{
					t.searchBox.attr('data-valid', "false")
				}

				// TODO: Update some visual indicator of success or failure
			}   
		})
	}

	App.prototype.login = function() {
		var button = $( '#btn-login' );

		Remixed.UI.spin( button );

		$.ajax({
			'url' : 'login',
			'data' : this.loginForm.serialize(),
			'type' : 'post',
			success : function(d){
				Remixed.UI.message({
					'rehide' : false,
					'response' : d
				});

				if ( ! d.success ) {
					Remixed.UI.spin( button, true );
					button.find( '.text' ).html( 'Sign In' );
				}
			}
		})

	};

	App.prototype.import = function(tracks, playlist){

		$.ajax({
			'url' : 'crunch',
			type : 'POST',
			data: JSON.stringify({'playlist_title' : playlist, 'tracks' : tracks}),
			success : function(d){

				Remixed.UI.message({
					'response' : d,
					'rehide' : true,
					'timeout' : 3000
				})


				Remixed.App.matchBox.fadeOut();
				Remixed.App.progressBar.css('width', '0%')
				Remixed.App.searchBox.prop('disabled', false)
				$( '#playlist-form-submit' )
					.css( 'background-color', '#0078e7' )
					.text( 'Find Matches' );

					$( '.playlist-form-submit-progress-back' ).removeClass( 'in-progress' );

				Remixed.App.searchBox.val('').blur()
				Remixed.App.currentSearch.html('...')
				Remixed.App.currentMiss.html('0')
				Remixed.App.currentHit.html('0')
			}
		})
	};

	function sortByKey(array, key) {
    	return array.sort(function(a, b) {
        	var x = a[key]; var y = b[key];
        	return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    	});
	}

	App.prototype.get_spotify_pl_complete = function(tracks, playlist){
			cur_track_num = 0;

			hits = [], misses = [];

			var t = this;
			$.each(tracks, function(){
				track = this;
				total_tracks = tracks.length

				if(track.valid) {

					$.ajax({
						'url' : 'find',
						'type' : 'post',
						'data' : JSON.stringify(track),
						error : function(){
							cur_track_num++;
						},
						success : function(d){
							 
							var index = d.match.meta.index

							if (d.match.valid)
								hits.push( {"id" : d.match.ids.google, "type" : "2", "index" : index})
							else
								misses.push( { } )

							cur_track_num  ++;

							var progress_percent = ( cur_track_num / total_tracks ) * 100;
							t.progressBar.css('width', "{0}%".format(progress_percent))

							t.currentSearch.html(d.match.meta.title);

							t.currentMiss.html(misses.length)
							t.currentHit.html(hits.length)

							// Sort, this is bad, the tracks should be inserted into array in proper order. Whatever
							sortByKey(hits, 'index')

							if(cur_track_num == total_tracks)
							{
								t.import(hits, playlist);                
							}
						}
					});
				}
		})
	}

	App.prototype.send_playlist = function() {
		
		// Ensure we have a valid sp URI, this is checked better on server side as well
		if(this.searchBox.attr('data-valid') != "true"){
			Remixed.UI.message({
				'message' : "please input a valid playlist url",
				'success' : false
			})
	
			return;
		}

		this.searchBox.prop( 'disabled', true );
		
		this.matchBox.slideDown();

		$( '#playlist-form-submit' )
			.css( 'background-color', 'transparent' )
			.text( 'Importing...' );

		$( '.playlist-form-submit-progress-back' ).addClass( 'in-progress' );

		var t = this;

		$.ajax({
			'url' : 'playlist',
			'data' : JSON.stringify({
				'link' : this.searchBox.val()
			}),
			type : 'POST',
			success : function(d) {

				if(!d.success){
					Remixed.UI.message({
						'response' : d,
						'rehide' : true,
						'timeout' : 3000
					})

					return;
				}
				
				t.get_spotify_pl_complete(d.tracks, d.playlist_title);
			}
		})
		
	};

	return App;
})();   
