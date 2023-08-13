FROM docker.io/python:3.11-alpine

WORKDIR /
#실행할때 어느 경로에서 실행을 할지.

COPY requirements.txt ./
#파일을 빌드되고있는 이미지에 복사해서 넣는다.

RUN pip install -r requirements.txt --no-cache-dir --disable-pip-version-check
#컨테이너에서 pip installdmf gownrh 

ARG DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE taxiRoka.settings


# RUN python server/manage.py collectstatic

COPY ./ /
#파이썬 코드드를 전부다 복사해서 넣어주고

EXPOSE 8000
#8000포트를 쓰겠다.

WORKDIR /

CMD ["gunicorn", "taxiRoka.asgi:application", "-c", "conf.d/gunicorn.conf.py"]