#!/bin/bash
set -e -E

GEMINI_API_KEY="AIzaSyDQqg59SZxTMEZ9tabm4OPO72PfNJ14zBM"
MODEL_ID="models/imagen-3.0-generate-002"
IMAGE_PATH="/Users/macbookpro/Pictures"
IMAGE_FILE="photorrealistic-stock-photograpy-COMPRESSED.webp"
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
        "mime_type": "image/webp"
    }
}
EOF

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

        # --- BEGIN COMPRESSION MODIFICATION ---
        COMPRESSED_IMAGE_FILE="compressed_${IMAGE_FILE}"
        echo
        echo "Attempting to compress ${IMAGE_FILE}..."
        if magick "${IMAGE_PATH}/${IMAGE_FILE}" -quality 80 "${IMAGE_PATH}/${COMPRESSED_IMAGE_FILE}"; then
            echo "Compression successful."
            # Optional: Get sizes for comparison
            original_size=$(stat -f%z "${IMAGE_PATH}/${IMAGE_FILE}")
            compressed_size=$(stat -f%z "${IMAGE_PATH}/${COMPRESSED_IMAGE_FILE}")
            echo "Original size: $original_size bytes. Compressed size: $compressed_size bytes."

            # Replace original with compressed file
            mv "${IMAGE_PATH}/${COMPRESSED_IMAGE_FILE}" "${IMAGE_PATH}/${IMAGE_FILE}"
            echo "Replaced original with compressed version: ${IMAGE_PATH}/${IMAGE_FILE}"
        else
            echo "WARNING: Compression failed for ${IMAGE_FILE}. Using the original image."
            # Ensure compressed file is removed if it exists and failed
            rm -f "${IMAGE_PATH}/${COMPRESSED_IMAGE_FILE}"
        fi
        echo "----------------------------------------"
        # --- END COMPRESSION MODIFICATION ---

        gcloud storage cp ${IMAGE_PATH}/${IMAGE_FILE} gs://media-topfinanzas-com/images/generated/activecampaign-broadcasts
        if [ $? -ne 0 ]; then
            echo
            echo "----------------------------------------"
            echo "ERROR: Failed to upload the image ${IMAGE_FILE} to Google Cloud Storage."
            echo "----------------------------------------"
            continue
        fi
        echo
        echo "----------------------------------------"
        echo
        echo "SUCCESS: The image ${IMAGE_FILE} was successfully uploaded to Google Cloud Storage."
        echo
        echo "${DOWNLOAD_URL}/${IMAGE_FILE}"
        echo
        echo "----------------------------------------"
        echo

        echo "Downloading the image '${IMAGE_FILE}' from Google Cloud Storage..."
        echo
        echo "Destination: ${IMAGE_PATH}/${IMAGE_FILE}"

        curl -O "${DOWNLOAD_URL}/${IMAGE_FILE}"
        echo
        echo "----------------------------------------"
        echo "SUCCESS: The image ${IMAGE_FILE} was successfully downloaded."
        echo "----------------------------------------"
        echo

    else
        echo
        echo "----------------------------------------"
        echo "ERROR: Image ${IMAGE_FILE}"
        echo "Reason: Failed to decode or save."
        echo "----------------------------------------"
        echo
    fi
done
