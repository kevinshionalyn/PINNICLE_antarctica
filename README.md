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
Using curl:
```bash
curl -L -O https://kevinshionalyn.github.io/PINNICLE_antarctica/data/antarctica_pinn_mosaic.pt)
```
Using wget:
```bash
wget --no-check-certificate https://kevinshionalyn.github.io/PINNICLE_antarctica/data/antarctica_pinn_mosaic.pt
```

Custom mesh product
```bash
curl -s [https://raw.githubusercontent.com/kevinshionalyn/PINNICLE_antarctica/main/client/mesh_cli.py](https://raw.githubusercontent.com/kevinshionalyn/PINNICLE_antarctica/main/client/mesh_cli.py) | \
python3 - \
    --lon-step {choose_lon} --lat-step {choose_lat} --depth-step {choose-depth} \
    --format netcdf \
    --output my_antarctica_mesh.nc
```

## 3. MATLAB
```matlab
url = '[https://kevinshionalyn.github.io/PINNICLE_antarctica/client/matlab/matlab_generate_mesh.m](https://kevinshionalyn.github.io/PINNICLE_antarctica/client/matlab/matlab_generate_mesh.m)';
websave('matlab_generate_mesh.m', url);
```

Mesh-free product
```matlab
% Download the raw PyTorch model file directly to current folder
url = '[https://kevinshionalyn.github.io/PINNICLE_antarctica/data/antarctica_pinn_mosaic.pt](https://kevinshionalyn.github.io/PINNICLE_antarctica/data/antarctica_pinn_mosaic.pt)';
websave('antarctica_pinn_mosaic.pt', url);
```

Custom Mesh Product
```matlab
% Define grid specifications and generate file
opts = struct(...
    'lon_step', {choose-lon}, ...
    'lat_step', {choose_lat}, ...
    'depth_step', {choose_depth}, ...
    'format', 'netcdf', ...
    'output', 'antarctica_mesh.nc' ...
);

matlab_generate_mesh(opts);
```

## License information
This data product and associated files are released for free use under the MIT License.
