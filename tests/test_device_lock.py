import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
from kernel_opt.device_lock import DeviceLock
class T(unittest.TestCase):
    def test_serializes_device(self):
        p=Path(tempfile.gettempdir())/'kernel-opt-device.lock'
        try:
            with DeviceLock(p):
                with self.assertRaises(FileExistsError):
                    with DeviceLock(p): pass
        finally:
            if p.exists(): p.unlink()
