FROM python:3.11-alpine as compiler
ENV PYTHONUNBUFFERED 1
WORKDIR /app/
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip --no-cache-dir
COPY ./requirements.txt /app/requirements.txt
RUN pip install -Ur requirements.txt
RUN pip install gunicorn

FROM python:3.11-alpine as runner
WORKDIR /app/
COPY --from=compiler /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . /app/
RUN chmod +x /app/cmd.sh
CMD ["/app/cmd.sh"]