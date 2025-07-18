import os
import re
import sys
from typing import List, Pattern, Callable

import clr
import os
clr.AddReference(os.path.abspath("dll/Fit.dll"))
from Dynastream.Fit import * # type: ignore

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from Swimming import SwimingWorkoutWarmup, SwimmingWorkout, SwimmingWorkoutStepRepeat, SwimmingWorkoutStepSwim, SwimmingWorkoutStepSwimRest

class InstructionsProcess:
    def __init__(self, instructions: List[str]):
        
        if not instructions:
            return
                
        self.pattern_handlers: List[tuple[Pattern, Callable[[re.Match], None]]] = []
        self.workout_steps = []
        self.message_index = 0

        self.instructions = instructions

        self._register_patterns()
        self.parse()

        print(f"Given instructions: {self.instructions}, parsed workout steps: {self.workout_steps}")

    def parse(self):
        for instruction in self.instructions:
            for pattern, handler in self.pattern_handlers:
                match = pattern.search(instruction)
                if match:
                    handler(match)
                    break
        return self.workout_steps
    
    def _register_patterns(self):
        self.pattern_handlers.append(
            (re.compile(r"Echauffementhorsdel'eau*:(\d+)min(.*)"), self._handle_warmup)
        )
        self.pattern_handlers.append(
            (re.compile(r"(\d+)mnageauchoix"), self._handle_choice)
        )
        self.pattern_handlers.append(
            (re.compile(r'(\d+)\s*[x×]\s*\((.*?)\)'), self._handle_repeat)
        )

    def _handle_warmup(self, match: re.Match):
        minutes = int(match.group(1))
        # type_text = match.group(2).strip()  # You can use this if needed
        self.workout_steps.append(
            SwimingWorkoutWarmup.create_workout_step_swim_warmup(
                message_index=self.message_index,
                name="Out of pool warmup",
                duration_time=minutes
            )
        )
        self.message_index += 1

    def _handle_choice(self, match: re.Match):
        distance = int(match.group(1))
        self.workout_steps.append(
            SwimmingWorkoutStepSwim.create_workout_step_swim(
                message_index=self.message_index,
                distance=distance,
                swim_stroke= SwimStroke.Freestyle  # type: ignore
            )
        )
        self.message_index += 1

    def _handle_repeat(self, match: re.Match):
        times = int(match.group(1))
        tasks = match.group(2).strip().split(";")
        start_index = self.message_index

        for task in tasks:
            task = task.strip()

            pattern_distance = re.search(r'(\d+)\s*m\s*(.*)', task, re.IGNORECASE)
            if pattern_distance:
                distance = int(pattern_distance.group(1))
                # swim_type = pattern_distance.group(2).strip().lower()  # If needed
                self.workout_steps.append(
                    SwimmingWorkoutStepSwim.create_workout_step_swim(
                        message_index=self.message_index,
                        distance=distance,
                        swim_stroke=SwimStroke.Invalid  # type: ignore
                    )
                )
                self.message_index += 1

            pattern_rest = re.search(r'(\d+)\s*s\s*récup', task, re.IGNORECASE)
            if pattern_rest:
                rest_time = float(pattern_rest.group(1))
                self.workout_steps.append(
                    SwimmingWorkoutStepSwimRest.create_workout_step_swim_rest(
                        message_index=self.message_index,
                        duration_time=rest_time
                    )
                )
                self.message_index += 1

        self.workout_steps.append(
            SwimmingWorkoutStepRepeat.create_workout_step_repeat(
                message_index=self.message_index,
                repeat_from=start_index,
                repetitions=times
            )
        )
        self.message_index += 1

if __name__ == '__main__':

    test = InstructionsProcess(
        instructions=[
            "Echauffement hors de l'eau: 10 min",
            "200m nage au choix",
            "4 x (50m crawl; 15s récupération)",
            "3 x (100m dos; 20s récupération)"
        ]
    )