const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'frontend', 'views'));

app.use('/static', express.static(path.join(__dirname, 'frontend', 'public')));

app.use(express.urlencoded({ extended: true}));
app.use(express.json());

app.get('/', (req, res) => {
    res.render('index', { title: 'Stock Brokerage System' });
});

app.get('/test-css', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/public/style.css'));
});



// Investors Page
app.get('/investors', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/api/Investors/');
        res.render('investor', { investors: response.data});
    } catch (error) {
        res.status(500).send('Error fetching investors');
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
    }   catch (error) {
        console.error('Error fetching stocks or bonds:', error);
        res.status(500).send('Error fetching either stocks or bonds');
    }
});

//Form Submissions for creating transactions
app.post('/transactions', async (req, res) => {
    console.log('Transaction request body:', req.body);

    const { investorid, assetType, stockid, bondid, quantity, transactionType} = req.body;

    const transactionData = {
        investorid: investorid,
        quantity: transactionType === 'sell' ? -Math.abs(quantity) : Math.abs(quantity),
        type: transactionType,
    };

    if (assetType === 'stock') {
        transactionData.stockid = stockid;
    }   else if (assetType === 'bond') {
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

//Portfolio for investors
app.get('/investors/:investorId/portfolio', async (req, res) => {
    const investorId = req.params.investorId;
    try {
        const response = await axios.get(`http://localhost:5000/api/Investors/${investorId}/portfolio`);
        res.render('portfolio', { portfolio: response.data, investorId: investorId});
    }   catch (error) {
        console.error('Erro(r fetching portfolio:', error);
        res.status(500).send('Error fetching portfolio');
    }
});


// Bonds Page
app.get('/bonds', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/api/Bonds/');
        res.render('bond', { bonds: response.data});
    } catch (error) {
        res.status(500).send('Error fetching bonds');
    }
});

// Stocks Page
app.get('/stocks', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/api/Stocks/');
        res.render('stock', { stocks: response.data});
    } catch (error) {
        res.status(500).send('Error fetching stocks');
    }
});




// Starting up the server here:
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Frontend server running on http://localhost:${PORT}`);
});