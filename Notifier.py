# Creates a new Notifier to send MMS to personal phone number
# using Twilio API.
# To use this class, create a twilio account and enter the following
# values in the configurations.yml file
# sid: Twilio account SID
# token: Twilio project authorization token
# twilio_num: Twilio project phone number
# user_num: User phone number.
# imgur_id: The imgur client id

from twilio.rest import Client
import os
import pyimgur
import cv2

class Notifier:

	#Constructor for Notifier class
	def __init__(self, sid, token, twilio_num, user_num, imgur_id):
		self.sid = sid
		self.token = token
		self.twilio_num = twilio_num
		self.user_num = user_num
		self.imgur_id = imgur_id

	# Send new mms message with twilio and imgur API
	# Arguments:
	#	-frame: The video frame to be sent (CV2 video frame)
	def new_msg(self, frame, loc):
		img_file = "images/temp.jpg"

		# Convert cv2 frame to jpeg
		cv2.imwrite(img_file, frame)

		# Upload to imgur application
		imgr = pyimgur.Imgur(self.imgur_id)
		uploaded = imgr.upload_image(img_file, title="Security")

		# Create new Twilio client
		client = Client(self.sid, self.token)
		message = "Motion Detected at:" + loc
		
		# Send message
		msg = client.messages.create(
						body=message,
						from_=self.twilio_num,
						media_url=uploaded.link,
						to=self.user_num
					)
		Message sent, delete local image file
		os.remove(img_file)
