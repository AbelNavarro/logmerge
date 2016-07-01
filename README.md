logmerge
--------

merge multiple log files chronologically

features:
- can detect file timestamp format
- can merge files with different timestamp formats
- recognizes multiline entries (i.e. stack traces)
- can add filename to output
- can add line number to output

limitations:
- file contents must be sorted chronologically
- cannot open compressed files
- inaccuracies by logging program ignored
- if logs come from multiple machines, user must ensure they are synchronized
- all files must be in same time zone


Sample usage:
```
$ find . -name *.log | xargs logmerge.py
```
