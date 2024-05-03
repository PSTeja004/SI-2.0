import compileall
import sys

def compile_py_to_pyc(file_path):
    try:
        compileall.compile_file(file_path, force=True)
        print(f"Successfully compiled {file_path} to .pyc")
    except Exception as e:
        print(f"Error compiling {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python setup.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    compile_py_to_pyc(file_path)
