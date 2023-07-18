# brainwave-entrainment-python
Python scripts for brainwave entrainment.
<h2>Usage of generate.py</h2>
Generate noise or isochronic noise<br/>
SAVE_PATH DURATION_SECONDS NOISE_GENERATOR [BEAT_FREQ VOLUME_GENERATOR]<br/><br/>
Generate tone only or tone with entrainment<br/>
arguments: SAVE_PATH DURATION_SECONDS TONE_GENERATOR SOUND_FREQ [ENTRAINMENT_TYPE BEAT_FREQ [ISOCHRONIC_VOLUME_GENERATOR]]<br/><br/>
NOISE_GENERATOR can be one of: white, pink, brown<br/>
VOLUME_GENERATOR and TONE_GENERATOR can be one of: sine, triangle, square, smooth_square<br/>
ENTRAINMENT_TYPE can be one of: binaural, monoural, isochronic<br/>
when ENTRAINMENT_TYPE == isochronic then VOLUME_GENERATOR is required<br/><br/>
<h2>Usage of loop.py</h2>
Seamlessly loops a given wav file and optionally provides visual entrainment.<br/>
Visual entrainment is performed by toggling the serial port TXD pin with set frequency and phase shift.<br/>
This can be used for visual entrainment with for example connecting LED -s to TXD and +5V<br/>
arguments: FILE_PATH VOLUME [SERIAL_PORT FREQUENCY PHASE_SHIFT]<br/>
FILE_PATH path to a generated audio entrainment file.<br/>
VOLUME is a floating point value, 1 is max<br/>
SERIAL_PORT is the serial port, for example on linux: /dev/ttyUSB0<br/>
FREQUENCY is the entrainment frequency of the audio file<br/>
PHASE_SHIFT is the phase shift for the visual entrainment
