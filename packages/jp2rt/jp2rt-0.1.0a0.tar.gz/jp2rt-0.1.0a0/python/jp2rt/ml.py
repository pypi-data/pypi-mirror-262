import importlib 
import io
from pathlib import Path
import zipfile

import joblib
import numpy as np
from packaging.version import Version, parse
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler # other scaler are: QuantileTransformer, PowerTransformer, MinMaxScaler, 

from jp2rt import __version__

MANIFEST_VERSION = Version('1.0')
JP2RT_VERSION = parse(__version__)
MANIFEST = f'Manifest-Version: {MANIFEST_VERSION}\nJP2RT-Version: {JP2RT_VERSION}\n'

def save_model(model, path):
  if not isinstance(path, Path): path = Path(path)
  mbuf = io.BytesIO()
  joblib.dump(model, mbuf)
  mbuf.flush()
  zbuf = io.BytesIO()
  with zipfile.ZipFile(zbuf, 'a', zipfile.ZIP_DEFLATED, True) as ouf:
    ouf.writestr(f'{path.stem}/MANIFEST.txt', MANIFEST.encode('utf-8'))
    ouf.writestr(f'{path.stem}/model.joblib', mbuf.getvalue())
  return path.with_suffix('.jp2rt').write_bytes(zbuf.getvalue())

def load_model(path):
  if not isinstance(path, Path): path = Path(path)
  zbuf = io.BytesIO(path.with_suffix('.jp2rt').read_bytes())
  with zipfile.ZipFile(zbuf, 'r') as inf:
    manifest = inf.read(f'{path.stem}/MANIFEST.txt').decode('utf-8')
    with inf.open(f'{path.stem}/model.joblib') as mbuf: model = joblib.load(mbuf)
  manifest = dict(line.strip().split(': ') for line in manifest.splitlines() if line)
  if 'Manifest-Version' not in manifest: raise ValueError('Invalid model file, manifest missing Manifest-Version')
  if parse(manifest['Manifest-Version']) > MANIFEST_VERSION: raise ValueError('Invalid model file, manifest version too high')
  if 'JP2RT-Version' not in manifest: raise ValueError('Invalid model file, manifest missing JP2RT-Version')
  if parse(manifest['JP2RT-Version']) > JP2RT_VERSION: raise ValueError('Invalid model file, jp2rt version too high')
  return model

def load_retention_times(path):
  return np.genfromtxt(path, delimiter = '\t', comments = None, usecols = (0, ))

def load_descriptors(path):
  with open(path, 'r') as inf: first_line = inf.readline()
  fields = first_line.split('\t')
  n_fields = len(fields)
  for n_descriptors, field in enumerate(reversed(fields)):
    try:
      float(field)
    except ValueError:
      break
  return np.genfromtxt(path, delimiter = '\t', comments = None, usecols = range(n_fields - n_descriptors, n_fields))

def simple_model_estimate(regressor_name, X, y):
  all_nan_cols = [i for i, x in enumerate(X.T) if all(np.isnan(x))]
  drop_all_nan_cols = ColumnTransformer([('drop_all_nan_cols', 'drop', all_nan_cols)], remainder = 'passthrough')
  imputer = SimpleImputer(strategy = 'mean')
  scaler = StandardScaler()
  module = importlib.import_module('sklearn.ensemble')
  regressor = getattr(module, regressor_name)()
  model =  make_pipeline(drop_all_nan_cols, imputer, scaler, regressor)
  model.fit(X, y)
  return model