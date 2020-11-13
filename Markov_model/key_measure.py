import pretty_midi
import numpy as np
KEYS = ['C_major','C#_major','D_major','D#_major','E_major','F_major','F#_major','G_major','G#_major','A_major','A#_major','B_major',
        'C_minor','C#_minor','D_minor','D#_minor','E_minor','F_minor','F#_minor','G_minor','G#_minor','A_minor','A#_minor','B_minor']
MAJOR_KEY_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_KEY_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
PITCHES_PER_OCTAVE = 12

def correlation(x,y):
    average_x = sum(x)/len(x)
    average_y = sum(y)/len(y)
    return sum((x-average_x)*(y-average_y))/((sum((x-average_x)**2)*sum((y-average_y)**2))**(1.0/2))
def find_key(filename):
    input_data = pretty_midi.PrettyMIDI(filename)
    pitch_mod_array = np.zeros(PITCHES_PER_OCTAVE,dtype=float)
    total_duration = 0
    for instrument in input_data.instruments:
            if not instrument.is_drum:
                for note in instrument.notes:
                    pitch_mod_array[note.pitch%PITCHES_PER_OCTAVE]+=note.get_duration()
                    total_duration+=note.get_duration()
    if total_duration!=0:
        pitch_mod_array/=total_duration
        # calculate correlation
        correlation_array = np.zeros(2*PITCHES_PER_OCTAVE)
        for i in range(0, PITCHES_PER_OCTAVE):
            # rotate MAJOR_KEY_PROFILE
            correlation_array[i] = correlation(pitch_mod_array,np.roll(MAJOR_KEY_PROFILE,i))
        for i in range(PITCHES_PER_OCTAVE,2*PITCHES_PER_OCTAVE):
            # rotate MINOR_KEY_PROFILE
            correlation_array[i] = correlation(pitch_mod_array,np.roll(MINOR_KEY_PROFILE,i-PITCHES_PER_OCTAVE))
        result = KEYS[np.argmax(correlation_array)]
        #print('Detected key: ' + result)
        return result
    else:
        print("Total duration null, no keys could be found.")
        return ""
def is_major_key(str):
    return str.endswith("major")