#!/bin/bash

if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found."
    exit 1
fi

LOG_PATH=./logs/index
BULK_PATH=../data/bulk

if [ -d "$LOG_PATH" ]; then
    rm -rf "$LOG_PATH"
fi

mkdir LOG_PATH

curl -X POST -u elastic:$ES_PASSWORD "$ES_URL/byline/_bulk?pretty" -H "Content-Type: application/x-ndjson" --data-binary @$BULK_PATH/byline.json -o ./logs/bulk/byline.log
echo ""
curl -X POST -u elastic:$ES_PASSWORD "$ES_URL/category/_bulk?pretty" -H "Content-Type: application/x-ndjson" --data-binary @$BULK_PATH/category.json -o ./logs/bulk/category.log
echo ""
curl -X POST -u elastic:$ES_PASSWORD "$ES_URL/news/_bulk?pretty" -H "Content-Type: application/x-ndjson" --data-binary @$BULK_PATH/news.json -o ./logs/bulk/news.log
echo ""
curl -X POST -u elastic:$ES_PASSWORD "$ES_URL/provider/_bulk?pretty" -H "Content-Type: application/x-ndjson" --data-binary @$BULK_PATH/provider.json -o ./logs/bulk/provider.log
echo ""
curl -X POST -u elastic:$ES_PASSWORD "$ES_URL/reporter/_bulk?pretty" -H "Content-Type: application/x-ndjson" --data-binary @$BULK_PATH/reporter.json -o ./logs/bulk/reporter.log
echo ""
