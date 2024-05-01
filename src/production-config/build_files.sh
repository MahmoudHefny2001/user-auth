echo "Starting build process"

pip install --upgrade pip


cd ../..

python3 -m venv .venv
. .venv/bin/activate

cd src/

pip3 install -r requirements.txt

python3 manage.py collectstatic --no-input

python3 manage.py makemigrations

python3 manage.py migrate

pip3 freeze

echo "Build process complete"
