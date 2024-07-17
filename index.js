var express = require('express');
var app = express();
var path = require('path');
var fs = require('fs')

var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({ extended: false })

app.use(express.static('public'));


// Set EJS as the view engine
app.set('view engine', 'ejs');

//create the tenant-specific webchat page and serve it
app.get('/:cluster?/:tenantName?/:botId?', urlencodedParser, function (req, res) {
            var tenantName = req.params.tenantName;
            var cluster = req.params.cluster;
            var botId = req.params.botId;
            
            var date = new Date();
            var current_date = date.getFullYear()+ "_" + (date.getMonth() + 1) + "_" + date.getDate();
            var current_time = date.getHours() +  "_" + date.getMinutes();
            var date_time = current_date + "_" + current_time;

            excel_filename = cluster + "_tenant" + tenantName + "_botid" + botId + "_excel_" + date_time + ".xlsx";
            response_string = "please check for your phrases file at aiseratenants-" + cluster + "/" + tenantName + "/KBPhrases/botid" + botId + "/results/" + excel_filename;

            args = [cluster, tenantName, botId, date_time]
            runPythonScript(args);

            res.end("running script for "  + tenantName + ", " + cluster + ", " + botId + "...");
 })

function runPythonScript(args) {
    const { exec } = require('child_process');
    console.log(args)
    const pythonScriptPath = path.join(__dirname, 'src', 'phrasegen.py');

    exec (`python3 ${pythonScriptPath} ${args[0]} ${args[1]} ${args[2]} ${args[3]}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing script: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Script stderr: ${stderr}`);
            return;
        }
    
        console.log(`${stdout}`);
        const result = stdout.trim();
        console.log(result);
    });
}
// views directory
app.set('views', path.join(__dirname, 'views'));

var server = app.listen(5000, function () {
   console.log("Express App running at http://127.0.0.1:5000/");
})
