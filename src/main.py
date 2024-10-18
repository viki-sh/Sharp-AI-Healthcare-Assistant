"""
This class allows us to interact with OpenAI using websockets to interact in real time
"""
import os
import signal
import time
import logging

from Realtime import Realtime

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


quitFlag = False

def signal_handler(sig, frame, realtime_instance):
    #When the user hits Ctrl+C, this function logs the shutdown request, stops realtime interaction, sets quitflag to true which terminates loop
    logging.info('Received Ctrl+C! Initiating shutdown...')
    realtime_instance.stop()
    global quitFlag
    quitFlag = True

def main():
    api_key = ''
    ws_url = 'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01'

    if not api_key:
        logging.error('OPENAI_API_KEY not found in environment variables!')
        return

    realtime = Realtime(api_key, ws_url)

    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, realtime)) 
    #binds the SIGINT signal to signal_handler dunction, ensuring the process stops when user interrupts it 

    try:
        realtime.start()
        while not quitFlag:
            time.sleep(0.1)
    #while realtime is running, (not quitflag) the main loop will continuously run until ctrl c is hit 
    #main loop keeps program running while websocket connection is active 
    
    except Exception as e:
        logging.error(f'Error in main loop: {e}')
        realtime.stop()

    finally:
        logging.info('Exiting main.')
        realtime.stop()  # Ensures cleanup if any error occurs

if __name__ == '__main__':
    main()
