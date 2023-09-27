FROM python:3.11-slim as compiler
ENV PYTHONUNBUFFERED 1
WORKDIR /app/
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip --no-cache-dir
COPY ./requirements.txt /app/requirements.txt
RUN pip install -Ur requirements.txt
RUN pip install gunicorn

FROM node:lts as js-compiler
WORKDIR /app/
COPY ./javascript .
WORKDIR /app/javascript/
RUN npm install
RUN npm run build

FROM python:3.11-slim as runner
WORKDIR /app/
COPY --from=compiler /opt/venv /opt/venv
COPY --from=js-compiler /app/javascript /app/javascript
ENV PATH="/opt/venv/bin:$PATH"
COPY . /app/
CMD ["gunicorn", "index:app", "--error-logfile", "/var/log/gunicorn/error.log", "--access-logfile", "/var/log/gunicorn/access.log", "--capture-output", "--timeout", "90"]