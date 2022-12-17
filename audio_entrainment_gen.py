from scipy.io.wavfile import write
import numpy as np
import sys


def gen_x(duration, sample_rate, freq):
	return np.linspace(0, duration * freq, int(duration * sample_rate))


def gen_sine(x):
	return np.sin(x * 2 * np.pi)


def gen_square(x):
	return np.round(x - np.floor(x), 0) * 2 - 1


def gen_triangle(x):
	return np.abs((x - np.floor(x)) - 0.5) * 4 - 1


def smooth_start_end(arr, ramp_length):
	ramp = np.linspace(0, 1, ramp_length)
	
	arr[:ramp_length] *= ramp
	
	ramp = ramp[::-1]
	arr[-ramp_length:] *= ramp


def gen_binaural(sound_freq, beat_freq, sample_rate, duration, tone_generator):
	diff = beat_freq / 2
	l_x = gen_x(duration, sample_rate, sound_freq - diff)
	r_x = gen_x(duration, sample_rate, sound_freq + diff)
	
	l_y = tone_generator(l_x)
	r_y = tone_generator(r_x)
	
	ramp_length = int(sample_rate * 0.5)
	
	smooth_start_end(l_y, ramp_length)
	smooth_start_end(r_y, ramp_length)
	
	y = np.concatenate((l_y[:, None], r_y[:, None]), 1)
	
	return y


def gen_monoural(sound_freq, beat_freq, sample_rate, duration, tone_generator):
	diff = beat_freq / 2
	x_1 = gen_x(duration, sample_rate, sound_freq - diff)
	x_2 = gen_x(duration, sample_rate, sound_freq + diff)
	
	y = (tone_generator(x_1) + tone_generator(x_2)) / 2
	
	ramp_length = int(sample_rate * 0.5)
	
	smooth_start_end(y, ramp_length)
	
	return y


def gen_isochronic(sound_freq, beat_freq, sample_rate, duration, tone_generator, volume_generator):
	x_1 = gen_x(duration, sample_rate, sound_freq)
	x_2 = gen_x(duration, sample_rate, beat_freq)
	
	y_1 = tone_generator(x_1)
	y_2 = volume_generator(x_2) / 2 + 0.5
	
	y = y_1 * y_2
	
	ramp_length = int(sample_rate * 0.5)
	
	smooth_start_end(y, ramp_length)
	
	return y


def save_wav(path, arr, sample_rate, save_np_type):
	if(np.issubdtype(save_np_type, np.integer)):
		arr = arr * np.iinfo(save_np_type).max
	
	arr = arr.astype(save_np_type)
	
	write(path, sample_rate, arr)
	

tone_generators = {"sine": gen_sine, "square": gen_square, "triangle": gen_triangle}
entrainment_generators = {"binaural": gen_binaural, "monoural": gen_monoural, "isochronic": gen_isochronic}


def main():
	sample_rate = 44100
	save_np_dtype = np.int16
	
	if(len(sys.argv) != 7 and len(sys.argv) != 8):
		print("arguments: SAVE_PATH DURATION_SECONDS SOUND_FREQ BEAT_FREQ WAVEFORM ENTRAINMENT_TYPE [ISOCHRONIC_AMPLITUDE_TYPE]")
		exit()
	
	save_path = sys.argv[1]
	duration = float(sys.argv[2])
	sound_freq = float(sys.argv[3])
	beat_freq = float(sys.argv[4])
	waveform = sys.argv[5]
	entrainment_type = sys.argv[6]
	
	
	tone_generator = tone_generators[waveform]
	entrainment_generator = entrainment_generators[entrainment_type]
	
	if(entrainment_type == "isochronic"):
		volume_generator = tone_generators[sys.argv[7]]
		arr = entrainment_generator(sound_freq, beat_freq, sample_rate, duration, tone_generator, volume_generator)
	else:
		arr = entrainment_generator(sound_freq, beat_freq, sample_rate, duration, tone_generator)
		
	save_wav(save_path, arr, sample_rate, save_np_dtype)


if __name__ == "__main__":
	main()
