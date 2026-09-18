## Verification Steps

After restarting, run:

```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8384/
```

This should output `200`.

If the command fails, open the Syncthing Web UI via `open_preview url="http://127.0.0.1:8384/" label="Syncthing Web UI"` in Hermes.