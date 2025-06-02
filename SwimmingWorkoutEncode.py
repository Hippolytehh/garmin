# import sys, os
# sys.path.append(os.path.abspath(".."))

import config

import clr
import os
import System.Reflection # type: ignore
clr.AddReference(os.path.abspath(config.FIT_DLL))
from Dynastream.Fit import * # type: ignore

from Swimming import SwimmingWorkout, SwimmingWorkoutStepRepeat, SwimmingWorkoutStepSwim, SwimmingWorkoutStepSwimRest

def create_pool_swim_workout():

    workout_steps = []

    # step 0 - warmp up -> any style
    workout_steps.append(
        SwimmingWorkoutStepSwim.create_workout_step_swim(
            message_index= len(workout_steps),
            distance= 200,
            intensity= Intensity.Warmup # type: ignore
        )
    )

    # step 1 - rest until lap button is pressed
    workout_steps.append(
        SwimmingWorkoutStepSwimRest.create_workout_step_swim_rest(
            message_index= len(workout_steps)
        )
    )

    # step 2 -> swimming (drill)
    workout_steps.append(
        SwimmingWorkoutStepSwim.create_workout_step_swim(
            message_index= len(workout_steps),
            distance= 400,
            swim_stroke= SwimStroke.Drill, # type: ignore
            equipment= WorkoutEquipment.SwimKickboard # type: ignore
        )
    )

    # step 3 - rest until lap button is pressed
    workout_steps.append(
        SwimmingWorkoutStepSwimRest.create_workout_step_swim_rest(
            message_index= len(workout_steps)
        )
    )

    # repetition
    # step 4 - swim freestyle
    workout_steps.append(
        SwimmingWorkoutStepSwim.create_workout_step_swim(
            message_index= len(workout_steps),
            distance= 200,
            swim_stroke= SwimStroke.Freestyle # type: ignore
        )
    )
    # step 5 - rest 2 minutes
    workout_steps.append(
        SwimmingWorkoutStepSwimRest.create_workout_step_swim_rest(
            message_index= len(workout_steps),
            duration_type= WktStepDuration.RepetitionTime, # type: ignore
            duration_time= 120.0
        )
    )
    # step 6 - repeat 5 times
    workout_steps.append(
        SwimmingWorkoutStepRepeat.create_workout_step_repeat(
            message_index= len(workout_steps),
            repeat_from= 4,
            repetitions= 5
        )
    )

    # step 7 - rest until lap button is pressed
    workout_steps.append(
        SwimmingWorkoutStepSwimRest.create_workout_step_swim_rest(
            message_index= len(workout_steps)
        )
    )

    workout_steps.append(
        SwimmingWorkoutStepSwim.create_workout_step_swim(
            message_index= len(workout_steps),
            distance= 100,
            intensity= Intensity.Cooldown # type: ignore
        )
    )

    workout_mesg = WorkoutMesg() # type: ignore
    workout_mesg.SetWktName("Pool Swim Python")
    workout_mesg.SetSport(Sport.Swimming) # type: ignore
    workout_mesg.SetSubSport(SubSport.LapSwimming) # type: ignore
    workout_mesg.SetPoolLengthUnit(DisplayMeasure.Metric) # type: ignore
    workout_mesg.SetPoolLength(50)
    workout_mesg.SetNumValidSteps(len(workout_steps))
    
    SwimmingWorkout.create_workout(workout_mesg, workout_steps)

def decode_to_json():

    os.makedirs('./jsons', exist_ok=True)

    from garmin_fit_sdk import Decoder, Stream
    import garmin_fit_sdk
    import json

    stream = Stream.from_file("./fits/Pool_Swim_Python.fit")
    decoder = Decoder(stream)
    messages, errors = decoder.read()

    with open('./jsons/Pool_Swim_Python.json', 'w') as f:
        json.dump(messages, f, default= str)
        print("Decoded messages to Pool_Swim_Python.json")

if __name__ == '__main__':

    create_pool_swim_workout()

    decode_to_json()