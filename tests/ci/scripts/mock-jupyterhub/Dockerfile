ARG MAX_PYTHON_VERSION
FROM cimg/python:${MAX_PYTHON_VERSION}
COPY mock-jupyterhub.py .
RUN pip install flask
EXPOSE 5000
CMD ["python", "mock-jupyterhub.py"]
