const express = require('express')
const router = express.Router()
var fs = require('fs');
const exec = require("child_process").execFile;


router.post('/upload', async (req, res) => {
  fs.writeFileSync(`${__dirname}/../../../cont/r_text.ref`, "")
  fs.writeFileSync(`${__dirname}/../../../cont/rsd_text.ref`, "")
  fs.writeFileSync(`${__dirname}/../../../cont/log_ref.dot`, "")

  let content = req.body.content

  fs.writeFileSync(`${__dirname}/../../../cont/text.ref`, content)
  res.json({
    msg: "File uploaded"
  })
});

router.post('/graph', async (req, res) => {
  exec(`docker run --rm -v ${__dirname}/../../../cont:/backend/cont my_image ./graphs.sh`, { shell: "/bin/bash" }, (error, stdout, stderr) => {
         
    if (error) {
      res.json({
        data: "It is impossible to build a graph"
      })
      return;
    }
    if (stderr) {
      res.json({
        data: "It is impossible to build a graph"
      })
      return;
    }
    res.json({
      data: "stdout"
    })
    return;
  })
});

router.post('/loadgraph', async (req, res) => {
  // console.log(`${__dirname}/../../../graphsload.sh`)
  exec(`${__dirname}/graphsload.sh`, { shell: "/bin/bash" }, (error, stdout, stderr) => {
    if (error) {
      res.json({
        data: "It is impossible to build a graph"
      })
      return;
    }
    if (stderr) {
      res.json({
        data: "It is impossible to build a graph"
      })
      return;
    }
    res.json({
      data: "stdout"
    })
    return;
  })
});

router.post('/transform', async (req, res) => {
  let compilerVersion = req.body.compilerVersion
  let fileFormat = req.body.fileFormat

  fs.writeFileSync(`${__dirname}/../../../cont/r_text.ref`, "")
  fs.writeFileSync(`${__dirname}/../../../cont/rsd_text.ref`, "")
  fs.writeFileSync(`${__dirname}/../../../cont/log_ref.dot`, "")

  if (compilerVersion === 'SCP4' && fileFormat === 'ref') {

    exec(`docker run --rm -v ${__dirname}/../../../cont:/backend/cont my_image ./compile.sh`, { shell: "/bin/bash" }, (error, stdout, stderr) => {
      if (error) {
        res.json({
          data: "Compilation failed"
        })
        return;
      }
      if (stderr) {
        console.log(`stderr: ${stderr}`);
        res.json({
          data: "Compilation failed"
        })
        return;
      }
      console.log(`stdout: ${stdout}`);
      let fileContent = fs.readFileSync(`${__dirname}/../../../cont/r_text.ref`, "utf8");
      res.json({
        data: fileContent
      })
    })

  } else if (compilerVersion === 'MSCP-A' && fileFormat === 'ref') {
    console.log(`docker run --rm -v ${__dirname}/../../../cont:/backend/cont my_image ./mscp.sh`)
    exec(`docker run --rm -v ${__dirname}/../../../cont:/backend/cont my_image ./mscp.sh`, { shell: "/bin/bash", timeout: 2000 }, (error, stdout, stderr) => {
      if (error) {
        res.json({
          data: error
        })
        return;
      }
      if (stderr) {
        console.log(`stderr: ${stderr}`);
        res.json({
          data: stderr
        })
        return;
      }

      console.log(`stdout: ${stdout}`);
      let fileContent = fs.readFileSync(`${__dirname}/../../../cont/rsd_text.ref`, "utf8");
      console.log(fileContent)
      res.json({
        data: fileContent
      })
    })

  } else if (compilerVersion === 'MSCP-A' && fileFormat === 'dot') {
      exec(`docker run --rm -v ${__dirname}/../../../cont:/backend/cont my_image ./mscp.sh`, { shell: "/bin/bash" }, (error, stdout, stderr) => {
       
        if (error) {
          res.json({
            data: "It is impossible to build a graph"
          })
          return;
        }
        if (stderr) {
          res.json({
            data: "It is impossible to build a graph"
          })
          return;
        }
        res.json({
          data: "stdout"
        })
        return;
      })

  }
});



module.exports = router