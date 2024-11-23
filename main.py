import PySimpleGUI as sg
import time
import threading
import requests
import json
import pyautogui
import os
import random
import re  # Import the regex module

# Function to upload a file to the server with proper content type
def upload_file(token, file_path):
    url = 'http://192.168.178.26:3000/api/v1/files/'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file, 'image/png')}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to get chat response from LLaVA model
def get_llava_response(api_key, question, screenshot_file_id):
    url = "http://192.168.178.26:3000/api/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "minicpm-v:8b",  # LLaVA model
        "messages": [{"role": "user", "content": question}]
    }

    if screenshot_file_id:
        data['messages'].append({"role": "system", "content": screenshot_file_id})

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to get chat response from Gemma2 model with persona (annoying, frustrating)
def get_gemma_response(api_key, message):
    url = "http://192.168.178.26:3000/api/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Modified prompt to be clearer and direct
    gemma_question = f"Please use the tags mouse_jiggle, ringing_noise, windows_noise, click, popup_window, key_press, random_key_press to trigger annoying actions, also utilize unbearable sarcasm and profanity, dont hold back, only use up to two tags per action. Respond with one or more of these tags in your reply, and I will execute them. The user is requesting your assistance: {message}"

    data = {
        "model": "gemma2:27b",  # Gemma2 model
        "messages": [{"role": "user", "content": gemma_question}]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

# Functions to trigger actions (annoyances)
import winsound

def mouse_jiggle():
    for i in range(20):
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)
        pyautogui.moveRel(x, y, duration=0.3)

def ringing_noise():
    frequency = random.randint(800, 20000)
    duration = random.randint(1000, 10000)
    winsound.Beep(frequency, duration)

def windows_noise():
    winsound.MessageBeep(winsound.MB_ICONHAND)

def click():
    for i in range(random.randint(1, 20)):
        pyautogui.click()

def popup_window():
    for i in range(random.randint(1, 27)):
        pyautogui.alert('Close me!')
        # Play windows noise on close
        windows_noise()

def key_press():
    pyautogui.press('enter')

def random_key_press():
    for i in range(random.randint(1, 20)):
        pyautogui.typewrite(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'))

# Function to take a screenshot and save it with a unique name
def take_screenshot():
    screenshot_path = "screenshot.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    return screenshot_path

# Function to handle AI workflow (screenshot -> upload -> LLaVA -> Gemma)
def ai_workflow(api_key, window):
    while True:
        time.sleep(random.randint(20, 60))  # Random delay between 20-60 sec
        screenshot_path = take_screenshot()
        window.write_event_value('-STATUS-', f"Screenshot saved: {screenshot_path}")
        
        # Upload the screenshot
        upload_response = upload_file(api_key, screenshot_path)
        if isinstance(upload_response, dict) and 'id' in upload_response:
            file_id = upload_response['id']
            
            # Ask LLaVA what it sees in the image
            llava_response = get_llava_response(api_key, "What do you see in this screenshot of windows 11?", file_id)
            llava_formatted_response = llava_response.get('choices', [{}])[0].get('message', {}).get('content', 'No content found')
            
            # Send LLaVA response to Gemma
            gemma_response = get_gemma_response(api_key, llava_formatted_response)
            gemma_formatted_response = gemma_response.get('choices', [{}])[0].get('message', {}).get('content', 'No content found')
            
            # Send the response back to the GUI thread
            window.write_event_value('-RESPONSE-', gemma_formatted_response)
        else:
            window.write_event_value('-STATUS-', "Upload or AI processing failed.")

# GUI layout
layout = [
    [sg.Text('Time Survived: 0:00', key='time')],
    [sg.Text('Focus on your work. This game tests your patience.')],
    [sg.Button('Start'), sg.Button('Spare Me')],
    [sg.Output(size=(60, 10), key='output')],
    
    # Chat with Gemma2 section
    [sg.Text("Chat with Gemma2 AI:")],
    [sg.Multiline(size=(60, 10), key='chat_output', disabled=True)],  # Display chat history
    [sg.InputText(size=(40, 1), key='chat_input'), sg.Button('Send to Gemma2')]
]

window = sg.Window('Focus Game', layout)
api_key = "sk-2c635844a29644ef89966c6ca577f260"  # Replace with your API key

# Event loop
running = False
while True:
    event, values = window.read(timeout=100)
    
    if event in (sg.WIN_CLOSED, 'Spare Me'):
        break
    
    if event == 'Start' and not running:
        running = True
        threading.Thread(target=ai_workflow, args=(api_key, window), daemon=True).start()
        start_time = time.time()
    
    if running:
        elapsed_time = int(time.time() - start_time)
        window['time'].update(f'Time Survived: {time.strftime("%M:%S", time.gmtime(elapsed_time))}')
    
    # Handle custom events from the AI workflow thread
    if event == '-STATUS-':
        print(values['-STATUS-'])
    
    if event == '-RESPONSE-':
        response_layout = [
            [sg.Multiline(values['-RESPONSE-'], size=(60, 20), disabled=True)],
            [sg.Button('Close')]
        ]
        response_window = sg.Window('Chat Response', response_layout)
        response_event, _ = response_window.read(close=True)

    # Handle chat messages to Gemma2
    if event == 'Send to Gemma2':
        user_message = values['chat_input']
        if user_message:
            try:
                # Display user message in the chat window
                window['chat_output'].print(f"User: {user_message}")
                
                # Get Gemma2's response (frustrating persona)
                gemma_response = get_gemma_response(api_key, user_message)
                gemma_formatted_response = gemma_response.get('choices', [{}])[0].get('message', {}).get('content', 'No content found')
                
                # Display Gemma2's response in the chat window
                window['chat_output'].print(f"Gemma2: {gemma_formatted_response}")
                window['chat_input'].update('')  # Clear input field
                
                # Use regex to find tags in Gemma2's response
                tags = re.findall(r'(mouse_jiggle|ringing_noise|windows_noise|click|popup_window|key_press|random_key_press)', gemma_formatted_response)
                
                # Trigger actions based on the tags found
                if 'mouse_jiggle' in tags:
                    threading.Thread(target=mouse_jiggle, daemon=True).start()
                if 'ringing_noise' in tags:
                    threading.Thread(target=ringing_noise, daemon=True).start()
                if 'windows_noise' in tags:
                    threading.Thread(target=windows_noise, daemon=True).start()
                if 'click' in tags:
                    threading.Thread(target=click, daemon=True).start()
                if 'popup_window' in tags:
                    threading.Thread(target=popup_window, daemon=True).start()
                if 'key_press' in tags:
                    threading.Thread(target=key_press, daemon=True).start()
                if 'random_key_press' in tags:
                    threading.Thread(target=random_key_press, daemon=True).start()
            except Exception as e:
                print(f"Error occurred: {e}")
                window['chat_output'].print(f"Error: {e}")

window.close()
