const express = require('express');
const cors = require('cors');
const multer = require('multer');
const { analyzeResume } = require('./analyze');

const app = express();
const upload = multer({ storage: multer.memoryStorage() });
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json({ limit: '2mb' }));

app.post('/api/analyze', upload.single('resumeFile'), (req, res) => {
  const jobDescription = req.body.jobDescription || req.body.jobDesc || '';
  let resumeText = req.body.resumeText || '';

  if (req.file) {
    resumeText = req.file.buffer.toString('utf8');
  }

  if (!resumeText.trim()) {
    return res.status(400).json({ error: 'Please provide resume text or upload a plain text file.' });
  }

  const analysis = analyzeResume({ resumeText, jobDescription });
  res.json(analysis);
});

app.listen(PORT, () => {
  console.log(`Resume Analyzer backend running on http://localhost:${PORT}`);
});
