import subprocess
import pytesseract
from PIL import Image
import os
import sys

BASH_SCRIPT_PATH = 'convert.sh'
class TextConverter():
    @property
    def pmids(self):
        try:
            return self._pmids
        except:
            directory = os.listdir('data/')
            pmids = list()
            for file in directory:
                if file.startswith('.DS'):
                    continue
                pmids.append(file.split()[0])
            self._pmids = pmids
        return self._pmids
    
    def convert(self, input_dir='images/', output_dir='results/', run_bash='True'):
        # Execute the bash script to unlock the images
        if run_bash:
            subprocess.run(['bash', BASH_SCRIPT_PATH])
        # Gather all images and create the right text files
        images = os.listdir(input_dir)
        for image in images:
            if image.startswith('.DS'):
                continue
            index = image.split('.')[0].split('-')[-1]
            new_file_name = '{}{}'.format(input_dir, image.replace('-{}'.format(index), '-{}'.format(index.zfill(2))))
            os.rename('{}{}'.format(input_dir, image), new_file_name)
        images = sorted(os.listdir('{}'.format(input_dir)))

        # Store all pdfs in one data structure
        texts = [[]] * len(self.pmids)
        # For all pmids, turn the image into text
        for i, pmid in enumerate(self.pmids):
            for image in images:
                if image.startswith(pmid):
                    texts[i].append(pytesseract.image_to_string(Image.open('{}{}'.format(input_dir, image))))
        
        # Output a text file per pdf
        for i in range(len(self.pmids)):
            outfile = "{}{}.txt".format(output_dir, self.pmids[i])
            with open(outfile, "w") as f:
                for line in texts[i]:
                    f.writelines(line)
        
def main():
    tc = TextConverter()
    if len(sys.argv) == 1:
        tc.convert()
    else:
        tc.convert(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
