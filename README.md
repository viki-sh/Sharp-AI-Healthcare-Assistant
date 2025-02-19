# 🔊 Real-time Voice Assistant with OpenAI API  

## 📌 Overview  
This project implements a real-time voice assistant using OpenAI's GPT-4o Realtime API. The assistant listens for user input, processes it, and provides intelligent responses. The system is designed to run continuously and handle interruptions gracefully.  

## 🛠 Features  
- 📡 **WebSocket Communication**: Utilizes WebSocket for real-time interactions.  
- 🎙 **Audio Processing**: Captures and processes user voice input.  
- 🛑 **Signal Handling**: Properly shuts down on `Ctrl+C` to prevent data loss.  
- 📄 **Data Storage**: Saves transcripts in `patient_data.csv` for future reference.  

## 🗂️ Project Structure  
```  
├── AudioIO.py       # Handles audio input/output  
├── Extract.py       # Extracts key information from user input  
├── Realtime.py      # Manages real-time OpenAI API interaction  
├── SaveCSV.py       # Saves data to CSV for record-keeping  
├── Socket.py        # Handles WebSocket connections  
├── main.py          # Entry point for the voice assistant  
├── patient_data.csv # Stores extracted patient information  
└── __pycache__/     # Cached Python files  
```  

## 🚀 Installation  
1. Clone the repository:  
   ```sh
   git clone https://github.com/your-username/your-repo.git  
   cd your-repo  
   ```  
2. Install dependencies:  
   ```sh
   pip install -r requirements.txt  
   ```  
3. Set up your OpenAI API key in the environment:  
   ```sh
   export OPENAI_API_KEY="your-api-key"  
   ```  

## ▶️ Usage  
Run the assistant:  
```sh
python main.py  
```  
Press `Ctrl+C` to gracefully shut down the assistant.  

## ⚙️ How It Works  
- `main.py` initializes the WebSocket connection with OpenAI’s real-time API.  
- `Realtime.py` handles real-time interactions.  
- `AudioIO.py` captures audio input.  
- `Extract.py` processes and extracts key data.  
- `SaveCSV.py` logs conversation data into `patient_data.csv`.  

## 📝 Contributing  
Feel free to fork and improve this project! Submit pull requests if you find issues or want to add features.  

