const axios = require('axios');
const { jsonToHTML } = require('nested-json-to-table')


module.exports = function(app){
    app.get("/process", function(request, response){
        var court = request.query['court'];
        var number = request.query['number'];
    
        var options = {
            host: "localhost",
            port: 8888,
            path: '/get?process_number='+number,
            method: 'GET'
        };

        var url = 'http://localhost:8888/get?court='+court+'&process_number='+number;


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

                var tabledData = null;
                var tabledTransactions = null;
                try {
                    tabledData = jsonToHTML([data]);
                     tabledTransactions = jsonToHTML([transactions]);
                } catch (TypeError) {
                    tabledData = "<table>"+JSON.stringify(data)+"</table>";
                    tabledTransactions = "<table>"+JSON.stringify(transactions)+"</table>"  ;
                }
               
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