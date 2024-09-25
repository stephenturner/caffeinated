FROM python:3.11-alpine
RUN pip install caffeinated
WORKDIR /files
ENTRYPOINT ["caffeinated"]
CMD ["--help"]
