import pathlib
import urllib.request
import json
from typing import Union

# ----------------------------------------------------------------------
# IMPORTANT: make sure this placeholder is the **actual GitHub Pages URL**
# after Pages is enabled (see step 8).  Example:
#   GITHUB_PAGES_BASE = "https://your-github-user.github.io/pinnicle-antarctica-data"
# ----------------------------------------------------------------------
GITHUB_PAGES_BASE = "https://kevinshionalyn.github.io/pinnicle_antarctica"

def _url_for(path: str) -> str:
    """Return the absolute URL for a file stored under the `data/` folder."""
    # GitHub Pages serves the repo root as static files, so we just concatenate
    return f"{GITHUB_PAGES_BASE}/{path.lstrip('/')}"

def download_pt(dest: Union[str, pathlib.Path] = "antarctica_pinn_mosaic.pt") -> pathlib.Path:
    """
    Download the binary tensor (antarctica_pinn_mosaic.pt) from GitHub Pages.

    Parameters
    ----------
    dest : str or pathlib.Path, optional
        Local path where the file should be written.  Default ``antarctica_pinn_mosaic.pt`` in cwd.

    Returns
    -------
    pathlib.Path
        Path object pointing to the downloaded file.
    """
    dest = pathlib.Path(dest)
    url = _url_for("data/antarctica_pinn_mosaic.pt")
    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)
    return dest

def download_json(dest: Union[str, pathlib.Path] = "param.json") -> pathlib.Path:
    """
    Download the `param.json` descriptor from GitHub Pages.

    Parameters
    ----------
    dest : str or pathlib.Path, optional
        Destination filename. Default ``param.json`` in cwd.

    Returns
    -------
    pathlib.Path
        Path object pointing to the downloaded JSON file.
    """
    dest = pathlib.Path(dest)
    url = _url_for("data/param.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)
    return dest

# ----------------------------------------------------------------------
# Helper to load the tensor directly with torch (optional convenience)
# ----------------------------------------------------------------------
def load_tensor(pt_path: Union[str, pathlib.Path] = None):
    """
    Load the downloaded ``antarctica.pt`` file with ``torch.load``.
    If ``pt_path`` is None, the function will first call ``download_pt()``.
    """
    import torch
    if pt_path is None:
        pt_path = download_pt()
    return torch.load(pt_path, map_location="cpu")
