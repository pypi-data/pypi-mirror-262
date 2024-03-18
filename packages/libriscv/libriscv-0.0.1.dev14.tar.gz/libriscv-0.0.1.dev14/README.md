# Python bindings of Spike RISC-V ISA Simulator (libriscv.so)

```text
LIU Yu <liuy@etech-inc.com>
2024/03/14 (v0.1)
```

## Setting Up

```bash
$ python -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
```

## Running Tests

```bash
(.venv) $ python setup.py build_ext --inplace
(.venv) $ pytest -v
```

## Packaging

```bash
(.venv) $ python -m build --no-isolation
```
