ARG SOURCE_IMAGE="python:3.6-alpine3.8"
FROM ${SOURCE_IMAGE} as builder

RUN apk add --no-cache gcc musl-dev postgresql-dev libev-dev \
    && mkdir -p /build/package/dependencies

RUN cd /build/ \
    && pip download psycopg2 \
    && tar xvzf psycopg2-*.tar.gz -C . \
    && rm -f *.tar.gz \
    && cd psycopg2*/ \
    && python setup.py bdist_wheel --dist-dir=/build/package/dependencies/
RUN cd /build \
    && pip download bjoern \
    && tar xvzf bjoern*.tar.gz -C . \
    && cd bjoern* / \
    && python setup.py bdist_wheel --dist-dir=/build/package/dependencies/
WORKDIR /opt/build

#: this step won't be cached, so please keep it as lower as possible
COPY ./src /opt/build
RUN python setup.py bdist_wheel --dist-dir=/build/package/

FROM ${SOURCE_IMAGE}
MAINTAINER "Nickolas Fox <tarvitz@blacklibrary.ru>"
LABEL net.w40k.app="backend" \
      net.w40k.description="kubernetes cluster example application"
RUN apk add --no-cache ca-certificates libpq libev

COPY --from=builder /build/package/ /build/

#: install binary dependencies and global runtime
RUN pip install /build/dependencies/*
RUN pip install /build/*.whl

#: bjoern wsgi server settings
CMD wsgi-server
