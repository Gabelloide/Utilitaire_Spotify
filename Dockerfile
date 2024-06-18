FROM debian:12

# Update, modules
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Using venv
RUN python3 -m venv /opt/venv
# Venv to PATH & install modules
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir mysql-connector-python

WORKDIR /app

# Copy the app's server to the container
COPY Server /app

# Expose the port the app runs on
EXPOSE 23456 23457 23458

# Container will exit as soon as the script is done, so we need to keep it running with a simple command workaround
#CMD ["tail", "-f", "/dev/null"]


# Run python main.py --db_address bd --db_port 3306 --db_user root --db_password pr0j3t_1nf0*** --zip_port 23456 --trend_port 23457 --userinfo_port 23458

# Database host is 'bd', defined in docker-compose.yml
CMD ["python3", "main.py", "--db_address", "bd", "--db_port", "3306", "--db_user", "root", "--db_password", "pr0j3t_1nf0***", "--zip_port", "23456", "--trend_port", "23457", "--userinfo_port", "23458"]