import functools
import itertools
import operator

import pipe21 as P
from musictool.chord import SpecificChord
from musictool.note import SpecificNote
from musictool.noterange import NoteRange
from musictool.progression import Progression
from musictool.scale import Scale
from musictool.util.sequence_builder import SequenceBuilder
from musictool.voice_leading import checks


def possible_chords(noterange: NoteRange) -> tuple[SpecificChord]:
    assert isinstance(noterange.noteset, Scale) and noterange.noteset.kind == 'diatonic'

    def _notes_to_chord(notes: frozenset[SpecificNote]):
        if root := noterange.noteset.notes_to_triad_root.get(SpecificNote.to_abstract(notes)):
            chord = SpecificChord(notes, root=root)

            if chord.abstract.name == 'diminished':
                return

            if chord[0].abstract != root:
                return

            yield chord

    return (
        noterange
        | P.Pipe(lambda it: itertools.combinations(it, 4))  # 4 voice chords
        | P.Map(frozenset)
        | P.FlatMap(_notes_to_chord)
        | P.FilterFalse(checks.large_spacing)
        | P.Pipe(tuple)
    )


checks_ = (
    lambda a, b: checks.parallel_interval(a, b, 0),
    lambda a, b: checks.parallel_interval(a, b, 7),
    lambda a, b: checks.hidden_parallel(a, b, 0),
    lambda a, b: checks.hidden_parallel(a, b, 7),
    lambda a, b: checks.voice_crossing(a, b),
    lambda a, b: checks.large_leaps(a, b, 5),
    #     lambda a, b: checks.large_leaps(a, b, 4),
    #     lambda a, b: checks.large_leaps(a, b, 3),
    lambda a, b: a.root == b.root,
)


@functools.cache
def no_bad_checks(a: SpecificChord, b: SpecificChord):
    return all(not check(a, b) for check in checks_)


def make_progressions(noterange: NoteRange, n: int = 4):
    return (
        SequenceBuilder(
            n,
            options=possible_chords(noterange),
            curr_prev_constraint={-1: no_bad_checks, -2: lambda a, b: a.root != b.root},
            i_constraints={0: lambda chord: chord.root == noterange.noteset.root},
            unique_key=lambda chord: chord,
            loop=True,
        )
        | P.Map(Progression)
        | P.Unique(operator.methodcaller('transpose_unique_key'))
        | P.Sorted(key=operator.attrgetter('distance'))
    )


# def notes_are_chord(notes: tuple, scale_chords: frozenset[Chord]):
#     abstract = tuple(n.abstract for n in notes)
#     abstract_fz = frozenset(abstract)
#
#     for chord in scale_chords:
#         if abstract_fz == chord.notes:
#             root = chord.root
#             break
#     else:
#         return
#     chord = SpecificChord(frozenset(notes), root=root)
#     if chord[0].abstract != root:
#         return
#     yield chord
#
#
# def possible_chords(scale: Scale, noterange: NoteRange) -> tuple[SpecificChord]:
#     return (
#         noterange
#         | P.Filter(lambda note: note.abstract in scale.notes)
#         | P.Pipe(lambda it: itertools.combinations(it, 4))  # 4 voice chords
#         | P.FlatMap(lambda notes: notes_are_chord(notes, frozenset(chord for chord in scale.triads if chord.name != 'diminished')))
#         | P.FilterFalse(checks.large_spacing)
#         | P.Pipe(tuple)
#     )
#
# checks_ = (
#     lambda a, b: checks.have_parallel_interval(a, b, 0),
#     lambda a, b: checks.have_parallel_interval(a, b, 7),
#     lambda a, b: checks.have_hidden_parallel(a, b, 0),
#     lambda a, b: checks.have_hidden_parallel(a, b, 7),
#     lambda a, b: checks.have_voice_crossing(a, b),
#     lambda a, b: checks.have_large_leaps(a, b, 5),
# )
#
#
# @functools.cache
# def no_bad_checks(a: SpecificChord, b: SpecificChord):
#     return all(not check(a, b) for check in checks_)
#
#
#
# def make_progressions(
#     scale: Scale,
#     note_range: tuple[SpecificNote],
#     n=4,
# ):
#     return (
#         SequenceBuilder(
#             n,
#             options=possible_chords(scale, note_range),
#             curr_prev_constraint=no_bad_checks,
#             i_constraints={0: lambda chord: chord.root == scale.root},
#             unique_key=lambda chord: chord.root,
#         )
#         | P.Pipe(lambda it: unique(it, key=transpose_uniqiue_key))
#         | P.KeyBy(progression_dist)
#         | P.Pipe(lambda x: sorted(x, key=operator.itemgetter(0)))
#         | P.Pipe(tuple)
#     )
#
# def make_progressions(note_range_, scale=Scale.from_name('C', 'phrygian')):
#     progressions = []
#     scales = [Scale.from_name(note, name) for note, name in scale.note_scales.items()]
#     for scale in scales:
#         for dist, p in voice_leading.make_progressions(scale, note_range_):
#             P = p, dist, scale
#             progressions.append(P)
#             config.progressions_search_cache[''.join(c.root.name for c in p)].append(P)
#     return progressions
