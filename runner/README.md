# Runner Image

This is a minimal Docker image used for sandboxed execution of student code.

## Features

- Minimal Python 3.11 with only pytest installed
- Non-root user (sandbox)
- No additional packages or network access
- Used by worker to execute tests in isolation

## Building

```bash
docker build -t py-playground-runner:latest .
```

## Security Measures

When run by the worker, additional constraints are applied:
- `--network none` - No network access
- `--read-only` - Filesystem is read-only
- `--tmpfs /tmp` - Temporary writable space
- `--cpus` and `--memory` limits
- Timeout enforcement
