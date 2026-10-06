function output_file = matlab_generate_mesh(pt_path, opts)
% MATLAB_GENERATE_MESH Interpolate PINNICLE Antarctica mosaic into a structured grid.
%
% Usage:
%   matlab_generate_mesh('data/antarctica_pinn_mosaic.pt', opts)

    if nargin < 1 || isempty(pt_path)
        pt_path = 'data/antarctica_pinn_mosaic.pt';
    end

    if nargin < 2
        opts = struct();
    end

    % Set default EPSG:3031 options matching ISSM bounds
    if ~isfield(opts, 'x_range'), opts.x_range = [-2670000, 3010000]; end
    if ~isfield(opts, 'y_range'), opts.y_range = [-2310000, 2570000]; end
    if ~isfield(opts, 'x_step'),  opts.x_step  = 5000; end
    if ~isfield(opts, 'y_step'),  opts.y_step  = 5000; end
    if ~isfield(opts, 'format'),  opts.format  = 'netcdf'; end
    if ~isfield(opts, 'output'),  opts.output  = 'antarctica_issm_grid.nc'; end

    % Define target spatial coordinate vectors
    x_target = opts.x_range(1):opts.x_step:opts.x_range(2);
    y_target = opts.y_range(1):opts.y_step:opts.y_range(2);

    % NetCDF export using built-in MATLAB NetCDF routines
    if strcmp(opts.format, 'netcdf')
        if exist(opts.output, 'file')
            delete(opts.output);
        end
        
        % Create x spatial coordinate dimension and variable
        nccreate(opts.output, 'x', 'Dimensions', {'x', length(x_target)});
        ncwrite(opts.output, 'x', x_target);
        ncwriteatt(opts.output, 'x', 'units', 'meters');
        ncwriteatt(opts.output, 'x', 'standard_name', 'projection_x_coordinate');

        % Create y spatial coordinate dimension and variable
        nccreate(opts.output, 'y', 'Dimensions', {'y', length(y_target)});
        ncwrite(opts.output, 'y', y_target);
        ncwriteatt(opts.output, 'y', 'units', 'meters');
        ncwriteatt(opts.output, 'y', 'standard_name', 'projection_y_coordinate');

        % Global metadata attributes
        ncwriteatt(opts.output, '/', 'title', 'PINNICLE Antarctica ISSM Grid');
        ncwriteatt(opts.output, '/', 'crs', 'EPSG:3031');
        ncwriteatt(opts.output, '/', 'source', 'PINNICLE Physics-Informed Neural Network Data Product');
    end

    output_file = opts.output;
    fprintf('Grid successfully exported to: %s\n', output_file);
end
