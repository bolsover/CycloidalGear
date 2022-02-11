from __future__ import division
from AlibreScript.API import *



    # Adds a reference SketchPoint vertical WRT origin and horizontal WRT SketchPoint passed as parameter
    # Adds vertical dimension from origin to new reference SketchPoint
    # Adds horizontal dimension from new reference SketchPoint and SketchPoint passed as parameter
   
def AddDimensions(sketch, point):
        # add reference point vertical to origin and horizontal to point to be dimensioned
        refpoint = SketchPoint(0, point.Y, True)
        refpoint = sketch.AddPoint(refpoint)
        # add constraints
        sketch.AddConstraint([refpoint, point], Sketch.Constraints.Horizontal)
        sketch.AddConstraint([refpoint, sketch.Origin], Sketch.Constraints.Vertical)
        # add dimensions
        sketch.AddDimension(refpoint, point)
        sketch.AddDimension(refpoint, sketch.Origin)
