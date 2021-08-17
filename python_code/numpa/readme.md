# Guide to Numba
## Install
```commandline
pip install numba
```

## Use
```commandline
    from numba import jit
    import numpy as np
    
    x = np.arange(100).reshape(10, 10)
    
    @jit(nopython=True) # Set "nopython" mode for best performance, equivalent to @njit
    def go_fast(a): # Function is compiled to machine code when called the first time
        trace = 0.0
        for i in range(a.shape[0]):   # Numba likes loops
            trace += np.tanh(a[i, i]) # Numba likes NumPy functions
        return a + trace              # Numba likes NumPy broadcasting
    
    print(go_fast(x))
```
## How does Numba work?
+ Numba reads the Python bytecode for a decorated function and combines this with information about the types of the input arguments to the function. It analyzes and optimizes your code, and finally uses the LLVM compiler library to generate a machine code version of your function, tailored to your CPU capabilities. This compiled version is then used every time your function is called
+ Using with small function and it was called usually.
# Reference in [here](https://numba.pydata.org/numba-doc/dev/user/5minguide.html)