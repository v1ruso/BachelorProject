import unittest
import numpy as np

import pretty_midi
from midi_transform import parse_midi
from pattern_discovery import find_biggest_recurring_pattern
class PatternDiscoveryTest(unittest.TestCase):
    def test_find_biggest_recurring_pattern(self):
        input = pretty_midi.PrettyMIDI("../MIDI_samples/midi_sample_c_major.mid")
        seq = input.instruments[0].notes
        result = pretty_midi.PrettyMIDI()
        result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
        result_instrument = pretty_midi.Instrument(program=result_program)
        result_instrument.notes,index = find_biggest_recurring_pattern(seq)
        result.instruments.append(result_instrument)
        result.write("../MIDI_samples/test_biggest_recurring_pattern.mid")
if __name__ == '__main__':
    unittest.main()