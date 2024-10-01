const express = require('express');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3000; // Use 443 if you're using HTTPS

app.use(cors());
app.use((req, res, next) => {
    console.log('Received request:', req.method, req.url);
    next();
});
app.use(express.static("../"));

app.get("/test", (req, res) => {
    console.log("Test route accessed");
    res.send("This is a response from the test route.");
});

app.listen(port, () => {
    console.log(`Server running at http://sxp4972.uta.cloud`);
});
