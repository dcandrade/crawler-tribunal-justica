var app = require("./config/express")();
var http = require("http").Server(app);

var port = process.env.PORT || 3000

http.listen(port, function(){
    console.log("Server online");
});