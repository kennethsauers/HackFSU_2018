from midiutil import MIDIFile
import random


def processCVInput(pitches):
    track = 0
    channel = 0
    time = 0
    duration = 1
    tempo = 250  # default tempo for now
    volume = 100

    newMidi = MIDIFile(1)

    newMidi.addTempo(track, time, tempo)

    for i, pitch in enumerate(pitches):
        newMidi.addNote(track, channel, pitch, time + i, duration, volume)

    with open("new-midi.mid", "wb") as midi_output:
        newMidi.writeFile(midi_output)


def getNum(note_name):
	note_defs = {
    	"g5": 79,
    	"gb5": 78,
    	"f5": 77,
    	"e5": 76,
    	"eb5": 75,
    	"d5": 74,
    	"db5": 73,
    	"c5": 72,
    	"b4": 71,
    	"bb4": 70,
    	"a4": 69,
    	"ab4": 68,
    	"g4": 67,
    	"gb4": 66,
    	"f4": 65,
    	"e4": 64,
    	"eb4": 63,
    	"d4": 62,
    	"db4": 61,
    	"c4": 60,
    	"b3": 59,
    	"bb3": 58,
    	"a3": 57,
   	 	"ab3": 56,
    	"g3": 55,
    	"gb3": 54,
    	"f3": 53,
    	"e3": 52,
    	"eb3": 51,
    	"d3": 50,
    	"db3": 49,
    	"c3": 48,
    	"b2": 47,
    	"bb2": 46,
    	"a2": 45
	}
	return note_defs[note_name]


def main():  # if called as main, generate random amount of pitches
   # degrees = random.sample(range(45, 75), random.randint(15, 25))
   BbMajor = ["bb3", "c4", "d4", "eb4", "f4", "g4", "a4", "bb4"]
   for i, note in enumerate(BbMajor):
   		BbMajor[i] = getNum(BbMajor[i])

    # degrees = degrees + list(reversed(degrees[0:7]))
   #print(BbMajor)
   processCVInput(BbMajor)


if __name__ == '__main__':
    main()
