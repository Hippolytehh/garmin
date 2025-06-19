import config

import clr
import os
import System.Reflection # type: ignore
clr.AddReference(os.path.abspath(config.FIT_DLL))
from Dynastream.Fit import * # type: ignore

def create_workout_step_swim_warmup(
        message_index: int, 
        name: str= None, 
        notes: str= None,
        duration_type: WktStepDuration= WktStepDuration.Open, # type: ignore
        duration_time: float= None
    ) -> WorkoutStepMesg: # type: ignore

        workout_step_mesg = WorkoutStepMesg() # type: ignore
        workout_step_mesg.SetMessageIndex(message_index)

        if name: 
            workout_step_mesg.SetWktStepName(name)

        if notes:
            workout_step_mesg.SetNotes(notes)

        workout_step_mesg.SetDurationType(duration_type)
        workout_step_mesg.SetDurationTime(duration_time)

        workout_step_mesg.SetTargetType(WktStepTarget.Open) # type: ignore
        
        workout_step_mesg.SetIntensity(Intensity.Warmup) # type: ignore

        return workout_step_mesg