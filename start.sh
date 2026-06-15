docker build --no-cache -t geetest_image .
docker rm -f geetest_container
docker run -d --restart=always --name geetest_container -p 8080:8080 geetest_image