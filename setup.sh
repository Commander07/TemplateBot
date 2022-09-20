python3 -m venv env --upgrade-deps
source env/bin/activate
pip install -r requirements.txt
read -p "TOKEN: " token
echo token="$token" > .env
git submodule update --init --recursive