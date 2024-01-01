import json
from urllib import request
import in_place

resp = request.urlopen('https://github.com/eko5624/nginx-nosni/raw/master/old.json')
x = json.loads(resp.read().decode('utf-8'))

mingw = x['Mingw-w64'][:x['Mingw-w64'].find('ucrt')+4]
   
pkgs = {}
pkgs['mcfgthread'] = mingw[:8]
pkgs['python-embed'] = x['Python']
pkgs['vapoursynth'] = x['VapourSynth'][1:]
for p in ['mpv', 'ffmpeg', 'luajit2']:
  pkgs['%s' % p] = x[p]
for p in [
  'aom',
  'avisynth',
  'brotli',
  'dav1d',
  'davs2',
  'ffnvcodec',
  'freetype2',
  'fribidi',
  'harfbuzz',
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
  'libjxl',
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
  'libsixel',
  'libspeex',
  'libssh',
  'libsrt',
  'libva',
  'libvpl',
  'libwebp',
  'libxml2',
  'libxvid',
  'libzimg',
  'libzvbi',
  'mbedtls',
  'mujs',
  'openssl',
  'openal-soft',
  'opus',
  'rubberband',
  'rav1e' 
  'shaderc',
  'spirv-cross',
  'uavs3d',
  'vulkan',
  'xxhash',
  'zlib',
  ]:
  pkgs['%s-dev' % p] = x[p]
for p in ['libplacebo-dev', 'mpv', 'ffmpeg', 'vulkan-dev', 'luajit2', 'python-embed', 'vapoursynth']:
  with in_place.InPlace('%s/PKGBUILD' % p, newline='') as f:
    for l in f:
      if l.startswith('pkgver'):
        l = 'pkgver=%s\n' % pkgs[p]
      f.write(l)
pkgs['amf-headers-dev'] = x['amf']
pkgs['angle-headers'] =x['angle']
pkgs['ffmpeg-shared-dev'] = x['ffmpeg']
pkgs['ffmpeg-shared'] = x['ffmpeg']
pkgs['libplacebo-shared-dev'] = x['libplacebo']
pkgs['libvorbis_aotuv-dev'] = x['libvorbis']
pkgs['luajit-dev'] = x['LuaJIT']
pkgs['luajit2-shared-dev'] = x['luajit2']
pkgs['luajit2-shared'] = x['luajit2']
pkgs['mpv-shared'] = x['mpv']
pkgs['vapoursynth-shared-dev'] = x['VapourSynth'][1:]
pkgs['vapoursynth-shared'] = x['VapourSynth'][1:]
pkgs['vulkan-shared-dev'] = x['vulkan']

for t in ['ffmpeg.yml', 'mpv.yml', 'build-all.yml', 'package.yml']:
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
      f.write(l)
