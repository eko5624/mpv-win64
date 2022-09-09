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
for p in ['freetype2', 'fribidi', 'harfbuzz', 'libjxl', 'libsixel', 'vulkan']:
  pkgs['%s-dev' % p] = x[p]
for p in pkgs:
  with in_place.InPlace('%s/PKGBUILD-new' % p, newline='') as f:
    for l in f:
      if l.startswith('pkgver'):
        l = 'pkgver=%s\n' % pkgs[p]
      f.write(l)        
pkgs['mcfgthread'] = mingw[:8]
pkgs['libvorbis_aotuv-dev'] = x['libvorbis']
pkgs['luajit'] = x['LuaJIT'] 
for p in ['ffmpeg', 'libsixel', 'luajit2', 'mujs', 'rubberband']:
  pkgs['%s' % p] = x[p]  
for p in [
  'amf',
  'angle',
  'avisynth', 
  'brotli', 
  'dav1d', 
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
  'libwebp', 
  'libxml2', 
  'libxvid', 
  'libzimg', 
  'mbedtls', 
  'openal-soft', 
  'opus', 
  'shaderc', 
  'spirv-cross', 
  'zlib',
  ]:
  pkgs['%s-dev' % p] = x[p]
for p in pkgs:
  with in_place.InPlace('%s/PKGBUILD' % p, newline='') as f:
    for l in f:
      if l.startswith('pkgver'):
        l = 'pkgver=%s\n' % pkgs[p]
      f.write(l)
pkgs['luajit-dev'] = x['LuaJIT']      
pkgs['luajit2-dev'] = x['luajit2']
pkgs['vapoursynth-dev'] = x['VapourSynth'][1:]
pkgs['ffmpeg-dev'] = x['ffmpeg']
pkgs['ffmpeg-git'] = x['ffmpeg']
pkgs['libmpv-git'] = x['mpv']
pkgs['mpv-git'] = x['mpv']

for t in ['ffmpeg.yml', 'libplacebo.yml', 'shaderc.yml', 'mpv-meson.yml', 'mpv-waf.yml', 'build-weekly.yml', 'package.yml']:
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
      f.write(l)
