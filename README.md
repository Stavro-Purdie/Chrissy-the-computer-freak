# Man VS AI
This LLM powered program serves to target the user with the most annoying distractions based off screenshots taken periodically. The aim is to surpass these distractions for as long as possible. Good Luck!


## SETUP

To set this program up you will need to set up Open-WebUI and then edit `main.py` to change API Key, Models used and the URI of the Open-WebUI server.

To install Open-WebUI Run these commands:

### Installation with Default Configuration
If Ollama is on your computer, use this command:
`docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main`

If Ollama is on a Different Server, use this command:
To connect to Ollama on another server, change the OLLAMA_BASE_URL to the server's URL:
`docker run -d -p 3000:8080 -e OLLAMA_BASE_URL=https://example.com -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main`

To run Open WebUI with Nvidia GPU support, use this command:
`docker run -d -p 3000:8080 --gpus all --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:cuda`

Installation for OpenAI API Usage Only
If you're only using OpenAI API, use this command:
`docker run -d -p 3000:8080 -e OPENAI_API_KEY=your_secret_key -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main`

### Installing Open WebUI with Bundled Ollama Support

This installation method uses a single container image that bundles Open WebUI with Ollama, allowing for a streamlined setup via a single command. Choose the appropriate command based on your hardware setup:
With GPU Support: Utilize GPU resources by running the following command:
`docker run -d -p 3000:8080 --gpus=all -v ollama:/root/.ollama -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:ollama`

For CPU Only: If you're not using a GPU, use this command instead:
`docker run -d -p 3000:8080 -v ollama:/root/.ollama -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:ollama`

After this you will need to navigate to `[IP ADDRESS OF Open-WebUI]:3000` and set up your account


## POST INSTALL  

You will need to download two models, this can be done by putting their names individually into the search bar
These models are:

`minicpm-v:8b` -- For Screenshot to Text system
`gemma2:27b`   -- For Main Agent

You can change these should you want to use different models however you will need to edit the models used in the script

### API

To use the API you will need to navigate to settings and then profile, then look for API key under advanced, copy that and paste it between the '' in the python script

### Dependencies for script itself

run pip install -r requirements.txt to install all python dependencies

# NOTE THIS SOFTWARE IS ONLY FOR USE ON WINDOWS (THE SERVER CAN RUN ON LINUX THOUGH)
