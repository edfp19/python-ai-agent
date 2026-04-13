"""Package exports for the functions helpers.

This module intentionally exposes some submodules as module objects (so test
helpers that import them as modules continue to work) while also exporting
convenience callables where tests or other code import them directly from the
package.
"""

import importlib

# Expose run_python_file as a callable at package level (so
# `from functions import run_python_file` yields the function)
from .run_python_file import run_python_file

# Expose the get_files_info and write_file submodules as module objects so
# `from functions import get_files_info as gfi` yields a module with
# `gfi.get_files_info(...)` as some tests expect.
get_files_info = importlib.import_module(".get_files_info", __name__)
write_file = importlib.import_module(".write_file", __name__)

# Convenience export for the get_file_content function (also available via
# `from functions.get_file_content import get_file_content`)
from .get_file_content import get_file_content

# Re-export the schema for get_files_info for callers that imported it from
# the package before.
schema_get_files_info = get_files_info.schema_get_files_info
