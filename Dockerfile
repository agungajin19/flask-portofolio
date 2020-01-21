FROM python:3.6.5
MAINTAINER Your Name "nugroho@alterra.id"
RUN mkdir -p /flask-portofolio
COPY . /flask-portofolio
RUN pip install -r /flask-portofolio/requirements.txt
WORKDIR /flask-portofolio
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
