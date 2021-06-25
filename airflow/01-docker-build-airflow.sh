cd ..
docker build -t ecosystemai/ecosystem-airflow:latest -f airflow/Dockerfile .
docker push ecosystemai/ecosystem-airflow:latest
cd airflow