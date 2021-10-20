#!/bin/bash
#three parameters of getMyMovies.py 1: output path. 2: output file name. 3: douban user ID.

docker run --user "$(id -u):$(id -g)" \
            -v /data:/data \
	    8a7e38489916 \
	    python3 getMyMovies.py /data/users/*** movie.csv 12345678


