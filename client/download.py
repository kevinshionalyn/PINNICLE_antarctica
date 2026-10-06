import pathlib
import urllib.request
import json
from typing import Union

# Note: Capitalization must match the GitHub repo name exactly (PINNICLE_antarctica)
GITHUB_PAGES_BASE = "https://kevinshionalyn.github.io/PINNICLE_antarctica"

def _url_for(path: str) -> str:
    """Return the absolute URL for a file stored under the static site root."""
    return f"{GITHUB_PAGES_BASE}/{path.lstrip('/')}"

def _fetch_file(url: str, dest: pathlib.Path) -> None:
    """Helper to download a remote URL to a local path with custom headers."""
    req = urllib.request.Request(
        url, 
        headers={"User-Agent": "pinnicle-antarctica-client/1.0"}
    )
    with urllib.request.urlopen(req) as response, open(dest, "wb") as out_file:
        out_file.write(response.read())

def download_pt(dest: Union[str, pathlib.Path] = "antarctica_pinn_mosaic.pt") -> pathlib.Path:
    """
    Download the binary tensor (antarctica_pinn_mosaic.pt) from GitHub Pages.

    Parameters
    ----------
    dest : str or pathlib.Path, optional
        Local path where the file should be written. Default ``antarctica_pinn_mosaic.pt`` in cwd.

    Returns
    -------
    pathlib.Path
        Path object pointing to the downloaded file.
    """
    dest = pathlib.Path(dest)
    url = _url_for("data/antarctica_pinn_mosaic.pt")
    dest.parent.mkdir(parents=True, exist_ok=True)
    _fetch_file(url, dest)
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
    _fetch_file(url, dest)
    return dest

# ----------------------------------------------------------------------
# Helper to load the tensor directly with torch (optional convenience)
# ----------------------------------------------------------------------
def load_tensor(pt_path: Union[str, pathlib.Path] = None):
    """
    Load the downloaded ``antarctica_pinn_mosaic.pt`` file with ``torch.load``.
    If ``pt_path`` is None, the function will first call ``download_pt()``.
    """
    import torch
    if pt_path is None:
        pt_path = download_pt()
    return torch.load(pt_path, map_location="cpu", weights_only=True)
