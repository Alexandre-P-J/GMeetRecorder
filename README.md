# Google Meet Bot
Attend and record google meet sessions automatically.
## Backends
 - UPC: Right now the only supported account type.
 - Google Mail: WIP.
 - Other Organizations that use the Google suite: By request.
## Instructions
This software only requires `docker-compose` and its dependencies.
### Installation:
 - Download or clone this repository.
 - `cd THIS_PROJECT_FOLDER`
 - `docker-compose build`
 - It may take up to several minutes depending on your internet connection.
### Execution:
After the installation you may execute the software. Although the program
can be run from terminal using `docker-compose up`, a common usecase is to set up `cron` or system equivalent
to automate temporized executions.
#### Arguments:
 - `EMAIL` **Required**.
 - `USER` **Required**.
 - `PASSWORD` **Required**.
 - `MEET_URL` **Required**.
 - `VIDEO_NAME` Defaults to `video`.
 - `OUTPUT_DIR` Defaults to the project directory.
 - `MAX_DURATION` The maximum meet duration. Defaults to `7200` (2h).
 - `MIN_DURATION` The minimum meet duration. Defaults to `1800` (30m).
 - `FRAC_TO_EXIT` The required fraction of people that already left the meet call to leave the call. `MIN_DURATION` must have been already exceeded. Defaults to `0.90` (90%).
 - `FPS` Recording frames per second, if the streaming consists in a presentation a low value (15 or less) is encouraged to reduce video size and cpu usage. Defaults to `25`.
 - `RESOLUTION` Recording resolution, Defaults to `1920x1080`.

#### Example:
Record a class with a duration between 60 and 120 seconds (the bot may exit if 83% of the people already left) into `~/CoolFolder/vid_1_23_45.webm`.

Inside the project directory run:
`EMAIL=john.smith@estudiantat.upc.edu USER=john.smith PASSWORD=h4k3rm4n1234 MEET_URL=https://meet.google.com/eas-tere-ggy MIN_DURATION=60 MAX_DURATION=120 OUTPUT_DIR=~/CoolFolder VIDEO_NAME=vid_1_23_45 FRAC_TO_EXIT=0.83 docker-compose up`

Notice that personal data is passed using environment variables, you may want to take this into account if you plan on running the software on untrusted devices.