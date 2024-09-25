const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const fs = require('fs');

const app = express();
const port = 3000;

// CORS configuration
app.use(cors({
  origin: '*', // Allow all origins
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(express.json());

// Read the private key from the specified file
const privateKey = fs.readFileSync('/Users/helenvaljataga/Documents/GitHub/krediit-union/krediit-union/private_key.pem', 'utf8');

app.post('/generate-token', (req, res) => {
  const { username, password } = req.body;

  // Your authentication logic here
  // For this example, let's assume authentication is successful
  const authenticated = true;

  if (authenticated) {
    const claims = {
      'name': username,
      'email': `${username}@mailinator.com`,
      'sub': username,
      'lookup_id': `${username}_id`,
      'exp': Math.floor(Date.now() / 1000) + 60 * 60 * 24 * 5, // 5 days from now
      'iat': Math.floor(Date.now() / 1000)
    };

    const token = jwt.sign(claims, privateKey, { algorithm: 'ES256' });

    res.json({ token });
  } else {
    res.status(401).json({ message: 'Authentication failed' });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});