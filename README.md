# Intrusion-Detection

Intrusion Detection system for security cameras. If a camera feed detects motion, the user will be notified via text message, along with an imnage of the perpetrator.

Demo can be seen here: ENTER YOUTUBE LINK

## Setup:

* Note: Because this project is still in a preliminary phase, it assumes that the user has a twilio user account with a demo project set up and a pyimgur user account.

To start with, clone this project using:

    git clone https://github.com/chrismits/Intrusion-Detection.git


Navigate to the main directory of the newly cloned repository and open the **configurations.yaml** file. There you can set your preferences for text notifications and initial setup. The configuration file will look like this:

    not:
        notified: "True"
        sid: "twilio sid"
        token: "twilio token"
        twilio_number: "twilio number"
        usr_number: "your number"
        imgur_client_id: "your imgur client id"

    main:
        input_video: "videos/sample1.mov"
        camera_src: "Choose camera source: with webcam enter 0"
        location_name: "Enter location name"



Note: To opt out of notifications, simply set notified to "False"

You should see a script called **main.py**. In your python environment run python3 main.py
