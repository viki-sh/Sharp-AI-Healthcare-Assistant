import base64
import logging
import threading
import openai
from Socket import Socket
from AudioIO import AudioIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class Realtime:
    def __init__(self, api_key, ws_url):
        self.socket = Socket(api_key, ws_url, on_msg=self.handle_message)
        self.audio_io = AudioIO(on_audio_callback=self.send_audio_to_socket)
        self.audio_thread = None  # Store thread references
        self.recv_thread = None
    
    #viki added 
    def get_medical_assistant_response(self, user_input):
        system_prompt = (
            "You are a helpful and professional medical assistant. "
            "You assist users by booking medical appointments, checking prescriptions, and gathering important patient information, "
            "including their name, age, symptoms, and medical history. Please ensure your responses are clear, respectful, "
            "and help guide the user to provide necessary information."
        )

        response = openai.chat_completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content']
    def extract_medical_info_from_gpt_response(self, response):
        """
        Extract structured medical data (e.g., Name, Age, Symptoms) from GPT's response.
        """
        structured_prompt = (
            f"Extract and return in a structured format the following information from the patient's message: "
            f"Name, Age, Symptoms, and any relevant medical history. Here is the patient's message: {response}"
        )
        
        extracted_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": structured_prompt}
            ]
        )
        return extracted_response.choices[0].message['content']
    
    def start(self):
        """ Start WebSocket and audio processing. """
        self.socket.connect()

        # Send initial request to start the conversation
        self.socket.send({
            'type': 'response.create',
            'response': {
                'modalities': ['audio', 'text'],
                'instructions': 'Please assist the user.'
            }
        })

        # Start processing microphone audio
        self.audio_thread = threading.Thread(target=self.audio_io.process_mic_audio)
        self.audio_thread.start()

        # Start audio streams (mic and speaker)
        self.audio_io.start_streams()

    #viki added 
    def send_audio_to_socket(self, mic_chunk):

        """ Callback function to send audio data to the socket and get the medical assistant's response. """
        logging.info(f'🎤 Sending {len(mic_chunk)} bytes of audio data to socket.')

        # Convert the audio chunk into text
        user_input_text = self.audio_io.convert_audio_to_text(mic_chunk)  # Assuming you have this conversion already
        
        # Get the GPT medical assistant's response
        gpt_response = self.get_medical_assistant_response(user_input_text)
        
        # You can also send the response via WebSocket if needed
        encoded_chunk = base64.b64encode(gpt_response.encode('utf-8')).decode('utf-8')
        self.socket.send({'type': 'input_audio_buffer.append', 'audio': encoded_chunk})

        logging.info(f'🎤 Processed and sent medical assistant response: {gpt_response}')

    def handle_message(self, message):
        """ Handle incoming WebSocket messages. """
        event_type = message.get('type')
        logging.info(f'Received message type: {event_type}')

        if event_type == 'response.audio.delta':
            audio_content = base64.b64decode(message['delta'])
            self.audio_io.receive_audio(audio_content)
            logging.info(f'Received {len(audio_content)} bytes of audio data.')

        elif event_type == 'response.audio.done':
            logging.info('AI finished speaking.')

            # Extract medical info from the GPT response
            gpt_response = message['response']
            extracted_info = self.extract_medical_info_from_gpt_response(gpt_response)
            
            # Example: assuming extracted_info is like: {"name": "John", "age": 30, "symptoms": "headache"}
            self.save_patient_info_to_csv(extracted_info['name'], extracted_info['age'], extracted_info['symptoms'], "No medical history")

    def stop(self):
        """ Stop all processes cleanly. """
        logging.info('Shutting down Realtime session.')

        # Signal threads to stop
        self.audio_io._stop_event.set()
        self.socket.kill()

        # Stop audio streams
        self.audio_io.stop_streams()

        # Join threads to ensure they exit cleanly
        if self.audio_thread:
            self.audio_thread.join()
            logging.info('Audio processing thread terminated.')