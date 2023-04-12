FROM python:3.10

WORKDIR /var/www/python

RUN pip install python-dotenv
RUN pip install pandas
RUN pip install scikit-learn
# RUN pip install pickle
RUN pip install requests
RUN pip install mysql-connector-python

CMD ["python", "main.py"] 