# docker build -t airflow-notebooks:latest .
# docker run -d -p 8080:8080 airflow-notebooks

FROM apache/airflow:2.0.2

RUN mkdir /opt/airflow/pythoncode
RUN mkdir /opt/airflow/pythoncode/prediction
RUN mkdir /opt/airflow/pythoncode/runtime
RUN export PYTHONPATH="/opt/airflow/pythoncode"
RUN rm -rf /home/airflow/.local/lib/python3.6/site-pacakges/airflow/example_dags/

COPY prediction/ /opt/airflow/pythoncode/prediction
COPY runtime/ /opt/airflow/pythoncode/runtime

