# Info
This is a Python script that will send a notification to your iPhone when there are any new available time slots for the Bupa immigration medical examination.

# How to run
1. Download Bark from the iOS App Store.
2. Create a `.env` file and put your Bark API key into it, following the `.env.example` file.
3. Install `miniconda` on your PC if you don't have it.
4. Run `sh oneclick.sh` in your terminal. The first time you run it, it will create a conda environment and install the required packages. After that, if you want to rerun it, just run `conda activate bupa && python scan.py`.
5. If you want to run it in the background, you could try `nohup sh oneclick.sh &`, but I haven't tested it yet. 😴