# Error
## Opencv
    1. error: (-2:Unspecified error) The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Cocoa support
        pip uninstall opencv-python-headless -y
        pip install opencv-python --upgrade
    2. ModuleNotFoundError: No module named 'models'in yolov5
        import sys
        sys.path.append('my/path/to/module/folder')
        import module_of_interest
    3. OMP: Info #274: omp_set_nested routine deprecated, please use omp_set_max_active_levels instead.
        Error  code, arange argument in function.