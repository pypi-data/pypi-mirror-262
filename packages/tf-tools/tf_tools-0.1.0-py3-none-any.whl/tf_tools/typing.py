from functools import wraps
import tensorflow as tf

def tf_function(f):
  """Like `tf.function` but uses `functools.wraps` to preserve linting of types and docstring"""
  return wraps(f)(tf.function(f))