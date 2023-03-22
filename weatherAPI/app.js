const express = require('express')
const https = require("https")
const bodyParser = require("body-parser");
const { urlencoded } = require('body-parser');


const app = express();
app.use(bodyParser.urlencoded({extended: true}))

app.get("/", (req, res)=>{
    res.sendFile(__dirname+"/index.html")
})

    


app.post("/", (req, res)=>{
    const key = "d1e4a7842ac22680f8deda47bf5bb24b"
    const cityName = req.body.cityName
    const url ="https://api.openweathermap.org/data/2.5/weather?q="+cityName+"&appid="+key
    console.log("post request recieved")
    https.get(url, (response)=>{
        console.log(response.statusCode)
        response.on("data", (data)=>{
            const weatherData = JSON.parse(data)
            console.log(weatherData);
            const temp  = Math.round(Number(weatherData.main.temp)-273) 
            const desc = weatherData.weather[0].description
            const icon = weatherData.weather[0].icon
            const imageUrl = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
            res.write("<h1>" + cityName + " temperature is " + temp + "</h1>")
            res.write("<p> Weather is currently " + desc + "</p> <img src="+imageUrl+">" )
            res.send()
    })
    })
    }
)

app.listen(3000, ()=>{
    console.log("server is running on 3000")
})
