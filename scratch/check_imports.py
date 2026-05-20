import sys
import os

# Add project root to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    import yfinance as yf
    print("yfinance: OK")
except Exception as e:
    print(f"yfinance: ERROR ({e})")

try:
    import tensorflow as tf
    # Handle namespace package versioning
    version = getattr(tf, "__version__", getattr(tf, "VERSION", "unknown"))
    print(f"tensorflow: OK (version: {version})")
    
    # Check for compat.v1 as used in the project
    try:
        tf_v1 = tf.compat.v1
        print("tf.compat.v1: OK")
    except AttributeError:
        print("tf.compat.v1: NOT FOUND")

except Exception as e:
    print(f"tensorflow: ERROR ({e})")

try:
    # Match the project's logic in train_stock_lstm.py
    import tensorflow as tf
    try:
        tf_v1 = tf.compat.v1
    except AttributeError:
        tf_v1 = tf
    
    try:
        rnn_cell = tf_v1.nn.rnn_cell
        print("tf.nn.rnn_cell: OK")
    except AttributeError:
        print("tf.nn.rnn_cell: ERROR (Not found in tf.nn)")
        
except Exception as e:
    print(f"RNN modules: ERROR ({e})")

try:
    import config as c
    print("config: OK")
except Exception as e:
    print(f"config: ERROR ({e})")

