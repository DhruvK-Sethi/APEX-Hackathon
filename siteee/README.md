## Structure
- *src* folder contains the main code and content, other stuff is just venv(containerisation)
- HTML goes in src/templates
- CSS and JS go in src/static
- Images and other resources go in src/static/res

## Running Instructions
- You'll need python and venv
    * get python from the website or package manager
    * install venv with ```pip install venv```
- *cd* here
- activate venv with
    * ```source bin/activate``` *(bash)*
    * ```source bin/activate.fish``` *(fish)*
- start server with ```python main.py```

- Also to expose the server you need ngrok, install from internet or package manager
- then expose with ```ngrok http 5000```
- It will start in a window and give a url that can be accessed globally

## Notes
- Keep code commented
- Keep stuff in correct folders
