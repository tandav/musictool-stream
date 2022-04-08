import subprocess
import shlex
import random




def get_videos():
    cmd = 'ssh or3 ls musictool-labeling/static'
    videos = [
        p for p in
        subprocess.check_output(shlex.split(cmd), text=True).splitlines()
        if p.endswith('.mp4')
    ]
    return videos


def creeate_and_upload():
    cmd = 'python -m musictool_stream.daw video_file 1'
    subprocess.check_call(shlex.split(cmd))
    cmd = 'scp *.mp4 or3:musictool-labeling/static'
    subprocess.check_call(cmd, shell=True)
    cmd = 'rm *.mp4'
    subprocess.check_call(cmd, shell=True)

def delete_extra(max_files: int = 1000):
    videos = get_videos()
    print(len(videos))
    if len(videos) <= max_files:
        return
    n_extra = len(videos) - max_files
    rm_videos = random.sample(videos, n_extra)
    rm_videos = ['musictool-labeling/static/' + v for v in rm_videos]
    rm_videos = ' '.join(rm_videos)
    cmd = f'ssh or3 rm {rm_videos}'
    subprocess.check_output(shlex.split(cmd), text=True).splitlines()


while True:
    creeate_and_upload()
    delete_extra()
