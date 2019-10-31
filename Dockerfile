FROM python:3.7-slim
WORKDIR /app
ADD . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "-u", "bot.py" ]
