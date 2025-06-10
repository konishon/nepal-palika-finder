import importlib.resources

def get_fgb_path():
    """
    Gets the path to the FlatGeobuf data file bundled with the package.
    
    Returns:
        A path-like object to the local_levels.fgb file.
    """
    try:
        return importlib.resources.files('nepal_palika_finder.data').joinpath('local_levels.fgb')
    except (ModuleNotFoundError, AttributeError):
        with importlib.resources.path('nepal_palika_finder.data', 'local_levels.fgb') as path:
            return path
