FROM debian:bullseye

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    automake \
    autoconf \
    libtool \
    pkg-config \
    cmake \
    wget \
    unzip \
    # Janus dependencies
    libmicrohttpd-dev \
    libjansson-dev \
    libssl-dev \
    libsrtp2-dev \
    libsofia-sip-ua-dev \
    libglib2.0-dev \
    libopus-dev \
    libogg-dev \
    libini-config-dev \
    libcollection-dev \
    libcurl4-openssl-dev \
    libnanomsg-dev \
    libconfig-dev \
    libnice-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

# ------------------------------------------------
# Build libwebsockets from source (stable v4.3.2)
# ------------------------------------------------
RUN git clone https://github.com/warmcat/libwebsockets.git && \
    cd libwebsockets && \
    git checkout v4.3.2 && \
    mkdir build && cd build && \
    cmake -DLWS_WITHOUT_TESTAPPS=ON -DCMAKE_INSTALL_PREFIX=/usr/local .. && \
    make -j$(nproc) && \
    make install

# ------------------------------------------------
# Build libusrsctp (for DataChannels support)
# ------------------------------------------------
RUN git clone https://github.com/sctplab/usrsctp.git && \
    cd usrsctp && \
    ./bootstrap && \
    ./configure && \
    make -j$(nproc) && \
    make install

# Ensure runtime linker can find installed libs
RUN echo "/usr/local/lib" > /etc/ld.so.conf.d/local.conf && ldconfig

# ------------------------------------------------
# Build Janus Gateway (latest stable)
# ------------------------------------------------
RUN git clone https://github.com/meetecho/janus-gateway.git
WORKDIR /opt/janus-gateway

RUN sh autogen.sh && \
    ./configure --prefix=/usr/local \
                --enable-websockets \
                --enable-data-channels \
                --disable-docs && \
    make -j$(nproc) && \
    make install && \
    make configs

# ------------------------------------------------
# Expose required ports
# ------------------------------------------------
EXPOSE 8188 8088 10000-10200/udp

# ------------------------------------------------
# Run Janus
# ------------------------------------------------
CMD ["janus", "-F", "/usr/local/etc/janus"]
