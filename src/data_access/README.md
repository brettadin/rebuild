# src/data_access/

Providers for both external archives and local file importers. This directory should contain provider clients, parsers, and caching/mapper utilities.

Suggested subdirectories:
- `providers/` — per-provider clients/parsers (e.g., nist, hitran, mast, pds, eso, local)
- `cache/` — on-disk cache logic
- `mappers/` — mapping provider responses to domain models

Follow the `Rebuild_Architecture.md` for implementation guidance.