const axios = require('axios');
const { jsonToHTML } = require('nested-json-to-table')


module.exports = function(app){
    app.get("/process", function(request, response){
        console.log("-------------------------------")
        console.log(request.query)
        var court = request.query['court'];
        var id = request.query['number'];
        console.log(court)
        console.log(id);

        var options = {
            host: "localhost",
            port: 8888,
            path: '/get?process_number='+id,
            method: 'GET'
        };

        var url = 'http://localhost:8888/get?court='+court+'&process_number='+id;


        axios.get(url).then(res => {
            data = res.data;
            
            // Something bad happenned
            if(data['errors']){
                var errors = data['errors'];
                var errorString = encodeURIComponent(errors);

                response.redirect('/?errors=' + errorString);

            } else{ // Request is OK
                delete data["_id"];
                var transactions = data["Movimentações"];
                delete data["Movimentações"]
                tabledData = jsonToHTML([data]);
                tabledTransactions = jsonToHTML([transactions]);

                response.render('processes/process',{
                    processData: tabledData,
                    transactions: tabledTransactions
                })
        }
        }).catch(error => {
            console.log(error);
          });
    });
}