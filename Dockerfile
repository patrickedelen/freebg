FROM amazon/aws-lambda-python:3.9

ENV NUMBA_CACHE_DIR=/tmp/does_not_exist
ENV NUMBA_NUM_THREADS=1
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV XDG_DATA_HOME=/tmp

ENV AWS_ACCESS_KEY_ID=
ENV AWS_SECRET_ACCESS_KEY=
ENV AWS_SESSION_TOKEN=

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY src/ /var/task

CMD [ "app.handler" ]