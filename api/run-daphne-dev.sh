#!/bin/sh

watchfiles "daphne -b 0.0.0.0 -p 8001 config.asgi:application" /usr/src/app