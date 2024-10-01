FROM hub.hamdocker.ir/python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --proxy=http://192.168.20.201:1081 --upgrade pip && pip install --proxy=http://192.168.20.201:1081 -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt


# Copy project
COPY . /app/


# Expose port
EXPOSE 8000

# # Run the application
CMD ["gunicorn", "--bind", ":8000", "postgresTest.wsgi:application"]