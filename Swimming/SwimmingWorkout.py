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

from garmin_fit_sdk import Decoder, Stream
import json

class SwimmingWorkout:

    def __init__(
            self,
            workout_mesg: WorkoutMesg, # type: ignore
            workout_steps,
            fits_folder: str= "./fits",
            jsons_folder: str= "./jsons",
            file_type: File = File.Workout, # type: ignore
            manufacturer_id = Manufacturer.Decathlon, # type: ignore
            product_id: int= 0,
            serial_number: int = random.randint(0, 2**32 - 1)
        ):
        
        self.workout_mesg = workout_mesg
        self.workout_steps = workout_steps

        self.fits_folder = fits_folder
        self.jsons_folder = jsons_folder

        self.activity_name = self.workout_mesg.GetWktNameAsString().replace(' ', '_')

        self.file_id_mesg = FileIdMesg() # type: ignore
        self.file_id_mesg.SetType(file_type)
        self.file_id_mesg.SetManufacturer(manufacturer_id)
        self.file_id_mesg.SetProduct(product_id)
        self.file_id_mesg.SetTimeCreated(DateTime(System.DateTime.UtcNow)) # type: ignore
        self.file_id_mesg.SetSerialNumber(serial_number)

        self.is_encoded = False

    def encode_fit(self):

        os.makedirs(self.fits_folder, exist_ok=True)
        
        self.fit_path = f"{self.fits_folder}/{self.activity_name}.fit"

        fit_dest = FileStream(self.fit_path, FileMode.Create, FileAccess.ReadWrite, FileShare.Read) # type: ignore
        
        encoder = Encode(ProtocolVersion.V10) # type: ignore

        encoder.Open(fit_dest)

        encoder.Write(self.file_id_mesg)
        encoder.Write(self.workout_mesg)

        for workout_step in self.workout_steps:
            encoder.Write(workout_step)
        
        print(f"Encoded messages to '{self.fit_path}.fit'")

    def decode_as_json(self):

        os.makedirs(self.jsons_folder, exist_ok=True)

        if not self.is_encoded:
            self.encode_fit()
                    
        stream = Stream.from_file(self.fit_path)
        decoder = Decoder(stream)
        messages, errors = decoder.read()
        
        with open(f"{self.jsons_folder}/{self.activity_name}.json", 'w') as f:
            json.dump(messages, f, default= str)
            print(f"Decoded messages to '{self.activity_name}.json'")