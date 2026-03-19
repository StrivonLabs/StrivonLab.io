const express = require("express");
const rateLimit = require("express-rate-limit");
const helmet = require("helmet");

const app = express();

app.use(helmet());
app.use(express.json());

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100
});

app.use(limiter);

app.use(express.static("public"));

app.listen(3000, () => console.log("Server running"));