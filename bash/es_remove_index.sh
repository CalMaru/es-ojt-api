#!/bin/bash

if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found."
    exit 1
fi

curl -X DELETE -u elastic:$ES_PASSWORD "$ES_URL/byline"
echo ""
curl -X DELETE -u elastic:$ES_PASSWORD "$ES_URL/category"
echo ""
curl -X DELETE -u elastic:$ES_PASSWORD "$ES_URL/news"
echo ""
curl -X DELETE -u elastic:$ES_PASSWORD "$ES_URL/provider"
echo ""
curl -X DELETE -u elastic:$ES_PASSWORD "$ES_URL/reporter"
echo ""
