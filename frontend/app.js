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

// Investors page
app.get('/investors', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/api/Investors/');
        res.render('investor', { investors: response.data });
    } catch (error) {
        res.status(500).send('Error fetching investors');
    }
});

// Route to render the form to add a new investor
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

// Route to handle deleting an investor
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

// Rendering transaction form for the investor
app.get('/transactions/:investorId', async (req, res) => {
    const investorId = req.params.investorId;
    try {
        const stocksResponse = await axios.get('http://localhost:5000/api/Stocks/');
        const bondsResponse = await axios.get('http://localhost:5000/api/Bonds/');

        res.render('transaction', {
            investorId: investorId,
            stocks: stocksResponse.data,
            bonds: bondsResponse.data,
        });
    } catch (error) {
        console.error('Error fetching stocks or bonds:', error);
        res.status(500).send('Error fetching either stocks or bonds');
    }
});

// Form submission for creating transactions
app.post('/transactions', async (req, res) => {
    console.log('Transaction request body:', req.body);

    const { investorid, assetType, stockid, bondid, quantity, transactionType } = req.body;

    const transactionData = {
        investorid: investorid,
        quantity: transactionType === 'sell' ? -Math.abs(quantity) : Math.abs(quantity),
        type: transactionType,
    };

    if (assetType === 'stock') {
        transactionData.stockid = stockid;
    } else if (assetType === 'bond') {
        transactionData.bondid = bondid;
    }

    try {
        const response = await axios.post('http://localhost:5000/api/Transactions/', transactionData);
        console.log('Transaction successful:', response.data);
        res.redirect(`/investors/${investorid}/portfolio`);
    } catch (error) {
        console.error('Error creating transaction:', error);
        res.status(500).send('Error creating transaction');
    }
});

// Portfolio for investors
app.get('/investors/:investorId/portfolio', async (req, res) => {
    const investorId = req.params.investorId;
    try {
        const response = await axios.get(`http://localhost:5000/api/Investors/${investorId}/portfolio`);
        res.render('portfolio', { portfolio: response.data, investorId: investorId });
    } catch (error) {
        console.error('Error fetching portfolio:', error);
        res.status(500).send('Error fetching portfolio');
    }
});

// Bonds page
app.get('/bonds', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/api/Bonds/');
        res.render('bond', { bonds: response.data });
    } catch (error) {
        res.status(500).send('Error fetching bonds');
    }
});

// Stocks page
app.get('/stocks', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/api/Stocks/');
        res.render('stock', { stocks: response.data });
    } catch (error) {
        res.status(500).send('Error fetching stocks');
    }
});

// Starting up the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Frontend server running on http://localhost:${PORT}`);
});





// Backend directory: CIS\2368\Project\2368-Project\backend

// Frontend Directory: CIS\2368Project\2368-Project       node frontend/app.js