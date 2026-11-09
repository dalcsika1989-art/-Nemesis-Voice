from pathlib import Path
import subprocess, wave
import numpy as np

out=Path('output'); out.mkdir(exist_ok=True)
text='Szia! NEMESIS vagyok. A rendszereim készen állnak. Örülök, hogy végre hallhatod a hangomat.'
subprocess.run(['piper','--model','hu_HU-anna-medium.onnx','--config','hu_HU-anna-medium.onnx.json','--output_file',str(out/'Anna_eredeti.wav')],input=text,encoding='utf-8',check=True)
with wave.open(str(out/'Anna_eredeti.wav'),'rb') as w:
    rate=w.getframerate(); channels=w.getnchannels(); width=w.getsampwidth(); raw=w.readframes(w.getnframes())
if width!=2: raise RuntimeError('16 bites WAV szükséges')
x=np.frombuffer(raw,dtype='<i2').astype(np.float32).reshape(-1,channels)/32768
# Hallható, de visszafogott térbeli visszhang, a beszéd érthetőségének megtartásával.
y=x.copy(); delays=[(0.105,0.32),(0.215,0.23),(0.34,0.14),(0.48,0.08)]
extra=int(rate*.52); y=np.pad(y,((0,extra),(0,0)))
for sec,gain in delays:
    offset=int(rate*sec); y[offset:offset+len(x)] += gain*x
# finom, lassú holografikus moduláció
n=np.arange(len(y)); shimmer=1+0.045*np.sin(2*np.pi*1.7*n/rate)
y*=shimmer[:,None]
y=np.tanh(y*1.12)/np.tanh(1.12)
with wave.open(str(out/'NEMESIS_futurisztikus.wav'),'wb') as w:
    w.setnchannels(channels);w.setsampwidth(2);w.setframerate(rate)
    w.writeframes((np.clip(y,-1,1)*32767).astype('<i2').tobytes())
print('Elkeszult: Anna_eredeti.wav es NEMESIS_futurisztikus.wav')
