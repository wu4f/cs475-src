FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p db_data
COPY servers/bad_sqlite_mcp_server_http.py .
COPY ./db_data/metactf_users.db ./db_data/metactf_users.db

EXPOSE 8080
CMD ["python", "bad_sqlite_mcp_server_http.py"]