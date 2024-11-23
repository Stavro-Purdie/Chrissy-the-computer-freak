import requests
import json
import pyautogui
import os
from datetime import datetime

# Function to upload a file to the server with proper content type
def upload_file(token, file_path):
    url = 'http://192.168.178.26:3000/api/v1/files/'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    
    # Open the file in binary mode for uploading
    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file, 'image/png')}  # Set content-type to 'image/png'
        
        # Sending POST request to upload the file
        response = requests.post(url, headers=headers, files=files)
        
    # Check for successful upload and return the response
    if response.status_code == 200:
        return response.json()  # Successfully uploaded
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to get chat response based on user input
def get_chat_response(api_key, question, screenshot_file_id=None):
    url = "http://192.168.178.26:3000/api/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Prepare the message data
    data = {
        "model": "llava:13b",  # Ensure the model supports image references
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }
    
    # If a screenshot file is uploaded, attach the file_id to the query
    if screenshot_file_id:
        data['messages'].append({
            "role": "system",
            "content": f"Here is a screenshot to consider: {screenshot_file_id}"
        })
    
    # Sending the POST request to get a response from the chat API
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()  # Returning the JSON response from the API
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to take a screenshot and save it with a unique name
def take_screenshot():
    # Create a unique filename based on the current time
    screenshot_path = f"screenshot.png"
    
    # Capture the screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    
    return screenshot_path

# Function to format chat response
def format_chat_response(response):
    try:
        message = response.get('choices', [{}])[0].get('message', {}).get('content', 'No content found')
        formatted_response = f"Chat Response:\n\n{message}"
        return formatted_response
    except Exception as e:
        return f"Error formatting response: {e}"

# Example usage:

api_key = "sk-56cc33d8124242fd92dbd04b2370aa64"

# Take a screenshot and save it
screenshot_path = take_screenshot()
print(f"Screenshot saved as: {screenshot_path}")

# Upload the screenshot to the server
upload_response = upload_file(api_key, screenshot_path)
print("Upload Response:", upload_response)

# Get the file ID from the upload response (make sure it's 'id' as the file ID)
screenshot_file_id = upload_response.get('id')  # Use 'id' as the file reference
if screenshot_file_id:
    print(f"File uploaded successfully, file ID: {screenshot_file_id}")
else:
    print("File upload failed, no file_id returned.")

# Ask a question and send the file ID for context if the file was uploaded successfully
question = 'Describe the contents of the screenshot, include application name, and any other positioning/relivent data that would help a agent play a nasty prank on the user'
chat_response = get_chat_response(api_key, question, screenshot_file_id)
formatted_response = format_chat_response(chat_response)

# Print the formatted response
print(formatted_response)

# Optionally, clean up the screenshot file after uploading
if os.path.exists(screenshot_path):
    os.remove(screenshot_path)
    print(f"Deleted the screenshot file: {screenshot_path}")


