
# :rocket: Launch with Docker

```
docker build -t image_tp2 .
docker run -v $(pwd)/outputs:/index/outputs image_tp2
```
... or open interactive terminal and play with argument
```
docker run -v $(pwd)/outputs:/index/outputs -it --entrypoint bash image_tp2
```
