import pyaudio
import wave
import sys
import traceback
import numpy as np


def load_wave(file_path):
	f = wave.open(file_path, 'rb')
	
	file_buffer = []
	
	while(True):
		data = f.readframes(1024)
		
		if(len(data) == 0):
			break
		
		data = np.frombuffer(data, np.int16)
		
		file_buffer.append(data)
		
		
	file_buffer = np.concatenate(file_buffer)
	
	sample_width = f.getsampwidth()
	num_channels = f.getnchannels()
	sample_rate = f.getframerate()
	
	f.close()
	
	return file_buffer, sample_width, num_channels, sample_rate


def loop_wave(file_buffer, sample_width, num_channels, sample_rate):
	file_buffer = file_buffer.astype(np.int16).tobytes()
	
	p = pyaudio.PyAudio()

	stream = p.open(format=p.get_format_from_width(sample_width),
					channels=num_channels,
					rate=sample_rate,
					output=True)
	
	while True:
		stream.write(file_buffer)
			
	stream.close()
	p.terminate()	


def main():
	try:
		file_path = sys.argv[1]
		
		if(len(sys.argv) > 2):
			volume = float(sys.argv[2])
		else:
			volume = 1
			
		file_buffer, sample_width, num_channels, sample_rate = load_wave(file_path)
	except:
		traceback.print_exc()
		
		print("parameters: FILE_PATH [VOLUME]")
		print("VOLUME is a floating point number 1 is default")
	
	
	print("")
	print("Press CTRL + C to stop playback")
	
	
	file_buffer = file_buffer * volume
	
	loop_wave(file_buffer, sample_width, num_channels, sample_rate)
		

if(__name__ == "__main__"):
	main()
