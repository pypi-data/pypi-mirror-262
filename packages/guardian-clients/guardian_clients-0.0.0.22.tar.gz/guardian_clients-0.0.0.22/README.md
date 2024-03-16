# TODO

# Testing client with Auth - TODO this is draft

```
export GUARDIAN_SCANNER_CLIENT_ID=guardian-sdk
export GUARDIAN_SCANNER_CLIENT_SECRET=
export GUARDIAN_SCANNER_OIDP_TOKEN_ENDPOINT=https://auth.dev.radar.protectai.com/realms/radar-unstable/protocol/openid-connect/token
export GUARDIAN_SCANNER_ENDPOINT=https://scanner.dev.protectai.local
export SCAN_TARGET_LOCATION=s3://guardian.protectai

python clients/python/guardian.py http://localhost:8000 s3://ml-pipeline-storage/mlflow/143466328962531796/67277e75e29a49c3a723180de76c712c/ --threshold high --log-level info || echo $?
```