module.exports = function(app){
    app.get("/flash-sales/form", function(request, response){
        var connection = app.infra.connectionFactory();
        var productsDAL = new app.infra.ProductsDAO(connection);

        productsDAL.list(function(error, result){
            response.render("flash-sales/form", {
                books: result
            });            
        });

        connection.end();
    });

    app.post("/flash-sales", function(request, response) {
        var flashSale = request.body;

        var connection = app.infra.connectionFactory();
        var productsDAL = new app.infra.ProductsDAO(connection);

        productsDAL.getBook(flashSale.book.id, function(error, results){
            app.get('io').emit("newFlashSale", results[0]); //Firing flash sale event through Socket.io
            response.redirect("/flash-sales/form");
        });
        connection.end();
    });
}