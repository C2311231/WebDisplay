import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any, Dict


class JSONStore:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _module_path(self, module_name: str) -> Path:
        if not re.match(r'^[a-zA-Z0-9_.-]+$', module_name):
            raise ValueError(f"Invalid module name: {module_name}")
        return self.base_path / f"{module_name}.json"

    def get_module(self, module_name: str, default: Dict[str, Any] | None = None) -> tuple[Dict[str, Any], bool]:
        """
        Load a module JSON file.
        If it does not exist, create it with the provided default and return true as well otherwise it will return the module and false.
        """
        path = self._module_path(module_name)

        if not path.exists():
            data = default if default is not None else {}
            self._atomic_write(path, data)
            return data, True

        with path.open("r", encoding="utf-8") as f:
            return json.load(f), False

    def save_module(self, module_name: str, data: Dict[str, Any]) -> None:
        """
        Atomically write JSON data for a module.
        """
        path = self._module_path(module_name)
        self._atomic_write(path, data)

    def delete_module(self, module_name: str) -> None:
        path = self._module_path(module_name)
        if path.exists():
            path.unlink()

    def list_modules(self) -> list[str]:
        return [p.stem for p in self.base_path.glob("*.json")]

    def _atomic_write(self, path: Path, data: Dict[str, Any]) -> None:
        """
        Write JSON safely using:
        1. Temporary file in same directory
        2. Flush + fsync
        3. Atomic replace
        """
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            delete=False
        ) as tmp:
            json.dump(data, tmp, indent=2)
            tmp.flush()
            os.fsync(tmp.fileno())
            temp_name = tmp.name

        os.replace(temp_name, path)
