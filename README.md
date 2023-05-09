# rest-api 4

To Run application
```
python -m venv .venv
pip install flask
flask run
```

### Image icon

./img/Screenshot from 2023-04-08 15-16-45.png

# Docker build
```
sudo docker build -t rest-apis-flask-python .
```

# Run in development mode in docker
-v so that our code will force the container's Flask app to restart whenever we make changes.
```
sudo docker run -dp 5000:5000 -w /app -v "$(pwd):/app" rest-apis-flask-python
```

or

```
sudo docker run -dp 5000:5000 -w /app -v "$(pwd):/app" rest-apis-flask-python sh -c "flask run --host 0.0.0.0"
```

```
sudo docker run -p 5000:80 rest-apis-flask-smorest-rq
```

swagger
```
http://127.0.0.1:5000/swagger-ui
```


https://dashboard.render.com


https://rest-apis-flask.teclado.com/