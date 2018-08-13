import pytest
import numpy as np
from pypif import pif
import pandas as pd
import json
from citrine_converters.mechanical.converter import process_files
from test.test_process_files import test_process_single_file

print("In the Function:")
results = process_files(['resources/simple_data.json'])
print(results.properties[0].scalars)
print("After Function:")
print(type(results))

res = test_process_single_file