# PINNICLE Antarctica Data Product

A **mesh‑free, physics‑informed neural‑network (PINN) representation** of the Antarctic ice sheet, produced with the open‑source model **[PINNICLE][pinnicle‑repo]**.

[pinnicle‑repo]: https://github.com/ISSMteam/PINNICLE

---

## 📥 How to script the data (Python)

The repository ships a **tiny pure‑Python client** (`client/`) that lets you fetch the data product directly from the static GitHub Pages site.  
Two usage patterns are supported:

| Mode                | What you get |
|---------------------|--------------|
| **Mesh‑free (default)** | `antarctica_pinn_mosaic.pt` – the raw Torch tensor that contains the PINN solution on a continuous (mesh‑free) domain. |
| **Custom mesh** | A regular/structured mesh file (NetCDF, CSV, or ISSM `.exp`) that is **generated on‑the‑fly** from the mesh‑free tensor. |

All commands work with the client package alone; you only need `torch` if you want to read the tensor in Python.

---

### 1️⃣ Install the client (once)

```bash
# Clone the repo (if you haven’t already)
git clone https://github.com/kevinshionalyn/PINNICLE_antarctica.git
cd PINNICLE_antarctica

# Optional – create an isolated environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install the client in editable mode (adds `pinnicle-antarctica` CLI as well)
pip install -e 

## Example (python): download mesh-free tensor
>>> from client.download import download_pt, load_tensor
>>> pt_path = download_pt()                # saves ./antarctica_pinn_mosaic.pt
>>> print("Tensor file saved at:", pt_path)

# If you also want the tensor as a torch.Tensor object:
>>> tensor = load_tensor()                 # will call download_pt() automatically
>>> print(tensor.shape)                    # e.g. torch.Size([N, 2])

## Example (python): generate a custom mesh
>>> from client.download import download_pt, generate_mesh
>>> # 1️⃣  Make sure the raw tensor is present
>>> pt_path = download_pt()

>>> # 2️⃣  Create a regular lat‑lon‑depth grid and write it to a file
>>> mesh_file = generate_mesh(
...     pt_path    = pt_path,
...     lon_range  = (-180, 180),   # degrees
...     lat_range  = (-90,   0),    # degrees
...     depth_range= (0, 3000),     # meters (positive down)
...     lon_step   = 0.5,           # grid spacing in degrees
...     lat_step   = 0.5,
...     depth_step = 100,
...     fmt        = "netcdf"      # "netcdf", "csv", or "json"
... )
>>> print("Mesh file written to:", mesh_file)

## Example (terminal with python): generate a custom mesh
# The `pinnicle-antarctica` command is available after `pip install -e .`
pinnicle-antarctica mesh \
    --lon-step 0.5 --lat-step 0.5 --depth-step 100 \
    --format netcdf \
    --output my_antarctica_mesh.nc

## Example (terminal): generate a custom mesh
curl -s https://raw.githubusercontent.com/kevinshionalyn/PINNICLE_antarctica/main/client/mesh_cli.py | \
python3 - \
    --lon-step 0.5 --lat-step 0.5 --depth-step 100 \
    --format netcdf \
    --output my_antarctica_mesh.nc

## Example (MATLAB): generate a custom mesh
### 🛠️ MATLAB users – generate a custom mesh without writing Python

The repository includes a tiny MATLAB wrapper (`matlab_generate_mesh.m`) that calls the same Python code used by the CLI.  
All you need is **MATLAB R2019b or newer** and a **working Python installation** (the same one you used for the CLI).

#### 3.1  Download the MATLAB helper

```matlab
% This will place `matlab_generate_mesh.m` in your current folder
url = 'https://kevinshionalyn.github.io/PINNICLE_antarctica/client/matlab/matlab_generate_mesh.m';
websave('matlab_generate_mesh.m', url);


## Licencse
This data product is released under the MIT License. Feel free to use for research and teaching purposes.

