var Remixed = (function(){

    Logger = new Logger()
    App = new App();
    UI = new UI()

    return {
        Logger : Logger,
        App : App,
        UI : UI,

        init : function(){
            Logger.log("Inited")
        }
    };
})();

$(document).ready(function(){
    Remixed.App.init()
    Remixed.UI.init()
    console.log(Remixed)
});
