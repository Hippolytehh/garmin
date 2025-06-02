import config

import clr
import os
import System.Reflection # type: ignore
from Dynastream.Fit import * # type: ignore
clr.AddReference(os.path.abspath(config.FIT_DLL))

def create_workout_step_swim(
        message_index: int, 
        distance: float,
        name: str= None,
        notes: str= None,
        intensity: Intensity= Intensity.Active, # type: ignore
        swim_stroke: SwimStroke= SwimStroke.Invalid, # type: ignore
        equipment: WorkoutEquipment= None # type: ignore
    ) -> WorkoutStepMesg: # type: ignore

    workout_step_mesg = WorkoutStepMesg() # type: ignore
    workout_step_mesg.SetMessageIndex(message_index)

    if name:
        workout_step_mesg.SetWktStepName(name)
    
    if notes:
        workout_step_mesg.SetNotes(notes)

    workout_step_mesg.SetIntensity(intensity);

    workout_step_mesg.SetDurationType(WktStepDuration.Distance) # type: ignore
    workout_step_mesg.SetDurationDistance(distance)

    workout_step_mesg.SetTargetType(WktStepTarget.SwimStroke) # type: ignore

    workout_step_mesg.SetTargetStrokeType(swim_stroke.value__)

    if equipment:
        workout_step_mesg.SetEquipment(equipment)

    return workout_step_mesg