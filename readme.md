# Info
This is a Python script that will send a notification to your iPhone when there are any new available time slots for the Bupa immigration medical examination.

# How to run
1. Download [Bark](https://apps.apple.com/au/app/bark-customed-notifications/id1403753865) from the iOS App Store. 
2. Download Chrome on your pc.
3. Create a `.env` file and put your Bark API key into it, following the `.env.example` file.
4. Install `miniconda` on your PC if you don't have it.
5. Run `sh oneclick.sh` in your terminal. The first time you run it, it will create a conda environment and install the required packages. After that, if you want to rerun it, just run `conda activate bupa && python scan.py`.
6. If you want to run it in the background, you could try `nohup sh oneclick.sh &`, but I haven't tested it yet. 😴