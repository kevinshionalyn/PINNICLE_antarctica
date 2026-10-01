# PINNICLE Antarctica Data Product

A **mesh‑free, physics‑informed neural‑network (PINN) representation** of the Antarctic ice sheet, produced with the open‑source model **[PINNICLE][pinnicle‑repo]**.

[pinnicle‑repo]: https://github.com/ISSMteam/PINNICLE

---  
## How to script the data (Python)

The repository ships a **tiny pure‑Python client** (`client/`) that lets you fetch the data product directly from the static GitHub Pages site.  
Two usage patterns are supported:

| Mode | What you get | When to use it |
|------|--------------|----------------|
| **Mesh‑free (default)** | `antarctica.pt` – the raw Torch tensor that contains the PINN solution on a continuous (mesh‑free) domain. | Most users who want to interpolate on‑the‑fly or re‑grid the data themselves. |
| **Pre‑meshed** | A regular/structured mesh file (e.g., NetCDF, CSV, or ISSM `.exp`) that has already been generated from the mesh‑free tensor. | If you prefer to drop the data straight into a downstream model (ISSM, Elmer, etc.) without writing your own interpolation code. |

Below are the minimal commands for each case. All of them work with **just the client package** – you only need `torch` if you want to read the tensor in Python.

---

### Install the client (once)

```bash
# Clone the repo (if you haven’t already)
git clone https://github.com/kevinshionalyn/PINNICLE_antarctica.git
cd PINNICLE_antarctica

# Optional – create an isolated environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install the client in editable mode
pip install -e .

### Download mesh-free tensor (default)
>>> from client.download import download_pt, load_tensor
>>> pt_path = download_pt()          # saves ./antarctica.pt
>>> print("Tensor file saved at:", pt_path)

# If you also want the tensor as a torch.Tensor object:
>>> tensor = load_tensor()           # will call download_pt() automatically
>>> print(tensor.shape)              # e.g. torch.Size([N, 2])

### Download with chosen mesh
>>> from client.download import download_pt, generate_mesh
>>> # 1️⃣  Make sure the raw tensor is available (download_pt() does that)
>>> pt_path = download_pt()

>>> # 2️⃣  Generate a regular lat‑lon‑depth mesh
>>> mesh_file = generate_mesh(
...     pt_path=pt_path,
...     lon_range = (-180, 180),      # degrees
...     lat_range = (-90,   0),       # degrees
...     depth_range = (0, 3000),      # meters (positive down)
...     lon_step   = 0.5,             # grid spacing in degrees
...     lat_step   = 0.5,
...     depth_step = 100,
...     fmt = "netcdf",               # can be "netcdf", "csv", or "json"
... )
>>> print("Mesh file written to:", mesh_file)


## Data sources used  

- Bed elevation: BedMachine + xOPR
- Surface velocity: NASA MEaSUREs 
- 
