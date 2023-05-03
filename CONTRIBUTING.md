# CONTRIBUTING

## How to run the Dockerfile locally

this tells the container not run the CMD line and instead run flask run, which
is going to use the flask development server
```
sh -c "flask run port(eg:-0.0.0.0)"
```

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run port(eg:-0.0.0.0)"
```