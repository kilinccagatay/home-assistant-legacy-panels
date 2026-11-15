import importlib.util
import io
from pathlib import Path
import unittest
from PIL import Image, ImageDraw

spec=importlib.util.spec_from_file_location('worker',Path(__file__).resolve().parents[1]/'examples/map-worker/prepare-map.py')
worker=importlib.util.module_from_spec(spec);spec.loader.exec_module(worker)
class MapTest(unittest.TestCase):
 def test_prepared_pixels_and_selection_match(self):
  source=Image.new('RGBA',(1000,800),(0,0,0,255));draw=ImageDraw.Draw(source)
  draw.rectangle((200,200,500,600),fill=(88,214,141,255));draw.rectangle((550,200,800,600),fill=(165,105,189,255))
  data=io.BytesIO();source.save(data,'PNG');rooms=[{'id':1,'color':[88,214,141]},{'id':2,'color':[165,105,189]}]
  png,meta=worker.prepare(data.getvalue(),rooms);image=Image.open(io.BytesIO(png));self.assertLessEqual(max(image.size),800);self.assertEqual(image.size,(meta['width'],meta['height']))
  seen=set()
  for y,row in enumerate(meta['rows']):
   last=0
   for start,end,room in row:
    self.assertGreaterEqual(start,last);self.assertGreater(end,start);self.assertLessEqual(end,image.width);last=end;seen.add(room)
    for x in (start,end-1):self.assertTrue(all(abs(image.getpixel((x,y))[i]-rooms[room-1]['color'][i])<=8 for i in range(3)))
  self.assertEqual(seen,{1,2})
 def test_ambiguous_colors_never_select(self):
  source=Image.new('RGBA',(30,30),(88,214,141,255));data=io.BytesIO();source.save(data,'PNG')
  _,meta=worker.prepare(data.getvalue(),[{'id':1,'color':[88,214,141]},{'id':2,'color':[88,214,141]}]);self.assertFalse(any(meta['rows']))
if __name__=='__main__':unittest.main()
