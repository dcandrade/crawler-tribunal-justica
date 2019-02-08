var http = require('http');

module.exports = function(app){
    app.get('/', function(request, response){

        var options = {
            host: "loadbalancer",
            port: 8080,
            path: '/courts',
            method: 'GET'
        };
        
        var errors = request.query['errors'];
        var errorList = [];

        if(errors){
            errorList = errors.split(',');
        }
        

        http.request(options, function(res) {
            res.setEncoding('utf8');

            res.on('data', function (chunk) {
              result = JSON.parse(chunk);
              response.render('home/index',{
                  courts: result.courts,
                  errors:errorList
              })
            });
            
        }).end();

    });
}