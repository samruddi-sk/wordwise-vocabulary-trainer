#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Checking backend..."
curl -fsS http://localhost:8000/openapi.json -o /dev/null

echo "Generating Python SDK..."

JAR="./openapi-generator-cli-7.17.0.jar"

if [ ! -f "$JAR" ]; then
    echo "Error: OpenAPI Generator JAR not found at $JAR"
    exit 1
fi

java -jar "$JAR" generate \
    -i http://localhost:8000/openapi.json \
    -g python \
    -o srs_sdk \
    --additional-properties=packageName=srs_sdk,projectName=srs-sdk

echo "SDK generation completed successfully!"
