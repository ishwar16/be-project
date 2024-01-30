// These lines make "require" available
import { createRequire } from "module";
const require = createRequire(
    import.meta.url);
import { generateUploadURL } from './s3.js'
const http = require('http') // import http module
const express = require('express')
const app = express();
const router = express.Router();

const port = 8000

const server = http.createServer(
    function(req, res) {
        res.write("Hello Ishwar")
        res.end()
    }
); // create server

app.get('/s3Url', async(req, res) => {
    const url = await generateUploadURL()
    res.send({ url })
})

app.use('/', router);

server.listen(port, () => {
    console.log('Server running on port 8000') // listening on the port
})