# tsvprint
python script to print tsv file.

```
usage: tsvprint.py [--file=PATH]

                   [--head=N]
                   [--tail=N]
                   [--print_interval=SEC]

                   [--header_freq=FREQ]
                   [--float_prec=P] [--float_max_len=M] [--of_handling=OF_HANDLING]

arguments:
  --file=PATH                path to tsv file. (default: none)
  
  ***only use one of the followings***
  default               print all.
  --head=N              print first N rows.
  --tail=N              print last N rows.
  --print_interval=SEC  print all and update whenever file changes.

optional arguments:
  --header_freq=FREQ         how often to print header. (default: -1 (only once at the beginning.))
  --select_cols              select columns by prompt.

  --float_prec=P             precision for printing float number. (default: 5)
  
  --float_max_len=M          max length for printing float number. (default: 11)
                             e.g. for float_prec=5, float_max_len=11,
                             numbers in (-10000.00000, -0.00001] and [0.00001, 10000.00000) will be printed normally.
                             otherwise, they will be printed like: -inf, -0.00000, 0.00000, inf
                             
  --of_handling=OF_HANDLING  whether to use scientific notation (e.g. 1.234e-15), when overflow or underflow occurs.
                             (default: False)
```
