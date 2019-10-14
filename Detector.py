import cv2
import numpy
from imutils.video import VideoStream
import imutils
import time
from Notifier import Notifier
import yaml

class Detector:
    def __init__(self, camera_src, input_file = None):
        ymlfile = open("configurations.yml", 'r')
        self.config = yaml.safe_load(ymlfile)

        if camera_src is not None:
            self.vid = cv2.VideoCapture(0)
        else:
            self.vid = cv2.VideoCapture(input_file)

        self.last = None
        self.executeStreamLoop()


    #Function that executes detection logic
    def executeStreamLoop(self):
        if (self.vid.isOpened() == False):
            print("Error opening video stream")

        _, background = self.vid.read()
        background = self.processImage(background)

        while(True):
            ret, frame = self.vid.read()

            #video stream has ended
            if ret is False:
                break

            proc_frame = self.processImage(frame)

            # Compute absolute difference, threshold pixel values and dilate
            diff = cv2.absdiff(background, proc_frame)
            (_, thresh) = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

            kernel = numpy.ones((5,5), numpy.uint8)
            eroded = cv2.erode(thresh, kernel, iterations = 4)
            dilated = cv2.dilate(eroded, kernel, iterations = 4)

            # Find object contours
            (contours, _) = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            frame = imutils.resize(frame, width = 500)
            contour_frame = frame.copy()

            for c in contours:
                # Non-significant objects discarded
                if cv2.contourArea(c) < 14000:
                    continue

                # Draw rectangles around moving objects
                cv2.drawContours(contour_frame, c, 0, (0,0,255),2)
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(contour_frame, (x, y), (x + w,y + h), (0, 255, 0), 2)


                if self.last:
                    seconds_elapsed = time.monotonic() - self.last
                    # make sure that the same detection is not sent to user twice
                    if seconds_elapsed > 15:
                        self.last = time.monotonic()
                        self.upload(contour_frame)
                else:
                    self.last = time.monotonic()
                    self.upload(contour_frame)

            cv2.imshow("Video Feed with Contours", contour_frame)
            cv2.waitKey(25)

        self.vid.release()
        cv2.destroyAllWindows()


    # Processes Image for contour detection
    # -> Resizes image
    # -> Converts to grayscale and applies Gaussian blur
    def processImage(self, frame):
        frame = imutils.resize(frame, width = 500)
        # BGR -> Grayscale
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Grayscale -> GaussianBlur
        g_blur = cv2.GaussianBlur(grayscale,(9, 9),0)
        return g_blur


    # # Uploads image to imgur application, to be sent as MMS.
    # #   ** IMPORTANT: ADD Twilio Credentials for notifier to work **
    def upload(self, frame):
        notify = Notifier(self.config['not']['sid'],self.config['not']['token'],self.config['not']['twilio_number'],
        self.config['not']['usr_number'],self.config['not']['imgur_client_id'])
        notify.new_msg(frame, self.config['main']['location_name'])


