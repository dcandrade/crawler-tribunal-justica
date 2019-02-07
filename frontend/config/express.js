var express = require("express");
var expressLoad = require("express-load");
var bodyParser = require("body-parser");
var expressValidator = require("express-validator");


module.exports = function(){
    var app = express();

    app.use(express.static("./app/public"));
    app.set("view engine", "ejs");
    app.set("views", "./app/views");

    app.use(bodyParser.urlencoded({extended:true}));
    app.use(bodyParser.json());
    app.use(expressValidator());

    expressLoad("routes", {cwd:"app"})
        .then("infra")
        .into(app);

    app.use(function(request, response, next){
         response.status(404).render("errors/404");
         next();
    });

    app.use(function(error, request, response, next){ //Called first if error occurs
        if (process.env.NODE_ENV == "production") {
            response.status(500).render("errors/500");
            return;            
        }
        next(error);
   });

    return app;
}