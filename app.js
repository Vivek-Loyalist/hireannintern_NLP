const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 4001;
const { MongoClient } = require('mongodb');

// MongoDB connection URL and database name
const mongoURL = 'mongodb+srv://amala:amala@Cluster0.eqtpl0g.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp'

const dbName = 'Hire_an_Intern_test'; // Use your database name

// Create a MongoDB client and connect to the database
const client = new MongoClient(mongoURL, { useUnifiedTopology: true });

client.connect()
  .then(() => {
    console.log('Connected to MongoDB');
  })
  .catch(err => {
    console.error('Error connecting to MongoDB:', err);
  });

// Define a MongoDB collection schema and model
const collectionName = 'apply_job';
const wordSimilaritySchema = {
  resume_score: Number, // Change the field name to "resume_score"
};
const WordSimilarityModel = client.db(dbName).collection(collectionName);

// API endpoint to trigger the execution of the Python script and save the output to MongoDB
app.get('/fetch-resume', (req, res) => {
  const pythonScript = 'test.py';


  // Execute the Python script "test.py" in macbook python3 command works in other rmove python3 to python

  exec(`python3 ${pythonScript}`, (error, stdout, stderr) => {
    if (error || stderr) {
      console.error('Error during script execution:', error || stderr);
      return res.status(500).send('Error during script execution.');
    }

    const scriptOutput = stdout;
    const resume_score = parseFloat(scriptOutput); // Updated field name

    if (!isNaN(resume_score)) {
      // Save the resume score value to MongoDB with the updated field name
      WordSimilarityModel.insertOne({
        resume_score, // Use the updated field name
      })
        .then(() => {
          console.log('Resume score saved to MongoDB');
        })
        .catch(err => {
          console.error('Error saving to MongoDB:', err);
        });

      return res.status(200).json({ resume_score }); // Updated field name
    } else {
      return res.status(500).send('Invalid resume score value.'); // Updated field name
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
