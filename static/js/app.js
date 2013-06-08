var App = (function(){
    var App = function(){
        //Remixed.Logger.log("Made")
    }

    App.prototype.init = function(first_argument) {
        
        buttonAdd = $('#btn-add');

        buttonAdd.bind('click', function(e){
           
           e.preventDefault()
            
            songs = []
            $("input[type=checkbox]:checked:not(.first-checkbox)").each(function()
            {
                console.log(this)
                songs.push({'id' : $(this).attr('data-id'), 'type' : '2'})
            })

            $.ajax({
                'url' : 'crunch',
                type : 'POST',
                data: JSON.stringify({'playlist_title' :  $('#playlist-form').attr('playlist-id'), 'tracks' : songs}),
                success : function(d){
                    Remixed.UI.message({
                        'response' : d,
                        'rehide' : true
                    })
                }
            })
        })

        checkboxCheckAll = $('#checkbox-check-all')
        checkboxCheckAll.bind('click', function(){
            $('input[type=checkbox]').filter(function(){ return !this.disabled }).attr('checked', true)
        })

        playlistValidityLabel = $('.control-group-pl')

        loginForm = $('#login-form')
        loginForm.bind('submit', function(e){
            e.preventDefault();
            $.ajax({
                'url' : 'login',
                'data' : loginForm.serialize(),
                'type' : 'post',
                success : function(d){
                    
                    Remixed.UI.message({
                        'rehide' : false,
                        'response' : d
                    })
                }
            })

            return false;
        });

        searchBox = $('#playlist-link')
        searchBox.bind('input', function(e){

            playlistValidityLabel.show();

            $.ajax({
                'url' : 'cpl',
                'data' : JSON.stringify({
                    'link' : searchBox.val()
                }),
                type : 'post',
                success : function(d){
                    if(d.success){
                        playlistValidityLabel.addClass('success')
                        searchBox.attr('data-valid', "true")
                    }
                    else{
                        playlistValidityLabel.addClass('error')
                        searchBox.attr('data-valid', "false")
                    }
                }   
            })
        });
        
        playlistForm = $('#playlist-form')
        playlistForm.bind('submit', function(e){
            e.preventDefault();

            if(searchBox.attr('data-valid') != "true"){
                Remixed.UI.message({
                    'message' : "please input a valid playlist url",
                    'success' : false
                })
                
                return;
            }
            else
                playlistValidityLabel.fadeOut();

            $.ajax({
                'url' : 'playlist',
                'data' : JSON.stringify({
                    'link' : $('#playlist-link').val()
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

                    console.log(JSON.stringify(d.tracks));

                    playlist_title = d.playlist_title

                    playlistForm.attr('playlist-id', playlist_title )

                    Remixed.UI.message({
                        'message' : "Preparing to process &mdash; " + playlist_title,
                        'success' : true,
                        'css' : 'muted'
                    })

                    $('#table-results').show();

                    for (var i = 0; i < d.tracks.length; i++) {

                        if( !d.tracks[i].valid )
                            continue;

                        var dummy_art = 'https://ssl.gstatic.com/music/fe/f7ce26e1c6738383c444c02f238a678b/default_album_art_big_card.png'
                        var html = 
                                   [
                                    '<tr class="warning" data-id="-1" id="row-' + i + '">',
                                        '<td class="table-results-cell"><input disabled class="checkbox-result" type="checkbox" id="checkbox-' + i + '"></input></td>',
                                        '<td class="table-results-cell thumb"><img src="' + dummy_art + '" id="img-' + i + '"/></td>',
                                        '<td>',
                                            '<div><strong>' + d.tracks[i].title + '</strong></div>',
                                            '<div>',
                                                '<p class="small muted"><small>'+ d.tracks[i].artist +'</small></p>',
                                            '</div>',
                                        '</td>',
                                    '</tr>'
                                   ].join('\n');

                        $('#table-results tr:last').after(html)
                    }

                    Remixed.UI.page()

                    cur_num = 1
                    $.each(d.tracks, function(){
                        track = this;
                        total_tracks = d.tracks.length

                        $.ajax({
                            'url' : 'find',
                            'type' : 'post',
                            'data' : JSON.stringify(track),
                            error : function(){
                                cur_num++;
                            },
                            success : function(d){
                                 
                                var index = d.match.index

                                var row = $('#table-results > tbody > tr').eq(index + 1);

                                row.toggleClass("warning", false)

                                if (d.match != null && d.match.google != null && d.match.spotify != null)
                                {
                                    row.addClass("success")
                                    $('#img-' + index).attr('src', d.match.google[2])
                                    row.attr('data-id', d.match.google[0])
                                    $('#checkbox-' + index).removeAttr('disabled').attr('data-id', d.match.google[0])
                                }
                                else
                                {
                                    row.addClass("error")
                                }

                                row.attr('data', JSON.stringify(d.match))


                                var msg = 'proccessing '+ playlist_title + ' &mdash; track ' + cur_num + ' of ' +
                                        total_tracks + ' (' + Math.floor((cur_num/total_tracks * 100)) + '%)'

                                Remixed.UI.message({
                                    'message' : msg,
                                    'rehide' : false,
                                    'css' : "muted"
                                })

                                cur_num  ++;

                                if( cur_num == total_tracks ){
                                    $('#btn-add').fadeIn();
                                    $('.page-message').hide();
                                }
                            }
                        })
                    })
                }
            })
        });
    };
    return App;
})();   
