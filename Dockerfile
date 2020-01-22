FROM python:3.6.5
MAINTAINER Your Name "nugroho@alterra.id"
RUN mkdir -p /flask-portofolioBE2
COPY . /flask-portofolioBE2
RUN pip install -r /flask-portofolioBE2/requirements.txt
WORKDIR /flask-portofolioBE2
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
