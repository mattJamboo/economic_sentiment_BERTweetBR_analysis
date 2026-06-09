
import os
import re
from pathlib import Path


import pandas as pd
import numpy as np
from pathlib import Path



from unidecode import unidecode 

# === MACHINE LEARNING ===
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


import matplotlib.pyplot as plt

import seaborn as sns



