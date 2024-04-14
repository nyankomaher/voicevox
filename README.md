# VOICEVOX with Your Voice

VOICEVOXのイントネーション調整を手動でやるのが面倒だったため、自分の声でイントネーションを設定できるようにしました。  

**⚠️EXPERIMENTAL⚠️**  
**⚠️ADHOC⚠️**  

## 感謝

### VOICEVOX

言わずと知れたVOICEVOXです。感謝。  
https://voicevox.hiroshiba.jp/

### 各種音声解析ツール

これらのツールのお陰で発声した文字ごとにピッチを抽出することができます。感謝。  
https://github.com/timmahrt/praatIO  
https://github.com/julius-speech/segmentation-kit/tree/master  
https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder  

## 前提

- [VOICEVOX](https://voicevox.hiroshiba.jp/)
- [Praat](https://www.fon.hum.uva.nl/praat/)
- [Julius 音素セグメンテーションキット](https://github.com/julius-speech/segmentation-kit/tree/master)
- python3
- perl5
- Mac

## インストール

### VOICEVOX

[VOICEVOX](https://github.com/VOICEVOX/voicevox)をforkしていますので、まずはそちらのインストール手順を実行してください。

### pythonライブラリ

```sh
pip install numpy scipy pyworld praatio
```

### .env設定

```sh
# python
PYTHON=/path/to/your/python
# perl
PERL=/path/to/your/perl
# Julius 音素セグメンテーションキット
EXTERNAL_SEGMENTATION_KIT=/path/to/your/segmentation-kit
# TextGridConverter
EXTERNAL_TEXT_GRID_CONTAINER=/path/to/your/TextGridConverter
```

上記のほか、VITE_DEFAULT_ENGINE_INFOSのexecutionFilePathをお使いの環境のものに合わせてください。

## 使用方法

1. fork元の[VOICEVOX](https://github.com/VOICEVOX/voicevox)を参考にしてVOICEVOXを起動してください。  
1. セリフを入力し、イントネーション欄にセリフのイントネーションを表示させてください。  
1. イントネーション欄の左上にある、マイクアイコンの録音ボタンをクリックしてください。  
1. お好みのイントネーションでセリフを喋ってください。  
1. マイクアイコンを再度クリックしてください。録音が停止され、イントネーションが反映されます。  

### チューニング

人によって声の高さは違いますので、望みのピッチにするためにはチューニングが必要です。  
public/python/extract_pitch.py の calc_adjusted_pitch を自分の声に合うように修正してください。  

## メモ

* 基本的に、アクセントタブで正しく語句を区切って、アクセントを設定してあげればいい感じになることが多いです。基本的に、本ツールの出番はありません。
  * ちょっと変わったイントネーションにしたいときは効果があるかもしれません。
  * 話者の演技力の問題もあると思いますが、ピッチをうまく取ってくれたり取ってくれなかったりします。
  * 役に立ったり立たなかったりするツールです。
* 入力デバイスを変更すると、VOICEVOXの再起動が必要になるようです。
  * コンソールにTextGridがNotFound的なエラーが出ますが、音声が取れていないためのようです。
  * MediaStreamを毎回作り直せば治る？
* ノイズが少ない方が精度は良くなると思いますが、MacBookAirの内蔵マイクでもなんとかなるようです？

## ライセンス

LGPL v3