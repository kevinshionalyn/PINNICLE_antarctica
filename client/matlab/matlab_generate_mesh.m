%=====================================================================
%       'outputFile', 'antarctica_mesh.mat', ...
%       'lonStep',    0.5, ...
%       'latStep',    0.5, ...
%       'depthStep',  100, ...
%       'format',    'mat');    % options: 'mat' (default) or 'netcdf'
%
%   % 2️⃣  If you need a NetCDF file instead of .mat:
%   matlab_generate_mesh('outputFile','antarctica_mesh.nc', ...
%                        'lonStep',0.5,'latStep',0.5,'depthStep',100, ...
%                        'format','netcdf');
%
%=====================================================================

function matlab_generate_mesh(varargin)
    %-------------------------------------------------------------
    % Parse name‑value pairs
    %-------------------------------------------------------------
    p = inputParser;
    addParameter(p, 'outputFile',  'antarctica_mesh.mat', @ischar);
    addParameter(p, 'lonStep',     0.5,  @isnumeric);
    addParameter(p, 'latStep',     0.5,  @isnumeric);
    addParameter(p, 'depthStep',   100,  @isnumeric);
    addParameter(p, 'lonRange',  [-180, 180], @isnumeric);
    addParameter(p, 'latRange',  [-90,   0],  @isnumeric);
    addParameter(p, 'depthRange',[0, 3000],  @isnumeric);
    addParameter(p, 'format',    'mat', @ischar);   % 'mat' or 'netcdf'
    parse(p, varargin{:});
    opts = p.Results;

    %-------------------------------------------------------------
    % 1️⃣  Make sure Python can see the `client` package
    %-------------------------------------------------------------
    % The client is installed in editable mode (`pip install -e .`),
    % so it lives in the same directory as this .m file.
    % We add that directory to Python's sys.path at runtime.
    clientRoot = fileparts(mfilename('fullpath'));   % -> .../client/matlab
    clientRoot = fullfile(clientRoot, '..');         % -> .../client

    if count(py.sys.path, clientRoot) == 0
        insert(py.sys.path, int32(0), clientRoot);
    end

    %-------------------------------------------------------------
    % 2️⃣  Import the Python helper
    %-------------------------------------------------------------
    try
        mesh_mod = py.importlib.import_module('client.mesh');
    catch err
        error(['Unable to import the Python module `client.mesh`. ' ...
               'Make sure you have run `pip install -e .` from the ' ...
               'root of the repository and that you have a compatible ' ...
               'Python interpreter configured in MATLAB. Original error: %s'], ...
               err.message);
    end

    %-------------------------------------------------------------
    % 3️⃣  Build arguments for the Python function
    %-------------------------------------------------------------
    py_opts = pyargs( ...
        'lon_range',    py.list(opts.lonRange), ...
        'lat_range',    py.list(opts.latRange), ...
        'depth_range',  py.list(opts.depthRange), ...
        'lon_step',     opts.lonStep, ...
        'lat_step',     opts.latStep, ...
        'depth_step',   opts.depthStep, ...
        'fmt',          opts.format );

    %-------------------------------------------------------------
    % 4️⃣  Call the function – it returns the path to the generated file
    %-------------------------------------------------------------
    try
        result_path = mesh_mod.generate_mesh(py_opts);
    catch err
        error('Python mesh generation failed: %s', err.message);
    end

    %-------------------------------------------------------------
    % 5️⃣  Move/rename the result to the user‑requested name
    %-------------------------------------------------------------
    % `result_path` is a Python `pathlib.Path` object; convert to string.
    result_str = char(result_path);
    movefile(result_str, opts.outputFile, 'f');
    fprintf('✅ Mesh written to %s\n', opts.outputFile);
end
