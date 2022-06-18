const express = require('express')
const router = express.Router()
var fs = require('fs');
const exec = require("child_process").execFile;


router.post('/exec', async (req, res) => {
  let data = req.body.data
  fs.writeFileSync(`${__dirname}/../../../cont/SuperCompilerInput.txt`, data)
  exec(`docker run --rm -v ${__dirname}/../../../cont:/backend/cont my_image ./syntaxcompl.sh`, { shell: "/bin/bash" }, (error, stdout, stderr) => {
      if (error) {
        res.status(201).json({
          error: error
        })
        return;
      }
    })
    let fileContent = fs.readFileSync(`${__dirname}/../../../cont/SuperCompilerOut.txt`, "utf8");
    res.json({
      data: fileContent
    })
});


module.exports = router