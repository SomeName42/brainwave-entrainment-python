# entrainment-python
Python scripts for generating wav files of noise, tones, binaural, monoural, and isochronic beats, and for playing them back seamlessly in an endless loop.

Usage of generate.py:<br/>
The script takes command line arguments.<br/><br/>
Generate noise or isochronic noise<br/>
SAVE_PATH DURATION_SECONDS NOISE_GENERATOR [BEAT_FREQ VOLUME_GENERATOR]<br/><br/>
Generate tone only or tone with entrainment<br/>
SAVE_PATH DURATION_SECONDS TONE_GENERATOR SOUND_FREQ [ENTRAINMENT_TYPE BEAT_FREQ [ISOCHRONIC_VOLUME_GENERATOR]]<br/><br/>
NOISE_GENERATOR can be one of: white, pink, brown<br/>
VOLUME_GENERATOR and TONE_GENERATOR can be one of: sine, triangle, square, smooth_square<br/>
ENTRAINMENT_TYPE can be one of: binaural, monoural, isochronic<br/>
when ENTRAINMENT_TYPE == isochronic then VOLUME_GENERATOR is required<br/><br/>
Usage of loop.py<br/><br/>
Seamlessly loops a given wav file<br/>
FILE_PATH [VOLUME]<br/>
VOLUME is a floating point value, 1 is normal<br/><br/>
Usage of loop_visual.py<br/><br/>
Additionaly provides visual entrainment through a serial port.<br/>
Turns on and off the TXD pin at the desired frequency.<br/>
This can be used for example with LED -s<br>
FILE_PATH SERIAL_PORT FREQUENCY [VOLUME]<br/>
FILE_PATH and VOLUME is the same<br/>
SERIAL_PORT is a path to a serial port device for example: /dev/ttyUSB0<br/>
FREQUENCY is the entrainment frequency of the audio file<br/>
