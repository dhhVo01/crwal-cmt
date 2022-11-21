import express from "express";
import { spawn } from "child_process";
import bodyParser from "body-parser";
const app = express();
const PORT = process.env.PORT || 3001;

app.use(bodyParser.urlencoded({ extended: false }));


app.post("/api/crawl",function(req, res){
    const url = req.body.url;
    var process = spawn("python", ["tool.py", url]);
    process.stdout.on("data", function(data){
        console.log(data.toString());
        res.send();
    })
    process.stderr.on('data', (data) => {
        res.write(data.toString());
        console.log(data.toString());
        res.send();
    }); 
})


app.listen(PORT, function(){
    console.log(`Server is running on port ${PORT}.`);
});