/* Logger.js - Stupidly simple (useless) console.log wrapper */

var Logger = (function(){

    var Logger = function(){
        this.date = new Date();
    }

    Logger.prototype.now = function(){ 
        return this.date.getHours() + ":" + this.date.getMinutes() + ":" + this.date.getSeconds();
    };

    Logger.prototype.log = function(arg) {

        time = this.now();

        // Don't build a string, we want the object dumped
        if(arg != null && typeof arg === 'object')
            console.log(arg);

        // Append some useful(?) info
        else 
            console.log( "[{0}]: {1}" .format(this.now(), arg) );
    };

    return Logger;
})();   
