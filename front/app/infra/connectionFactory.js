module.exports = function(){
    return createDBConnection;
}

var createDBConnection = function(){
    var mysql = require("mysql");
    var connectionData = require("./connectionData")();
    var env = process.env.NODE_ENV;

    //console.log(connectionData())
    
    if(!process.env.NODE_ENV || process.env.NODE_ENV == 'development'){
            return mysql.createConnection(connectionData.development);
    }

    if(process.env.NODE_ENV == 'production'){
        return mysql.createConnection(connectionData.production);
    }
}
