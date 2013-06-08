/* UI.js - This does UI stuff */

var UI = (function(){

    var UI = function(){
    }

    UI.prototype.init = function(){
        this.pageMessage = $('.page-message')
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
                this.pageMessage.fadeOut();
            }, settings.timeout );
        }
    };

    return UI;
})();   
