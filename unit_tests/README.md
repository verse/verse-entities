Unit tests for vrsent module
============================

This directory contains unit tests for `vrsent` module. To be able to run
these test you have to set up `PYTHONPATH` system variable. This variable
has to include path to package `vrsent` and binary module verse.so

```bash
export PYTHONPATH=/path/to/verse/module:/path/to/vrsent/module
```

If you want to perform test_verse.py, then you have to start verse server
first. Then you can perform test with following command:

```bash
python3 test_verse.py
```
