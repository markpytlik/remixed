var UI = (function(){

    var UI = function(){
    }

    UI.prototype.init = function(){

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

        pageMessage = $('.page-message')
        $.extend( settings, options );       

        pageMessage.removeClass("success").removeClass("error").removeClass('muted')

        if(settings.response != null)
            pageMessage.fadeIn()
            .addClass( settings.response.success == true ? "success" : "error" )
            .addClass(settings.css)
            .html( settings.response.message )  
        else
            pageMessage.fadeIn()
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
                pageMessage.fadeOut();
            }, settings.timeout );
        }
    };

    UI.prototype.page = function(){
        var currentPage = 0;
        var numPerPage = 10;
        var table = $('#table-results')

        table.bind('repaginate', function() {
            table.find('tbody tr:not(.first-row)').hide().slice(currentPage * numPerPage, (currentPage + 1) * numPerPage).show();

            $('.page-link').removeClass('active');
            $('#page-parent-' + currentPage).addClass('active')

        });

        table.trigger('repaginate');

        var numRows = table.find('tbody tr:not(.first-row)').length;
        var numPages = Math.ceil(numRows / numPerPage);

        var pages = $('#pages')

        for (var page = 0; page < numPages; page++) {
             var pageLink = '<li class="page-link" id="page-parent-' + page +'"> <a href="#" id="page-' + page + '">' + ( page + 1 ) + '</a></li>'

            pages.append(pageLink);

            $('#page-' + page).bind('click', {
                next_page: page
            }, function(e) {
                e.preventDefault();
                currentPage = e.data['next_page'];
                table.trigger('repaginate');
            });

            if(currentPage == 0)
                $('#page-parent-0').addClass('active')

        }

    };

    return UI;
})();   
