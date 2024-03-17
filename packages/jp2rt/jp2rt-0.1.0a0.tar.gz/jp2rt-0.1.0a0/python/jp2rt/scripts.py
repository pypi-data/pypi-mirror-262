from json import dumps

import click

from jp2rt import descriptors, add_descriptors_via_tsv, load_model, save_model, load_descriptors, simple_model_estimate, load_retention_times

@click.group()
def cli():
  pass

@click.command() 
@click.argument('src', type = click.Path(exists = True, resolve_path = True))
@click.argument('dst', type = click.Path(writable = True, resolve_path = True))
def add_descriptors(src, dst):
  """Computes molecular descriptions reading a TSV file with SMILES and producing another TSV file appending molecular descriptor values.
  
  \b
  SRC   The source TSV file (must contain SMILES on the last column).
  DST   Destination TSV file (will have the same columns of SRC, followed by molecular descriptor values).
  """
  add_descriptors_via_tsv(src, dst)

@click.command()
@click.option('--json', '-j', is_flag = True, help = 'Produces JSON output.')
def list_descriptors(json):
  "List the known molecular descriptors."
  if (json):
    print(dumps(descriptors(), indent = 2))
  else:
    n = 1
    for name, desc in descriptors().items():
      print(name)
      for d in desc:
        print(f'\t{n}: {d}')
        n += 1

@click.command() 
@click.argument('model', type = click.Path(exists = True, resolve_path = True))
@click.argument('src', type = click.Path(exists = True, resolve_path = True))
@click.argument('dst', type = click.Path(writable = True, resolve_path = True))
def predict_rt(model, src, dst):
  """Uses the model to predict the retention time given a TSV containing the molecular descriptors producing another TSV file prepending the predicted value.
  
  \b
  MODEL The model file.
  SRC   The source TSV file (the molecular descriptors must be on the last columns).
  DST   Destination TSV file (will have the predicted retention time, followed by the same columns of SRC).
  """
  model = load_model(model)
  X = load_descriptors(src)
  click.echo(f'Read {X.shape[0]} molecules with {X.shape[1]} descriptor values each...')
  y = model.predict(X)
  with open(src, 'r') as inf, open(dst, 'w') as ouf:
    for line, rt in zip(inf, y):
      ouf.write(f'{rt}\t{line}')
  click.echo(f'Predicted retention times written to {dst}...')

@click.command()
@click.argument('name', type = click.STRING)
@click.argument('src', type = click.Path(exists = True, resolve_path = True))
@click.argument('dst', type = click.Path(writable = True, resolve_path = True))
def estimate_model(name, src, dst):
  X = load_descriptors(src)
  y = load_retention_times(src)
  click.echo(f'Read {X.shape[0]} molecules with {X.shape[1]} descriptor values each...')
  model = simple_model_estimate(name, X, y)
  size = save_model(model, dst)
  click.echo(f'Model saved to {dst} ({size} bytes)...')


cli.add_command(add_descriptors)
cli.add_command(list_descriptors)
cli.add_command(estimate_model)
cli.add_command(predict_rt)

if __name__ == '__main__':
    cli()