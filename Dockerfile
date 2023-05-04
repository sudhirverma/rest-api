FROM python:3.10
# EXPOSE 5000

WORKDIR /app
COPY requirements.txt .
# pip install doesn't use a cache folder if there is one
RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY . .
# to tell it where to run
# that's the address and port that it's gonna be running on
# CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]

CMD [ "/bin/bash", "docker-entrypoint.sh" ]

# CMD ["flask", "run", "--host", "0.0.0.0"]