const fs = require('fs');
const path = require('path');

// Set the directories where the transcript and audio files are located
const transcriptDir = "/path/to/transcript/directory";
const audioDir = "/path/to/audio/directory";

function findMatchingAudio() {
  // Get a list of all transcript files
  const transcriptFiles = fs.readdirSync(transcriptDir);

  // Select a random transcript file
  const transcriptFile = transcriptFiles[Math.floor(Math.random() * transcriptFiles.length)];

  // Extract the timestamp from the transcript filename (assuming it's in the format "timestamp.txt")
  const timestamp = path.parse(transcriptFile).name;

  // Look for a matching audio file in the audio directory
  const audioFile = path.join(audioDir, `${timestamp}.wav`);

  // Check if the audio file exists
  if (fs.existsSync(audioFile)) {
    console.log(`Found matching audio file: ${audioFile}`);
  } else {
    console.log(`No matching audio file found for transcript: ${transcriptFile}`);
    findMatchingAudio();
  }
}

findMatchingAudio();

// JavaScript code to synchronize the transcript with the audio using linear interpolation
const transcriptElement = document.getElementById('transcript');
const audioElement = document.getElementById('audio');
const text = 'This is a sample transcript.';
const words = text.split(' ');

// Update the transcript as the audio plays
audioElement.addEventListener('timeupdate', () => {
  const percent = audioElement.currentTime / audioElement.duration;
  const index = Math.floor(percent * words.length);
  const highlightedWords = words.slice(0, index);
  const remainingWords = words.slice(index);

  transcriptElement.innerHTML = highlightedWords.join(' ');
  transcriptElement.innerHTML += `<span class="highlight">${remainingWords.join(' ')}</span>`;
});

// Display the transcript
transcriptElement.innerHTML = words.join(' ');
