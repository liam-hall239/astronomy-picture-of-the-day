# Daily APOD

A Cylc 8 workflow downloads NASA's Astronomy Picture of the Day every day at
06:00 UTC, starting at the next 06:00 after the workflow starts. The wall-clock
trigger prevents future cycles from running early. Failed downloads retry three
times at 30-minute intervals, then once more after an hour.

The latest image is converted to PNG and overwrites `output/picture/apod.png`;
metadata overwrites `output/json/apod.json`. Point your desktop wallpaper
setting at this image; whether it refreshes automatically depends on the desktop.
Downloads replace the previous file only after completing successfully.
No housekeeping task is needed. On video days, the previous wallpaper is kept
and only metadata is updated. NASA's current APOD endpoint needs no API key.
Pillow handles PNG conversion. The script lives in `app/apod/apod.py`.

## Start

From this folder, with Cylc 8 and Python 3.8+ available:

```sh
python3 -m pip install -r requirements.txt
cylc validate .
cylc install . --workflow-name apod
cylc play apod
```

Keep the host and Cylc scheduler running for daily downloads. Stop with
`cylc stop apod`; resume with `cylc play apod`.

The output folder is configured as `APOD_DIR` in `flow.cylc`. Update it if you
move this folder. The schedule uses a fixed UTC time; changing
`cycle point time zone` to an offset such as `+0100` makes it 06:00 at that
offset, but does not automatically follow daylight-saving changes.

## Download Now

```sh
python3 app/apod/apod.py
```