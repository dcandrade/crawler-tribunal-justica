var express = require('../config/express')();
var request = require('supertest')(express);
var DatabaseCleaner = require('database-cleaner');

var databaseCleaner = new DatabaseCleaner('mysql');

var cleanDB = function(callback){
    var connection = express.infra.connectionFactory();
    databaseCleaner.clean(connection, function(){
        connection.end();
        callback();
    });
}

describe('#Products Controller', function(){
    beforeEach(function(done){
        cleanDB(done);
    });

    it('#JSON Listing', function(done){
        request.get('/products')
        .set('Accept', 'application/json')
        .expect('Content-Type', /json/)
        .expect(200, done);
    });

    it('#Insert invalid products', function(done){
        var invalidProduct = {
            title: '',
            description: '',
            price: ''
        }

        request.post('/products')
        .send(invalidProduct)
        .expect(400, done);
    });

    it('#Insert valid product', function(done){
        var validProduct = {
            title: 'NodeJS for Beginners',
            description: 'Start your career in NodeJS',
            price: '39.90'
        }

        request.post('/products')
        .send(validProduct)
        .expect(302, done);
    })
});