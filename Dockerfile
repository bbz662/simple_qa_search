# Define custom function directory
ARG FUNCTION_DIR="/app"

FROM python:3.10 as build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Install aws-lambda-cpp build dependencies
RUN apt-get update &&
  apt-get install -y \
    g++ \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}
COPY . ${FUNCTION_DIR}

# Install the function's dependencies
RUN pip install \
  --target ${FUNCTION_DIR} \
  awslambdaric

FROM python:3.10

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y sqlite3 libblas3 liblapack3
RUN pip install sqlite_vss numpy openai boto3

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ENV LD_LIBRARY_PATH=/path/to/lib:$LD_LIBRARY_PATH

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "app.lambda_handler" ]
