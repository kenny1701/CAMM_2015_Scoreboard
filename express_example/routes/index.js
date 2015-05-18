var express = require('express');
var router = express.Router();
var r = require('rethinkdb');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/camm_2015_scoreboard', function(req, res, next) {
    r.connect({host: "localhost", port: 28015  }, function(err, connection) {
        r.db("mm_2015_scores").table("scoreboard").orderBy(r.desc("completed"), "time_ms", r.desc("cell_count")).run(connection, function(err, cursor) {
        //r.db("mm_2015_scores").table("scoreboard").orderBy(r.desc("completed"), r.desc("cell_count"), "time_ms").run(connection, function(err, cursor) {
        //r.db("mm_2015_scores").table("scoreboard").orderBy(r.desc("completed"), "time_ms", "cell_count").run(connection, function(err, cursor) {
            if (err) {
            }
            else {
                cursor.toArray(function(err, results) {
                  if(err) {
                  } else {
                    res.render('scoreboard', { entries: results, title: 'CAMM 2015 Scoreboard' });
                  }
                  connection.close();
                });
            }
        });
    });
});

module.exports = router;
