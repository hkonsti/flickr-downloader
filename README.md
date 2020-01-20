# flickr-downloader

Docker usage:
You can use the Dockerfile to build and run the script inside of a Docker container.

Open the terminal in the directory containing all the files and build the container from the Dockerfile with:

`docker build -t flickr-downloader .`

Now you can run the newly created image with:

`docker run flickr-downloader -url <your album url>`