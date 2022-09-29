import glob
import os

from engine.processing import PngProcessing

def read_all_png_files():
    return glob.glob(os.path.join("image", "*.jpg"))


def main():
    proc = PngProcessing()
    for pngfile in read_all_png_files():
        print(pngfile)
        proc.run(Pngfile=pngfile)

if __name__ == "__main__":
    main()