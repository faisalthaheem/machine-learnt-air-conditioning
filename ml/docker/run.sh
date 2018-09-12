#!/bin/sh
docker run -d -p 5000:5000 --name ltrest \
-v /home/faisal/ml-assets/:/scripts/assets \
-v /home/faisal/ml-assets/:/assets \
-v /home/faisal/work/learning-thermostat/ml/jupyter:/scripts \
-e mongodbhost=192.168.100.100 \
--restart unless-stopped \
faisalthaheem/lt-rest:1.0
