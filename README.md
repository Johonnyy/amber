# Amber
Amber is a voice assistant I made in my freetime. It is inspired by Jarvis from Iron Man. It is built off of three core aspects:
1. Porcupine - Wake word engine to detect when you say "Hey Amber" or "Yo Amber"
2. Azure Speech Services - Speech to text and Text to speech. It was the easiest and cheapest to integrate and I found it very accurate.
3. OpenAI Functions - Uses GPT-3.5-Turbo to determine the function you want to run. I like this over Dialogflow or Wit.AI because it is easier to create dynamic functions. It also has general knowledge information which makes it useful for general queries. The only downside is that there is no free version. It is very cheap however, and pricing is explained [here](#Cost)

Still in development.

# Features

1. [Web Dashboard](#Dashboard) - You can control pretty much everything from here. I am still adding features.
2. [Modular System](#Developing) - It is super easy to create modules and functions that can add functionality.
3. SQLite - Automatically saves all conversations into an SQLite database.
4. Made with expandability in mind - Everything is made so it can be expanded. Modules are super easy to create and can be loaded at run time
5. Automatic Updater - Just ask Amber to update and it will pull the latest version from github and update itself. **WARNING: This will overwrite any changes you have made. It will not overwrite plugin modules**
6. Local Device - The device that runs locally. This handles all of the listening and text to speech. It also has a display for the time and date. I am adding functionality for weather, lists, and code displays.

#### Other features:

1. Weather

# Installing
Installing is easy and only needs three steps. 
Amber is not supported on the ARM architecture. As of October 2023, [Azure Speech](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-speech-to-text?tabs=linux%2Cterminal&pivots=programming-language-python#set-up-the-environment) only supports x64 architectures on Linux.
You might need to install `pyaudio` on linux. If you get an error, try installing it. Any other errors please create an issue.
```
git clone https://github.com/Johonnyy/amber
cd amber
python .\wrapper.py
```
**You will need to copy the config.yml.example to config.yml. If you do not do this, you get an error.**
**I strongly recommend running it from the wrapper, as that allows it to be updated and restarted while it is running without needing to go back and interact with the console.**

The wrapper will automatically create a virtual environment and install all of the modules so you don't have to worry about that.
You can use `python .\wrapper.py --debug` to start it quicker. This disables the check for libraries and doesn't install them. Don't use this the first time.

# Configuration
All of these are required  
`adminPass`: The password for the dashboard.  
`azureKey`: The key obtained from Microsoft Azure for speech services.  
`initialPrompt`: The prompt that is first sent to GPT. This is included in every conversation.  
`openaiKey`: The API key obtained from the OpenAI website.  
`picovoiceKey`: The API key obtained from the Picovoice website.  
`port`: Port to run the admin Dashboard on.  
`speech.region`: Region for the text to speech. Required by Azure.  
`speech.voice`: The voice for the assistant. Voices can be found [here](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts#prebuilt-neural-voices).

# Dashboard
The dashboard is a useful feature that allows you to manage Amber entirely on the web. It is available on the port configured in `config.yml`. An example URL would look like: `localhost:8000/dashboard`. This will probably redirect you to the login page where the default login is `admin` and `password`. The password can be changed. These are the different pages:

##### Configuration
JSON editor for editing the config.yml file. These values are updated automatically so you shouldn't have to restart. If you change the picovoiceKey you will need to restart, which can be done on the main page if you are using the wrapper (recommended).

##### Interactive
Page for interacting with Amber on a text based conversation. This is useful for debugging, as it shows the raw json for each message and how many tokens the conversation takes up. Each of these conversations are saved in the conversations.db database.

##### Module Manager
Page for configuring functions and modules. Here you can edit API Keys, reload functions, and edit modules.

##### Device Manager
I haven't worked too much on device because I've only had a need for the local device so I don't think this will work.

##### Conversation Logs
This has not be created yet. This page will be for reading the previous conversations and maybe doing something with that data.

##### Console Logs
Pretty self explanatory. Amber comes with it's own `log()` function which logs everything in the console and on this page.

# Developing
### Quick Overview
It is easy to expand the functionality, and can be easily done from the dashboard. First there is a little bit of terminalogy to get familiar with:
1. [Module](https://github.com/Johonnyy/amber/blob/main/documentation/MODULES.md) - Python file in app/modules folder. These files can contain classes called `functions`
2. [Functions](https://github.com/Johonnyy/amber/blob/main/documentation/FUNCTIONS.md) - Classes within a module that have data to construct a function. This is sent to OpenAI with your message.
3. Plugins - You shouldn't see this super often. This was the old name for the plugin type of modules. Base modules used to hardcoded and now they are dynamically loaded with plugins.

### Quick Start
To develop a new module and function, you can use the [dashboard](#Dashboard). Navigate to the Module Manager page and click on `Create New Module`. This will take you to a page where you input the module name and what type you want it to be. The current types are `base` and `plugin`. After you create it, it should redirect you to a page with a text editor that looks similar to VSCode. You can use that or develop on your own IDE. I made this so it was easier to develop on-the-go without having to connect to your device via ssh if Amber was running on a separate device. At this point I would recommend reading the [Function Documentation](https://github.com/Johonnyy/amber/blob/main/documentation/FUNCTIONS.md) for creating functions.

# Cost to Run
You can download Amber for free and modify it how you'd like, but OpenAI charges a fee to use their API. The current rate for GPT-3.5-Turbo (4K) is `1000 Tokens / $0.0015`. This is fairly cheap, as every function adds at most 100-150 tokens. More detailed pricing will be coming soon.

# The deprecated folder :O
These are my previous attempts before finally landing on using OpenAI Functions. This includes Wit.ai and Dialogflow attempts. You are welcome to look at these and modify them.

# Version History and Notes
`1.3.1 (current)` - Edited for deployment    
`1.2.5` - Almost full documentation  
`1.1.0` - Added an updater function (still not sure if it fully works)  
`1.0.0` - Base assistant with minimum functionality  