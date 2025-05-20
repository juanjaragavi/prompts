#!/bin/bash
set -e -E

# To run this script, install jq for JSON processing

GEMINI_API_KEY="AIzaSyDQqg59SZxTMEZ9tabm4OPO72PfNJ14zBM"
MODEL_ID="models/imagen-3.0-generate-002"
IMAGE_PATH="/Users/macbookpro/Pictures"
IMAGE_FILE="photorrealistic-stock-photograpy-new-version.webp"
DOWNLOAD_URL="https://storage.googleapis.com/media-topfinanzas-com/images/generated/activecampaign-broadcasts"

cd "$IMAGE_PATH"

cat <<EOF >request.json
{
    "instances": [
        {
            "prompt": "Create a photorealistic 4k professional stock photography illustration related to discovering financial offers. The image should show a person's hand interacting with a futuristic, transparent digital interface displaying abstract representations of financial products (e.g., glowing card shapes, upward-trending graphs). The background should be a clean, modern, slightly blurred office or home setting, with high-quality lighting and a professional, optimistic feel. The composition should be horizontal and suitable for email marketing."
        }
    ],
    "parameters": {
        "sampleCount": 1,
        "personGeneration": "ALLOW_ADULT",
        "aspectRatio": "16:9",
    }
}
EOF

# Store the full response from curl.
# Added -sS for silent operation (no progress meter) but to show errors if curl itself fails.
API_RESPONSE=$(
    curl \
        -X POST \
        -H "Content-Type: application/json" \
        -sS \
        "https://generativelanguage.googleapis.com/v1beta/${MODEL_ID}:predict?key=${GEMINI_API_KEY}" -d '@request.json'
)

# Process each prediction:
# 1. Use jq to extract all 'bytesBase64Encoded' strings from the 'predictions' array.
#    The '.predictions[]?.bytesBase64Encoded' path gets each string.
#    The '[]' iterates over the array.
#    The '?' makes it safe if 'predictions' is null or an item lacks 'bytesBase64Encoded'.
# 2. Pipe each Base64 string to a while loop.
echo "$API_RESPONSE" | jq -r '.predictions[]?.bytesBase64Encoded' | while IFS= read -r b64_data; do
    # Increment image counter for unique filenames
    image_count=$((image_count + 1))

    # Check if b64_data is actually null (as a string from jq) or empty
    if [ "$b64_data" = "null" ] || [ -z "$b64_data" ]; then
        echo # Add a newline for spacing
        echo "----------------------------------------"
        echo "WARNING: Skipping image $image_count"
        echo "Reason: Missing or null Base64 data."
        echo "----------------------------------------"
        echo     # Add a newline for spacing
        continue # Skip to the next iteration
    fi

    # Decode the Base64 string and save it to a uniquely named file
    echo "$b64_data" | base64 --decode >"${IMAGE_FILE}"
    if [ $? -eq 0 ]; then
        echo # Add a newline for spacing
        echo "----------------------------------------"
        echo "SUCCESS: The image ${IMAGE_FILE} was successfully generated."
        echo "----------------------------------------"
        echo "Saved to local path: ${IMAGE_PATH}/${IMAGE_FILE}"

        gcloud storage cp ${IMAGE_PATH}/${IMAGE_FILE} gs://media-topfinanzas-com/images/generated/activecampaign-broadcasts
        if [ $? -ne 0 ]; then
            echo # Add a newline for spacing
            echo "----------------------------------------"
            echo "ERROR: Failed to upload the image ${IMAGE_FILE} to Google Cloud Storage."
            echo "----------------------------------------"
            continue # Skip to the next iteration
        fi
        echo # Add a newline for spacing
        echo "----------------------------------------"
        echo "SUCCESS: The image ${IMAGE_FILE} was successfully uploaded to Google Cloud Storage."
        echo "----------------------------------------"
        echo "${DOWNLOAD_URL}/${IMAGE_FILE}"
        echo # Add a newline for spacing

        echo "Downloading the image '${IMAGE_FILE}' from Google Cloud Storage..."
        echo
        echo "Destination: ${IMAGE_PATH}/${IMAGE_FILE}"

        curl -O "${DOWNLOAD_URL}/${IMAGE_FILE}"
        echo
        echo "----------------------------------------"
        echo "SUCCESS: The image ${IMAGE_FILE} was successfully downloaded."
        echo "----------------------------------------"
        echo # Add a newline for spacing

    else
        # This error might occur if b64_data is invalid or disk is full, etc.
        echo # Add a newline for spacing
        echo "----------------------------------------"
        echo "ERROR: Image ${IMAGE_FILE}"
        echo "Reason: Failed to decode or save."
        echo "----------------------------------------"
        echo # Add a newline for spacing
    fi
done
