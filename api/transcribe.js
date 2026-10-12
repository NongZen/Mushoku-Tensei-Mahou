// Vercel Serverless Function: /api/transcribe
// Supports Groq Whisper-large-v3, OpenAI Whisper, and Gemini Audio

export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Authorization, x-api-key, x-engine'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const customKey = req.headers['x-api-key'];
    const targetSpell = req.headers['x-target-spell'] || '';
    const groqKey = customKey || process.env.GROQ_API_KEY;
    const openaiKey = customKey || process.env.OPENAI_API_KEY;

    // Receive audio buffer from body
    // Using binary or base64 body
    let audioBuffer;
    if (Buffer.isBuffer(req.body)) {
      audioBuffer = req.body;
    } else if (typeof req.body === 'string') {
      audioBuffer = Buffer.from(req.body, 'base64');
    } else if (req.body && req.body.audio) {
      audioBuffer = Buffer.from(req.body.audio, 'base64');
    } else {
      return res.status(400).json({ error: 'No audio data received' });
    }

    // Call Groq Whisper if groqKey is available
    if (groqKey) {
      const formData = new FormData();
      const audioBlob = new Blob([audioBuffer], { type: 'audio/webm' });
      formData.append('file', audioBlob, 'chant.webm');
      formData.append('model', 'whisper-large-v3');
      formData.append('language', 'ja');
      formData.append('prompt', '無職転生 呪文詠唱 ' + targetSpell);

      const groqResp = await fetch('https://api.groq.com/openai/v1/audio/transcriptions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${groqKey}`
        },
        body: formData
      });

      if (!groqResp.ok) {
        const errText = await groqResp.text();
        return res.status(groqResp.status).json({ error: 'Groq API error', details: errText });
      }

      const groqData = await groqResp.json();
      return res.status(200).json({
        engine: 'groq-whisper-v3',
        text: groqData.text || ''
      });
    }

    // Fallback to OpenAI Whisper if openaiKey
    if (openaiKey) {
      const formData = new FormData();
      const audioBlob = new Blob([audioBuffer], { type: 'audio/webm' });
      formData.append('file', audioBlob, 'chant.webm');
      formData.append('model', 'whisper-1');
      formData.append('language', 'ja');
      formData.append('prompt', '無職転生 呪文詠唱 ' + targetSpell);

      const oaiResp = await fetch('https://api.openai.com/v1/audio/transcriptions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${openaiKey}`
        },
        body: formData
      });

      if (!oaiResp.ok) {
        const errText = await oaiResp.text();
        return res.status(oaiResp.status).json({ error: 'OpenAI API error', details: errText });
      }

      const oaiData = await oaiResp.json();
      return res.status(200).json({
        engine: 'openai-whisper',
        text: oaiData.text || ''
      });
    }

    return res.status(400).json({
      error: 'No Whisper API key configured. Provide GROQ_API_KEY or OPENAI_API_KEY in Vercel settings or in user settings modal.'
    });

  } catch (error) {
    return res.status(500).json({ error: error.message || 'Internal server error' });
  }
}
