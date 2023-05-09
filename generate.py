import wave
import numpy as np
import sys
import traceback


def gen_x(duration, sample_rate, freq):
	return np.linspace(0, duration * freq - freq / sample_rate, int(duration * sample_rate))


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
	dur = x[1] * x.shape[0]
	n = (x.shape[0] - 2) // 2
	
	scales = 1 / np.sqrt(np.fft.fftfreq(x.shape[0], x[1])[1:1 + n])
	scales[:int(16 * dur)] = 0
	
	return fft_noise(scales)


def gen_brown(x):
	dur = x[1] * x.shape[0]
	n = (x.shape[0] - 2) // 2
	
	scales = 1 / np.fft.fftfreq(x.shape[0], x[1])[1:1 + n]
	scales[:int(16 * dur)] = 0
	
	return fft_noise(scales)


def gen_binaural(sound_freq, beat_freq, sample_rate, duration, tone_generator, volume_generator):
	diff = beat_freq / 2
	l_x = gen_x(duration, sample_rate, sound_freq - diff)
	r_x = gen_x(duration, sample_rate, sound_freq + diff)
	
	l_y = tone_generator(l_x)
	r_y = tone_generator(r_x)
	
	ramp_length = int(sample_rate * 0.5)
	
	y = np.concatenate((l_y[:, None], r_y[:, None]), 1)
	
	return y


def gen_monoural(sound_freq, beat_freq, sample_rate, duration, tone_generator, volume_generator):
	diff = beat_freq / 2
	x_1 = gen_x(duration, sample_rate, sound_freq - diff)
	x_2 = gen_x(duration, sample_rate, sound_freq + diff)
	
	y = (tone_generator(x_1) + tone_generator(x_2)) / 2
	
	return y


def gen_none(sound_freq, beat_freq, sample_rate, duration, tone_generator, volume_generator):
	x = gen_x(duration, sample_rate, sound_freq)
	
	y = tone_generator(x)
	
	return y


def gen_isochronic(sound_freq, beat_freq, sample_rate, duration, tone_generator, volume_generator):
	x_1 = gen_x(duration, sample_rate, sound_freq)
	x_2 = gen_x(duration, sample_rate, beat_freq)
	
	y_1 = tone_generator(x_1)
	y_2 = volume_generator(x_2) / 2 + 0.5
	
	y = y_1 * y_2
	
	return y


def save_wav(path, arr, sample_rate):
	arr *= np.iinfo(np.int16).max
	arr = arr.astype(np.int16)
	
	f = wave.open(path, "wb")
	
	f.setnchannels(len(arr.shape))
	f.setsampwidth(2)
	f.setframerate(sample_rate)
	
	f.writeframes(arr)
	
	f.close()


noise_generators = set({"white", "pink", "brown"})
sound_generators = {"sine": gen_sine, "square": gen_square, "triangle": gen_triangle, "smooth_square": gen_smooth_square, "white": gen_white, "pink": gen_pink, "brown": gen_brown}
entrainment_generators = {"binaural": gen_binaural, "monoural": gen_monoural, "isochronic": gen_isochronic, "none": gen_none}


def parse_entrainment(args):
	beat_f = float(args[1])
	
	if(args[0] == "isochronic"):
		return entrainment_generators[args[0]], beat_f, sound_generators[args[2]]
	else:
		return entrainment_generators[args[0]], beat_f, None


def parse_noise_args(args):
	if(len(args) == 0):
		return 1, entrainment_generators["none"], None, None
	else:
		return (1,) + parse_entrainment(["isochronic"] + args)


def parse_tone_args(args):
	sound_f = float(args[0])
	
	if(len(args) == 1):
		return sound_f, entrainment_generators["none"], None, None
	else:
		return (sound_f,) + parse_entrainment(args[1:])


def parse_args(args):
	save_path = args[1]
	duration = float(args[2])
	sound_generator = sound_generators[args[3]]
	
	res = (save_path, duration, sound_generator)
	
	if(args[3] in noise_generators):
		return res + parse_noise_args(args[4:])
	else:
		return res + parse_tone_args(args[4:])


def main():
	sample_rate = 44100
	
	try:
		save_path, duration, sound_generator, sound_f, entrainment_generator, beat_f, volume_generator = parse_args(sys.argv)
	except:
		traceback.print_exc()
		
		print("see README.md for usage")
		
		exit()
		
	

	arr = entrainment_generator(sound_f, beat_f, sample_rate, duration, sound_generator, volume_generator)
	
	save_wav(save_path, arr, sample_rate)


if(__name__ == "__main__"):
	main()
