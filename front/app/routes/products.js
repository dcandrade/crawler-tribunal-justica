module.exports = function(app){
    var listProducts = function(request, response, next){
        var connection = app.infra.connectionFactory();
        var productsDAL = new app.infra.ProductsDAO(connection);

        productsDAL.list(function(error, result){
            if(error){
                return next(error);
            }

            response.format({
                html: function(){
                    response.render("products/list", {
                        books: result
                    });
                },
                json: function(){
                    response.json(result);
                }
            });
        
        });

        connection.end();
    };

    app.get("/products", listProducts);

    app.get("/products/form", function(request, response){
        response.render("products/form",{
            validationErrors:{},
            product:{}
        });
    });

    app.post("/products", function(request, response){
        var product = request.body;

        request.assert('title', 'Title cannot be blank').notEmpty();
        request.assert('price', 'Invalid price format').isFloat();

        var validationErrors = request.validationErrors();
        if(validationErrors){
            response.status(400);

            responseContent =  {
                validationErrors: validationErrors,
                product: product
            };
            response.format({
                html: function(){
                    response.render('products/form', responseContent);
                },
                json: function(){
                    response.json(responseContent);
                }
            });
          
            return;
        }

        var connection = app.infra.connectionFactory();
        var productsDAO = new app.infra.ProductsDAO(connection);
        
        productsDAO.insert(product, function(error, result){
            response.redirect("/products");
        });

        connection.end();
    });

    app.get("/products/detail", function(request, response){
        var id = request.query.id;
        var connection = app.infra.connectionFactory();
        var productsDAL = new app.infra.ProductsDAO(connection);

        productsDAL.getBook(id, function(error, result){
            var book = result[0];
            response.format({
                html: function(){
                    response.render("products/detail", {
                        product: book
                    });
                },
                json: function(){
                    response.json(book);
                }
            });
       
        })

        connection.end();
    });

    app.post("/products/detail", function(request, response){
        var book = request.body;
        var connection = app.infra.connectionFactory();
        var productsDAL = new app.infra.ProductsDAO(connection);

        productsDAL.editBook(book, function(error, result){
            response.format({
                html: function(){
                    response.redirect("/products");                    
                },
                json: function(){
                    response.status(200).json(book);
                }
            });
        });

        connection.end();
    });

    app.post("/products/delete", function(request, response){
        var id = request.body.id;
        var connection = app.infra.connectionFactory();
        var productsDAL = new app.infra.ProductsDAO(connection);

        productsDAL.deleteBook(id, function(error, result){
            response.format({
                html: function(){
                    response.redirect("/products");
                },
                json: function(){
                    response.status(200).json(id);
                }
            });
        });

        connection.end();
    });
}
