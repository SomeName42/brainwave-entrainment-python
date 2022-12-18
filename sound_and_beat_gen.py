from scipy.io.wavfile import write
import numpy as np
import sys
import traceback


def gen_x(duration, sample_rate, freq):
	return np.linspace(0, duration * freq, int(duration * sample_rate))


def gen_sine(x):
	return np.sin(x * 2 * np.pi)


def gen_square(x):
	return np.round(x - np.floor(x), 0) * 2 - 1


def gen_triangle(x):
	return np.abs(x - np.floor(x) - 0.5) * 4 - 1


def gen_smooth_square(x):
	y = gen_triangle(x) * 7
	y[y > 1] = 1
	y[y < -1] = -1
	
	return y


def fft_noise(scales):
	n = scales.shape[0]
	
	phases = np.random.rand(n) * 2 * np.pi
	phases = np.cos(phases) + 1j * np.sin(phases)
	phases *= scales
	
	res = np.zeros((n + 1) * 2, dtype=complex)
	
	res[1:1+n] = phases
	res[-1:-1-n:-1] = np.conj(phases)
	
	res = np.fft.ifft(res).real
	
	return res / np.abs(res).max()


def gen_white(x):
	return np.random.rand(x.shape[0]) * 2 - 1


def gen_pink(x):
	dur = x[-1]
	n = (x.shape[0] - 2) // 2
	
	scales = 1 / np.sqrt(np.fft.fftfreq(x.shape[0], x[1])[1:1 + n])
	scales[:int(16 * x[-1])] = 0
	
	return fft_noise(scales)


def gen_brown(x):
	dur = x[-1]
	n = (x.shape[0] - 2) // 2
	
	scales = 1 / np.fft.fftfreq(x.shape[0], x[1])[1:1 + n]
	scales[:int(16 * x[-1])] = 0
	
	return fft_noise(scales)


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


def gen_none(sound_freq, beat_freq, sample_rate, duration, tone_generator):
	x = gen_x(duration, sample_rate, sound_freq)
	
	y = tone_generator(x)
	
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
	

sound_generators = {"sine": gen_sine, "square": gen_square, "triangle": gen_triangle, "smooth_square": gen_smooth_square, "white": gen_white, "pink": gen_pink, "brown": gen_brown}
entrainment_generators = {"binaural": gen_binaural, "monoural": gen_monoural, "isochronic": gen_isochronic, "none": gen_none}


def main():
	sample_rate = 44100
	save_np_dtype = np.int16
	
	noise_generators = set({"white", "pink", "brown"})
	
	try:
		save_path = sys.argv[1]
		duration = float(sys.argv[2])
		sound_type = sys.argv[3]
		
		
		if(sound_type in noise_generators):
			sound_freq = 1
			beat_freq = None
			
			if(len(sys.argv) == 4):
				entrainment_type = "none"
			else:
				entrainment_type = "isochronic"
				beat_freq = float(sys.argv[4])
				volume_generator = sound_generators[sys.argv[5]]
		else:
			sound_freq = float(sys.argv[4])
			
			if(len(sys.argv) == 5):
				entrainment_type = "none"
				beat_freq = None
			else:
				entrainment_type = sys.argv[5]
				beat_freq = float(sys.argv[6])
				
				if(entrainment_type == "isochronic"):
					volume_generator = sound_generators[sys.argv[7]]
			
		
		sound_generator = sound_generators[sound_type]
		entrainment_generator = entrainment_generators[entrainment_type]
	except:
		traceback.print_exc()
		
		print("")
		print("Usages:")
		print("")
		print("Generate noise or isochronic noise")
		print("SAVE_PATH DURATION_SECONDS NOISE_GENERATOR [BEAT_FREQ VOLUME_GENERATOR]")
		print("")
		print("Generate tone only or tone with entrainment")
		print("SAVE_PATH DURATION_SECONDS TONE_GENERATOR SOUND_FREQ [ENTRAINMENT_TYPE BEAT_FREQ [ISOCHRONIC_VOLUME_GENERATOR]]")
		print("")
		print("NOISE_GENERATOR can be one of: white, pink, brown")
		print("VOLUME_GENERATOR and TONE_GENERATOR can be one of: sine, triangle, square, smooth_square")
		print("ENTRAINMENT_TYPE can be one of: binaural, monoural, isochronic")
		print("when ENTRAINMENT_TYPE == isochronic then VOLUME_GENERATOR is required")
		print("")
		print("Example:")
		print("")
		print("\"python3 ./audio_entrainment_gen.py ./test.wav 300 white\"")
		
		exit()
		
	
	if(entrainment_type == "isochronic"):
		arr = entrainment_generator(sound_freq, beat_freq, sample_rate, duration, sound_generator, volume_generator)
	else:
		arr = entrainment_generator(sound_freq, beat_freq, sample_rate, duration, sound_generator)
		
	save_wav(save_path, arr, sample_rate, save_np_dtype)


if __name__ == "__main__":
	main()
