import clr
import System.Reflection
import config
clr.AddReference(config.FIT_DLL)
assembly = System.Reflection.Assembly.Load("Fit")
types = assembly.GetTypes()
for t in types:
    if t.IsClass and t.IsPublic:
        print(f"\nClass: {t.Name}")
        methods = t.GetMethods()
        for method in methods:
            print(f"    Method: {method.Name}")

from Dynastream.Fit import WorkoutStepMesg, WorkoutMesg, Sport, SubSport, DisplayMeasure, CreateWorkoutStepSwim
from WorkoutEncode import CreateWorkoutStepSwim
class Parameters:
   class POOL_SIZE:
        semi_olympic_25 = 25
        olympic_50 = 50 # 25 yards
        yards_25 = 22.86


def main():
    
    workout_step_msgs = []

    workout_step_msgs.append(
        CreateWorkoutStepSwim()
    )

    workout_mesg = WorkoutMesg()
    workout_mesg.SetSport(Sport.Swimming)
    workout_mesg.SetSubSport(SubSport.LapSwimming)
    workout_mesg.SetPoolLength(Parameters.POOL_SIZE.olympic_50)
    workout_mesg.SetPoolLengthUnit(DisplayMeasure.Metric)


if __name__ == "__main__":
    main()
    