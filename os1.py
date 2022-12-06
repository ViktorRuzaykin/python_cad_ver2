import os

print(os.environ)
for name in os.environ:
    rt = os.environ[f'{name}']
    print(f'{name}:  {rt}')
