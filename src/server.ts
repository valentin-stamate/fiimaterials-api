import express = require("express");

const app = express();
const port = 8080;
const host = `http://localhost:${port}`

app.get('/', (req, res) => {
    res.end('Hello word!')
});

app.listen(port, () => {
    console.log(`Server started at ${host}`);
});