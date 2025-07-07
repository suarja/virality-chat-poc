Issues running FFMPEG on railway
hugo-farroba
PRO

7 months ago

Hi,

We have a service which runs multiple jobs using BullMQ + Redis.

One of those jobs requires FFMPEG, the job will expect a HLS url to be provided. When we pass that HLS url into ffmpeg it will generate a sprite sheet/storyboard for the HLS stream, once processed it will output to a /tmp directory so we can then upload the output to remote storage, which looking at logs on railway goes to /app/tmp/. However the problem appear to be that ffmpeg is not running on railway vs how it runs locally.

When running the job locally for a 22 minute HLS video, it will take roughly 1 minute to complete the sprite sheet using ffmpeg. If we look at the logs on railway it will state that the same job is completed in 10-100ms which if that was real would be great but nothing is actually saved to the /tmp directory, doesnt even look like ffmpeg ran at all, but there is also no error code from ffmpeg.

We have also attached a storage volume to the service on railway mounted to /tmp

Locally its running on a windows machine, on railway its running on linux.

Here is the function that initialises FFMPEG:

async function initialize() {

    const { path: ffmpegPath } = await import('@ffmpeg-installer/ffmpeg');

    const { path: ffprobePath } = await import('ffprobe-static');

    FFMPEG_PATH = ffmpegPath;

    FFPROBE_PATH = ffprobePath;

}

Output from railway logs for FFMPEG:
FFmpeg path: /app/node_modules/@ffmpeg-installer/linux-x64/ffmpeg

FFprobe path: /app/node_modules/ffprobe-static/bin/linux/x64/ffprobe

We are using the following args for ffmpeg:

[

'-i',

'https://example.com/ivs/v1/586794478830/vTFMa3IgALpd/2024/11/28/12/45/kg379rHgqhNp/media/hls/master.m3u8';,

'-threads',

'0',

'-filter_threads',

'4',

'-filter_complex_threads',

'4',

'-vsync',

'0',

'-preset',

'ultrafast',

'-vf',

'fps=1/13.28,scale=160:90:flags=fast_bilinear,format=yuv420p,tile=10x10',

'-frames:v',

'1',

'-qscale:v',

'3',

'-an',

'-y',

'/app/tmp/1733743050703/storyboard.jpg'

]

This is what initialises the ffmpeg command:

const ffmpegResult = spawnSync(FFMPEG_PATH, ffmpegArgs, { stdio: 'inherit' });

ffmpeg log:

{ "severity": "error", "timestamp": "2024-12-09T11:17:39.956129562Z", "message": "ffmpeg version N-47683-g0e8eb07980-static https://johnvansickle.com/ffmpeg/ Copyright (c) 2000-2018 the FFmpeg developers", "attributes": { "level": "error" } }

No ffmpeg exit code

{ "severity": "info", "timestamp": "2024-12-09T11:17:39.956392585Z", "message": "FFmpeg exit code: null", "attributes": { "level": "info" } }

ffmpeg stderr:

{ "severity": "info", "timestamp": "2024-12-09T11:17:39.956412758Z", "message": "FFmpeg stderr: undefined", "attributes": { "level": "info" } }

Error: Error: ENOENT: no such file or directory, open '/app/tmp/1733743050703/storyboard.jpg'

Just trying to understand why this would fail when deployed to railway, but when I trigger the job locally it works and saves the output to /tmp/ and uploads it to remote storage with no problems.

Cant tell if ffmpeg configuration needs tweaking for linux, or if my storage volume is mounted incorrectly.

Any help would be appreciated.

Solved

1

10 Replies

hugo-farroba
PRO

7 months ago


We have also tried adding a nixpacks.toml file to the project in case that was required for ffmpeg, but no luck.

[phases.setup]

aptPkgs = ["ffmpeg"]

[start]

cmd = "node dist/index.js"

[build]

builder = "nixpacks"

[phases.build]

cmds = [

"npm install",

"npm run build"

]

[env]

NODE_ENV = "production"


Reply

angelo
EMPLOYEE

7 months ago


This feels like an issue with the storage volume mount, but since this isn't a platform issue- there isn't much help we can offer here. Other users do happen to run FFMpeg just fine. (Although I think SSH would be a great addition to have to make it easier to debug.)


Reply

Status changed to Awaiting User Response railway[bot] • 7 months ago

hugo-farroba
PRO

7 months ago


Don't the containers for projects have ephemeral storage regardless if a storage volume is attached? I would expect that I could save at least a few MB of data to a /tmp/ dir which would be lost next time the project initialises without a dedicated storage volume? I only recently added the storage volume to see if that would make any difference but it doesn't appear to have changed the output. So now I'm thinking its around how FFMPEG is initializing on linux or running in the container and its hard to tell exactly why it doesnt work on railway vs local which runs every time we trigger the job. I have included a screenshot of the logs from railway when we run the FFMPEG command using nodes spawnSync and then a screenshot from the output of FFMPEG when its running locally.

Paths when running local:

FFmpeg path: C:\Github\project\service-bullmq\node_modules\@ffmpeg-installer\win32-x64\ffmpeg.exe

FFprobe path: C:\Github\project\service-bullmq\node_modules\ffprobe-static\bin\win32\x64\ffprobe.exe

In the screenshots provided they are both using the same HLS url.

In the screenshot for railway you can see in the logs the output states it completes the storyboard output almost instantly after we initialise ffmpeg, it doesnt even try to go through each .ts file.

In the screenshot for local ffmpeg you can see once we initialise ffmpeg it starts to work through each of the .ts for the HLS url which is the expected behaviour.

The 3rd screenshot includes the ffmpeg output from a completed run on my local machine for the same HLS url. So couple of things, one it takes a lot longer to finish as expected since its a 22 minute video, secondly it outputs a file to local directory /tmp, for the sake of being verbose the output file from ffmpeg is 243KB in size.

Thanks.

Attachments

local-ffmpe...
railway-ffm...
local-ffmpe...

Reply

Status changed to Awaiting Railway Response railway[bot] • 7 months ago

brody
EMPLOYEE

7 months ago


Chiming in here to say that @ffmpeg-installer is known to give strange issues in containerized environments.

Remove any npm package that installs ffmpeg or ffprobe, and instead, install it as a nix package via a nixpacks.toml file -

[phases.setup]
	nixPkgs = ['...', 'ffmpeg']
Not saying this is going to magically fix the issue, but it's best to at least use best practices first.


Reply

Status changed to Awaiting User Response railway[bot] • 7 months ago

brody

Chiming in here to say that @ffmpeg-installer is known to give strange issues in containerized environments.Remove any npm package that installs ffmpeg or ffprobe, and instead, install it as a nix package via a nixpacks.toml file -[phases.setup] nixPkgs = ['...', 'ffmpeg']Not saying this is going to magically fix the issue, but it's best to at least use best practices first.

hugo-farroba
PRO

7 months ago


Thanks for the feedback, will try removing the node packages for sure - in my second post I did post my nixpacks.toml file which is using aptPkgs syntax, is nixPkgs what I should be using there?

The only thing that is unclear doing it this way would be how I get the ffmpeg path values to initialise ffmpeg, for example if I remove the ffmpeg node packages and use nixpacks what would the path be? /opt/bin/ffmpeg perhaps? This was something that we had to do when running this on an AWS lambda environment, so wondering if it would be similar path (not to familiar with containers to find that info easily). By that i mean that the current FFMPEG path when running on railway is:/app/node_modules/@ffmpeg-installer/linux-x64/ffmpeg .


Reply

Status changed to Awaiting Railway Response railway[bot] • 7 months ago

brody
EMPLOYEE

7 months ago


> in my second post I did post my nixpacks.toml file which is using aptPkgs syntax, is nixPkgs what I should be using there?

Yes, nix will install both ffmpeg and ffprobe.

> The only thing that is unclear doing it this way would be how I get the ffmpeg path values to initialise ffmpeg

You don't need to, they will be in $PATH, and any good wrapper library should be able to pick that up without you configuring anything extra.


Reply

Status changed to Awaiting User Response railway[bot] • 7 months ago

brody

> in my second post I did post my nixpacks.toml file which is using aptPkgs syntax, is nixPkgs what I should be using there?Yes, nix will install both ffmpeg and ffprobe.> The only thing that is unclear doing it this way would be how I get the ffmpeg path values to initialise ffmpegYou don't need to, they will be in $PATH, and any good wrapper library should be able to pick that up without you configuring anything extra.

hugo-farroba
PRO

7 months ago


I will change the syntax to nixPkgs thank you for that.

Guess I can just output the path and see what it says when running on railway, as we arent using any wrappers we are just passing the FFMPEG args along with the FFMPEG path straight into nodes spawnSync functions which is part of node utils child_process. So we would need to have knowledge of where ffmpeg path is to initialise ffmpeg command we are running.

example of command syntax used:

import { spawnSync } from 'node:child_process'

const ffmpegResult = spawnSync(FFMPEG_PATH, ffmpegArgs, { stdio: 'inherit' });


Reply

Status changed to Awaiting Railway Response railway[bot] • 7 months ago

brody
EMPLOYEE

7 months ago


You could call something like which to get the path, or there might even be a native node solution.


Reply

Status changed to Awaiting User Response railway[bot] • 7 months ago

brody

You could call something like which to get the path, or there might even be a native node solution.

hugo-farroba
PRO

7 months ago


Looks to be working now after tweaking nixpacks.toml and FFMPEG paths. Guess if anyone comes across this and isn't doing ffmpeg via dockerfile and wants to run ffmpeg directly from a node project using spawnSync with just nixpacks then these 2 steps should be sufficient.

Add ffmpeg to nixpacks.toml as advised above.

Use which to find ffmpeg path using something like this to automatically set it: FFMPEG_PATH = execSync('which ffmpeg');

With those two changes I was able to use FFMPEG on railway and get the same output as my local env. So now I can simply just use an if statement when initializing the project and use @ffmpeg-installer packages if I'm running the project locally to debug and then use which to deterministically set it when running in a container environment like railway.


Reply

Status changed to Awaiting Railway Response railway[bot] • 7 months ago

brody
EMPLOYEE

7 months ago


Awsome, glad it worked for you!


Reply

