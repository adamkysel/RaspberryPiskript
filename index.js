const express = require('express')
const path = require('path')
const PORT = process.env.PORT || 5000
var Cloudant = require('@cloudant/cloudant');
var cloudant = Cloudant({ username:'a8319e14-276b-4500-9437-6012195a6c59-bluemix', password:'dd55554a1c9962c6c542656de61a2bea205555ac3cac1ca43c1d0991bb377e84', url:'https://a8319e14-276b-4500-9437-6012195a6c59-bluemix:dd55554a1c9962c6c542656de61a2bea205555ac3cac1ca43c1d0991bb377e84@a8319e14-276b-4500-9437-6012195a6c59-bluemix.cloudantnosqldb.appdomain.cloud' });
var db = cloudant.db.use('diplo')
var db_control = cloudant.db.use('diplo1423')

express()
  .use(express.static(path.join(__dirname, 'public')))
  .set('views', path.join(__dirname, 'views'))
  .set('view engine', 'ejs')
  .get('/', (req, res) => {
    res.render('pages/index')})
  .get('/goro', (req, res) => {
    var hums = [];
    var temps = [];
    var soils1 = [];
    var soils2 = [];
    var soils3 = [];
    var soils4 = [];
    var datimes = [];

    db.list(async function (err, body) {
      if (err) {
        console.log(err)
      } else {
        for(i=0;i<10;i++){
          await db.get(body.rows[i].id, async function(err, body) {
            if (!err && body.temperature !== null && body.temperature !== undefined)
            {
              temps.push(body.temperature);
              console.log(temps);
            }

            if (!err && body.humidity !== null && body.humidity !== undefined)
            {
              hums.push(body.humidity);
              console.log(hums);
            }

            if (!err && body.soil1 !== null && body.soil1 !== undefined)
            {
              soils1.push(body.soil1);
              console.log(soils1);
            }

            if (!err && body.soil2 !== null && body.soil2 !== undefined)
            {
              soils2.push(body.soil2);
              console.log(soils2);
            }
            if (!err && body.soil3 !== null && body.soil3 !== undefined)
            {
              soils3.push(body.soil3);
              console.log(soils3);
            }
            if (!err && body.soil4 !== null && body.soil4 !== undefined)
            {
              soils1.push(body.soil4);
              console.log(soils4);
            }
            if (!err && body.datetime !== null && body.datetime !== undefined)
            {
              datimes.push(body.datetime);
              console.log(datimes);
            }
          })
        }     
      }
    })
  
    setTimeout(function(){ res.render('pages/graph',
    { temps:temps, 
      hums:hums,
      datimes:datimes,
      soils1:soils1, 
      soils2:soils2, 
      soils3:soils3, 
      soils4:soils4}); }, 1800);
  })

  .post('/control1', (req, res) => {
    db_control.get('commands',async function(err, body){
      if(body.motor1 ==='open'){
        await db_control.insert({ _id: 'commands',_rev: body._rev, motor1: 'close', motor2:body.motor2, relay:body.relay}, function (err, body) {
          if (err) {
            console.log(err)
          } else {
            console.log(body)
          }
        })
      }
      if(body.motor1 ==='close'){
        await db_control.insert({ _id: 'commands',_rev: body._rev, motor1: 'open', motor2:body.motor2, relay:body.relay}, function (err, body) {
          if (err) {
            console.log(err)
          } else {
            console.log(body)
          }
        })
      }
      res.sendStatus(200)
    })
  })
  .post('/control2', (req, res) => {
    db_control.get('commands',async function(err, body){
      if(body.motor2 ==='open'){
        await db_control.insert({ _id: 'commands',_rev: body._rev, motor1:body.motor1, motor2: 'close', relay:body.relay}, function (err, body) {
          if (err) {
            console.log(err)
          } else {
            console.log(body)
          }
        })
      }
      if(body.motor2 ==='close'){
        await db_control.insert({ _id: 'commands',_rev: body._rev, motor1:body.motor1, motor2: 'open', relay:body.relay}, function (err, body) {
          if (err) {
            console.log(err)
          } else {
            console.log(body)
          }
        })
      }
      res.sendStatus(200)
    })
  })
  .post('/control3', (req, res) => {
    db_control.get('commands',async function(err, body){
      if(body.relay ==='off'){
        await db_control.insert({ _id: 'commands',_rev: body._rev, motor1:body.motor1, motor2:body.motor2, relay: 'on'}, function (err, body) {
          if (err) {
            console.log(err)
          } else {
            console.log(body)
          }
        })
      }
      if(body.relay ==='on'){
        await db_control.insert({ _id: 'commands',_rev: body._rev, motor1:body.motor1, motor2:body.motor2, relay: 'off'}, function (err, body) {
          if (err) {
            console.log(err)
          } else {
            console.log(body)
          }
        })
      }
      res.sendStatus(200)
    })
  })

  .get('/state1', (req, res) => {
    var hums = [];
    var temps = [];
    var motor1 = "";
    var motor2 = "";
    var relay = "";


    db_control.get('commands',async function(err, body){
      motor1 = body.motor1;
      motor2 = body.motor2;
      relay = body.relay;
    })

    console.log(motor1)
    console.log(motor2)
    setTimeout(function(){ res.send({motor1:motor1,motor2:motor2}); }, 2000);})

  .listen(PORT, () => console.log(`Listening on ${ PORT }`))

