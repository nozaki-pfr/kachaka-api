FROM ubuntu:22.04

RUN apt-get update && \
    apt-get -y install --no-install-recommends \
        clang-format-15 \
        git \
        python3 \
        python3-pip \
        python3-setuptools \
        shellcheck \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install -U pip
RUN --mount=source=tools/lint,target=/lint \
    pip3 install -r /lint/requirements.txt
