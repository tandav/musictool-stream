
default_octave = 5
# DEFAULT_TUNING = 440  # default A hz tuning
DEFAULT_TUNING = 500
RANDOM_TUNING_RANGE = 420, 510
tuning = DEFAULT_TUNING


# piano_img_size = 14 * 60, 280
piano_img_size = 14 * 18, 85
beats_per_minute = 120
beats_per_second = beats_per_minute / 60
beats_per_bar = 4
bar_seconds = beats_per_bar / beats_per_second


# daw
sample_rate = 44100  # samples per second
midi_folder = 'static/midi/'
# midi_file = 'weird.mid'
# midi_file = 'overlap.mid'
# midi_file = 'dots.mid'
# midi_file = 'halfbar.mid'
# midi_file = 'halfbar-and-short.mid'
# midi_file = 'bassline.mid'
# midi_file = 'drumloop.mid'
# midi_file = '4-4-8.mid'
# chunk_size = 1024 * 32
chunk_size = 1024
# chunk_size = 1024 * 2
# chunk_size = 1024 * 128
# chunk_size = 1024 * 4
chunk_seconds = chunk_size / sample_rate
wav_output_file = 'out.wav'

# samples
kick = 'static/samples/kick-909.wav'
hat = 'static/samples/open-hat-909.wav'
clap = 'static/samples/clap-909.wav'


# streaming
audio_pipe = 'audio.fifo'
video_pipe = 'video.fifo'

# fps = 24
# fps = 30
# fps = 48
# fps = 50
# fps = 44
# fps = 40
# fps = 30
# fps = 55
fps = 60

# frame_width, frame_height = 2560, 1440
frame_width, frame_height = 1920, 1080  # 1080p, recommended bitrate 4.5M
# frame_width, frame_height = 1280, 720  # 720p
# frame_width, frame_height = 854, 480  # 480p
# frame_width, frame_height = 640, 360 # 360p
# frame_width, frame_height = 426, 240  # 240p
video_bitrate = '500k'
# video_bitrate = '3000k'
# video_bitrate = '3m'
audio_bitrate = '128k'

# video_bitrate = '1M'
# video_bitrate = '12M'
# video_bitrate = '24M'
# keyframe_seconds = 0.05  # drastically changes bitrate
# keyframe_seconds = 0.25  # drastically changes bitrate <-----------------------------
# keyframe_seconds = 0.5  # drastically changes bitrate
keyframe_seconds = 1.5  # drastically changes bitrate
# keyframe_seconds = 2  # drastically changes bitrate

gop = int(keyframe_seconds * fps)
draw_threads = 1
# assert draw_threads == 1

bars_per_screen = 4
screen_seconds = bars_per_screen * bar_seconds

chord_px = frame_height / bars_per_screen
# pxps = frame_height // screen_seconds  # pixels per second
pxps = frame_height / screen_seconds  # pixels per second

# video_queue_item_size = 20
video_queue_item_size = 1
assert video_queue_item_size < fps


# OUTPUT_VIDEO = '/tmp/output.flv'
# OUTPUT_VIDEO = '/dev/null'
OUTPUT_VIDEO = None


note_range = None
messages = []

progressions = None
progressions_queue = None


# progressions_search_cache = collections.defaultdict(list)

ui_thread = None


# midi explorer ui

# MIDI_UI_FILE = 'static/midi/vespers-04.mid'
# MIDI_UI_FILE = 'static/midi/vivaldi-winter.mid'
