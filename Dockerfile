FROM python:3.7-alpine
ADD . /tc
WORKDIR /tc
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "-u", "bot.py" ]%