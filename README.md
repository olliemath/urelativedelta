# urelativedelta
A small fast implementation of relativedeltas

# benchmarks

Shifting 5mn datetime objects gives us:

| interpreter | urelativedelta | python-dateutil | speedup |
| ------ | ------ | ------ | ------ |
| cpython 3.11 | 6.72s | 20.36s | 3.03x |
| pypy 3.9 | 0.72s | 3.13s | 4.34x |
