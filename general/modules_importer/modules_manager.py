import importlib
import sys
import os
import traceback
from typing import List, Optional
from types import ModuleType


class ModulesManager:
    @staticmethod
    def import_custom_module(module_path: str) -> Optional[ModuleType]:
        """
        Import a single module by path. Reload if already imported.
        """
        try:
            if module_path in sys.modules:
                return importlib.reload(sys.modules[module_path])
            return importlib.import_module(module_path)
        except Exception as e:
            print(f"[Error] Failed to import module '{module_path}': {e}")
            traceback.print_exc()
            return None

    @staticmethod
    def import_modules_from_folder(root_path: str, subfolder: str, prefix: str = "") -> List[ModuleType]:
        """
        Dynamically import all .py modules in a given subfolder.
        - root_path: Absolute project root path.
        - subfolder: Relative subfolder (e.g., "launch", "tools").
        - prefix: Import path prefix (e.g., "launch", "tools.ui").
        """
        modules: List[ModuleType] = []
        folder_path = os.path.join(root_path, subfolder)

        if not os.path.isdir(folder_path):
            print(f"[Warning] Folder not found: {folder_path}")
            return modules

        for filename in os.listdir(folder_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                import_path = f"{prefix}.{module_name}" if prefix else module_name
                imported = ModulesManager.import_custom_module(import_path)
                if imported:
                    modules.append(imported)

        return modules