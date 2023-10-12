### [Go Back](https://github.com/Johonnyy/amber)
# Function Documentation
# Creating a Function
Functions can be created on the dashboard or in the files.

Go to edit the module where you want the function to be in whether that is in the dashboard or from the files and create a new class. Here is an example of one of these classes:
```
class GetWeather:
    def __init__(self):
        self.name = "GetWeather"
        self.description = "Get weather data."
        self.version = "1.0.0"
        self.parameters = {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city,state,and/or country to get the weather from. OPTIONAL. Not accepted values: tomorrow, today, next week, etc",
                }
            },
        }
        self.configOptions = [
            {
                "value": "googleMapsAPI",
                "title": "Google Maps API Key",
                "description": "The API key obtained from Google Cloud Maps Console.",
                "type": "text",
            },
            {
                "value": "openWeatherMap",
                "title": "Open Weather Map API Key",
                "description": "The API key obtained from https://openweathermap.org/. You must enable One Call API.",
                "type": "text",
            },
        ]

    def handle(self, args):
        # Handle getting the weather
        pass
```

This is a stripped down version of the weather function. Let's explain it. First, In the \_\_init\_\_ function, there are multiple fields. These fields tell the system about your function.  
\*`self.name`: Name of the function. Should match class name  
\*`self.description`: Description  
`self.version`: Version number  
\*`self.parameters`: Basically the arguments of the function. The format for constructing these can be found [here](https://platform.openai.com/docs/guides/gpt/function-calling).  
`self.configOptions`: Array of inputs such as API Keys needed for the function. For format can be found in the example.  
\* = Being sent to OpenAI Functions  

### Handle function
This function **is required** and should only contain two arguments: self and args (this can be called anything it doesn't matter).
The Arguments passed through is a dictionary with all of the parameters. You can get one of these by using this code: `args.get("location", None)` if you needed to get a location parameter.
Currently, the `return` statement should just be text. **This can change though and probably will change to a dictionary.** This can be as simple as `return "Success"` to let GPT know the function succeeded. You can also send errors through there (still in string format) and GPT will change it to a readable/speakable format. For this example you would send the result of the weather data and GPT would format that.

If a function does not have a handle function, it will not be loaded. More examples can be found in the base modules.

After you do all of this and save, you can go back to the module manager and reload the functions and it should appear. Congratulations!

