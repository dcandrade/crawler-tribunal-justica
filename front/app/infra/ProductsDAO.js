function ProductsDAO(dbConnection){
    this._dbConnection = dbConnection;
}

ProductsDAO.prototype.list = function(callback){
    this._dbConnection.query("SELECT * FROM products", callback);
}

ProductsDAO.prototype.insert = function(product, callback){
    this._dbConnection.query("INSERT INTO products SET ?", product, callback);
}

ProductsDAO.prototype.getBook = function(productId, callback){
    this._dbConnection.query("SELECT * FROM products WHERE id=?", productId, callback);
}

ProductsDAO.prototype.editBook = function(book, callback){
    this._dbConnection.query("UPDATE products SET ? WHERE id=?", [book, book.id], callback);
}

ProductsDAO.prototype.deleteBook = function(id, callback){
    this._dbConnection.query("DELETE FROM products WHERE id=?", id, callback);
}

module.exports = function(){
   return ProductsDAO;
}
