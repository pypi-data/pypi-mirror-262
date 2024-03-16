import importlib_metadata

metadata = importlib_metadata.metadata("ip-check")

__version__ = metadata['version']