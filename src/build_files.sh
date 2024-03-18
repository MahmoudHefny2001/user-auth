echo "Starting build process"

pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input

mkdir media 
mkdir images


echo "Build process complete"
