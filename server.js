const express = require('express');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const fs = require('fs');

const app = express();
app.use(express.json());
app.use(cors());

const privateKey = fs.readFileSync('/Users/helenvaljataga/Documents/GitHub/krediit-union/krediit-union/private_key.pem', 'utf8');

app.post('/generate-token', (req, res) => {
    const { username } = req.body;
    const payload = {
        visitorId: username,
        siteId: '447028fc-8f05-4ca5-92f8-b1c7bb1e292f', // Replace with your actual site ID
        lookup_id: username,
        email: `${username}@mailinator.com`,
        exp: Math.floor(Date.now() / 1000) + (5 * 60) // Token expires in 5 minutes
    };

    const token = jwt.sign(payload, privateKey, { algorithm: 'ES256' });
    res.json({ token });
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));