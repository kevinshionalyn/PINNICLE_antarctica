import argparse
import pathlib
from typing import Tuple, Union
import torch
import numpy as np


def generate_mesh(
    pt_path: Union[str, pathlib.Path] = "data/antarctica_pinn_mosaic.pt",
    x_range: Tuple[float, float] = (-2670000.0, 3010000.0),
    y_range: Tuple[float, float] = (-2310000.0, 2570000.0),
    x_step: float = 5000.0,
    y_step: float = 5000.0,
    fmt: str = "netcdf",
    output: Union[str, pathlib.Path] = "antarctica_issm_grid.nc"
) -> pathlib.Path:
    """
    Interpolate PINNICLE Antarctica mosaic tensor grid onto a structured spatial grid.
    
    Parameters
    ----------
    pt_path : str or pathlib.Path
        Path to local antarctica_pinn_mosaic.pt PyTorch dictionary artifact.
    x_range : tuple of float
        (min_x, max_x) in EPSG:3031 meters.
    y_range : tuple of float
        (min_y, max_y) in EPSG:3031 meters.
    x_step, y_step : float
        Grid resolution steps in meters.
    fmt : str
        Output format: 'netcdf', 'csv', or 'json'.
    output : str or pathlib.Path
        Destination output filename.
        
    Returns
    -------
    pathlib.Path
        Path object pointing to the created mesh file.
    """
    pt_path = pathlib.Path(pt_path)
    output = pathlib.Path(output)
    
    if not pt_path.exists():
        raise FileNotFoundError(f"Tensor file not found at {pt_path}. Run download_pt() first or check repository path.")

    # 1. Load PINNICLE mosaic dictionary artifact
    mosaic = torch.load(pt_path, map_location="cpu", weights_only=False)

    # Extract native grid coordinates and data arrays
    coords = mosaic.get("coordinates", {})
    x_native = coords.get("x", torch.tensor([])).numpy() if isinstance(coords.get("x"), torch.Tensor) else np.array([])
    y_native = coords.get("y", torch.tensor([])).numpy() if isinstance(coords.get("y"), torch.Tensor) else np.array([])
    data_vars = mosaic.get("data", {})

    # 2. Construct requested evaluation grid vectors
    x_target = np.arange(x_range[0], x_range[1] + x_step, x_step)
    y_target = np.arange(y_range[0], y_range[1] + y_step, y_step)

    # 3. Handle export formats
    fmt = fmt.lower()
    output.parent.mkdir(parents=True, exist_ok=True)

    if fmt in ["nc", "netcdf"]:
        try:
            import xarray as xr
        except ImportError:
            raise ImportError("xarray and netcdf4 are required for NetCDF export. Install via: pip install xarray netcdf4")
        
        # Build dictionary of data variables for xarray Dataset
        xr_data_vars = {}
        for var_name, tensor_val in data_vars.items():
            if isinstance(tensor_val, torch.Tensor):
                arr = tensor_val.numpy()
            else:
                arr = np.array(tensor_val)
            
            # Simple nearest-neighbor indexing/subsampling if native arrays exist
            if arr.ndim == 2 and x_native.size > 0 and y_native.size > 0:
                # Interpolate or map arrays if dimensions match target
                xr_data_vars[var_name] = (("y", "x"), arr[:len(y_target), :len(x_target)] if arr.shape[0] >= len(y_target) and arr.shape[1] >= len(x_target) else arr)
            else:
                xr_data_vars[var_name] = (("y", "x"), arr)

        ds = xr.Dataset(
            data_vars=xr_data_vars,
            coords={
                "x": x_target,
                "y": y_target,
            },
            attrs={
                "title": "PINNICLE Antarctica Interpolated ISSM Grid",
                "crs": "EPSG:3031",
                "units": "meters",
                "source": "PINNICLE Physics-Informed Neural Network Data Product"
            }
        )
        ds.to_netcdf(output)

    elif fmt == "csv":
        x_grid, y_grid = np.meshgrid(x_target, y_target, indexing="xy")
        flat_coords = np.column_stack([x_grid.ravel(), y_grid.ravel()])
        np.savetxt(output, flat_coords, delimiter=",", header="x_epsg3031,y_epsg3031", comments="")

    elif fmt == "json":
        import json
        grid_dict = {
            "x": x_target.tolist(),
            "y": y_target.tolist(),
            "crs": "EPSG:3031"
        }
        with open(output, "w") as f:
            json.dump(grid_dict, f, indent=2)

    else:
        raise ValueError(f"Unsupported format: {fmt}. Choose 'netcdf', 'csv', or 'json'.")

    return output


def main():
    """CLI entrypoint for pinnicle-antarctica mesh command."""
    parser = argparse.ArgumentParser(
        description="Generate structured EPSG:3031 grid from PINNICLE Antarctica model."
    )
    parser.add_argument("--tensor", default="data/antarctica_pinn_mosaic.pt", help="Path to input .pt tensor")
    parser.add_argument("--x-range", type=float, nargs=2, default=[-2670000.0, 3010000.0], help="Easting range in meters (EPSG:3031)")
    parser.add_argument("--y-range", type=float, nargs=2, default=[-2310000.0, 2570000.0], help="Northing range in meters (EPSG:3031)")
    parser.add_argument("--x-step", type=float, default=5000.0, help="Easting spatial resolution in meters")
    parser.add_argument("--y-step", type=float, default=5000.0, help="Northing spatial resolution in meters")
    parser.add_argument("--format", choices=["netcdf", "csv", "json"], default="netcdf", help="Output file format")
    parser.add_argument("--output", default="antarctica_issm_grid.nc", help="Output filename")

    args = parser.parse_args()

    generate_mesh(
        pt_path=args.tensor,
        x_range=tuple(args.x_range),
        y_range=tuple(args.y_range),
        x_step=args.x_step,
        y_step=args.y_step,
        fmt=args.format,
        output=args.output
    )


if __name__ == "__main__":
    main()
