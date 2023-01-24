FROM alpine

WORKDIR /init_files

COPY . .

USER root
RUN apk --no-cache add curl
RUN apk add jq
RUN chmod +x init_db.sh
ENTRYPOINT ["sh", "./init_db.sh"]

#RUN apt-get update && apt-get install -y wget
#RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
#RUN chmod +x wait-for-it.sh
#
#
#RUN /usr/local/bin/wait-for-it.sh elasticsearch:9200 -s -t 30
#RUN curl -XPUT 'http://elasticsearch:9200/orders_index' -H 'Content-Type: application/json' -d @index_mapping.json



#HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
#    CMD curl -XPUT 'http://localhost:9201/orders_index' -H 'Content-Type: application/json' -d @index_mapping.json || exit 1

