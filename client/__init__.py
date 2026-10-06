"""
pinnicle_antarctica_data.client
--------------------------------
Very small helper that knows how to fetch the data product from the
GitHub Pages site of this repository.
"""

from .download import download_pt, download_json

__all__ = ["download_pt", "download_json", "load_tensor"]

from client.mesh_cli import generate_mesh
