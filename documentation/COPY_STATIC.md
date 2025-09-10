# Static File Copying Implementation

## Overview

The static file copying functionality recursively copies files and directories from the `static/` directory to the output directory, maintaining the directory structure.

## Implementation

### Module: `copystatic.py`

```python
import os
import shutil

def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)
```

## Features

- **Recursive copying**: Handles nested directory structures
- **Automatic directory creation**: Creates destination directories as needed
- **Logging**: Shows each file operation for transparency
- **File preservation**: Maintains file attributes and directory structure

## File Structure Example

```
static/
├── images/
│   ├── tolkien.png
│   └── glorfindel.png
└── index.css

docs/          # Generated automatically
├── images/
│   ├── tolkien.png
│   └── glorfindel.png
└── index.css
```

## Usage

The function is called automatically by `main.py` during the site generation process:

```python
copy_files_recursive(dir_path_static, dir_path_docs)
```
