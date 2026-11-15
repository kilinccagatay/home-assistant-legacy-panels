#!/usr/bin/env python3
"""Prepare one versioned, bounded map on the Pi. No vacuum service calls.

Runs in the existing SSH addon. Supervisor credentials stay in memory.
The output is served through the dashboard's existing HA proxy.
"""
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import time
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import urllib.request
from PIL import Image


def prepare(raw, rooms):
    image = Image.open(io.BytesIO(raw)).convert('RGBA')
    if image.width * image.height > 16000000:
        raise ValueError('Map too large')
    sample = image.resize((240, 240), Image.Resampling.BILINEAR)
    points = [(x, y) for y in range(240) for x in range(240)
              if (p := sample.getpixel((x, y)))[3] > 20 and max(p[:3]) > 45]
    if points:
        xs, ys = zip(*points)
        box = (max(0, min(xs)-4), max(0, min(ys)-4),
               min(240, max(xs)+5), min(240, max(ys)+5))
    else:
        box = (0, 0, 240, 240)
    box = (int(box[0]*image.width/240), int(box[1]*image.height/240),
           int(box[2]*image.width/240), int(box[3]*image.height/240))
    image = image.crop(box)
    ratio = min(1, 800/image.width, 800/image.height)
    image = image.resize((max(1, round(image.width*ratio)), max(1, round(image.height*ratio))), Image.Resampling.BILINEAR)
    # Exact scanline hit areas for this output image. Walls/ambiguous pixels stay empty.
    rows = []
    pixels = image.load()
    for y in range(image.height):
        runs, previous, start = [], None, 0
        for x in range(image.width+1):
            room = None
            if x < image.width:
                p = pixels[x, y]
                matches = [r['id'] for r in rooms if p[3] > 20 and all(abs(p[i]-r['color'][i]) <= 8 for i in range(3))]
                if len(matches) == 1:
                    room = matches[0]
            if room != previous:
                if previous is not None:
                    runs.append([start, x, previous])
                start, previous = x, room
        rows.append(runs)
    out = io.BytesIO()
    image.save(out, 'PNG')
    return out.getvalue(), {'width': image.width, 'height': image.height, 'rows': rows}


def atomic(path, content):
    temporary = path.with_suffix(path.suffix+'.tmp')
    temporary.write_bytes(content)
    temporary.replace(path)


def main():
    config = json.loads(Path(sys.argv[1]).read_text())
    output = Path(config['output']); output.mkdir(parents=True, exist_ok=True)
    lock = (Path(sys.argv[1]).parent/'worker.lock').open('w')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            name=self.path.split('?',1)[0].lstrip('/')
            if name != 'manifest.json' and not __import__('re').fullmatch(r'map-[0-9a-f]{24}\.(png|json)', name):
                self.send_error(404);return
            try: content=(output/name).read_bytes()
            except OSError: self.send_error(404);return
            origin=self.headers.get('Origin')
            if origin and origin not in config.get('origins',[]):
                self.send_error(403);return
            self.send_response(200)
            if origin:self.send_header('Access-Control-Allow-Origin',origin)
            self.send_header('Vary','Origin')
            self.send_header('Content-Type','image/png' if name.endswith('.png') else 'application/json')
            self.send_header('Cache-Control','no-store' if name=='manifest.json' else 'public, max-age=31536000, immutable')
            self.send_header('Content-Length',str(len(content)));self.end_headers();self.wfile.write(content)
        def log_message(self,*args):pass
    server=ThreadingHTTPServer((config['bind'],config['port']),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    token = os.environ.get('SUPERVISOR_TOKEN') or Path('/run/s6/container_environment/SUPERVISOR_TOKEN').read_text().strip()
    def get(path):
        request = urllib.request.Request('http://supervisor/core/api/'+path, headers={'Authorization':'Bearer '+token})
        with urllib.request.urlopen(request, timeout=10) as response:
            raw=response.read(16000001)
            if len(raw)>16000000: raise ValueError('Response too large')
            return raw
    last = None
    manifest = None
    while True:
        try:
            state = json.loads(get('states/'+config['entity']))
            stamp = state['state']
            if stamp in ('unknown','unavailable'): raise ValueError('Map unavailable')
            if stamp != last:
                raw = get('image_proxy/'+config['entity'])
                png, prepared = prepare(raw, config['rooms'])
                version=hashlib.sha256(png+json.dumps(prepared,sort_keys=True).encode()).hexdigest()[:24]
                image='map-'+version+'.png'
                atomic(output/image,png)
                hit='map-'+version+'.json'
                atomic(output/hit,json.dumps(prepared,separators=(',',':')).encode())
                manifest=dict(version=version,image=image,hit=hit)
                last=stamp
            manifest['checkedAt']=int(time.time()*1000)
            atomic(output/'manifest.json', json.dumps(manifest,separators=(',',':')).encode())
            # Keep recent revisions long enough for slower clients to finish loading.
            for path in output.glob('map-*.*'):
                if path.name not in (manifest['image'],manifest['hit']) and time.time()-path.stat().st_mtime > 3600:
                    path.unlink()
        except Exception as error:
            # No URLs, token or private map data in logs. Old manifest expires at client.
            print('map preparation failed: '+type(error).__name__, flush=True)
        time.sleep(15)

if __name__ == '__main__':
    main()
