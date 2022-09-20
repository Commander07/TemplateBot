@echo off
py -3 -m venv env --upgrade-deps
call env\Scripts\activate.bat
pip install -r requirements.txt
set /p "token=TOKEN: "
echo token="%token%" > .env
git submodule update --init --recursive