cat << EOF > request.json
{
    "endpoint": "projects/absolute-brook-452020-d5/locations/us-central1/publishers/google/models/imagen-4.0-generate-001",
    "instances": [
        {
            "prompt": "Generate an ultra-realistic stock image of a cheerful and confident person in their late 20s or early 30s, sitting at a clean, modern desk with a laptop. They are holding a credit card and smiling as they look at the camera, conveying a sense of financial empowerment and satisfaction. The lighting is bright and natural. Generate the image with a 16:9 aspect ratio.",
        }
    ],
    "parameters": {
        "aspectRatio": "16:9",
        "sampleCount": 1,
        "negativePrompt": "",
        "enhancePrompt": false,
        "personGeneration": "allow_all",
        "safetySetting": "block_few",
        "addWatermark": true,
        "includeRaiReason": true,
        "language": "auto"
    }
}
EOF

PROJECT_ID="absolute-brook-452020-d5"
LOCATION_ID="us-central1"
API_ENDPOINT="us-central1-aiplatform.googleapis.com"
MODEL_ID="imagen-4.0-generate-001"

curl \
-X POST \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
"https://${API_ENDPOINT}/v1/projects/${PROJECT_ID}/locations/${LOCATION_ID}/publishers/google/models/${MODEL_ID}:predict" -d '@request.json'