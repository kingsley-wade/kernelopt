from pathlib import Path
import os

class DeviceLock:
    """Small process lock used to serialize measurements on one device."""
    def __init__(self, path): self.path=Path(path); self.fd=None
    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fd=os.open(self.path, os.O_CREAT|os.O_EXCL|os.O_WRONLY)
        return self
    def __exit__(self, exc_type, exc, tb):
        if self.fd is not None: os.close(self.fd); self.fd=None
        try: self.path.unlink()
        except FileNotFoundError: pass
