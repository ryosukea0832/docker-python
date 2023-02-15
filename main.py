
# -*- coding: utf-8 -*-
# gui

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

#
import os,subprocess,shutil,sys,threading

import speech_recognition as sr

# 音声ファイルの分割
import wave
import math
import struct
import numpy as geek
import time

start_flag  = False
videoPach = str("")

def meke_c():
    
    os.makedirs('./wav', exist_ok=True)
    os.makedirs('./cut_wav',exist_ok=True)
    return

def meke_d():
    if os.path.exists('./wav'):
        shutil.rmtree('./wav')
    if os.path.exists('./cut_wav'):
        shutil.rmtree('./cut_wav')
    return
    

# mp4から音声ファイルへの変換
def move_to_wav(mp4f):

    fileNme = os.path.splitext(os.path.basename(mp4f))[0]
    fileNme + '.wav'
    work_wav = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'wav',fileNme + '.wav')
    
    print(work_wav)

    
    if os.path.exists(work_wav):
     os.remove(work_wav)
  
    command = ['ffmpeg', '-i', mp4f, work_wav]
    startFfmpeg(command)
    print("mp4から音声ファイルへの変換")
    print(work_wav)
    return work_wav

# 音声ファイルの分割(デフォルト30秒)
def cut_wav(wavf,time=30):
    # timeの単位は[sec]
    # ファイルを読み出し
    print("cut_wav",wavf)
    wr = wave.open(wavf, 'r')

    # waveファイルが持つ性質を取得
    ch = wr.getnchannels()
    width = wr.getsampwidth()
    fr = wr.getframerate()
    fn = wr.getnframes()
    total_time = 1.0 * fn / fr
    integer = math.floor(total_time) # 小数点以下切り捨て
    t = int(time)  # 秒数[sec]
    frames = int(ch * fr * t)
    num_cut = int(integer//t)

    # waveの実データを取得し、数値化
    data = wr.readframes(wr.getnframes())
    wr.close()
    X = geek.fromstring(data, dtype='int16')
  
    # wavファイルを削除
    os.remove(wavf)

    iDir = os.path.abspath(os.path.dirname(sys.argv[0]))
  
    outf_list = []
    for i in range(num_cut):
        # 出力データを生成
        outf = iDir + '/cut_wav/' + str(i).zfill(3) + '.wav'
        start_cut = i*frames
        end_cut = i*frames + frames
        Y = X[start_cut:end_cut]
        outd = struct.pack("h" * len(Y), *Y)

        # 書き出し
        ww = wave.open(outf, 'w')
        ww.setnchannels(ch)
        ww.setsampwidth(width)
        ww.setframerate(fr)
        ww.writeframes(outd)
        ww.close()
      
        # リストに追加
        outf_list.append(outf)
        
    print(outf_list)
    return outf_list

# 複数ファイルの音声のテキスト変換（日本語）
def cut_wavs_str(outf_list):
    output_text = []
    cont = 0
    # 複数処理
    print('音声のテキスト変換')
    for fwav in outf_list:
            try:
                r = sr.Recognizer()
                # 音声->テキスト
                with sr.AudioFile(fwav) as source:
                    print('音声→テキスト ')
                    audio = r.record(source)
                    text = r.recognize_google(audio, language='ja-JP')
                    # 各ファイルの出力結果の結合
                    output_text.append(text)
                    # wavファイルを削除
                    #os.remove(fwav)
            except sr.UnknownValueError:
                print("could not understand audio " + fwav)
                # wavファイルを削除
                os.remove(fwav)
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return output_text


# 実行ボタン押下時の実行関数
def conductMain():
    global videoPach
    global start_flag

    while True:
 
        if start_flag:

            if os.path.exists(videoPach):

                print(videoPach)

                # 音声ファイルへの変換
                wav_file = move_to_wav(videoPach)
                print(wav_file)

                # 音声ファイルの分割(デフォルト30秒)
                cut_wavs = cut_wav(wav_file)

                # 複数ファイルの音声のテキスト変換
                out_text = cut_wavs_str(cut_wavs)

                for text in out_text:
                # テキストファイルへの入力
                    text =  text + '\n'
                    txtbox.insert(tk.END,text)
                print("終了　後処理")
            start_flag  = False
            progress.withdraw()

def start_transcription():
    global videoPach
    global start_flag 

    
    if not (start_flag):
        videoPach = entry2.get()    
        start_flag  = True
        
        bar.start()
        progress.deiconify()

    print("start_transcription",videoPach,start_flag)

# フォルダ指定の関数
def dirdialog_clicked():
    print("dirdialog_clicked")
#    iDir = os.path.abspath(os.path.dirname(__file__))
#    iDirPath = filedialog.askdirectory(initialdir = iDir)
#    entry1.set(iDirPath)

# ファイル指定の関数
def filedialog_clicked():
    fTyp = [("", "*.mov")]
    iFile = os.path.abspath(os.path.dirname(sys.argv[0]))
    iFilePath = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
    entry2.set(iFilePath)

def startFfmpeg(command):

    subprocess.run(command ,encoding='utf-8', stdout=subprocess.PIPE)
#    p = subprocess.Popen(command ,encoding='utf-8', shell=True)
#    p.wait


def mozi_exe():
    meke_d()
    sub_window.destroy()
    progress.destroy()
    baseGround.destroy()
    sys.exit()


if __name__ == "__main__":

    #main関数的な。。
    meke_c()

    # メインウィンドウを作成
    baseGround = tk.Tk()
    # ウィンドウのサイズを設定
    baseGround.geometry('500x300')
    # 画面タイトル
    baseGround.title('動画より文字お越しアプリ')

    # Frame1の作成
    frame1 = ttk.Frame(baseGround, padding=10)
    frame1.grid(row=0, column=1, sticky=E)

    # 「フォルダ参照」ラベルの作成
    IDirLabel = ttk.Label(frame1, text="フォルダ参照＞＞", padding=(5, 2))
    IDirLabel.pack(side=LEFT)

    # 「フォルダ参照」エントリーの作成
    entry1 = StringVar()
    IDirEntry = ttk.Entry(frame1, textvariable=entry1, width=30)
    IDirEntry.pack(side=LEFT)

    # 「フォルダ参照」ボタンの作成
    IDirButton = ttk.Button(frame1, text="参照", command=dirdialog_clicked)
    IDirButton.pack(side=LEFT)

    # Frame2の作成
    frame2 = ttk.Frame(baseGround, padding=10)
    frame2.grid(row=2, column=1, sticky=E)

    # 「ファイル参照」ラベルの作成
    IFileLabel = ttk.Label(frame2, text="ファイル参照＞＞", padding=(5, 2))
    IFileLabel.pack(side=LEFT)

    # 「ファイル参照」エントリーの作成
    entry2 = StringVar()
    IFileEntry = ttk.Entry(frame2, textvariable=entry2, width=30)
    IFileEntry.pack(side=LEFT)

    # 「ファイル参照」ボタンの作成
    IFileButton = ttk.Button(frame2, text="参照", command=filedialog_clicked)
    IFileButton.pack(side=LEFT)

    # Frame3の作成
    frame3 = ttk.Frame(baseGround, padding=10)
    frame3.grid(row=5,column=1,sticky=W)

    # 実行ボタンの設置
    button1 = ttk.Button(frame3, text="実行", command=start_transcription)
    button1.pack(fill = "x", padx=30, side = "left")

    # キャンセルボタンの設置
    button2 = ttk.Button(frame3, text=("閉じる"), command=mozi_exe)
    button2.pack(fill = "x", padx=30, side = "left")

    #フレームの作成
    sub_window = tk.Toplevel()
    sub_window.title("動画より変換した文字列を表示")
    sub_window.geometry('700x600')

    # Frame4の作成
    frame4 = ttk.Frame(sub_window, padding=10)
    frame4.pack(fill=tk.BOTH, expand=tk.YES)

    #テキストボックスの作成
    txtbox = tk.Text(frame4, width=400, height=300)  

    #縦方向スクロールバーの作成
    yscroll = ttk.Scrollbar(frame4, orient=tk.VERTICAL, command=txtbox.yview)
    yscroll.pack(side=tk.RIGHT, fill="y")

    #動きをスクロールバーに反映
    txtbox["yscrollcommand"] = yscroll.set

    #テキストボックスの設置
    txtbox.pack()

    progress = tk.Toplevel()
    bar = ttk.Progressbar(progress,mode='indeterminate')
    bar.pack()
    progress.withdraw()

    th1 = threading.Thread(target=conductMain)
    th1.setDaemon(True)
    th1.start()
    
    baseGround.protocol("WM_DELETE_WINDOW", mozi_exe)
    sub_window.protocol("WM_DELETE_WINDOW", mozi_exe)
    progress.protocol("WM_DELETE_WINDOW", mozi_exe)
    baseGround.mainloop()
        