# PINNICLE Antarctica Data Product

A mesh-free, physics-informed neural network (PINN) representation of the Antarctic ice sheet generated using the open-source **[PINNICLE](https://github.com/ISSMteam/PINNICLE)** model.

---

## Basic Data Information

* **Raw Data Product**: A continuous, mesh-free model output stored as a PyTorch tensor (`antarctica_pinn_mosaic.pt`).
* **Custom Grids**: Interpolated spatial products (NetCDF, CSV, or JSON) generated across custom ranges and resolutions (longitude, latitude, depth).
* **Coordinate Reference System**: WGS 84 / Antarctic Polar Stereographic (EPSG:3031)  
* Model Information
    * Data sources: velocity, ....


---

## Installation

### Mesh-free product
```bash
# Ensure Git LFS is installed
git lfs install
# clone repository
git clone https://github.com/kevinshionalyn/PINNICLE_antarctica.git
cd PINNICLE_antarctica
pip install -e .
```

Python: custom mesh product (requires Python 3.8+ and PyTorch) 
```python
from client.mesh_cli import generate_mesh

# Interpolate continuous PINN tensor onto a structured NetCDF grid
mesh_file = generate_mesh(
    pt_path="data/antarctica_pinn_mosaic.pt",
    x_range=(-2670000, 3010000),   # EPSG:3031 Easting (m)
    y_range=(-2310000, 2570000),   # EPSG:3031 Northing (m)
    x_step=5000,                   # 5 km spacing
    fmt="netcdf",                  # "netcdf", "csv", or "json"
    output="antarctica_mesh.nc"
)
print(f"Mesh file written to: {mesh_file}")
```

## 2. Command line
Using curl (mesh-free):
```bash
curl -L -O https://kevinshionalyn.github.io/PINNICLE_antarctica/data/antarctica_pinn_mosaic.pt)
```
Using wget (mesh-free):
```bash
wget --no-check-certificate https://kevinshionalyn.github.io/PINNICLE_antarctica/data/antarctica_pinn_mosaic.pt
```

curl (custom-mesh):
```bash
curl -sL https://raw.githubusercontent.com/kevinshionalyn/PINNICLE_antarctica/main/client/mesh_cli.py | \
python3 - \
    --x-step 5000 --y-step 5000 \
    --format netcdf \
    --output antarctica_issm_grid.nc
```

CLI command (custom-mesh):
```bash
curl -sL https://raw.githubusercontent.com/kevinshionalyn/PINNICLE_antarctica/main/client/mesh_cli.py | \
python3 - \
    --x-step 5000 --y-step 5000 \
    --format netcdf \
    --output antarctica_issm_grid.nc
```



### MATLAB

#### Setup MATLAB Helper Script
```matlab
% Fetch the MATLAB grid generation helper
url = 'https://kevinshionalyn.github.io/PINNICLE_antarctica/client/matlab/matlab_generate_mesh.m';
websave('matlab_generate_mesh.m', url);
```

Mesh-free product
```matlab
% Download raw tensor file (only if not already present from git clone)
if ~exist('data/antarctica_pinn_mosaic.pt', 'file')
    url = 'https://kevinshionalyn.github.io/PINNICLE_antarctica/data/antarctica_pinn_mosaic.pt';
    websave('data/antarctica_pinn_mosaic.pt', url);
end
```

Custom Mesh Product
```matlab
% Define EPSG:3031 grid specifications (meters) for ISSM workflows
opts = struct(...
    'x_range', [-2670000, 3010000], ... % Easting (m)
    'y_range', [-2310000, 2570000], ... % Northing (m)
    'x_step', 5000, ...                 % 5 km spacing
    'y_step', 5000, ...                 % 5 km spacing
    'format', 'netcdf', ...             % 'netcdf', 'csv', or 'json'
    'output', 'antarctica_issm_grid.nc' ...
);

matlab_generate_mesh('data/antarctica_pinn_mosaic.pt', opts);
```

## License information
This data product and associated files are released for free use under the MIT License.
