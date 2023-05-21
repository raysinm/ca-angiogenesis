# Cellular Automata Model of Angiogenesis
### Simulating the emergence of new blood vessels using discrete cellular automata with accordance to the classical model of angiogenesis.

By Matan Hoory and Maya Raysin

![alt text](./logo.png)

## Table of Contents

- [Introduction](#introduction)
- [Usage](#usage)
- [Installation](#installation)


## Introduction

To simulate angiogenesis, we implemented a cellular automaton based on two driving forces:
The chemical gradient created by the concentrations of the growth factor (VEGF), and the
mechanical pressure exerted by cells. We used a finite lattice, which hosted three different
types of cells, each following a different set of probabilistic rules which were applied synchronously:
* Attractor Cells (blue): These cells represent locations that require blood such as new or injured
tissue, or cancer cells. They increase the concentration of VEGF in their surroundings in
relation to the distance. Meaning that as you get closer to the attractor, the concentration
rises.
* Stalk Cells (red): Proliferative cells that act as the main building block of the blood vessel. By
proliferation, they are able to create Tip Cells during a process called sprouting.
* Tip Cells (yellow): Migratory cells that migrate along the gradient of VEGF. In the biological system, the
tip cells are physically attached to the stalk cells. In our model, we use a simplification in
which the movement of tip cells creates a trail of stalk cells.  

See project report for more information.  

## Installation
First, clone the repository via git clone to your desired directory.
```
git clone https://github.com/raysinm/ca-angiogenesis.git  
```

### Option A: Docker Compose - RECOMMENDED
1. Install docker and docker-compose on your machine. We recommend running linux or wsl2 for that matter. 
See official docker docs: 
  - Docker engine: https://docs.docker.com/engine/install/
  - Docker compose: https://docs.docker.com/compose/install/

2. Simply run the following command from the main directory:
```
docker-compose up
```
This will pull the latest docker images of the engine and the web client from dockerhub, set all configurations needed and will run the container.

### Option B: Local Docker Build
As in option A, you will need docker installed on your machine.
Next, go to the /docker directory and perform docker-compose up as before:
```
cd docker/
docker-compose build && docker-compose up
```
This will build the images locally instead of pulling them from dockerhub. The yml file will configure everything for you and will run the application.

### Option C: Manual Setup (No Docker)
If you do not want to run via docker and docker-compose, you can still run the web app directly from your computer. 
We recommend using a python 3.10 virtual environment and installing the following requirements (available in /requirements.txt):
```
grpcio==1.53.0
ipython==8.13.2
protobuf==4.21.12
Flask==2.3.2
numpy==1.24.2
matplotlib==3.7.1
pandas==2.0.1
Pillow==9.5.0
```
1. In /engine directory run:
```
python3 engine_server.py
```
2. In a seperate window, in /web directory run:
```
export FLASK_MANUAL_RUN=1
flask run
```

### Option D: Manual Visualization
This option does not use the web app in this git repository. We recommend having python>=3.8 and the following requirements installed:
(specified in /requirements_option_d.txt)
```
numpy==1.24.2
matplotlib==3.7.1
pandas==2.0.1
```

## Usage

### Options A+B:
1. Make sure that 'docker-compose up' command did not fail and that the flask server is running.
2. Open a new browser window and enter "https://localhost"
3. Follow the instructions inside
4. Enjoy!

### Option C:
1. Make sure that the engine-server is showing "Engine server running".
2. Make sure that the flask service is running in a seperate window.
3. Open a new browser window and enter "https://localhost:5000"
4. Follow the instructions and enjoy!

### Option D:

Simply go to engine/main.py and follow the unstructions.
Parameter configurations can be manually inputted in engine/config.json.
Run the following line from engine/ to show the results:
```
python3 main.py
```

See project report for more information on usage and methods, and the meaning behind them.


