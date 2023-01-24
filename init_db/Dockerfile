FROM alpine

WORKDIR /init_files

COPY . .

USER root
RUN apk --no-cache add curl
RUN apk add jq
RUN chmod +x init_db.sh
ENTRYPOINT ["sh", "./init_db.sh"]
