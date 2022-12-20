import pyaudio
import wave
import sys
import traceback
import numpy as np


def main():
	try:
		file_path = sys.argv[1]
		
		if(len(sys.argv) > 2):
			volume = float(sys.argv[2])
		else:
			volume = 1
	except:
		traceback.print_exc()
		
		print("parameters: FILE_PATH [VOLUME]")
		print("VOLUME is a floating point number 1 is default")
	
	wf = wave.open(file_path, 'rb')
	
	file_buffer = []
	
	while(True):
		data = wf.readframes(1024)
		
		if(len(data) == 0):
			break
		
		data = np.fromstring(data, np.int16)
		
		file_buffer.append(data)
		
		
	file_buffer = np.concatenate(file_buffer)
	file_buffer = file_buffer * volume
	file_buffer = file_buffer.astype(np.int16).tostring()
	
	
	p = pyaudio.PyAudio()

	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
					channels=wf.getnchannels(),
					rate=wf.getframerate(),
					output=True)
	
	wf.close()
	
	
	print("")
	print("Use CTRL + C to stop playback")
	
	while True:
		stream.write(file_buffer)
			
	stream.close()
	p.terminate()	
		

if(__name__ == "__main__"):
	main()
