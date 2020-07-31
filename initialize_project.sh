docker-compose build
docker-compose up -d db
docker-compose up -d backend
docker exec -it saphire_backend_1 sh -c "python manage.py deletealldata"
docker exec -it saphire_backend_1 sh -c "python manage.py updatehistoricalstocks"
docker-compose down
