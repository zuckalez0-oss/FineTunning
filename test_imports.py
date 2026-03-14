import time
import sys

def measure_import(module_name):
    start = time.time()
    try:
        __import__(module_name)
        end = time.time()
        print(f"Import {module_name} took {end - start:.4f} seconds")
    except Exception as e:
        print(f"Failed to import {module_name}: {e}")

measure_import('dateutil.parser')
measure_import('strictyaml')
measure_import('pyiceberg')
measure_import('supabase')
