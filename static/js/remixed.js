/* Remixed.js - Namespace(s) and JS init */

var Remixed = (function(){

    Logger = new Logger()
    App = new App();
    UI = new UI()

    return {
        Logger : Logger,
        App : App,
        UI : UI,

        extend_prototypes : function(){

            // Extend string to create a sprintf type deal, via Google
            if (!String.prototype.format) {
                String.prototype.format = function() {
                    var args = arguments;
                        return this.replace(/{(\d+)}/g, function(match, number) { 
                          return typeof args[number] != 'undefined'
                            ? args[number]
                            : match;
                });
              };
            }

        },

        init : function(){

            this.extend_prototypes();
            
            Logger.log("Remixed init!")
        }
    };
})();

$(document).ready(function(){
    Remixed.init();
    Remixed.App.init()
    Remixed.UI.init()
});
