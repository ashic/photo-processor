import fire
import os
from exif import Image as ExifImage
from PIL import Image as PillowImage
from PIL import ExifTags
import json

def fix_photographed_date(dir: str, file: str):
    path = os.path.join(dir, file)

    if not os.path.isfile(path):
        return 
    
    try:
        with PillowImage.open(path) as pillow_img:
            img_exif = pillow_img.getexif()
        

            if img_exif.get(ExifTags.Base.DateTimeOriginal):
                img_exif[ExifTags.Base.DateTime] = img_exif[ExifTags.Base.DateTimeOriginal]

                out_dir = os.path.join(dir, 'out')
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)

                out_path = os.path.join(out_dir, file)
                pillow_img.save(out_path, exif=img_exif)
                print(f'..saved {out_path}') 
    except:
        print(f'..could not process {path}. Likely a non-image file.')

    


class Processor:

    def fix_date(self, path: str):
        for file in os.listdir(path):
                fix_photographed_date(path, file)
            
            


if __name__ == '__main__':
    fire.Fire(Processor)