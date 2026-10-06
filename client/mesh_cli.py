import argparse
import pathlib
from typing import Tuple, Union
import torch
import numpy as np


def generate_mesh(
    pt_path: Union[str, pathlib.Path] = "data/antarctica_pinn_mosaic.pt",
    lon_range: Tuple[float, float] = (-180.0, 180.0),
    lat_range: Tuple[float, float] = (-90.0, -60.0),
    depth_range: Tuple[float, float] = (0.0, 3000.0),
    lon_step: float = 0.5,
    lat_step: float = 0.5,
    depth_step: float = 100.0,
    fmt: str = "netcdf",
    output: Union[str, pathlib.Path] = "antarctica_mesh.nc"
) -> pathlib.Path:
    """
    Interpolate continuous PINN tensor model output onto a structured spatial grid.
    
    Parameters
    ----------
    pt_path : str or pathlib.Path
        Path to the local antarctica_pinn_mosaic.pt PyTorch tensor.
    lon_range : tuple of float
        (min_lon, max_lon) in degrees.
    lat_range : tuple of float
        (min_lat, max_lat) in degrees.
    depth_range : tuple of float
        (min_depth, max_depth) in meters.
    lon_step, lat_step, depth_step : float
        Grid resolution steps.
    fmt : str
        Output format: 'netcdf', 'csv', or 'json'.
    output : str or pathlib.Path
        Output file destination.
        
    Returns
    -------
    pathlib.Path
        Path object pointing to the created mesh file.
    """
    pt_path = pathlib.Path(pt_path)
    output = pathlib.Path(output)
    
    if not pt_path.exists():
        raise FileNotFoundError(f"Tensor file not found at {pt_path}. Run download_pt() first.")

    # 1. Load trained PINN model tensor
    model_data = torch.load(pt_path, map_location="cpu", weights_only=False)

    # 2. Construct evaluation grid vectors
    lons = np.arange(lon_range[0], lon_range[1] + lon_step, lon_step)
    lats = np.arange(lat_range[0], lat_range[1] + lat_step, lat_step)
    depths = np.arange(depth_range[0], depth_range[1] + depth_step, depth_step)

    # 3. Handle export formats
    fmt = fmt.lower()
    output.parent.mkdir(parents=True, exist_ok=True)

    if fmt in ["nc", "netcdf"]:
        try:
            import xarray as xr
        except ImportError:
            raise ImportError("xarray and netcdf4 are required for NetCDF export. Install via: pip install xarray netcdf4")
        
        # Build 3D mesh evaluation grid
        lon_grid, lat_grid, depth_grid = np.meshgrid(lons, lats, depths, indexing="ij")
        
        # Placeholder evaluation evaluation call (adjust based on your PINN tensor forward pass)
        # Assuming model_data represents evaluated points or neural net weights
        data_values = np.zeros(lon_grid.shape) 

        ds = xr.Dataset(
            data_vars={"pinn_output": (("longitude", "latitude", "depth"), data_values)},
            coords={
                "longitude": lons,
                "latitude": lats,
                "depth": depths,
            },
            attrs={
                "title": "PINNICLE Antarctica Interpolated Mesh",
                "crs": "EPSG:3031",
                "source": "PINNICLE Physics-Informed Neural Network Data Product"
            }
        )
        ds.to_netcdf(output)

    elif fmt == "csv":
        lon_grid, lat_grid, depth_grid = np.meshgrid(lons, lats, depths, indexing="ij")
        flat_coords = np.column_stack([lon_grid.ravel(), lat_grid.ravel(), depth_grid.ravel()])
        np.savetxt(output, flat_coords, delimiter=",", header="longitude,latitude,depth", comments="")

    elif fmt == "json":
        import json
        grid_dict = {
            "longitude": lons.tolist(),
            "latitude": lats.tolist(),
            "depth": depths.tolist()
        }
        with open(output, "w") as f:
            json.dump(grid_dict, f, indent=2)

    else:
        raise ValueError(f"Unsupported format: {fmt}. Choose 'netcdf', 'csv', or 'json'.")

    return output


def main():
    """CLI entrypoint for pinnicle-antarctica mesh command."""
    parser = argparse.ArgumentParser(description="Generate structured grid from PINNICLE Antarctica model.")
    parser.add_argument("--tensor", default="data/antarctica_pinn_mosaic.pt", help="Path to input .pt tensor")
    parser.add_argument("--lon-step", type=float, default=0.5, help="Longitude resolution (degrees)")
    parser.add_argument("--lat-step", type=float, default=0.5, help="Latitude resolution (degrees)")
    parser.add_argument("--depth-step", type=float, default=100.0, help="Depth resolution (meters)")
    parser.add_argument("--format", choices=["netcdf", "csv", "json"], default="netcdf", help="Output file format")
    parser.add_argument("--output", default="antarctica_mesh.nc", help="Output filename")

    args = parser.parse_args()

    generate_mesh(
        pt_path=args.tensor,
        lon_step=args.lon_step,
        lat_step=args.lat_step,
        depth_step=args.depth_step,
        fmt=args.format,
        output=args.output
    )


if __name__ == "__main__":
    main()
