#!/bin/bash

# Set API endpoint
API_ENDPOINT="http://localhost:5000/generate"

# Set API key (replace with your actual key if needed)
#API_KEY="YOUR_API_KEY"

# Set image file path
IMAGE_PATH="baseline.png"

# Check if image file exists
if [ ! -f "$IMAGE_PATH" ]; then
  echo "Error: Image file '$IMAGE_PATH' not found."
  exit 1
fi

# Create a dummy image file if baseline.png doesn't exist
if [ ! -f "$IMAGE_PATH" ]; then
  echo "Creating dummy baseline.png"
  touch baseline.png
fi

# Create a multipart form data request
BOUNDARY="----WebKitFormBoundary7MA4YWxkTrZu0gW"
REQUEST_BODY=$(cat <<EOF
--$BOUNDARY
Content-Disposition: form-data; name="image"; filename="$IMAGE_PATH"
Content-Type: image/png

$(cat "$IMAGE_PATH")
--$BOUNDARY
Content-Disposition: form-data; name="resolution"

1080x1920
--$BOUNDARY
Content-Disposition: form-data; name="url"

https://example.com
--$BOUNDARY--
EOF
)

# Send the request using curl
RESPONSE=$(curl -s -X POST \
  -H "Content-Type: multipart/form-data; boundary=$BOUNDARY" \
  -d "$REQUEST_BODY" \
  "$API_ENDPOINT")

# Print the response
echo "Response:"
echo "$RESPONSE"

# Check if the request was successful (status code 200)
if [[ $(echo "$RESPONSE" | jq -r '.status') == "ready" ]]; then
  echo "API test successful!"
else
  echo "API test failed."
  exit 1
fi

exit 0