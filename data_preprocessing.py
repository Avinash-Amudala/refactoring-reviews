import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def preprocess_data(X):
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    X_imputed = imputer.fit_transform(X)
    return X_imputed
