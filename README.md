# 🔊 Real-time Voice Assistant with OpenAI API  

## 📌 Overview  
This project implements a real-time voice assistant using OpenAI's GPT-4o Realtime API. The assistant listens for user input, processes it, and provides intelligent responses. The system is designed to run continuously and handle interruptions gracefully.  

## 🛠 Features  
- 📡 **WebSocket Communication**: Utilizes WebSocket for real-time interactions.  
- 🎙 **Audio Processing**: Captures and processes user voice input.  
- 🛑 **Signal Handling**: Properly shuts down on `Ctrl+C` to prevent data loss.  
- 📄 **Data Storage**: Saves transcripts in `patient_data.csv` for future reference.  

## 📂 Project Structure  

├── AudioIO.py # Handles audio input/output
├── Extract.py # Extracts key information from user input
├── Realtime.py # Manages real-time OpenAI API interaction
├── SaveCSV.py # Saves data to CSV for record-keeping
├── Socket.py # Handles WebSocket connections
├── main.py # Entry point for the voice assistant
├── patient_data.csv # Stores extracted patient information
└── pycache/ # Cached Python files


