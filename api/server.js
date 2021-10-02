var express = require("express");
var app = express();
var db = require("./database.js")

var HTTP_PORT = 8000

var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.listen(HTTP_PORT, () => {
	console.log("server running on port %PORT%".replace("%PORT",HTTP_PORT))
});

app.get("/", (req,res,next) => {
	res.json({"message":"Ok"})
});

app.get("/api/users", (req, res, next) => {
    var sql = "select * from user"
    var params = []
    db.all(sql, params, (err, rows) => {
        if (err) {
          res.status(400).json({"error":err.message});
          return;
        }
        res.json({
            "message":"success",
            "data":rows
        })
      });
});

app.get("/api/mostoutdatepage/:id", (req, res, next) => {
    //var sql="select A.page_id, A.page_title, A.page_namespace, A.page_touched, A.revision_id, cat_title, A.link, B.page_id, B.page_namespace, B.page_touched, B.page_touched - A.page_touched as update_interval from (page inner join pagel on pagel.page_id=page.page_id inner join category on category.cat_pages=page.page_id) as A inner join page as B on A.link=B.page_title where cat_title=? order by update_interval desc limit 10;"    
    var sql="select A.page_title, cat_title, A.link, B.page_touched, B.page_touched - A.page_touched as update_interval from (page inner join pagel on pagel.page_id=page.page_id inner join category on category.cat_pages=page.page_id) as A inner join page as B on A.link=B.page_title where cat_title=? AND update_interval >0 order by update_interval desc limit 1;"    
    var params = [req.params.id]
    db.get(sql, params, (err, rows) => {
        if (err) {
          res.status(400).json({"error":err.message});
          return;
        }
        res.json({
            "message":"success",
            "data":rows
        })
    });
	
});

app.post("/api/runsql", (req, res, next) => {
	var errors = []
	var data = {
		sql: req.body.sql
	}
	var params  =[]
	if ( data.sql.split(" ")[0].toUpperCase() == "SELECT" ){
		db.all(data.sql, params, (err,rows) => {
			if (err) {
				res.status(400).json({"error": err.message})
				return;
			}
			res.json({
				"message": "success",
				"data": data,
				"result": rows,
				"id" : this.lastID
			})
		});
	}else{
		db.run(data.sql, params, function(err, result) {
			if (err){
				res.status(400).json({"error": err.message})
				return;
			}
			res.json({
				"message": "success",
				"data": data,
				"id" : this.lastID
			})
		});
	}
});

app.use(function(req,res){
	res.status(404);
});
