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


start_time = None

def do_visual(port, num_iters, sleep_duration, offset):
	target_time = start_time
	
	if(offset >= 0):
		target_time += offset
		sleep(target_time - time())
		
		port.break_condition = True
		
		target_time += sleep_duration
		sleep(target_time - time())
		
		port.break_condition = False
		
		target_time += sleep_duration
		sleep(target_time - time())
	else:
		target_time += sleep_duration + offset
		sleep(target_time - time())
		
		port.break_condition = False
		
		target_time += sleep_duration
		sleep(target_time - time())
	
	for _ in range(num_iters - 2):
		port.break_condition = True
		
		target_time += sleep_duration
		sleep(target_time - time())
		
		port.break_condition = False
		
		target_time += sleep_duration
		sleep(target_time - time())
	
	if(offset >= 0):
		port.break_condition = True
		
		target_time += sleep_duration
		sleep(target_time - time())
		
		port.break_condition = False
	else:
		port.break_condition = True
		
		target_time += sleep_duration
		sleep(target_time - time())
		
		port.break_condition = False
		
		target_time += sleep_duration
		sleep(target_time - time())
		
		port.break_condition = True

def loop_wave(file_buffer, sample_width, num_channels, sample_rate, serial_port, frequency, phase_shift):
	global start_time
	
	file_buffer = file_buffer.astype(np.int16).tobytes()
	
	p = pyaudio.PyAudio()

	stream = p.open(format=p.get_format_from_width(sample_width),
					channels=num_channels,
					rate=sample_rate,
					output=True)
	
	duration = len(file_buffer) / sample_rate / sample_width
	sleep_duration = 1 / frequency / 2
	port = serial.Serial(serial_port)
	num_iters = int(duration * frequency)
	offset = phase_shift * sleep_duration * 2
	
	while True:
		start_time = time()
		Thread(target=do_visual, args=[port, num_iters, sleep_duration, offset]).start()
		stream.write(file_buffer)
		
			
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
