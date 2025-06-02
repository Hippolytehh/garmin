import config

import clr
import os
import System.Reflection # type: ignore
from Dynastream.Fit import * # type: ignore
clr.AddReference(os.path.abspath(config.FIT_DLL))

def create_workout_step_repeat(
        message_index: int, 
        repeat_from: int, 
        repetitions: int
    ) -> WorkoutStepMesg: # type: ignore
    
    workout_step_mesg = WorkoutStepMesg() # type: ignore
    workout_step_mesg.SetMessageIndex(message_index)

    workout_step_mesg.SetDurationType(WktStepDuration.RepeatUntilStepsCmplt) # type: ignore
    workout_step_mesg.SetDurationValue(repeat_from)

    workout_step_mesg.SetTargetType(WktStepTarget.Open) # type: ignore
    workout_step_mesg.SetTargetValue(repetitions)

    return workout_step_mesg