import os
import requests
import time
import pyautogui

# Function to take a screenshot
def take_screenshot():
    screenshot = pyautogui.screenshot()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    screenshot_filename = f"screenshot_{timestamp}.png"
    screenshot.save(screenshot_filename)
    print(f"Screenshot saved as: {screenshot_filename}")
    return screenshot_filename

# Function to upload the screenshot to the API
def upload_file(token, file_path):
    url = 'http://192.168.178.26:3000/api/v1/files/'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'image/png'
    }
    # Set the content type explicitly
    files = {
        'file': (file_path.split('/')[-1], open(file_path, 'rb'), 'image/png')
    }
    response = requests.post(url, headers=headers, files=files)
    return response.json()

# Function to interact with the API and analyze the image
def analyze_image(token, file_id, question):
    url = 'http://192.168.178.26:3000/api/chat/completions'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    # Create payload with the question and image file ID
    payload = {
        'model': 'minicpm-v:8b',
        'messages': [{'role': 'user', 'content': question}],
        'files': [{'type': 'image', 'id': file_id}]
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Main process
def main():
    # API Token (replace with your actual token)
    token = 'sk-2c635844a29644ef89966c6ca577f260'

    # Take a screenshot
    screenshot_filename = take_screenshot()

    # Upload the screenshot
    upload_response = upload_file(token, screenshot_filename)

    if 'id' in upload_response:
        file_id = upload_response['id']
        print(f"Image uploaded successfully. File ID: {file_id}")
        
        # Ask the user for a question about the screenshot
        question = input("Enter your question about the screenshot: ")
        
        # Analyze the uploaded image
        analysis_response = analyze_image(token, file_id, question)
        
        # Print the response from the API
        if 'choices' in analysis_response:
            print("Analysis Result:", analysis_response['choices'][0]['message']['content'])
        else:
            print("Error analyzing image:", analysis_response)
    else:
        print("Error uploading image:", upload_response)

if __name__ == '__main__':
    main()
