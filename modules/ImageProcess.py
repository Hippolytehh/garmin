import os
from typing import List
import pytesseract
import cv2
from PIL import Image
import numpy as np

class ImageProcess:

    def __init__(self, path: str, instructions: List[str]= []):

        if not os.path.exists(path):
            print(f"The following path '{path}' does not exist.")
            raise Exception("Path does not exist")
        
        if not (os.path.isfile(path) and path.lower().endswith(('.jpg', '.png'))):
            print(f"The file '{path} is not valid.")
            raise Exception("File not valid")

        self.path = path

        image_bgr = cv2.imread(self.path)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

        # Define blue range in HSV
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(image_hsv, lower_blue, upper_blue)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        self.instructions = instructions
        
        for cnt in contours[::-1]:

            x, y, w, h = cv2.boundingRect(cnt)
            if w > 100 and w < 200 and h > 100:  # Filter out small noise
                # Crop a horizontal strip to the right of the blue circle
                line_crop = image_rgb[y:y+h, x+w:x+w+1000] # Adjust width as needed

                # Convert to PIL Image for pytesseract
                pil_img = Image.fromarray(line_crop)

                text = pytesseract.image_to_string(pil_img)

                self.instructions.append(text.replace('\n', '').replace(' ', '').strip())

class BatchImageProcess:
    """
    Process multiple images once sorting alphabetically image basenames.

    Args:
    - paths: List[str] is a list of strings supporting both directories and files (ending with either '.jpg' or '.png' extensions).
    """

    def __init__(self, paths: List[str]):

        self.img_paths = set()
        
        for path in paths:

            if not os.path.exists(path):
                print(f"The following path '{path}' does not exist.")
                raise Exception("Path does not exist")
            
            if os.path.isfile(path) and path.lower().endswith(('.jpg', '.png')) and path not in self.img_paths:

                self.img_paths.add(path)

            elif path not in self.img_paths:
                    
                self.img_paths.update(
                    {
                        os.path.join(path, f) for f in os.listdir(path)
                        if os.path.isfile(os.path.join(path, f)) and f.lower().endswith(('.jpg', '.png')) and path not in self.img_paths
                    }
                )

        print(self.img_paths)

        self.img_paths = list(
            sorted(
                self.img_paths,
                key= lambda x: os.path.basename(x)
            )
        )

        print(self.img_paths)

        self.img_processes = [
            ImageProcess(path) for path in self.img_paths
        ]
    
    def print_all_instructions(self):

        for img_process in self.img_processes:
            print(
                img_process.instructions
            )

if __name__ == '__main__':

    batch_image_process = BatchImageProcess(
        paths= [
            "images/IMG_9245.PNG",
            "images/",
            "dll/",
            "/"
        ]
    )

    # batch_image_process.print_all_instructions()