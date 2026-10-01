# PINNICLE Antarctica Data Product

A mesh-free, physics-informed neural network (PINN) representation of the Antarctic ice sheet generated using the open-source **[PINNICLE](https://github.com/ISSMteam/PINNICLE)** model.

---

## Basic Data Information

* **Raw Data Product**: A continuous, mesh-free model output stored as a PyTorch tensor (`antarctica_pinn_mosaic.pt`).
* **Custom Grids**: Interpolated spatial products (NetCDF, CSV, or JSON) generated on-the-fly across custom ranges and resolutions (longitude, latitude, depth).
* **Coordinate Systems & Units**:
  * Longitude: Degrees (`-180` to `180`)
  * Latitude: Degrees (`-90` to `0`)
  * Depth: Meters (`0` to `3000`, positive down)

---

## 1. Python

### Installation (requieres Python 3.8+ and PyTorch)
```bash
git clone [https://github.com/kevinshionalyn/PINNICLE_antarctica.git](https://github.com/kevinshionalyn/PINNICLE_antarctica.git)
cd PINNICLE_antarctica
pip install -e .

### Mesh-free product
from client.download import download_pt, load_tensor

# Download raw tensor file to working directory
pt_path = download_pt()

# Load as a torch.Tensor object
tensor = load_tensor()
print(f"Loaded tensor shape: {tensor.shape}")

### Custom mesh product
from client.download import download_pt, generate_mesh

pt_path = download_pt()

# Generate structured grid file
mesh_file = generate_mesh(
    pt_path=pt_path,
    lon_range=(-180, 180),   # degrees
    lat_range=(-90, 0),      # degrees
    depth_range=(0, 3000),   # meters
    lon_step=0.5,
    lat_step=0.5,
    depth_step=100,
    fmt="netcdf"             # "netcdf", "csv", or "json"
)
print(f"Mesh file written to: {mesh_file}")

## 2. Command line
### Using curl:
curl -O [https://kevinshionalyn.github.io/PINNICLE_antarctica/data/antarctica_pinn_mosaic.pt](https://kevinshionalyn.github.io/PINNICLE_antarctica/data/antarctica_pinn_mosaic.pt)
### Using wget:
wget [https://kevinshionalyn.github.io/PINNICLE_antarctica/data/antarctica_pinn_mosaic.pt](https://kevinshionalyn.github.io/PINNICLE_antarctica/data/antarctica_pinn_mosaic.pt)

### Custom mesh product
curl -s [https://raw.githubusercontent.com/kevinshionalyn/PINNICLE_antarctica/main/client/mesh_cli.py](https://raw.githubusercontent.com/kevinshionalyn/PINNICLE_antarctica/main/client/mesh_cli.py) | \
python3 - \
    --lon-step {choose_lon} --lat-step {choose_lat} --depth-step {choose-depth} \
    --format netcdf \
    --output my_antarctica_mesh.nc

## 3. MATLAB
url = '[https://kevinshionalyn.github.io/PINNICLE_antarctica/client/matlab/matlab_generate_mesh.m](https://kevinshionalyn.github.io/PINNICLE_antarctica/client/matlab/matlab_generate_mesh.m)';
websave('matlab_generate_mesh.m', url);

### Mesh-free product
% Download the raw PyTorch model file directly to current folder
url = '[https://kevinshionalyn.github.io/PINNICLE_antarctica/data/antarctica_pinn_mosaic.pt](https://kevinshionalyn.github.io/PINNICLE_antarctica/data/antarctica_pinn_mosaic.pt)';
websave('antarctica_pinn_mosaic.pt', url);

### Custom Mesh Product
% Define grid specifications and generate file
opts = struct(...
    'lon_step', {choose-lon}, ...
    'lat_step', {choose_lat}, ...
    'depth_step', {choose_depth}, ...
    'format', 'netcdf', ...
    'output', 'antarctica_mesh.nc' ...
);

matlab_generate_mesh(opts);

## License information
This data product and associated files are released for free use under the MIT License.
