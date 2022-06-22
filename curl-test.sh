#!/bin/bash

echo testing POST and GET endpoints of MYPORTFOLIO API

REQUEST=$(curl --request POST http://localhost:5000/api/timeline_post -d "name=curlTest&email=test&content=test")
RESPONSE=$(curl http://localhost:5000/api/timeline_post)

echo "The request: $REQUEST"
echo "The response: $RESPONSE"

if [[ "$RESPONSE" == *"$REQUEST"* ]] || [[ "$RESPONSE" != "" ]]; then
	echo "Success!"
else
	echo "Test Unsuccessful!"
fi

curl --request DELETE http://localhost:5000/api/timeline_post -d "name=curlTest"
