module.exports = function(app){
    var http = require('http');
    app.get('/', function(request, response){
        var connection = app.infra.connectionFactory();
        var productsDAL = new app.infra.ProductsDAO(connection);
        var options = {
            host: "localhost",
            port: 8888,
            path: '/courts',
            method: 'GET'
        };
        

        http.request(options, function(res) {
            res.setEncoding('utf8');

            res.on('data', function (chunk) {
              result = JSON.parse(chunk);
              response.render('home/index',{
                  courts: result.courts
              })
            });
            
        }).end();

    });
}