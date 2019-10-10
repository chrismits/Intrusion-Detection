# Camera motion detection system. Run this script to start main logic

from Detector import Detector
import yaml



def main():
    print("""Intrusion Detection Camera System enabled. 
            (Optional) Open configurations.yml to update your preferences""")

    yml = yaml.safe_load(open("configurations.yml", "r"))



    detector = Detector(None, yml['main']['input_video'])

if __name__ == "__main__":
    main()