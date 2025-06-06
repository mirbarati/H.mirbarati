# -*- coding: utf-8 -*-
"""Untitled26.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cIr5W_NkfYsZTs0B1c2zyLQqSd4gTZTD
"""

# filename: main.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
import numpy as np
from scipy import integrate

app = FastAPI()

# Safe math environment
allowed_names = {
    'sin': np.sin, 'cos': np.cos, 'tan': np.tan, 'exp': np.exp,
    'log': np.log, 'log10': np.log10, 'sqrt': np.sqrt,
    'pi': np.pi, 'e': np.e
}

def get_function(expr, dim):
    def func(x, y, z=0):
        context = allowed_names.copy()
        context.update({'x': x, 'y': y, 'z': z})
        return eval(expr, {"__builtins__": {}}, context)
    return func

@app.get("/integrate")
def integrate_expr(expr: str, x_min: float, x_max: float, y_min: float, y_max: float, z_min: float = 0, z_max: float = 0, dim: int = 2):
    f = get_function(expr, dim)
    if dim == 2:
        result, err = integrate.dblquad(f, x_min, x_max, lambda x: y_min, lambda x: y_max)
    else:
        result, err = integrate.tplquad(f, x_min, x_max, lambda x: y_min, lambda x: y_max, lambda x, y: z_min, lambda x, y: z_max)
    return {"integral": result, "error": err}