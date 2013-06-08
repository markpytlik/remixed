var Logger = (function(){
    var Logger = function(){

    }

    Logger.prototype.now = function(){ 
        date = new Date()
        return date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
    };

    Logger.prototype.log = function(arg, class_name) {
        time = this.now();
        console.log( (( class_name  != undefined ) ? "[" + class_name + "] - [" + time + "]: " : time + ": ") + arg)        
    };

    return Logger;
})();   
