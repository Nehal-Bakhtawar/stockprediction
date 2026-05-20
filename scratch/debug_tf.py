import sys
import os
print(f"Python: {sys.version}")
print(f"Executable: {sys.executable}")
print(f"Path: {sys.path}")

try:
    import tensorflow as tf
    print(f"TF found at: {getattr(tf, '__path__', 'No Path')}")
    print(f"TF file: {getattr(tf, '__file__', 'No File')}")
    print(f"TF dir: {dir(tf)}")
    import tensorflow.compat.v1 as tf_v1
    print("Import tensorflow.compat.v1: SUCCESS")
except Exception as e:
    print(f"TF Error: {e}")
