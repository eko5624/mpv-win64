import json
from urllib import request
import in_place

resp = request.urlopen('https://github.com/eko5624/nginx-nosni/raw/master/old.json')
x = json.loads(resp.read().decode('utf-8'))

mingw = x['Mingw-w64'][:x['Mingw-w64'].find('ucrt')+4]

for t in ['build-toolchain-lhmouse.yml']:
  with in_place.InPlace('.github/workflows/%s' % t, newline='') as f:
    for l in f:
      if (i:=l.find('key: mcf_')) > -1:
        l = '%s%s\n' % (l[:i+9], mingw)
      elif (i:=l.find('mingw-w64-gcc-mcf_')) > -1:
        l = '%s%s.7z\n' % (l[:i+18], x['Mingw-w64'])
      f.write(l)
    
pkgs = {} 
pkgs['libsixel'] = x['libsixel']
for p in ['freetype2', 'fribidi', 'harfbuzz', 'libjxl', 'spirv-cross']:
  pkgs['%s-dev' % p] = x[p]
for p in pkgs:
  with in_place.InPlace('%s/PKGBUILD-new' % p, newline='') as f:
    for l in f:
      if l.startswith('pkgver'):
        l = 'pkgver=%s\n' % pkgs[p]
      f.write(l)        
pkgs['vapoursynth'] = x['VapourSynth'][1:]
for p in ['curl', 'mpv', 'ffmpeg', 'luajit2', 'mujs', 'rubberband']:
  pkgs['%s' % p] = x[p]
pkgs['mcfgthread'] = mingw[:8]
pkgs['libvorbis_aotuv-dev'] = x['libvorbis']
for p in [
  'amf',
  'aom',
  'angle',
  'avisynth',
  'brotli',
  'dav1d',
  'davs2',
  'ffnvcodec',
  'highway',
  'lame',
  'lcms2',
  'libaribcaption',    
  'libass',
  'libbluray',
  'libbs2b',
  'libcaca',
  'libdovi', 
  'libdvdcss',
  'libdvdnav',
  'libdvdread',
  'libiconv',
  'libudfread',
  'libunibreak',
  'libjpeg',
  'libmodplug',
  'libmysofa',
  'libogg',
  'libopenmpt',
  'libplacebo',
  'libpng',
  'libsdl2',
  'libspeex',
  'libssh',
  'libsrt',
  'libvpl',
  'libvpx',
  'libwebp',
  'libxml2',
  'libxvid',
  'libva',
  'libzimg',
  'libzvbi',
  'mbedtls',
  'openal-soft',
  'openssl',
  'opus',
  'rav1e',
  'shaderc',
  'uavs3d',
  'vulkan',
  'xxhash',
  'zlib',
  ]:
  pkgs['%s-dev' % p] = x[p]
for p in pkgs:
  with in_place.InPlace('%s/PKGBUILD' % p, newline='') as f:
    for l in f:
      if l.startswith('pkgver'):
        l = 'pkgver=%s\n' % pkgs[p]
      f.write(l)
pkgs['amf-headers-dev'] = x['amf']
pkgs['angle-headers-dev'] = x['angle']
pkgs['libsixel-dev'] = x['libsixel']
pkgs['luajit-dev'] = x['LuaJIT']      
pkgs['luajit2-dev'] = x['luajit2']
pkgs['mujs-dev'] = x['mujs']
pkgs['rubberband-dev'] = x['rubberband']
pkgs['vapoursynth-dev'] = x['VapourSynth'][1:]
pkgs['ffmpeg-dev'] = x['ffmpeg']
pkgs['ffmpeg-git'] = x['ffmpeg']
pkgs['libmpv-git'] = x['mpv']
pkgs['mpv-git'] = x['mpv']

for t in ['curl.yml', 'ffmpeg.yml', 'libplacebo.yml', 'shaderc.yml', 'vulkan.yml', 'mpv.yml', 'build-all.yml', 'package.yml']:
  with in_place.InPlace('.github/workflows/%s' % t, newline='') as f:
    for l in f:
      if (i:=l.find('key: mcf_')) > -1:
        l = '%s%s\n' % (l[:i+9], mingw)
      elif (i:=l.find('/dev/')) > -1:
        r = l.find('-1-x86_64')
        rr = l.rfind('-', i, r)
        p = l[i+5:rr]
        if p in pkgs:
          l = '%s%s-%s%s' % (l[:i+5], p, pkgs[p], l[r:])
      elif (i:=l.find('/latest/')) > -1:
        r = l.find('-1-x86_64')
        rr = l.rfind('-', i, r)
        p = l[i+8:rr]
        if p in pkgs:
          l = '%s%s-%s%s' % (l[:i+8], p, pkgs[p], l[r:])
      elif (i:=l.find('/yt-dlp/releases/download/')) > -1:
        l = '%s%s/yt-dlp.exe\n' % (l[:i+26], x['yt-dlp'])                 
      f.write(l)      
