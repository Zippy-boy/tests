import pyaudio
import wave
import datetime

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORDING_TIME = 120  # Duration of each recording in seconds

def record_audio():
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    start_time = datetime.datetime.now()

    while (datetime.datetime.now() - start_time).total_seconds() < RECORDING_TIME:
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return frames

def save_audio(frames, output_file):
    audio = pyaudio.PyAudio()

    wf = wave.open(output_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def main():
    output_file = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav"
    frames = record_audio()
    save_audio(frames, output_file)
    print(f"Audio recorded and saved as {output_file}")
    return output_file

if __name__ == "__main__":
    main()
