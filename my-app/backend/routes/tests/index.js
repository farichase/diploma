const express = require('express')
const router = express.Router()
var fs = require('fs');


router.post('/load', async (req, res) => {
  let fileContent = fs.readFileSync(`${__dirname}/${req.body.file}`, "utf8");
  res.json({
    data: fileContent
  })
});

module.exports = router