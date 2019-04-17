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

## Unpaired parton analyzer

output is:

* a table whose header is
  ```.bash
  filename, tot_events, count_distr, count_tot
  ```
  where:
  1. `tot_events` is the total number of events in the file
  1. `count_distr` is a list whose entry with index `i` is the number of events such that `i` partons are unpaired in the file
  2. `count_tot` is the number of events in which at least one parton is unpaired in the file
* histograms as png and root files of pt and eta of unpaired partons for every file

In order to complete this step, you should merge all intermediate root files
with

```.bash
python histo_merger_unpaired.py
```


## efficiencies from datacards

Example 

The path that you have to specify is the one where the `configuration.py` file resides.
This script expects that the directory `datacard` resides alongside with that script,
inside the directory that you specify.

```
python efficiencies_from_datacards.py /path/to/plot/configuration
```