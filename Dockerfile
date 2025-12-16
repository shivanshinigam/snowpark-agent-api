FROM public.ecr.aws/snowflake/snowpark-python:latest

WORKDIR /app

COPY app /app

RUN pip install --no-cache-dir fastapi uvicorn pandas

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
