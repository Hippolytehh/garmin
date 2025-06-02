import config

import clr
import os
import System.Reflection # type: ignore
from Dynastream.Fit import * # type: ignore
clr.AddReference(os.path.abspath(config.FIT_DLL))


def create_workout_step_swim_rest(
        message_index: int,
        duration_type: WktStepDuration= WktStepDuration.Open, # type: ignore
        duration_time: float= None
    ) -> WorkoutStepMesg: # type: ignore

    workout_step_mesg = WorkoutStepMesg() # type: ignore
    workout_step_mesg.SetMessageIndex(message_index)

    workout_step_mesg.SetDurationType(duration_type)
    workout_step_mesg.SetDurationTime(duration_time)

    workout_step_mesg.SetTargetType(WktStepTarget.Open) # type: ignore
    
    workout_step_mesg.SetIntensity(Intensity.Rest) # type: ignore

    return workout_step_mesg
