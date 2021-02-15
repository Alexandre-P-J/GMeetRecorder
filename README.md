# Google Meet Recorder
<img src="./logo.svg" alt="Google Meet Recorder logo" height="200"/><p>Attend and record google meet calls automatically.</p>
## Backends
 - UPC (polytechnic university of catalonia)
 - Gmail
 - Other Organizations that use the Google suite: By request.
## Instructions
This software only requires [docker-compose](https://docs.docker.com/compose/install "Install docker-compose") and it should run on any platform supported by docker.
### Installation:
 - This project runs entirelly on a docker container, ensure your SO has [docker-compose](https://docs.docker.com/compose/install "Install docker-compose") installed.
 - Download or clone this repository.
 - Open a terminal in the project directory or `cd THIS_PROJECT_FOLDER`
 - Run `docker-compose build`
 - It may take up to several minutes depending on your internet connection.
### Execution:
After the installation you may execute the software. Although the program
can be run from terminal using `docker-compose up`, a common usecase is to set up `cron` or system equivalent
to automate temporized executions.
#### Arguments:
 - `BACKEND` Options are `upc` and `gmail`. Defaults to `gmail`.
 - `EMAIL` **Required**.
 - `ORG_USER` **Required if `BACKEND` is not `gmail`**.
 - `PASSWORD` **Required**.
 - `MEET_URL` **Required**.
 - `VIDEO_NAME` Defaults to `video`.
 - `OUTPUT_DIR` Defaults to the project directory.
 - `MAX_DURATION` The maximum meet duration. Defaults to `7200` (2h).
 - `MIN_DURATION` The minimum meet duration. Defaults to `1800` (30m).
 - `ASK_JOIN` Whether asking to join a class is allowed for the bot. Defaults to True.
 - `FRAC_TO_EXIT` The required fraction of people that already left the meet call to leave the call. `MIN_DURATION` must have been already exceeded. Defaults to `0.90` (90%).
 - `FPS` Recording frames per second, if the streaming consists in a presentation a low value (15 or less) is encouraged to reduce video size and cpu usage. Defaults to `25`.
 - `RESOLUTION` Recording resolution, Defaults to `1920x1080`.

#### Example:
Record a call using UPC credentials with a duration between 60 and 120 seconds (the bot may exit if 83% of the people already left) into `~/CoolFolder/vid_1_23_45.webm`.

Inside the project directory run:
`BACKEND=upc EMAIL=john.smith@estudiantat.upc.edu ORG_USER=john.smith PASSWORD='h4k3rm4n1234' MEET_URL=https://meet.google.com/eas-tere-ggy MIN_DURATION=60 MAX_DURATION=120 OUTPUT_DIR=~/CoolFolder VIDEO_NAME=vid_1_23_45 FRAC_TO_EXIT=0.83 docker-compose up`

## FAQ
> How can i fully automate recordings?
>> There are many tools for task scheduling, for Linux you may want to check `cron`, for MacOS either `launchd` or `cron` and for Windows `Task Scheduler`.

> My organization requires its own login and doesn't have a supported backend, what can i do?
>> I encourage you to try implement it yourself and maybe do a PR to include it in the project officially, but you can aswell write an issue asking for it.

> What can I do if the software doesnt work?
>> If it doesnt work due to an invalid argument it might print what's the issue or report a stacktrace, if its due to an incorrect argument like a wrong password it will still record a video that shows what went wrong. If the problem is none of the above (a bug perhaps) feel free to report the issue or open a PR if you managed to fix it. 