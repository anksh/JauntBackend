# Jaunt Backend

## Setup
Aside from setting up django and installing requirements.txt, you will need to place a `SECRET_KEY` in `Jaunt/secret_key.txt` and a Firebase API key in `Jaunt/firebase_key.txt`. The `generate_words_file.py` script also expects a file called `full_list.txt` which has words separated by newlines. This script will create the necessary files that the backed expects when creating a Jaunt object, and should be run before setting up the server.
