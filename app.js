const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 4001;

// Define the API endpoint to trigger the execution of the Python script
app.get('/fetch-resume', (req, res) => {
  const pythonScript = 'test.py';

  // Execute the Python script "test.py" in macbook; you might need to adjust this command
  exec(`python3 ${pythonScript}`, (error, stdout, stderr) => {
    if (error || stderr) {
      console.error('Error during script execution:', error || stderr);
      return res.status(500).send('Error during script execution.');
    }

    const scriptOutput = stdout;
    const resume_score = parseFloat(scriptOutput);

    if (!isNaN(resume_score)) {
      // Return the resume score as a JSON response
      return res.status(200).json({ resume_score });
    } else {
      return res.status(500).send('Invalid resume score value.');
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});












