"""Test loading all pattern modules"""

import sys
from pathlib import Path
import importlib.util

base_path = Path(__file__).parent

patterns = [
    ("Decorator", "src/structural/decorator/main.py"),
    ("Observer", "src/behavioral/observer/main.py"),
    ("State", "src/behavioral/state/main.py"),
    ("Adapter", "src/structural/adapter/main.py"),
    ("Facade", "src/structural/facade/main.py"),
]

print("\nTesting pattern module loading...\n")

for pattern_name, module_path in patterns:
    try:
        # Add pattern directory to path
        pattern_dir = (base_path / module_path).parent
        if str(pattern_dir) not in sys.path:
            sys.path.insert(0, str(pattern_dir))

        # Load module
        spec = importlib.util.spec_from_file_location(
            f"{pattern_name.lower()}_main",
            base_path / module_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        print(f"✓ {pattern_name:12} - OK - {module.app.title}")
    except Exception as e:
        print(f"✗ {pattern_name:12} - FAILED: {e}")

print("\nDone!")
