FROM python:3.13
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY ./app ./app
EXPOSE 8080

# Setup an app user so the container doesn't run as the root user
RUN useradd --create-home --shell /usr/sbin/nologin appuser
COPY --chown=appuser:appuser ./app ./app
EXPOSE 8000
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]