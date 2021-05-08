# 3dedm

A small gcode generator for making EDM plunge cuts on a 3D printer.

## Usage
```
edm.py <depth> [options]
```

## Options
```
--flutter-depth <float> how much the depth should vary durin flutter cycles. Default 0.1
--flutter-cycles <int> How many futter cycles to perform at depth. Default 10
--feed <float> How much to advance the tool per plunge in mm. Default 0.01
--retract-height <int> The height the tool will be retracted above the workpiece for flushing in mm. Default 10
```