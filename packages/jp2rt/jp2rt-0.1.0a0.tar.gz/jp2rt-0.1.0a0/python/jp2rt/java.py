from collections import OrderedDict
import importlib.resources

from scyjava import config, jimport, to_python

JP2RT_REF = ref = importlib.resources.files('jp2rt') / 'lib.jar'

class JavaLib:
  def __init__(self) -> None:
    self._cm = importlib.resources.as_file(JP2RT_REF)
  def __enter__(self):
    path = self._cm.__enter__()
    config.add_classpath(str(path))
    return lambda name: jimport('it.unimi.di.jp2rt.' + name)
  def __exit__(self, exc_type, exc_value, traceback):
    return self._cm.__exit__(exc_type, exc_value, traceback)
  
def add_descriptors_via_tsv(src, dst):
  with JavaLib() as jl:
    MDC = jl('MolecularDescriptorsCalculator')
    MDC.toFile(MDC.fromFile(src), dst)

def descriptors():
  with JavaLib() as jl:
    MDW = jl('MolecularDescriptorsWrapper')
    res = OrderedDict()
    for wd in MDW(): res[str(wd.name())] = to_python(wd.descriptors())
    return res