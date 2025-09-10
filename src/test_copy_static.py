import os
import tempfile
import shutil
from copystatic import copy_files_recursive


def test_copy_function_manually():
    """Manual test for the copy function with nested directories."""

    # Create temporary directories for testing
    temp_dir = tempfile.mkdtemp()
    source_dir = os.path.join(temp_dir, "test_static")
    dest_dir = os.path.join(temp_dir, "test_public")

    try:
        # Create test directory structure
        os.makedirs(source_dir)
        os.makedirs(os.path.join(source_dir, "css"))
        os.makedirs(os.path.join(source_dir, "js"))
        os.makedirs(os.path.join(source_dir, "images", "nested"))

        # Create test files
        with open(os.path.join(source_dir, "index.html"), "w") as f:
            f.write("<html><body>Test</body></html>")

        with open(os.path.join(source_dir, "css", "style.css"), "w") as f:
            f.write("body { color: blue; }")

        with open(os.path.join(source_dir, "js", "script.js"), "w") as f:
            f.write("console.log('test');")

        with open(os.path.join(source_dir, "images", "nested", "test.png"), "w") as f:
            f.write("fake image data")

        copy_files_recursive(source_dir, dest_dir)

        assert os.path.exists(os.path.join(dest_dir, "index.html"))
        assert os.path.exists(os.path.join(dest_dir, "css", "style.css"))
        assert os.path.exists(os.path.join(dest_dir, "js", "script.js"))
        assert os.path.exists(os.path.join(dest_dir, "images", "nested", "test.png"))

        with open(os.path.join(dest_dir, "should_remain.txt"), "w") as f:
            f.write("This should remain")

        copy_files_recursive(source_dir, dest_dir)

        assert os.path.exists(os.path.join(dest_dir, "should_remain.txt"))
        assert os.path.exists(os.path.join(dest_dir, "index.html"))

    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    test_copy_function_manually()
