"""
Version 1.2
Script by David Bolsover:  david at bolsover dot com
Generates Cycloidal Gear and Pinions pairs on a single sketch.

With credit for the earlier work by Dr. Rainer Hessmer and Hugh Sparks
https://www.csparks.com/watchmaking/CycloidalGears/index.jxl
http://www.hessmer.org/gears/CycloidalGearBuilder.html

Also for the assistance of Alibre Users idslk and NateLiqGrav who helped with debugging and general Python pointers

Revisions
1.0 Initial Release 
1.1 Coding corrections
1.2 Added Info dialog when gear set completed.

"""
sys.path.append(ScriptFolder)
import CycloidalGearModule

reload(CycloidalGearModule)

win = Windows()

scriptName = 'Cycloidal Gear Generator'

module = 4.0
wheel_count = 30
pinion_count = 6
wheel_center_hole = 6
pinion_center_hole = 6
custom_slop = 0.0
custom_slop_enabled = False
draw_wheel = True
draw_pinion = True
plane = None

show_once = False

values = (
    [None, module, wheel_count, pinion_count, wheel_center_hole, pinion_center_hole, custom_slop, custom_slop_enabled,
     draw_wheel, draw_pinion, plane])


def showOptionsDialog(values):
    options = [[None, WindowsInputTypes.Image, 'CycloidalGear.png', 400],
               ['Module', WindowsInputTypes.Real, values[1]],
               ['Wheel Tooth Count', WindowsInputTypes.Integer, values[2]],
               ['Pinion Tooth Count', WindowsInputTypes.Integer, values[3]],
               ['Wheel Center Hole Diameter', WindowsInputTypes.Real, values[4]],
               ['Pinion Center Hole Diameter', WindowsInputTypes.Real, values[5]],
               ['Custom Slop', WindowsInputTypes.Real, values[6]],
               ['Custom Slop Enabled', WindowsInputTypes.Boolean, values[7]],
               ['Draw Wheel', WindowsInputTypes.Boolean, values[8]],
               ['Draw Pinion', WindowsInputTypes.Boolean, values[9]],
               ['Plane', WindowsInputTypes.Plane, values[10]]]
    values = win.OptionsDialog(scriptName, options, 400)
    return values


while (values[10] == None) | (values[2] <= values[3]):
    if show_once:
        if values[10] == None:
            win.ErrorDialog("Please select a Plane.", "Error!")
        elif values[2] <= values[3]:
            win.ErrorDialog("Wheel Tooth count must be greater than Pinion Tooth count.", "Error!")
    values = showOptionsDialog(values)
    show_once = True

Units.Current = UnitTypes.Millimeters
part = CurrentPart()
part.PauseUpdating()
sketch = part.AddSketch("Gear", values[10])
sketch.AutomaticStartEndEditing = False
sketch.StartEditing()

values.append(sketch)

gear = CycloidalGearModule.CycloidalGear(values)

print(gear)

sketch.StopEditing()
sketch.AutomaticStartEndEditing = True
part.ResumeUpdating()

win.InfoDialog("Gear set generated as:\n\n" + str(gear), "Cycloidal Gear")
