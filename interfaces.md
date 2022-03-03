## Main Notebook
- Import packages 
    - numpy as np
    - pandas as pd
- Constants
    - thres_stat
    - thres_num

## In Class:
### Name: 
    InClass
### Attributes
    - expec
    - npop
    - table
    - efield
    - nstate_i
### Functions


## Statistics class
### Name: 
    StatisticsClass
### Requirements
    - Data sets (expec, npop, table)
    - Constants (thres_stat)
    - Packages (numpy, pandas)
### Tasks
    - Data cleaning
    - ...

## Numerics class
### Name: 
    NumericsClass
### Requirements
    - Data sets (efield, nstate_i)
    - Constants (thres_num)
    - Packages 
### Tasks
    - Data cleaning
    - ...

## Output class
- Numerics and Statistics class ONLY do mathematical stuff, all plotting is "hardcoded" into the Output class
- savepdf = False as optional arg to output constructor

### Requirements:
    - Statistics:
        - df_expec
        - df_expec2 (Here we dropped some columns)
        - df_npop2
        - corr2
        - x
        - out_dist
    - Numerics:
        - freq
        - fcols
        - cols
        - time
        - autocorr
        - freq2 (Task 5/6)
        - fcols2 (Task 5/6)

