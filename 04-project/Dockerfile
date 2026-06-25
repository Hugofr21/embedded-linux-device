FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    build-essential \
    g++ \
    clang \
    clang-tidy \
    cmake \
    ninja-build \
    gcovr \
    git \
    python3 \
    python3-pip \
    && apt clean

WORKDIR /app

COPY . .

RUN mkdir -p build

CMD ["/bin/bash"]