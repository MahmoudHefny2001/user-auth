echo "Starting build process"

pip install --upgrade pip

pip3 uninstall urllib3
pip3 install urllib3==1.26.7

pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input

mkdir media 
mkdir images

pip3 freeze 

echo "Build process complete"
