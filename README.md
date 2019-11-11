# What the Punch?
## Boxing Workout Assistant

## Overview
How do the top performing athletes get to the top of their game and consistently improve their performance?

They look at the data.

Quantification of workouts and training allows the athlete to identify strengths, weaknesses, and improvements of their chosen craft.

The purpose of this capstone is to create a feedback system that gives the user insight into their boxing workouts.

Main focus from a data science perspective is to measure quantitative attributes to each punch and classify each signature into a specific strike (jab, cross, hook, uppercut, etc.) using a Tensor Flow based LSTM Recursive Neural Network.

Data stream will then be analyzed post workout to determine quantity and quality of each strike.  
Future work includes making an app that can track and display results in real time from streaming data.

## Potential use of system:
- Provide feedback to user about quality of workout and establish baseline data about fitness level at different points in time
- Combine with heart rate sensor to see relationship between fatigue and quality of hit
- Generate custom training workout regimine that is user specific
- Gamification of workouts based on user dealing a certain amount of "damage" to the bag
- Ideally be able to critique form when compared to professionals and recommend exercises and drills to improve


# Project Workflow

## DATA GATHERING METHODOLOGY

In order to gather data about punches, a typical set of 12oz boxing gloves were expertly fitted with sensors that captured 3 axis of accelerometer data and gyroscopic data that synced via bluetooth to a smartphone.

![Gloves with Sensors](images/Golden_Gloves.png)

The data is then backed up to a cloud service and downloaded locally for processing.

![MetaCloud](images/MetaCloud.png)

Sensors were purchased from www.mbientlab.com

Scope that behind the scenes action:

![DATA](images/matt_punch.gif)


## Initial Data

Here is an example of what an workout session consisting of 100 left hand jabs looks like:

![100 Jabs](images/100_Jabs.png)

The overall magnitude of acceleration was calculated by combining info from each X, Y, and Z axis.

Let's zoom into a smaller example of a session consisting of only 10 jabs.

![10 Jab](images/10_Jabs.png)

Punch "event" occurrances can be easily identified by looking for the spikes in magnitude of overall acceleration.  We can then record the timestamp of each of these events.

![10 Jab Test](images/10_Jab_Test.png)

If we zoom into each punch occurance and take a snapshot of the window of events slightly prior and post the peak magnitude event, we can determine a signature of this event to be classified into a specific strike and determine other metrics such as impact force and hand speed.  Basically, at this point we know a punch occurred, but we don't know what kind.

## Comparison of Different Strikes - Combined Magnitude Accelerometer

Let's take a look at the combined magnitude of multiple occurrances of specific punches overlaid on top of each other:

### Left Jab
![200 Jabs](images/200LJ.png)

### Right Cross
![200 Cross](images/200RC.png)

### Left Hook
![200 Hooks](images/200LH.png)

### Right Hook
![150 Hooks](images/150RH.png)

Note: These are COMBINED magnitudes of acceleration from 3 axes and shown for demonstrational purposes.  The classification model discussed later will take data inputs of the individual axis separately to not lose any info.  Also, variace of the left hook data could stem from windowization of the events.  Will be discussed in the future work section.

## Comparison of Different Strikes - Gyroscopic Data

Angular acceleration is also captured by the sensor.  In the below graphs, blue corresponds to deg/s in the X-Axis, red to Y, green to Z.

### Jab
![50 Jabs Velo](images/50JabsAngularVelo.png)

### Hook
![50 Hooks Velo](images/50HooksAngularVelo.png)

### Cross
![50 Cross Velo](images/50CrossesAngularVelo.png)

Common signatures for each strike can be visually identified already.  Should be light work for the TF LSTM RNN.

## DATA PROCESSING

In the one week timeframe of this project, ~4000 punches were recorded from 10 individuals across ~70 sessions to create the intial dataset.  Shout out to my Galvanize Fam.

Cleaning Workflow:
- Accelerometer and Gyroscopic data were combined for each session
- Events were identified and windows were recorded
- Processed session info was pickled and stored for future use

All of this is automated via the cleaning_data.py and folder organization.

Selected data can then be loaded into a single list for further processing prior to modeling.  This is to achieve flexibility for various tests (selected punches only / selected users only / other things you can think of / etc.)

Pickled data is put into the "load data" directory to be picked up automatically by the load_data.py script which proceeds to:

- Combine all data into a single numpy array
- Standardize data 
- Generate labels

At this point we are ready to feed the model.

## MODELING

Since we are concerned with time series data, 



