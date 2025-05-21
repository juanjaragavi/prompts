#!/bin/bash
set -e -E

GEMINI_API_KEY="AIzaSyDQqg59SZxTMEZ9tabm4OPO72PfNJ14zBM"
MODEL_ID="models/imagen-3.0-generate-002"
IMAGE_PATH="/var/lib/n8n/activecampaign-broadcasts/images/generated"
IMAGE_FILE="photorrealistic-stock-photograpy.webp"
DOWNLOAD_URL="https://static.topfinanzas.com"

cd "$IMAGE_PATH"

API_RESPONSE=$(
    curl \
        -X POST \
        -H "Content-Type: application/json" \
        -sS \
        "https://generativelanguage.googleapis.com/v1beta/${MODEL_ID}:predict?key=${GEMINI_API_KEY}" -d '@request.json'
)

echo "$API_RESPONSE" | jq -r '.predictions[]?.bytesBase64Encoded' | while IFS= read -r b64_data; do

    if [ "$b64_data" = "null" ] || [ -z "$b64_data" ]; then
        echo
        echo "----------------------------------------"
        echo "WARNING: Skipping image $image_count"
        echo "Reason: Missing or null Base64 data."
        echo "----------------------------------------"
        echo
        continue
    fi

    echo "$b64_data" | base64 --decode >"${IMAGE_FILE}"
    if [ $? -eq 0 ]; then
        echo
        echo "----------------------------------------"
        echo "SUCCESS: The image ${IMAGE_FILE} was successfully generated."
        echo "----------------------------------------"
        echo "Saved to local path: ${IMAGE_PATH}/${IMAGE_FILE}"
        echo "----------------------------------------"
        echo "Download URL: ${DOWNLOAD_URL}/${IMAGE_FILE}"

    else
        echo
        echo "----------------------------------------"
        echo "ERROR: Image ${IMAGE_FILE}"
        echo "Reason: Failed to decode or save."
        echo "----------------------------------------"
        echo
    fi
done
