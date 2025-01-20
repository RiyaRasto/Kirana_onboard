const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const port = 3000; // You can change this to your desired port

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const db = new sqlite3.Database('kirana_store.db', (err) => {
  if (err) {
    console.error('Failed to connect to the database:', err.message);
  } else {
    console.log('Connected to the database.');

    // Create table if it doesn't exist
    db.run(`
      CREATE TABLE IF NOT EXISTS sellers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        store_name TEXT,
        contact_number TEXT,
        address TEXT
      )
    `);
  }
});

// Onboard a new seller
app.post('/onboard', (req, res) => {
  const { name, store_name, contact_number, address } = req.body;

  db.run(
    'INSERT INTO sellers (name, store_name, contact_number, address) VALUES (?, ?, ?, ?)',
    [name, store_name, contact_number, address],
    (err) => {
      if (err) {
        console.error('Error onboarding seller:', err.message);
        res.status(500).json({ message: 'Error onboarding seller' });
      } else {
        res.status(201).json({ message: 'Onboarding successful!' });
      }
    }
  );
});

// Get all sellers
app.get('/sellers', (req, res) => {
  db.all('SELECT * FROM sellers', [], (err, rows) => {
    if (err) {
      console.error('Error fetching sellers:', err.message);
      res.status(500).json({ message: 'Error fetching sellers' });
    } else {
      res.status(200).json(rows);
    }
  });
});

// Update seller information
app.put('/sellers/:id', (req, res) => {
  const { id } = req.params;
  const { name, store_name, contact_number, address } = req.body;

  db.run(
    'UPDATE sellers SET name = ?, store_name = ?, contact_number = ?, address = ? WHERE id = ?',
    [name, store_name, contact_number, address, id],
    (err) => {
      if (err) {
        console.error('Error updating seller:', err.message);
        res.status(500).json({ message: 'Error updating seller' });
      } else {
        res.status(200).json({ message: 'Seller updated successfully!' });
      }
    }
  );
});

// Delete a seller
app.delete('/sellers/:id', (req, res) => {
  const { id } = req.params;

  db.run(DELETE FROM sellers WHERE id = ?, [id], (err) => {
    if (err) {
      console.error('Error deleting seller:', err.message);
      res.status(500).json({ message: 'Error deleting seller' });
    } else {
      res.status(200).json({ message: 'Seller deleted successfully!' });
    }
  });
});

app.listen(port, () => {
  console.log(Server listening on port ${port});
});

// Gracefully close database on server shutdown
process.on('exit', () => {
  db.close((err) => {
    if (err) {
      console.error('Error closing the database:', err.message);
    } else {
      console.log('Database connection closed.');
    }
  });
});
