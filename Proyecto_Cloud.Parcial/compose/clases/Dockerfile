FROM python:3-slim
WORKDIR /programas/clases
RUN pip3 install fastapi uvicorn pydantic mysql-connector-python
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
