# Utils
Library of useful functions to work with quadrimomenta. 
For example functions to get all possible invariant mass pairs, or find the nearest vector from a target.


## Parton analyzer
Script to analyze the partons quadrimomenta at Gen level from latino trees. 

How to use:
```
python parton_analyzer.py  latino_tree_file.root [nevents=10] [1 debug=True]
```

## Top Counter

output is a table whose header is:

```.bash
file tot_events no_t_no_tbar t tbar t_tbar
```

where:

* `no_t_no_tbar`: number of events without a top and a tbar
* `t`: number of events with a t (can include events with a tbar)
* `tbar`: number of events with a tbar (can include events with a t)
* `t_tbar`: number of events with a t _and_ a tbar

if you want to get the number of events with only a `t` (`tbar`), it is `t - t_tbar` (`tbar - t_tbar`)
