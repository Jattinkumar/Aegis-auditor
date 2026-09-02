FROM python:3.13-slim
WORKDIR /app
COPY main.py .
RUN touch audit_report.json
CMD ["python", "main.py"]
