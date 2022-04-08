import subprocess
import shlex
import random
from pathlib import Path

import datetime
import itertools
import random
import sys
from collections import deque

import mido
from musictool.note import SpecificNote
from musictool.noteset import NoteRange
from musictool.rhythm import Rhythm
from musictool.scale import Scale
from musictool.progression import Progression
from musictool.chord import SpecificChord

from musictool_stream import config
from musictool_stream.daw.midi.parse.sounds import ParsedMidi
from musictool_stream.daw.streams.pcmfile import PCM16File
from musictool_stream.daw.streams.speakers import Speakers
from musictool_stream.daw.streams.video.stream import Video
from musictool_stream.daw.streams.wavfile import WavFile
from musictool_stream.daw.vst.adsr import ADSR
from musictool_stream.daw.vst.organ import Organ
from musictool_stream.daw.vst.sampler import Sampler
from musictool_stream.daw.vst.sine import Sine8
from musictool_stream.util.text import ago


def random_progression():
    return Progression(tuple(
        SpecificChord(frozenset(random.sample(config.note_range, config.n_notes)))
        for _ in range(4)
    ))

def make_rhythms():
    _ = (Rhythm.all_rhythms(n_notes) for n_notes in range(5, 8 + 1))
    _ = itertools.chain.from_iterable(_)
    return tuple(_)


def render_loop(stream, rhythms, progression, bass, synth, drum_midi, drumrack, messages):
    progression, scale = progression
    # rhythm = random.choice(rhythms)

    bass_midi = []
    chord_midi = []

    config.tuning = random.randint(*config.RANDOM_TUNING_RANGE) if random.random() < 0.15 else config.DEFAULT_TUNING

    drumrack.note_mute = {
        SpecificNote('C', 3): random.random() < 0.1,
        SpecificNote('e', 3): random.random() < 0.1,
        SpecificNote('b', 3): random.random() < 0.1,
        SpecificNote('f', 3): random.random() < 0.5,
    }

    # bass.mute = random.random() < 0.03
    bass.mute = True
    bass_rhythm0 = random.choice(rhythms)
    bassline_str = f'bassline {bass_rhythm0.bits}'
    rhythm_score_str = f'score {bass_rhythm0.score:.2f}'

    if random.random() < 0.05:
        bass_rhythm1 = random.choice(rhythms)
        bassline_str += f' {bass_rhythm1.bits}'
        rhythm_score_str += f' {bass_rhythm1.score:.2f}'
    else:
        bass_rhythm1 = bass_rhythm0

    for chord_i, chord in enumerate(progression):
        if chord_i % 2 == 0:
            bass_midi.append(bass_rhythm0.to_midi(note_=chord.notes_ascending[0] + -12))
        else:
            bass_midi.append(bass_rhythm1.to_midi(note_=chord.notes_ascending[0] + -12))
        chord_midi.append(chord.to_midi(n_bars=1))

    bass._adsr.decay = random.uniform(0.1, 0.5)
    bass_midi = ParsedMidi.hstack(bass_midi)
    chord_midi = ParsedMidi.hstack(chord_midi)

    timestamp, rest = random.choice(messages).split(maxsplit=1)
    timestamp = int(timestamp)
    ago_ = ago(datetime.datetime.now().timestamp() - timestamp)
    sha, message = rest.split(maxsplit=1)
    stream.render_chunked(ParsedMidi.vstack(
        [drum_midi, bass_midi, chord_midi],
        [drumrack, bass, synth],
        ['drumrack', 'bass', 'synth'],
        meta={
            'muted': {
                'kick': drumrack.note_mute[SpecificNote('C', 3)],
                'clap': drumrack.note_mute[SpecificNote('e', 3)],
                'open_hat': drumrack.note_mute[SpecificNote('b', 3)],
                'closed_hat': drumrack.note_mute[SpecificNote('f', 3)],
                'bassline': bass.mute,
            },
            'message': f'{sha} | {ago_} | {message}',
            'bassline': bassline_str,
            'rhythm_score': rhythm_score_str,
            'bass_decay': f'bass_decay{bass._adsr.decay:.2f}',
            'tuning': f'tuning{config.tuning}Hz',
            'root_scale': f'root scale: {scale.root.name} {scale.name}',
            'progression': progression,
            'dist': f'dist{progression.distance}',
            'scale': scale,
        },
    ))


def get_videos():
    return list(Path('static').glob('*.mp4'))


def delete_extra(max_files: int = 1000):
    videos = get_videos()
    print(len(videos))
    if len(videos) <= max_files:
        return
    n_extra = len(videos) - max_files
    rm_videos = random.sample(videos, n_extra)
    for v in rm_videos:
        print('rm', v)
        v.unlink()


def main():


    # note_range = NoteRange(SpecificNote('C', 5), SpecificNote('C', 8), noteset=Scale.from_name('C', 'major'))
    # note_range = NoteRange(note_range[0] + -24, note_range[-1])
    # config.note_range = note_range

    rhythms = make_rhythms()
    drum_midi = ParsedMidi.hstack([mido.MidiFile(config.midi_folder + 'drumloop-with-closed-hat.mid')] * config.bars_per_screen)
    bass = Organ(adsr=ADSR(attack=0.001, decay=0.15, sustain=0, release=0.1), amplitude=0.05, transpose=-12)
    drumrack = Sampler()
    synth = Sine8(adsr=ADSR(attack=0.05, decay=0.1, sustain=1, release=0.1), amplitude=0.003, transpose=-24)

    messages = open('static/messages.txt').read().splitlines()

    while True:
        # todo: cleanup
        config.note_range = NoteRange(SpecificNote('C', 6), SpecificNote('C', 8), noteset=Scale.from_name('C', 'major'))
        progression = random_progression()
        config.note_range = NoteRange(config.note_range[0] + -36, config.note_range[-1])

        config.OUTPUT_VIDEO = f"static/{'-'.join(map(str, progression))}.mp4"
        with Video() as stream:
            render_loop(stream, rhythms, (progression, Scale.from_name('C', 'major')), bass, synth, drum_midi, drumrack, messages)
        delete_extra()

if __name__ == '__main__':
    raise SystemExit(main())



# def creeate_and_upload():
#     cmd = 'python -m musictool_stream.daw video_file 1'
#     subprocess.check_call(shlex.split(cmd))
#     cmd = 'mv *.mp4 static'
#     subprocess.check_call(cmd, shell=True)
#
#
# def delete_extra(max_files: int = 1000):
#     videos = get_videos()
#     print(len(videos))
#     if len(videos) <= max_files:
#         return
#     n_extra = len(videos) - max_files
#     rm_videos = random.sample(videos, n_extra)
#     for v in rm_videos:
#         print('rm', v)
#         v.unlink()
#
# while True:
#     creeate_and_upload()
#     delete_extra()
