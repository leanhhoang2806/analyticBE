

# Spin up a server
docker-compose down -v; docker-compose up --build --remove-orphans -d

# Test for endpoint with upload
`curl -X POST -H "Authorization: Bearer your_token" -F "file=@requirements.txt" http://localhost:8000/uploadfile/`