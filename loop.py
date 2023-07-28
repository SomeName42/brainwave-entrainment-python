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

def sleep_until(target_time):
	sleep(max(target_time - time(), 0))

def do_visual(port, sleep_duration, offset, start_time):
	target_time = start_time + 2 * sleep_duration + offset
	sleep_until(target_time)
	
	while(True):
		port.break_condition = True
		
		target_time += sleep_duration
		sleep_until(target_time)
		
		port.break_condition = False
		
		target_time += sleep_duration
		sleep_until(target_time)


def adjust_start_i_dir(file_buffer_np, last_i, start_i, ch):
	val = file_buffer_np[last_i]
	grad_sign = np.sign(file_buffer_np[last_i + ch] - val)
	
	buffer_start_i = file_buffer_np[start_i]
	buffer_start_i_1 = file_buffer_np[start_i + ch]
	
	next_grad = buffer_start_i_1 - buffer_start_i
	last_abs_diff = abs(val - buffer_start_i)
	next_abs_diff = abs(val - buffer_start_i_1)
	
	while np.sign(next_grad) != grad_sign or next_abs_diff < last_abs_diff:
		start_i += ch
		
		buffer_start_i_1 = file_buffer_np[start_i + ch]
	
		next_grad = buffer_start_i_1 - file_buffer_np[start_i]
		last_abs_diff = next_abs_diff
		next_abs_diff = abs(val - buffer_start_i_1)
	
	return start_i, last_abs_diff


def adjust_start_i(file_buffer_np, last_i, start_i):
	start_i_pos, diff_pos = adjust_start_i_dir(file_buffer_np, last_i, start_i, 1)
	start_i_neg, diff_neg = adjust_start_i_dir(file_buffer_np, last_i, start_i, -1)
	
	if(diff_pos < diff_neg):
		return start_i_pos
	else:
		return start_i_neg


def loop_wave(file_buffer, sample_width, num_channels, sample_rate, serial_port, frequency, phase_shift):
	max_abs_diff = 0.005
	
	file_buffer_np = file_buffer.astype(np.int16)
	file_buffer = file_buffer_np.tobytes()
	
	p = pyaudio.PyAudio()

	stream = p.open(format=p.get_format_from_width(sample_width),
		channels=num_channels,
		rate=sample_rate,
		output=True)
	
	original_len = len(file_buffer) / sample_width
	duration = original_len / sample_rate
	
	start_time = int(time() / duration) * duration
	
	if(serial_port is not None):
		port = serial.Serial(serial_port)
		sleep_duration = 1 / frequency / 2
		offset = phase_shift * sleep_duration * 2
		Thread(target=do_visual, args=[port, sleep_duration, offset, start_time], daemon = True).start()
	
	target_time = start_time
	
	while True:
		time_diff = target_time - time()
		
		if(abs(time_diff) <= max_abs_diff):
			stream.write(file_buffer)
		elif(time_diff > 0):
			extend_count = adjust_start_i(file_buffer_np, 0, int(time_diff * sample_rate))
			
			if(extend_count > 0):
				stream.write(file_buffer[:extend_count * sample_width])
				
			stream.write(file_buffer)
		else:
			reduce_count = adjust_start_i(file_buffer_np, -2, int(-time_diff * sample_rate))
			stream.write(file_buffer[reduce_count * sample_width:])
		
		target_time += duration
		
		
	stream.close()
	p.terminate()	


def main():
	try:
		file_path = sys.argv[1]
		volume = float(sys.argv[2])
		
		if(len(sys.argv) == 3):
			serial_port = None
			frequency = None
			phase_shift = None
		elif(len(sys.argv) == 6):
			serial_port = sys.argv[3]
			frequency = float(sys.argv[4])
			phase_shift = float(sys.argv[5])
		else:
			print("see README.md for usage")
			exit()
		
		
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
