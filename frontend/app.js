const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));


app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.render('index', { title: 'Stock Brokerage System' });
});


// Investors Page
app.get('/investors', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/api/Investors/');
        res.render('investor', { investors: response.data});
    } catch (error) {
        read.status(500).send('Error fetching investors');
    }
});

// Bonds Page
app.get('/bonds', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/api/Bonds/');
        res.render('bond', { bonds: response.data});
    } catch (error) {
        read.status(500).send('Error fetching bonds');
    }
});

// Stocks Page
app.get('/stocks', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/api/Stocks/');
        res.render('stock', { stocks: response.data});
    } catch (error) {
        read.status(500).send('Error fetching stocks');
    }
});



// Starting up the server here:
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Frontend server running on http://localhost:${PORT}`);
});