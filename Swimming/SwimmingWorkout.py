import config

import clr
import os
import System.Reflection # type: ignore
clr.AddReference(os.path.abspath(config.FIT_DLL))
from Dynastream.Fit import * # type: ignore
clr.AddReference("System.IO") # type: ignore
clr.AddReference("System") # type: ignore
from System.IO import FileStream, FileMode, FileAccess, FileShare # type: ignore
import System # type: ignore
from typing import List

import random

def create_workout(
        workout_mesg,
        workout_steps: List[WorkoutStepMesg] # type: ignore
    ) -> None:
    
    file_type = File.Workout # type: ignore
    manufacturer_id = Manufacturer.Decathlon # type: ignore
    product_id = 0
    serial_number = random.randint(0, 2**32 - 1)

    file_id_mesg = FileIdMesg() # type: ignore
    file_id_mesg.SetType(file_type)
    file_id_mesg.SetManufacturer(manufacturer_id)
    file_id_mesg.SetProduct(product_id)
    file_id_mesg.SetTimeCreated(DateTime(System.DateTime.UtcNow)) # type: ignore
    file_id_mesg.SetSerialNumber(serial_number)

    os.makedirs('./fits', exist_ok=True)
    fit_dest = FileStream(f"./fits/{workout_mesg.GetWktNameAsString().replace(' ', '_')}.fit", FileMode.Create, FileAccess.ReadWrite, FileShare.Read) # type: ignore
    
    encoder = Encode(ProtocolVersion.V10) # type: ignore

    encoder.Open(fit_dest)

    encoder.Write(file_id_mesg)
    encoder.Write(workout_mesg)

    for workout_step in workout_steps:
        encoder.Write(workout_step)

    encoder.Close()

    fit_dest.Close()

    print(f"Encoded FIT file {fit_dest.Name}")