# Apply migrations only if necessary
echo "Checking for pending migrations..."
python3 manage.py makemigrations
python3 manage.py migrate



# Start the Django development server
echo "Starting Django server..."
exec python3 manage.py runserver 0.0.0.0:8000
