# -*- coding: ISO-8859-1 -*-
import sys,os
#sys.path.append("..")
#from Song import Song
from canta.song.song_segment import SongSegment
from MidiOutStream import MidiOutStream


#from cantaCli import *

class MidiToText(MidiOutStream):


    def __init__(self, song):
        self.song = song


    """
    This class renders a midi file as text. It is mostly used for debugging
    """

    #############################
    # channel events


    def channel_message(self, message_type, channel, data):
        """The default event handler for channel messages"""
        print 'message_type:%X, channel:%X, data size:%X' % (message_type, channel, len(data))


    #def note_on(self, channel=0, note=((int("0x40",16))-12), velocity=0x40):
    #   print 'note_on  - ch:%02X,  note:%d,  vel:%02X time:%s' % (channel, note, velocity, self.rel_time())

        #print 'note_on  - ch:%02X,  note:%02X,  vel:%02X time:%s' % (channel, note, velocity, self.rel_time())
    #def note_on(self, channel=0, note=0x40, velocity=0x40):
        #print '%s %d '% ( self.rel_time()/30, note-60)
        #       time:    note:

    def note_off(self, channel=0, note=0x40, velocity=0x40):
        print ': %s %s %d- '% ( (self.abs_time()-self.rel_time())/30,self.rel_time()/30, note-60)
        #       time:    note:

        #print 'note_off - ch:%02X,  note:%02X,  vel:%02X time:%s' % (channel, note, velocity, self.rel_time())

        self.song.addSegment(SongSegment(type='note', time_stamp=(self.abs_time()-self.rel_time())/30, duration=self.rel_time()/30, pitch=note-60, text=""))

    def aftertouch(self, channel=0, note=((int("0x40",16))-12), velocity=0x40):
        print 'aftertouch', channel, note, velocity


    def continuous_controller(self, channel, controller, value):
        print 'controller - ch: %02X, cont: #%02X, value: %02X' % (channel, controller, value)


    def patch_change(self, channel, patch):
        print 'patch_change - ch:%02X, patch:%02X' % (channel, patch)


    def channel_pressure(self, channel, pressure):
        print 'channel_pressure', channel, pressure


    def pitch_bend(self, channel, value):
        print 'pitch_bend ch:%s, value:%s' % (channel, value)



    #####################
    ## Common events


    def system_exclusive(self, data):
        print 'system_exclusive - data size: %s' % len(date)


    def song_position_pointer(self, value):
        print 'song_position_pointer: %s' % value


    def song_select(self, songNumber):
        print 'song_select: %s' % songNumber


    def tuning_request(self):
        print 'tuning_request'


    def midi_time_code(self, msg_type, values):
        print 'midi_time_code - msg_type: %s, values: %s' % (msg_type, values)



    #########################
    # header does not really belong here. But anyhoo!!!

    def header(self, format=0, nTracks=1, division=96):
        #print 'format: %s, nTracks: %s, division: %s' % (format, nTracks, division)
        #print '----------------------------------'
        #print ''
        pass

    def eof(self):
        #print 'End of file'
        pass


    def start_of_track(self, n_track=0):
        #print 'Start - track #%s' % n_track
        pass


    def end_of_track(self):
        self.song.addSegment(SongSegment(type='end', time_stamp=(self.abs_time()-self.rel_time())/30, duration=self.rel_time()/30, 		pitch=0, text=""))

        print 'E'




    ###############
    # sysex event

    def sysex_event(self, data):
        print 'sysex_event - datasize: %X' % len(data)



    #####################
    ## meta events

    def meta_event(self, meta_type, data):
        print 'undefined_meta_event:', meta_type, len(data)


    def sequence_number(self, value):
        print 'sequence_number', number



    def text(self, text):
        #print 'text', text
        pass




    def copyright(self, text):
        print 'copyright', text


    def sequence_name(self, text):
        #print 'sequence_name:', text
        pass


    def instrument_name(self, text):
        print 'instrument_name:', text


    def lyric(self, text):
        print 'lyric', text


    def marker(self, text):
        print 'marker', text


    def cuepoint(self, text):
        print 'cuepoint', text


    def midi_ch_prefix(self, channel):
        print 'midi_ch_prefix', channel


    def midi_port(self, value):
        print 'midi_port:', value


    def tempo(self, value):
        #print 'tempo:', value
        print '#BPM:', 60000000/value
        self.song.info['bpm']=60000000/value


    def smtp_offset(self, hour, minute, second, frame, framePart):
        print 'smtp_offset', hour, minute, second, frame, framePart


    def time_signature(self, nn, dd, cc, bb):
        #print 'time_signature:', nn, dd, cc, bb
        pass


    def key_signature(self, sf, mi):
        #print 'key_signature', sf, mi
        pass


    def sequencer_specific(self, data):
        print 'sequencer_specific', len(data)


#
def func1(song):

    #song = Song( "testLied", "ich", "test.ogg", 110, 50)
    #song.addSegment(SongSegment( "tone", 19, 5, 12, "hallo"))
    #song.addSegment(SongSegment( "tone", 24, 5, 33, "blub"))
    #song.addSegment(SongSegment( "tone", 29, 2, 69, "was"))
    #song.addSegment(SongSegment( "tone", 31, 5, 17, "geh-ht"))
    #song.addSegment(SongSegment( "pause", 39))
    #song.addSegment(SongSegment( "tone", 42, 5, 12, "es"))
    #song.addSegment(SongSegment( "tone", 47, 5, 6, "geht"))
    #song.addSegment(SongSegment( "tone", 52, 2, 2, "fast"))
    #song.addSegment(SongSegment( "tone", 54, 5, 3, "allet"))


    #song = Song( "testLied", "ich", "test.ogg", 110, 50)
    #song.readFile('song.txt')



    print "\nSong:"
    print "\tName: " , song.title
    print "\tArtist: " , song.artist
    print "\tAudioFile: " , song.audioFile
    print "\tBPM: " , song.bpm
    print "\tGap: " , song.gap

    print "\n\nSegments:\n"
    startTime = time()

    beatTime = 60. / song.bpm
    #play so   #und
    started = False
    startOfLine = 0
    endOfLine = 6
    end = False
    lineText = ''
    x = 0
    while True:
        x+=1
        #sleep(1)
        actTime = time()
        posTime = actTime - startTime
        realPosTime = posTime - song.gap / 1000
        #print aktTime, " ", position, " ", realPos

        if realPosTime > (song.segments[endOfLine].timeStamp + song.segments[endOfLine].duration) * beatTime:
            print "<zeile zu ende>"
            if end:
                sys.exit()
            startOfLine = endOfLine + 2
            for i in range(startOfLine, len(song.segments)):
                if song.segments[i].type == 'pause':
                    endOfLine = i-1
                    break
                elif song.segments[i].type == 'end':
                    endOfLine = i-1
                    end = True
                    break

        lineSegments = song.segments[startOfLine:endOfLine+1]
        lineText = ''
        goalPitch = '0'
        for segment in lineSegments:
            #print (segment.timeStamp * beatTime)
            #print beatTime
            #actSegment = lineSegments[i]
            if realPosTime >= segment.timeStamp * beatTime and \
                realPosTime < (segment.timeStamp + segment.duration) * beatTime:

                lineText += '[' + segment.text + ']'
                goalPitch = segment.pitch
                timeStamp = segment.timeStamp
            else:
                lineText += segment.text


        print 'Timestamp:'+ str(timeStamp) + 'pitch: ' + str(goalPitch-60) + ' LineText: ' + lineText
        sleep(0.1)
        '''

    for segment in song.songSegments:
        print "\tType: " , segment.type , "\tTimeStamp: " , segment.timeStamp , "\tDuration: " , segment.duration , 			"\tPitch: " , segment.pitch , "\ttext: " , segment.text, "\tFrequenz: ", 440 * (2 ** ((segment.pitch-12-69) / 12))

        print "\n\n"

        '''








if __name__ == '__main__':

    # get data
    #test_file = 'test/midifiles/alleMeineEntchen.mid'
    test_file = 'test/midifiles/Bruder Jakob.mid'
    f = open(test_file, 'rb')

    # do parsing
    from MidiInFile import MidiInFile
    x = MidiToText()
    midiIn = MidiInFile(x, f)
    midiIn.read()
    f.close()
    func1(x.song)
    x.song.write_to_txt('test.txt')
