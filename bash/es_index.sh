#!/bin/bash

if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found."
    exit 1
fi

LOG_PATH=$LOG_PATH
INDEX_PATH=../data/index

if [ -d "$LOG_PATH" ]; then
    rm -rf "$LOG_PATH"
fi

mkdir "$LOG_PATH"

curl -X PUT -u elastic:$ES_PASSWORD "$ES_URL/byline" -H "Content-Type: application/json" -d @$INDEX_PATH/byline.json -o $LOG_PATH/byline.log
echo ""
curl -X PUT -u elastic:$ES_PASSWORD "$ES_URL/category" -H "Content-Type: application/json" -d @$INDEX_PATH/category.json -o $LOG_PATH/category.log
echo ""
curl -X PUT -u elastic:$ES_PASSWORD "$ES_URL/news" -H "Content-Type: application/json" -d @$INDEX_PATH/news.json -o $LOG_PATH/news.log
echo ""
curl -X PUT -u elastic:$ES_PASSWORD "$ES_URL/provider" -H "Content-Type: application/json" -d @$INDEX_PATH/provider.json -o $LOG_PATH/provider.log
echo ""
curl -X PUT -u elastic:$ES_PASSWORD "$ES_URL/reporter" -H "Content-Type: application/json" -d @$INDEX_PATH/reporter.json -o $LOG_PATH/reporter.log
echo ""
