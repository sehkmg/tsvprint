# tsvprint
python script to print tsv file.

```
usage: tsvprint.py [--file=PATH]
                   [--float_prec=P] [--float_max_len=M] [--of_handling=OF_HANDLING]
                   [--header_freq=FREQ]
                   [--head=N]
                   [--tail=N]
                   [--print_interval=SEC]

arguments:
  --file_name=PATH           path to tsv file. (default: none)
  
  --float_prec=P             precision for printing float number. (default: 3)
  
  --float_max_len=M          max length for printing float number. (default: 10)
                             e.g. for float_prec=3, float_max_len=9,
                             numbers in (-10000.000, -0.001] and [0.001, 10000.000) will be printed normally.
                             otherwise, they will be printed like: -inf, -0.000, 0.000, inf
                             
  --of_handling=OF_HANDLING  whether to use scientific notation (e.g. 1.234e-15), when overflow or underflow occurs.
                             (default: False)
  
  --header_freq=FREQ         how often to print header. (default: -1 (only once at the beginning.))
  
  ***only use one of the followings***
  default               print all.
  --head=N              print first N rows.
  --tail=N              print last N rows.
  --print_interval=SEC  print all and update whenever file changes.
```
