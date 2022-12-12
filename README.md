# MPV Player Win64 Build
[![releases](https://img.shields.io/github/v/release/eko5624/mpv-win64)](https://github.com/eko5624/mpv-win64/releases/latest)
![stars](https://img.shields.io/github/stars/eko5624/mpv-win64?style=social)
## Installation
Grab and extract the All-in-One archive from <https://github.com/eko5624/mpv-win64/releases>  
You can also manually install these pacman-based packages if you are using MSYS2  
All my builds are portable and compiled with VapourSynth support, these plugins will have no effect if MPV can't find python environment

## Requirements
- [Microsoft Visual C++ Redistributable](https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170)
- Download [vc_redist.x64](https://aka.ms/vs/17/release/vc_redist.x64.exe)


## Main project site:
<https://mpv.io/>

## Configuration
<https://mpv.io/manual/>  
All your configurations can be saved within the ***portable_config*** subdirectory

## Awesome Links
- [User Scripts from Official](https://github.com/mpv-player/mpv/wiki/User-Scripts)
- [Default MPV Setting](https://github.com/mpv-player/mpv/blob/master/etc/mpv.conf)
- [Default MPV Key Binding](https://github.com/mpv-player/mpv/blob/master/etc/input.conf)
### Lua Plugin
- [Autoload](https://github.com/mpv-player/mpv/blob/master/TOOLS/lua/autoload.lua)
- [Play List Manager](https://github.com/jonniek/mpv-playlistmanager)
- [MPV Thumbnail](https://github.com/po5/thumbfast)
- [uosc](https://github.com/tomasklaen/uosc)
- [SmartCopyPaste](https://github.com/Eisa01/mpv-scripts/blob/master/script-opts/SmartCopyPaste_II.conf)
### VapourSynth Plugin
- [SVP](https://www.svp-team.com) proprietary motion interpolation solution to produce high frame rate video
- [MVTools](https://github.com/dubhater/vapoursynth-mvtools) another motion interpolation plugin and it was open source
- [FFMS2](https://github.com/FFMS/ffms2) video source library for multimedia editing
### Shader
- [Anime4K](https://bloc97.github.io/Anime4K/)
- [SSim/Krig](https://gist.github.com/igv)
- [FSRCNNX](https://github.com/igv/FSRCNN-TensorFlow/releases)
- [ACNet](https://github.com/TianZerL/ACNetGLSL/releases)

## How to Compile
Fork this repo and build these packages by Github Action  
**NOTICE**  
Don't build it on your personal msys2 environment unless it was in sandbox, these shitty scripts will spoil your whole weekend!

## Detail
The FFmpeg and MPV library were built with the following libraries
- lame: MP3 Audio Encoding
- libogg/libvorbis-aotuv: Ogg Vorbis Audio Encoding
- opus: Opus Audio Encoding
- nvcodec: Nvidia Hardware Accelerated video Encoding/Decoding
- lcms2: Reading ICC Profiles for Your Monitor
- libass/freetype2/fribidi/harfbuzz: Subtitle Support
- luajit: Lua Plugin
- vapoursynth: VapourSynth Plugin and VSS Video Source
- shaderc/spirv/libplacebo: D3D11 & Vulkan Context
- libbluray/libdvdnav/libdvdread/libdvdcss: Parsing BD/DVD
- libdav1d: av1 decoding
- libjxl: jxl decoding

## TODO ???
### Build FFmpeg with x264/x265/libaom for video encoding
I prefer to directly use these utilities
### Build FFmpeg with libfdk_aac for high quality AAC audio encoding
Yes, fdk aak produce better aac than FFmpeg native, but it is still not in the top tier. I recommend you to use xHE-AAC or Apple AAC instead
### Build libass with fontconfig for POSIX-like system font configuration
Fontconfig sucks in windows, and... do you really want to learn it?
