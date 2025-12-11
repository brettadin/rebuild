# config/

Top-level configuration. Should include:
- `app_config.yaml` (application settings)
- `providers.yaml` (enabled providers, endpoints, timeouts, keys)
- `logging.yaml` (logging settings)

Do not store production API keys directly in the repo; use secrets or an external key store.