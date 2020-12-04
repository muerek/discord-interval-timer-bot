# Discord Interval Timer Bot

This is a simple Python-based bot for Discord. It provides an interval timer with voice announcements designed to be used for HIIT workouts, for example. The timer will run for a specified number of intervals. Each interval has a work phase and a rest phase.

## Setup and run
Always do this:
1. Create an application and add a bot to it in the [Discord developer portal](https://discord.com/developers/applications).
1. Get the bot token from the dashboard.

Then either do that to run the bot inside a container:
1. Build a docker image using the dockerfile in this repository.
1. Run the docker image and pass the bot token to the container as a environment variable named `BOT_TOKEN`, i.e. run `docker run -e BOT_TOKEN=<token> <image> `.

Or do that to run the bot outside a container:
1. Store the bot token either in an environment variable named `BOT_TOKEN` or add it under the same name to an `.env` file in the project root. The bot is already set up to pick up `.env` files.
1. Install [FFmeg](https://ffmpeg.org/) as it is required for audio processing.
1. Install the necessary Python packages with `python -m pip install -r requirements.txt`.
1. Run `interval_timer_bot.py`.

## Usage
Here is a typical workflow:
1. Login to Discord, go to a server with the bot and join a voice channel.
1. Summon the bot to your voice channel with `!voice` in any text channel on that server.
1. Start a timer using `!start 4 45 15`, for example, for four repetitions of 45 seconds work and 15 seconds rest each.
1. The bot will give you 17 seconds to prepare, then... workout!
1. Grab some water and prepare for another set of exercises, then use `!restart` to start the timer again.
1. If things go sideways, use `!stop` to stop the bot from shouting at you.
1. Clean up after you are done by using `!mute` to end your voice session with the bot.

If the bot is part of a voice channel, it will let you know about the current state of the timer. The bot broadcasts the following in the voice channel:
- An announcement when the timer is started.
- A countdown for the last three seconds in the preparation phase and each work and rest phase.
- A reminder to prepare yourself five seconds before the end of a rest phase.
- A bell halfway through a work phase 30 seconds or longer.
- An announcement when the timer is done after the last interval has been completed.

If the bot is not part of a voice channel, well, it does not do much for you.

For a more detailed documentation, see below or use the `!help` command with the bot to see the auto-generated documentation. The latter is automatically generated from the code and is therefore always up-to-date while the below may miss some new stuff.

Command | Usage
---|---
`!hello` | Bot says hello back.
`!start <reps> <work> <rest>` | Starts the timer. The number of intervals is specified as `<reps>`, the seconds of work and rest in each interval as `<work>` and `<rest>` respectively. There is a 17 second preparation phase before the first interval starts.
`!stop` | Stops the timer if it is running.
`!restart` | Starts the timer. The number of intervals and seconds of work and rest are taken from the previous timer run. If there are no previous runs, the timer has default values. There is a 17 second preparation phase before the first interval starts.
`!show` | Shows the current settings of the timer. You can use this to verify that a `!restart` actually does what you want.
`!voice` | Summons the bot to a voice channel. The bot will follow the user issuing this command into their current voice channel.
`!mute` | Makes the bot leave its voice channel. Note that the timer itself is not affected, but keeps running. Voice announcements resume if the bot is summoned again.

## Limitations
- **Major:** The bot can only run a single timer at all times, across different voice channels and different servers as well. The timer is currently implemented as a global object and is therefore shared between all users.
- The bot does not provide precise time measurements. API rate limiting, network latency or losses may cause occasional hiccups and can hardly be avoided. The way the timer is implemented can also cause a little time skew in the long run. However, the typical usage for HIIT workouts should not be affected since those do not have the timer running for hours, and the network-related delays are probably more impactful.
- The bot seems to work, but I do not trust myself. I am still figuring out concurrency in Python and why some things execute asynchronously or not, so while things seem to work alright, I cannot fully explain them.
