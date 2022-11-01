import json
from urllib import request
import in_place

resp = request.urlopen('https://github.com/eko5624/nginx-nosni/raw/master/old.json')
x = json.loads(resp.read().decode('utf-8'))

mingw = x['Mingw-w64'][:x['Mingw-w64'].find('ucrt')+4]
with in_place.InPlace('.github/workflows/toolchain.yml', newline='') as f:
  for l in f:
    if (i:=l.find('key: mcf_')) > -1:
      l = '%s%s-${{ env.random_hash }}\n' % (l[:i+9], mingw)
    elif (i:=l.find('curl')) > -1:
      l = '%s%s.7z\n' % (l[:i+55], x['Mingw-w64'])
    f.write(l)
    
pkgs = {} 
pkgs['libsixel'] = x['libsixel']
pkgs['mpv'] = x['mpv']
for p in ['freetype2', 'fribidi', 'harfbuzz', 'libjxl', 'opus', 'vulkan']:
  pkgs['%s-dev' % p] = x[p]
for p in pkgs:
  with in_place.InPlace('%s/PKGBUILD-new' % p, newline='') as f:
    for l in f:
      if l.startswith('pkgver'):
        l = 'pkgver=%s\n' % pkgs[p]
      f.write(l)        
pkgs['vapoursynth'] = x['VapourSynth'][1:]
for p in ['ffmpeg', 'luajit2', 'mujs', 'rubberband']:
  pkgs['%s' % p] = x[p]
pkgs['mcfgthread'] = mingw[:8]
pkgs['libvorbis_aotuv-dev'] = x['libvorbis']
for p in [
  'amf',
  'angle',
  'avisynth',
  'brotli',
  'dav1d',
  'davs2',
  'ffnvcodec',
  'highway',
  'lame',
  'lcms2',
  'libass',
  'libbluray',
  'libbs2b',
  'libcaca',
  'libdvdcss',
  'libdvdnav',
  'libdvdread',
  'libiconv',
  'libudfread',
  'libjpeg',
  'libmfx',
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
  'libwebp',
  'libxml2',
  'libxvid',
  'libzimg',
  'mbedtls',
  'openal-soft',
  'shaderc',
  'spirv-cross',
  'uavs3d',
  'zlib',
  ]:
  pkgs['%s-dev' % p] = x[p]
for p in pkgs:
  with in_place.InPlace('%s/PKGBUILD' % p, newline='') as f:
    for l in f:
      if l.startswith('pkgver'):
        l = 'pkgver=%s\n' % pkgs[p]
      f.write(l)
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

for t in ['ffmpeg.yml', 'libplacebo.yml', 'shaderc.yml', 'vulkan.yml', 'mpv-meson.yml', 'mpv-waf.yml', 'build-weekly.yml', 'package.yml']:
  with in_place.InPlace('.github/workflows/%s' % t, newline='') as f:
    for l in f:
      if (i:=l.find('key: mcf_')) > -1:
        l = '%s%s-${{ env.random_hash }}\n' % (l[:i+9], mingw)
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
      elif (i:=l.find('ffmpeg-${date}-')) > -1:
        l = '%s%s.7z D:\msys64\opt\\ffmpeg\*\n' % (l[:i+15], x['ffmpeg-git'][:7])           
      elif (i:=l.find('mpv-player/mpv@')) > -1:
        l = '%s%s\n' % (l[:i+15], x['mpv-git'][:7])         
      f.write(l)      
