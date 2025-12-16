# ChatGPT Terminal Assistant

## Windows Installation

1. Visit https://platform.openai.com/api-keys and create a new API key.

2. Copy the API key.

3. Type the following command in Powershell (Recommended) - Then restart the Powershell

```
setx OPENAI_API_KEY "your_api_key_here"

```

4. Verify the key (Powershell)

```
echo $Env:OPENAI_API_KEY
```

5. . Clone the git repository/ download the zip

```
git clone "https://github.com/81131/ChatGPT-Terminal-Assistant"
```

6. Copy the chat.bat file and chat.py to a desired folder (Create if not available)

```
C:\bin
```

7. Add the bat file to system path.

- Press `Win + R` & type

```
sysdm.cpl
```

- Press `Enter`

- In the `Advanced` tab Select `Environment Variables`> PATH variable > Edit

- Click `New`
- Paste the bin folder path

```
C:\bin
```

- Save the info

Do this for both System variables and user variables.

8. Install Python and pip using https://www.python.org/downloads/

9. Install the necessary packages (Run in CMD)

```
pip install prompt_toolkit openai rich
```

10. Try running using following command

```
chat
```
