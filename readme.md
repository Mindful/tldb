# Setup
- `pip install -r requirements.txt`
- `python -m spacy download en`
- The environment variable `GOOGLE_APPLICATION_CREDENTIALS` must be set to the location of valid credentials that will be used to call Google Translate. Alternatively, the location can be set by changing code at the top of translation_client.py


# Config / Auth
If you create a file named in the same directory as the app is running `config.ini`, it will be loaded and used by the application. Right now, the only section supported is `auth`. Creating a config file like this:
``` 
[auth]
username = uuu
password = p123
```
Will result in all endpoints requiring basic auth with the username `uuu` and the password `p123`.