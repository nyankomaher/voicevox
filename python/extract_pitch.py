import sys
from os.path import join
import math
from pathlib import Path
import numpy as np
from scipy.io import wavfile
import pyworld
from praatio import textgrid, utilities
import json
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('tempdir')
args = parser.parse_args()

tempdir = args.tempdir

def extract_pitch(wav_file_path):
    fs, data = wavfile.read(wav_file_path)
    data = data.astype(np.float64)
    _f0, t = pyworld.dio(data, fs)
    f0 = pyworld.stonemask(data, _f0, t, fs)
    pitch_by_time = [(time, pitch) for time, pitch in zip(t, f0) if pitch != 0]

    return pitch_by_time


def assign_pitch_to_mora(text, text_grid_file_path, pitch_by_time):
    mora_text = re.findall(r'.[ゃゅょぁぃぅぇぉ]?', text)  # 拗音などはまとめて1モーラにする
    tg = textgrid.openTextgrid(text_grid_file_path, False)
    intervals = tg.getTier("mora").getValuesInIntervals(pitch_by_time)
    pitch_by_mora = []
    for index, (interval, pitches) in enumerate(intervals):
        if len(pitches) == 0:
            pitches = [
                utilities.utils.getValueAtTime(interval.start, pitch_by_time, True)[0],
                utilities.utils.getValueAtTime(interval.end, pitch_by_time, True)[0]
            ]
        pitch_by_mora.append(
            {
                "mora": mora_text[index],
                "label": interval.label,
                "pitch": calc_adjusted_pitch(interval, pitches),
            }
        )

    return pitch_by_mora


# 1モーラから抽出したピッチ（複数。モーラの頭、モーラの中、モーラの最後、など）が引数で与えられるので、
# VOICEVOX上で当該モーラに設定する最終的なピッチを計算する。
def calc_adjusted_pitch(interval, pitches):
    pitch_values = [v for _, v in pitches]
    pitch = np.array(pitch_values).mean()

    return math.log(pitch) + 0.8


text_file_path = join(tempdir, "voice.txt")
wav_file_path = join(tempdir, "voice.wav")
text_grid_file_path = join(tempdir, "voice.TextGrid")
text = Path(text_file_path).read_text()

pitch_by_time = extract_pitch(wav_file_path)
pitch_by_mora = assign_pitch_to_mora(text, text_grid_file_path, pitch_by_time)
pitch_by_mora_json = json.dumps(pitch_by_mora, indent=2)

sys.stdout.write(pitch_by_mora_json)
Path(join(tempdir, "pitchByMora.json")).write_text(pitch_by_mora_json)
