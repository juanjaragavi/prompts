#!/bin/bash
set -e -E

GEMINI_API_KEY="AIzaSyDQqg59SZxTMEZ9tabm4OPO72PfNJ14zBM"
MODEL_ID="models/imagen-3.0-generate-002"

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
        echo "WARNING: Skipping image"
        echo "Reason: Missing or null Base64 data."
        echo "----------------------------------------"
        echo
        continue
    fi

    echo "$b64_data" | base64 --decode >"generated_image.webp"
    if [ $? -eq 0 ]; then
        echo
        echo "----------------------------------------"
        echo "SUCCESS: Image generated_image.webp"
        echo "----------------------------------------"
        echo "Saved to local path: generated_image.webp"

        sudo gcloud storage cp generated_image.webp gs://media-topfinanzas-com/images/generated/activecampaign-broadcasts

        echo "Uploaded to Google Cloud Storage:"
        echo "https://storage.googleapis.com/media-topfinanzas-com/images/generated/activecampaign-broadcasts/generated_image.webp"
        echo

        sleep 1

        echo "Downloading the image 'generated_image.webp' from Google Cloud Storage..."
        echo "Destination: generated_image.webp"

        sudo curl -O "https://storage.googleapis.com/media-topfinanzas-com/images/generated/activecampaign-broadcasts/generated_image.webp"
        echo "Download complete."
        echo "----------------------------------------"
        echo

    else
        echo
        echo "----------------------------------------"
        echo "ERROR: Image generated_image.webp"
        echo "Reason: Failed to decode or save."
        echo "----------------------------------------"
        echo
    fi
done
