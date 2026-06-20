"""CI Test runner to execute all Jupyter notebooks headlessly and check for errors."""
import json
import sys
import os
import types
from pathlib import Path

def run_notebook(nb_path: Path) -> bool:
    print(f"\n=========================================")
    print(f"Executing: {nb_path.relative_to(Path.cwd())}")
    print(f"=========================================")
    
    with open(nb_path, "r", encoding="utf-8") as f:
        nb_data = json.load(f)
        
    # Set up headless matplotlib and mock GUI operations
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.show = lambda *args, **kwargs: None
    
    import cv2
    cv2.waitKey = lambda *args, **kwargs: ord('q')
    cv2.destroyAllWindows = lambda *args, **kwargs: None
    cv2.imshow = lambda *args, **kwargs: None
    
    # Pre-mock ipywidgets so Aula 5 interact() calls are no-ops in headless mode.
    _widgets_mock = types.ModuleType("ipywidgets")
    _widgets_mock.interact = lambda f, **kw: f(**{k: v.value if hasattr(v, "value") else v for k, v in kw.items()})
    _widgets_mock.Dropdown = lambda **kw: types.SimpleNamespace(value=kw.get("options", [None])[0])
    sys.modules.setdefault("ipywidgets", _widgets_mock)

    # Track notebook state in a dedicated namespace
    namespace = {
        "__file__": str(nb_path),
        "__name__": "__main__",
        "CI": True,   # notebooks can gate interactive-only code: if not globals().get("CI")
    }
    
    # Temporarily switch working directory to the notebook's folder
    # so relative paths to inputs/outputs resolve correctly.
    old_cwd = os.getcwd()
    os.chdir(nb_path.parent)
    
    try:
        cell_idx = 0
        for cell in nb_data.get("cells", []):
            if cell.get("cell_type") == "code":
                cell_idx += 1
                source = "".join(cell.get("source", []))
                # Skip blank cells
                if not source.strip():
                    continue
                try:
                    exec(source, namespace)
                except Exception as e:
                    print(f"\n[ERROR] Cell {cell_idx} failed:")
                    print("-" * 40)
                    print(source)
                    print("-" * 40)
                    print(f"Exception: {e}")
                    return False
        print(f"[OK] Notebook executed successfully.")
        return True
    finally:
        os.chdir(old_cwd)

def main():
    repo_root = Path(__file__).resolve().parents[1]
    experiment_dir = repo_root / "experiment"
    
    if not experiment_dir.exists():
        print(f"[WARN] Experiment folder not found at {experiment_dir} — skipping.")
        sys.exit(0)
        
    notebooks = sorted(list(experiment_dir.glob("**/notebook.ipynb")))
    if not notebooks:
        print("[WARN] No notebooks found to test.")
        sys.exit(0)
        
    print(f"Found {len(notebooks)} notebook(s) to validate.")
    
    success = True
    for nb in notebooks:
        if not run_notebook(nb):
            success = False
            
    if not success:
        print("\n[FAIL] One or more notebooks failed execution.")
        sys.exit(1)
        
    print("\n[SUCCESS] All notebooks executed without errors.")
    sys.exit(0)

if __name__ == "__main__":
    main()
