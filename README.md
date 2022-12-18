# audio-brainwave-entrainment-gen-python
A python script to generate wav files of noise, tones, and binaural, monoural, isochronic beats.

Usage of the script:<br/>
The script takes command line arguments.<br/><br/>
Generate noise or isochronic noise<br/>
SAVE_PATH DURATION_SECONDS NOISE_GENERATOR [BEAT_FREQ VOLUME_GENERATOR]<br/><br/>
Generate tone only or tone with entrainment<br/>
SAVE_PATH DURATION_SECONDS TONE_GENERATOR SOUND_FREQ [ENTRAINMENT_TYPE BEAT_FREQ [ISOCHRONIC_VOLUME_GENERATOR]]<br/><br/>
NOISE_GENERATOR can be one of: white, pink, brown<br/>
VOLUME_GENERATOR and TONE_GENERATOR can be one of: sine, triangle, square, smooth_square<br/>
ENTRAINMENT_TYPE can be one of: binaural, monoural, isochronic<br/>
when ENTRAINMENT_TYPE == isochronic then VOLUME_GENERATOR is required<br/><br/>
Example:<br/><br/>
python3 ./sound_and_beat_gen.py ./test.wav 300 white
