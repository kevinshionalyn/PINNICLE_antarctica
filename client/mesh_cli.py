import argparse
import json
import pathlib
from typing import Optional, Tuple, Union

import numpy as np
import torch
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator


def _to_1d_float64(val) -> np.ndarray:
    if val is None:
        return np.empty(0, dtype=np.float64)
    if isinstance(val, torch.Tensor):
        arr = val.detach().cpu().numpy()
    else:
        arr = np.asarray(val)
    return np.asarray(arr, dtype=np.float64).ravel()


def _interpolate_to_grid(
    x_src: np.ndarray,
    y_src: np.ndarray,
    vals_src: np.ndarray,
    x_grid: np.ndarray,
    y_grid: np.ndarray,
    extrapolate_nearest: bool = False,
) -> np.ndarray:
    """Interpolate 1D scattered mesh-free values onto 2D meshgrid (x_grid, y_grid)."""
    valid = np.isfinite(x_src) & np.isfinite(y_src) & np.isfinite(vals_src)
    if not np.any(valid):
        return np.full(x_grid.shape, np.nan, dtype=np.float64)

    pts = np.column_stack([x_src[valid], y_src[valid]])
    v = vals_src[valid]
    q_pts = np.column_stack([x_grid.ravel(), y_grid.ravel()])

    interp = LinearNDInterpolator(pts, v, fill_value=np.nan)
    out = np.asarray(interp(q_pts), dtype=np.float64)

    if extrapolate_nearest:
        missing = ~np.isfinite(out)
        if np.any(missing):
            nn = NearestNDInterpolator(pts, v)
            out[missing] = np.asarray(nn(q_pts[missing]), dtype=np.float64)

    return out.reshape(x_grid.shape)


def generate_mesh(
    pt_path: Union[str, pathlib.Path] = "data/pinn_mesh_free_antarctica_medians_mosaic.pt",
    x_range: Tuple[float, float] = (-2670000.0, 3010000.0),
    y_range: Tuple[float, float] = (-2310000.0, 2570000.0),
    x_step: float = 5000.0,
    y_step: Optional[float] = None,
    fmt: str = "netcdf",
    output: Union[str, pathlib.Path] = "antarctica_issm_grid.nc",
    extrapolate_nearest: bool = False,
) -> pathlib.Path:
    """
    Interpolate a mesh-free PINNICLE Antarctica .pt product onto a structured EPSG:3031 grid.

    Parameters
    ----------
    pt_path : str or pathlib.Path
        Path to local mesh-free PyTorch dictionary artifact.
    x_range : tuple of float
        (min_x, max_x) in EPSG:3031 meters.
    y_range : tuple of float
        (min_y, max_y) in EPSG:3031 meters.
    x_step : float
        Easting grid spacing in meters.
    y_step : float or None
        Northing grid spacing in meters. If None, defaults to x_step.
    fmt : str
        Output format: 'netcdf', 'csv', or 'json'.
    output : str or pathlib.Path
        Destination output filename.
    extrapolate_nearest : bool
        If True, fill points outside the mesh-free convex hull using nearest-neighbor.

    Returns
    -------
    pathlib.Path
        Path object pointing to the created mesh file.
    """
    pt_path = pathlib.Path(pt_path)
    output = pathlib.Path(output)

    if y_step is None:
        y_step = float(x_step)
    x_step = float(x_step)
    y_step = float(y_step)

    if not pt_path.exists():
        raise FileNotFoundError(
            f"Tensor file not found at {pt_path}. Ensure the file exists or run 'git lfs pull'."
        )

    # 1. Load PINNICLE mesh-free mosaic dictionary artifact
    mosaic = torch.load(pt_path, map_location="cpu", weights_only=False)
    coords = mosaic.get("coordinates", {})
    data_vars = mosaic.get("data", {})

    x_raw = coords.get("x")
    y_raw = coords.get("y")
    x_np = x_raw.detach().cpu().numpy() if isinstance(x_raw, torch.Tensor) else np.asarray(x_raw)
    y_np = y_raw.detach().cpu().numpy() if isinstance(y_raw, torch.Tensor) else np.asarray(y_raw)

    # 2. Construct requested 2D evaluation grid (shape: ny x nx)
    x_target = np.arange(float(x_range[0]), float(x_range[1]) + 0.5 * x_step, x_step, dtype=np.float64)
    y_target = np.arange(float(y_range[0]), float(y_range[1]) + 0.5 * y_step, y_step, dtype=np.float64)
    x_grid, y_grid = np.meshgrid(x_target, y_target, indexing="xy")

    # 3. Interpolate each variable from mesh-free points onto target grid
    gridded_vars = {}
    if x_np.ndim == 1 and y_np.ndim == 1 and x_np.size == y_np.size:
        x_pts = np.asarray(x_np, dtype=np.float64).ravel()
        y_pts = np.asarray(y_np, dtype=np.float64).ravel()
        for var_name, val in data_vars.items():
            vals_pts = _to_1d_float64(val)
            if vals_pts.size == x_pts.size:
                gridded_vars[var_name] = _interpolate_to_grid(
                    x_pts,
                    y_pts,
                    vals_pts,
                    x_grid,
                    y_grid,
                    extrapolate_nearest=extrapolate_nearest,
                )
    else:
        raise ValueError(
            f"Expected 1D coordinate arrays (x, y) of matching length in {pt_path}, "
            f"got shapes x={x_np.shape}, y={y_np.shape}."
        )

    # 4. Write requested output format
    fmt_clean = fmt.lower()
    output.parent.mkdir(parents=True, exist_ok=True)

    if fmt_clean in {"nc", "netcdf"}:
        try:
            import xarray as xr
        except ImportError as exc:
            raise ImportError(
                "xarray and netcdf4 are required for NetCDF export. Install via: pip install xarray netcdf4"
            ) from exc

        xr_data_vars = {
            var_name: (("y", "x"), arr.astype(np.float32))
            for var_name, arr in gridded_vars.items()
        }
        ds = xr.Dataset(
            data_vars=xr_data_vars,
            coords={
                "x": ("x", x_target, {"units": "m", "standard_name": "projection_x_coordinate"}),
                "y": ("y", y_target, {"units": "m", "standard_name": "projection_y_coordinate"}),
            },
            attrs={
                "title": "PINNICLE Antarctica Interpolated Grid",
                "crs": "EPSG:3031",
                "x_step_m": x_step,
                "y_step_m": y_step,
                "source": "PINNICLE Mesh-Free Physics-Informed Neural Network Data Product",
            },
        )
        ds.to_netcdf(output)

    elif fmt_clean == "csv":
        import pandas as pd

        df_dict = {
            "x_epsg3031": x_grid.ravel(),
            "y_epsg3031": y_grid.ravel(),
        }
        for var_name, arr in gridded_vars.items():
            df_dict[var_name] = arr.ravel()
        pd.DataFrame(df_dict).to_csv(output, index=False)

    elif fmt_clean == "json":
        grid_payload = {
            "x": x_target.tolist(),
            "y": y_target.tolist(),
            "crs": "EPSG:3031",
            "variables": {
                var_name: arr.tolist()
                for var_name, arr in gridded_vars.items()
            },
        }
        with open(output, "w", encoding="utf-8") as f:
            json.dump(grid_payload, f)

    else:
        raise ValueError(f"Unsupported format: {fmt}. Choose 'netcdf', 'csv', or 'json'.")

    return output


def main():
    """CLI entrypoint for pinnicle-antarctica mesh command."""
    parser = argparse.ArgumentParser(
        description="Generate structured EPSG:3031 grid from mesh-free PINNICLE Antarctica product."
    )
    parser.add_argument(
        "--tensor",
        default="data/pinn_mesh_free_antarctica_medians_mosaic.pt",
        help="Path to input mesh-free .pt tensor",
    )
    parser.add_argument(
        "--x-range",
        type=float,
        nargs=2,
        default=[-2670000.0, 3010000.0],
        help="Easting range in meters (EPSG:3031)",
    )
    parser.add_argument(
        "--y-range",
        type=float,
        nargs=2,
        default=[-2310000.0, 2570000.0],
        help="Northing range in meters (EPSG:3031)",
    )
    parser.add_argument("--x-step", type=float, default=5000.0, help="Easting spatial resolution in meters")
    parser.add_argument(
        "--y-step",
        type=float,
        default=None,
        help="Northing spatial resolution in meters (defaults to --x-step)",
    )
    parser.add_argument("--format", choices=["netcdf", "csv", "json"], default="netcdf", help="Output file format")
    parser.add_argument("--output", default="antarctica_issm_grid.nc", help="Output filename")
    parser.add_argument(
        "--extrapolate-nearest",
        action="store_true",
        help="Fill outside convex hull using nearest-neighbor interpolation",
    )

    args = parser.parse_args()

    generate_mesh(
        pt_path=args.tensor,
        x_range=tuple(args.x_range),
        y_range=tuple(args.y_range),
        x_step=args.x_step,
        y_step=args.y_step,
        fmt=args.format,
        output=args.output,
        extrapolate_nearest=args.extrapolate_nearest,
    )


if __name__ == "__main__":
    main()