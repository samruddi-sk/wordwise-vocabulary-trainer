@echo off
setlocal
cd /d "%~dp0"
echo Make sure the backend is running at http://localhost:8000 before continuing.
where openapi-generator-cli >nul 2>nul
if errorlevel 1 (
  echo Install the CLI first: npm install -g @openapitools/openapi-generator-cli
  exit /b 1
)
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o srs_sdk --additional-properties=packageName=srs_sdk,projectName=srs-sdk
