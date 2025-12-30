# Installing Udacity simulator
Clone the Unity_2020_3 from the Udacity github (https://github.com/udacity/self-driving-car-sim)


## Training
Use Unity editor version 2020.3.0f1, download it from the unity hub

Open the simulator in training mode and drive the car for about 3 rounds to collect data

To start collecting data, press the record button on the top right that shows up in the training mode

Train the model using the training.ipynb
## Usage
Before running the proxy.js, make sure you have package.json and package-lock.json in the directory and run npm install to get the required packages for proxy.js to run

Run the the proxy.js and drive.py simultaneously after training the model

proxy.js acts as a middleware between drive.py and the Udacity simulator

In the Udacity simulator go into autonomous mode, and the car should start driving automatically
