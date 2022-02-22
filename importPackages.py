# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 06:56:18 2022

@author: Олег Дмитренко
"""

import importlib.util
import sys

def setup_packeges(packages):
    for package in packages:       
        if package in sys.modules:
            print(f"{package!r} already in sys.modules")
        elif (spec := importlib.util.find_spec(package)) is not None:
            # If you choose to perform the actual import ...
            module = importlib.util.module_from_spec(spec)
            sys.modules[package] = module
            spec.loader.exec_module(module)
            print(f"{package!r} has been imported")
        else:
            print(f"can't find the {package!r} module")
        