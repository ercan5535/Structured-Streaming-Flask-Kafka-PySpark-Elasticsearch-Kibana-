#!/bin/bash

# Wait until elasticsearch is ready
seconds=10
until curl "${ES_HOST}:${ES_PORT}/_cluster/health?wait_for_status=yellow&timeout=30s"; do
    >&2 echo "Elastisearch is unavailable - waiting for it... 😴 ($seconds)"
    sleep 10
    seconds=$(expr $seconds + 10)
done

# Create index on elasticsearch
curl -XPUT "${ES_HOST}:${ES_PORT}/orders_index" -H "Content-Type: application/json" -d @index_mapping.json

seconds=10
# Wait until kibana is ready
until [[ "$status" == "All services are available" ]]; do
    >&2 echo "Kibana is unavailable - waiting for it... 😴 ($seconds)"
    status=$(curl -s ${KIBANA_HOST}:${KIBANA_PORT}/api/status | jq -r '.status.overall.summary')
    sleep 10
    seconds=$(expr $seconds + 10)
done

# Import dashboard to kibana
curl -XPOST "${KIBANA_HOST}:${KIBANA_PORT}/api/kibana/dashboards/import" -H "Content-Type: application/json" -H "kbn-xsrf: true" -d @dashboard.json 

