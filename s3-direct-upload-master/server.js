// These lines make "require" available
import { createRequire } from "module";
const require = createRequire(
    import.meta.url);
import { generateUploadURL } from './back/s3.js'
const express = require('express')
const path = require('path');
const router = express.Router();

const app = express()

app.use(express.static('front'))

router.get('/home', function(req, res) {
    res.sendFile(path.join(__dirname + '/public/index.html'));
    //__dirname : It will resolve to your project folder.
});

app.get('/s3Url', async(req, res) => {
    const url = await generateUploadURL()
    res.send({ url })
})

app.listen(8080, () => console.log("listening on port 8080"))