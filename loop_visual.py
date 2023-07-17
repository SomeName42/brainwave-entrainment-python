from time import sleep, time
import serial
import pyaudio
import wave
import sys
import traceback
import numpy as np
from threading import Thread


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

def do_visual(port, sleep_duration, offset, start_time):
	target_time = start_time
	
	if(offset >= 0):
		target_time += offset
		sleep(target_time - time())
		
		port.break_condition = True
		
		target_time += sleep_duration
		sleep(target_time - time())
	else:
		target_time += sleep_duration + offset
		sleep(target_time - time())
	
	while(True):
		port.break_condition = False
		
		target_time += sleep_duration
		sleep(target_time - time())
		
		port.break_condition = True
		
		target_time += sleep_duration
		sleep(target_time - time())
		
		

def loop_wave(file_buffer, sample_width, num_channels, sample_rate, serial_port, frequency, phase_shift):
	file_buffer = file_buffer.astype(np.int16).tobytes()
	
	p = pyaudio.PyAudio()

	stream = p.open(format=p.get_format_from_width(sample_width),
					channels=num_channels,
					rate=sample_rate,
					output=True)
					
	original_len = len(file_buffer) / sample_width
	duration = original_len / sample_rate
	sleep_duration = 1 / frequency / 2
	port = serial.Serial(serial_port)
	offset = phase_shift * sleep_duration * 2
	
	start_time = time()
	Thread(target=do_visual, args=[port, sleep_duration, offset, start_time], daemon = True).start()
	
	target_time = start_time
	
	while True:
		time_diff = target_time - time()
		
		if(abs(time_diff) <= 0.005):
			stream.write(file_buffer)
		elif(time_diff > 0):
			extend_count = int(time_diff * sample_rate)
			stream.write(file_buffer[:sample_width] * extend_count + file_buffer)
		else:
			reduce_count = int(-time_diff * sample_rate)
			stream.write(file_buffer[reduce_count * sample_width:])
		
		target_time += duration
		
		
	stream.close()
	p.terminate()	


def main():
	try:
		file_path = sys.argv[1]
		serial_port = sys.argv[2]
		frequency = float(sys.argv[3])
		phase_shift = float(sys.argv[4])
		
		if(len(sys.argv) > 5):
			volume = float(sys.argv[5])
		else:
			volume = 1
			
		file_buffer, sample_width, num_channels, sample_rate = load_wave(file_path)
	except:
		traceback.print_exc()
		
		print("see README.md for usage")
	
	
	print("")
	print("Press CTRL + C to stop playback")
	
	
	file_buffer = file_buffer * volume
	
	loop_wave(file_buffer, sample_width, num_channels, sample_rate, serial_port, frequency, phase_shift)
		

if(__name__ == "__main__"):
	main()
