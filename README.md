# audio-brainwave-entrainment-gen-python
A python script to generate binaural, monoural, isochronic beats wav files for audio brainwave entrainment.

The script takes the following parameters:<br/><br/>
SAVE_PATH DURATION_SECONDS SOUND_FREQ BEAT_FREQ WAVEFORM ENTRAINMENT_TYPE [ISOCHRONIC_AMPLITUDE_TYPE]<br/><br/>
WAVEFORM and ISOCHRONIC_AMPLITUDE_TYPE has to be one of: sine, square, triangle, smooth_square, noise<br/>
ENTRAINMENT_TYPE has to be one of: binaural, monoural, isochronic<br/>
ISOCHRONIC_AMPLITUDE_TYPE only have to be provided when ENTRAINMENT_TYPE == isochronic
