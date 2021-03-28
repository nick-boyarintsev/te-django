FROM python:3.9-alpine

# Root bin to PATH:
ENV PATH=$PATH:/root/.local/bin

WORKDIR /var/www/backend

COPY ./backend/requirements.txt /var/www/backend/

RUN pip3 install --upgrade pip && \
    pip3 install --user --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

CMD python3 manage.py test && python3 manage.py runserver 0.0.0.0:8000
