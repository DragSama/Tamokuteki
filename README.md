# Tamokuteki
A multipurpose userbot written using telethon

## Steps to deploy
## Setting up on Heroku:
Here are the ENV variable needed:
- `API_ID` - Self explanatory, Get this from [my.telegram.org/apps](https://my.telegram.org/apps)
- `API_HASH` - Self explanatory, Get this from [my.telegram.org/apps](https://my.telegram.org/apps)
- `STRING_SESSION` - See how to get this [here](https://github.com/DragSama/Tamokuteki#generating-string-session)
## Setting up locally:
- `git clone https://github.com/DragSama/Tamokuteki.git`
- `cd Tamokuteki`
- `cd TamokutekiBot`
- `cp sample_config.py config.py` then open it in your preferred text editor/code editor.
Then change following values:
- `API_ID` - Self explanatory, Get this from [my.telegram.org/apps](https://my.telegram.org/apps)
- `API_HASH` - Self explanatory, Get this from [my.telegram.org/apps](https://my.telegram.org/apps)
- `STRING_SESSION` - See how to get this [here](https://github.com/DragSama/Tamokuteki#generating-string-session)

## Starting the bot:
- `python3 -m TamokutekiBot` or `python -m TamokutekiBot` on windows.

## Generating String Session
Step by Step instruction:
- `git clone https://github.com/DragSama/Tamokuteki.git` Ignore if already cloned.
- `cd Tamokuteki`
- `python3 stringsession.py` or `python stringsession.py` on windows. Then enter your API_ID and API_HASH, You can get these from [my.telegram.org/apps](https://my.telegram.org/apps)

## Inspirations / Credits
- [Uniborg](https://github.com/SpEcHiDe/UniBorg) (Heavily Inspired)
