const express = require('express');
const axios = require('axios');
const path = require('path');
const methodOverride = require('method-override');

const app = express();

// Set the view engine to EJS and set the views directory correctly
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views')); // Adjusted to match your current folder structure

// Serve static files from the public directory
app.use('/static', express.static(path.join(__dirname, 'public'))); // Updated path

// Middleware for parsing request bodies and overriding HTTP methods
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(methodOverride('_method'));

// Home page route
app.get('/', (req, res) => {
    res.render('index', { title: 'Stock Brokerage System' });
});

// Investors page - Display list of investors
app.get('/investors', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/api/Investors/');
        res.render('investor', { investors: response.data });
    } catch (error) {
        res.status(500).send('Error fetching investors');
    }
});

// Add Investor Page - Render the form for adding a new investor
app.get('/investors/add', (req, res) => {
    res.render('add_investor');
});

// Form submission to add a new investor
app.post('/investors', async (req, res) => {
    const { firstname, lastname } = req.body;

    if (!firstname || !lastname) {
        return res.status(400).send('First name and last name are required');
    }

    try {
        await axios.post('http://localhost:5000/api/Investors/', {
            firstname: firstname,
            lastname: lastname
        });
        res.redirect('/investors');
    } catch (error) {
        console.error('Error adding investor:', error);
        res.status(500).send('Error adding investor');
    }
});

// Route to delete an investor
app.delete('/investors/:id', async (req, res) => {
    const investorId = req.params.id;

    try {
        await axios.delete(`http://localhost:5000/api/Investors/${investorId}`);
        res.redirect('/investors');
    } catch (error) {
        console.error('Error deleting investor:', error);
        res.status(500).send('Error deleting investor');
    }
});

// Bonds page - Display list of bonds
app.get('/bonds', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/api/Bonds/');
        res.render('bond', { bonds: response.data });
    } catch (error) {
        res.status(500).send('Error fetching bonds');
    }
});

// Add Bond Page - Render the form for adding a new bond
app.get('/bonds/add', (req, res) => {
    res.render('add_bond');
});

// Form submission to add a new bond
app.post('/bonds', async (req, res) => {
    const { bondname, abbreviation, currentprice } = req.body;

    if (!bondname || !abbreviation || !currentprice) {
        return res.status(400).send('All fields are required');
    }

    try {
        await axios.post('http://localhost:5000/api/Bonds/', {
            bondname: bondname,
            abbreviation: abbreviation,
            currentprice: currentprice
        });
        res.redirect('/bonds');
    } catch (error) {
        console.error('Error adding bond:', error);
        res.status(500).send('Error adding bond');
    }
});

// Route to delete a bond
app.delete('/bonds/:id', async (req, res) => {
    const bondId = req.params.id;

    try {
        await axios.delete(`http://localhost:5000/api/Bonds/${bondId}`);
        res.redirect('/bonds');
    } catch (error) {
        console.error('Error deleting bond:', error);
        res.status(500).send('Error deleting bond');
    }
});

// Stocks page - Display list of stocks
app.get('/stocks', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/api/Stocks/');
        res.render('stock', { stocks: response.data });
    } catch (error) {
        res.status(500).send('Error fetching stocks');
    }
});

// Add Stock Page - Render the form for adding a new stock
app.get('/stocks/add', (req, res) => {
    res.render('add_stock');
});

// Form submission to add a new stock
app.post('/stocks', async (req, res) => {
    const { stockname, abbreviation, currentprice } = req.body;

    if (!stockname || !abbreviation || !currentprice) {
        return res.status(400).send('All fields are required');
    }

    try {
        await axios.post('http://localhost:5000/api/Stocks/', {
            stockname: stockname,
            abbreviation: abbreviation,
            currentprice: currentprice
        });
        res.redirect('/stocks');
    } catch (error) {
        console.error('Error adding stock:', error);
        res.status(500).send('Error adding stock');
    }
});

// Route to delete a stock
app.delete('/stocks/:id', async (req, res) => {
    const stockId = req.params.id;

    try {
        await axios.delete(`http://localhost:5000/api/Stocks/${stockId}`);
        res.redirect('/stocks');
    } catch (error) {
        console.error('Error deleting stock:', error);
        res.status(500).send('Error deleting stock');
    }
});

// Starting up the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Frontend server running on http://localhost:${PORT}`);
});





// Backend directory: CIS\2368\Project\2368-Project\backend

// Frontend Directory: CIS\2368Project\2368-Project       node frontend/app.js