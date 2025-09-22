# 🎈 Wellcome to the backdoor of the "Stressless Living!" Application

The original template is right here: [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

0. Download the code packet and run in a python running environment

2. Build secrets.toml file

3. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

4. Run the app  

   ```
   $ streamlit run streamlit_app.py
   ```
### Asspects of this application run with 

1. The assistance of an internet connection
2. API keys that are not included in these files
3. Accees to a mongo database

### To build the secrets file follow this format

[mongo]

uri = URL to Mongo Database

[API]

groqkey = Groq access key

geminikey = URL to Gemini access key

active_model = "Groq" or "Gemini"

### For Admins

The Evaluation page will not be operational via the Streamlit platform, you will need to do that function locally. Admin Passcode might not be provided.

### For Everyone Else (and the admins):

Documentation will be found via 

1. Comments in the code
2. README.txt where all functions and global variables can be found in a tree like structure. Functions/Variables called by an function is seen a tad forward that said function
3. find_your_function.txt has all functions/global variables will tell you everything you need to know: how to call them, parameters required, results, what they do and what safe guards exist. Use README.txt and find_your_function.txt together

