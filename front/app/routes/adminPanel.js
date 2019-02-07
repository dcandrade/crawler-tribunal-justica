module.exports = function(app){
    app.get("/admin-panel", function(request, response) {
        response.render("panels/admin-panel");
    });
}