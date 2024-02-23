FROM alpine:edge

RUN addgroup -S Flask_app && adduser -S flask_app -G Flask_app

WORKDIR /app

RUN apk add --update py3-pip

COPY requirements.txt /app/
RUN pip install --break-system-packages --no-cache-dir -r /app/requirements.txt

COPY app.py stegano.py /app/
COPY templates/* /app/templates/
COPY static/main.css /app/static/

RUN chown -R flask_app:Flask_app /app

USER flask_app

EXPOSE 80

CMD ["python3", "/app/app.py"]