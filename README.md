# eds

Simple CLI tool to download YouTube videos/audio using yt-dlp, save files with numbering, and copy path to clipboard.

## Features

- Download video or audio (mp3)
- Specify quality (e.g., 720, 1080)
- Default save folder: `~/eds`
- Clear save folder with `-d`
- Cross-platform clipboard support (Windows, macOS, Linux)

## Install

```bash
pip install eds
## Usage
`eds <url> [-a] [-v] [-q QUALITY] [-p PATH] [-d]`

-a, --audio — download audio only

-v, --video — download video only (default)

-q, --quality — max quality (e.g. 720)

-p, --path — custom save folder

-d, --delete — clear save folder and exit

-h, --help — show help

## Example
`eds https://youtube.com/watch?v=abc123 -a -q 192`