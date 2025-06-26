FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY servers/bad_sqlite_mcp_server_http.py .

EXPOSE 8080
CMD ["python", "bad_sqlite_mcp_server_http.py"]