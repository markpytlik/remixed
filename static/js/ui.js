/* UI.js - This does UI stuff */

var UI = (function(){

    var UI = function(){
    }

    UI.prototype.init = function(){
        this.pageMessage = $('.page-message')
    };

    UI.prototype.spin = function(el, hide){

        var spinner_opts = {
          lines: 9, // The number of lines to draw
          length: 5, // The length of each line
          width: 3, // The line thickness
          radius: 8, // The radius of the inner circle
          corners: 1, // Corner roundness (0..1)
          rotate: 0, // The rotation offset
          direction: 1, // 1: clockwise, -1: counterclockwise
          color: '#000', // #rgb or #rrggbb
          speed: 1, // Rounds per second
          trail: 60, // Afterglow percentage
          shadow: false, // Whether to render a shadow
          hwaccel: false, // Whether to use hardware acceleration
          className: 'spinner', // The CSS class to assign to the spinner
          zIndex: 2e9, // The z-index (defaults to 2000000000)
          top: 'auto', // Top position relative to parent in px
          left: 'auto' // Left position relative to parent in px
        };

        if(!hide)
            $('#' + el).show().spin();
        else
            $('#' + el).hide().spin(false);
    };

    UI.prototype.message = function(options){
        var settings = {
            message  : "",
            response : null,
            timeout  : 1500,
            rehide   : false,
            success : true,
            css : "",
            redirect_wait : 2000
        }

        $.extend( settings, options );       

        this.pageMessage.removeClass("success").removeClass("error").removeClass('muted')

        if(settings.response != null)
            this.pageMessage.fadeIn()
            .addClass( settings.response.success == true ? "success" : "error" )
            .addClass(settings.css)
            .html( settings.response.message )  
        else
            this.pageMessage.fadeIn()
            .addClass(settings.success == true ? "success" : "error")
            .addClass(settings.css)
            .html(settings.message)

        if(settings.response != null && settings.response.next != undefined){
            setTimeout( function(){
                window.location.href = settings.response.next
            }, settings.redirect_wait );

        }
        else if(settings.next != undefined) {
            setTimeout( function(){
                window.location.href = settings.next
            }, settings.redirect_wait );
        }

        else if( settings.rehide ) {
            setTimeout(function(){
                Remixed.UI.pageMessage.fadeOut();
            }, settings.timeout );
        }
    };

    return UI;
})();   
