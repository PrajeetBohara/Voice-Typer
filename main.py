# import asyncio
# import threading
# import tkinter as tk
# from dotenv import load_dotenv
# from deepgram import (
#     DeepgramClient,
#     DeepgramClientOptions,
#     LiveTranscriptionEvents,
#     LiveOptions,
#     Microphone,
# )
# from pynput.keyboard import Controller
#
# # Load environment variables
# load_dotenv()
#
# # Initialize Deepgram and Keyboard Controller
# keyboard = Controller()
# transcript_collector = None
# microphone = None
# transcription_active = False
# deepgram = None
#
# class TranscriptCollector:
#     def __init__(self):
#         self.reset()
#
#     def reset(self):
#         self.transcript_parts = []
#
#     def add_part(self, part):
#         self.transcript_parts.append(part)
#
#     def get_full_transcript(self):
#         return ' '.join(self.transcript_parts)
#
#
# async def get_transcript():
#     global transcript_collector, microphone, deepgram, transcription_active
#
#     try:
#         config = DeepgramClientOptions(options={"keepalive": "true"})
#         deepgram = DeepgramClient("ba92e7efbc845208e2356801c8546a6b03f6c46d", config)
#
#         dg_connection = deepgram.listen.asyncwebsocket.v("1")
#
#         async def on_message(self, result, **kwargs):
#             global transcription_active
#             # Extract the recognized sentence
#             sentence = result.channel.alternatives[0].transcript
#
#             if not result.speech_final:
#                 transcript_collector.add_part(sentence)
#             else:
#                 # This is the final part of the current sentence
#                 transcript_collector.add_part(sentence)
#                 full_sentence = transcript_collector.get_full_transcript()
#                 print(f"speaker: {full_sentence}")
#
#                 # Send the recognized sentence to the active window via keyboard simulation
#                 if transcription_active:
#                     for char in full_sentence:
#                         keyboard.type(char)
#
#                 # Reset the collector for the next sentence
#                 transcript_collector.reset()
#
#         async def on_error(self, error, **kwargs):
#             print(f"\n\n{error}\n\n")
#
#         # Set the Deepgram events
#         dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
#         dg_connection.on(LiveTranscriptionEvents.Error, on_error)
#
#         options = LiveOptions(
#             model="nova-2",
#             punctuate=True,
#             language="en-US",
#             encoding="linear16",
#             channels=1,
#             sample_rate=16000,
#             endpointing=True
#         )
#
#         await dg_connection.start(options)
#
#         # Open a microphone stream on the default input device
#         microphone = Microphone(dg_connection.send)
#
#         # Start the microphone
#         microphone.start()
#
#         while transcription_active:
#             await asyncio.sleep(1)
#
#         # Wait for the microphone to close
#         microphone.finish()
#
#         # Indicate that we've finished
#         dg_connection.finish()
#
#         print("Finished")
#
#     except Exception as e:
#         print(f"Could not open socket: {e}")
#         return
#
#
# def start_transcription():
#     global transcription_active, transcript_collector
#
#     if not transcription_active:
#         transcription_active = True
#         transcript_collector = TranscriptCollector()
#         transcription_thread = threading.Thread(target=asyncio.run, args=(get_transcript(),))
#         transcription_thread.start()
#         status_label.config(text="Status: Transcription is ON")
#
#
# def stop_transcription():
#     global transcription_active
#
#     if transcription_active:
#         transcription_active = False
#         status_label.config(text="Status: Transcription is OFF")
#
#
# # Create the GUI using Tkinter
# root = tk.Tk()
# root.title("Voice Typing with Deepgram")
#
# root.attributes("-topmost", True)
#
# start_button = tk.Button(root, text="Start Voice Typing", command=start_transcription, width=25, height=2)
# stop_button = tk.Button(root, text="Stop Voice Typing", command=stop_transcription, width=25, height=2)
# status_label = tk.Label(root, text="Status: Transcription is OFF", font=("Arial", 14))
#
# start_button.pack(pady=10)
# stop_button.pack(pady=10)
# status_label.pack(pady=10)
#
# root.geometry("400x200")
# root.mainloop()















import asyncio
import threading
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)
from pynput.keyboard import Controller
from PyQt5 import QtWidgets, QtCore
from asyncqt import QEventLoop

# Load environment variables
load_dotenv()

# Initialize Deepgram and Keyboard Controller
keyboard = Controller()
transcript_collector = None
microphone = None
transcription_active = False
deepgram = None

class TranscriptCollector:
    def __init__(self):
        self.reset()

    def reset(self):
        self.transcript_parts = []

    def add_part(self, part):
        self.transcript_parts.append(part)

    def get_full_transcript(self):
        return ' '.join(self.transcript_parts)


async def get_transcript():
    global transcript_collector, microphone, deepgram, transcription_active

    try:
        config = DeepgramClientOptions(options={"keepalive": "true"})
        deepgram = DeepgramClient("ba92e7efbc845208e2356801c8546a6b03f6c46d", config)

        dg_connection = deepgram.listen.asyncwebsocket.v("1")

        async def on_message(self, result, **kwargs):
            global transcription_active
            # Extract the recognized sentence
            sentence = result.channel.alternatives[0].transcript

            if not result.speech_final:
                transcript_collector.add_part(sentence)
            else:
                # This is the final part of the current sentence
                transcript_collector.add_part(sentence)
                full_sentence = transcript_collector.get_full_transcript()
                print(f"speaker: {full_sentence}")

                # Send the recognized sentence to the active window via keyboard simulation
                if transcription_active:
                    for char in full_sentence:
                        keyboard.type(char)

                # Reset the collector for the next sentence
                transcript_collector.reset()

        async def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        # Set the Deepgram events
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        options = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            endpointing=True
        )

        await dg_connection.start(options)

        # Open a microphone stream on the default input device
        microphone = Microphone(dg_connection.send)

        # Start the microphone
        microphone.start()

        while transcription_active:
            await asyncio.sleep(1)

        # Wait for the microphone to close
        microphone.finish()

        # Indicate that we've finished
        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return


class VoiceTypingApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global status_label

        self.setWindowTitle("Voice Typer")
        self.setGeometry(100, 100, 400, 200)

        # Set up the buttons and status label
        self.start_button = QtWidgets.QPushButton("Start Voice Typing", self)
        self.start_button.setGeometry(50, 30, 300, 50)
        self.start_button.clicked.connect(self.start_transcription)

        self.stop_button = QtWidgets.QPushButton("Stop Voice Typing", self)
        self.stop_button.setGeometry(50, 90, 300, 50)
        self.stop_button.clicked.connect(self.stop_transcription)

        self.status_label = QtWidgets.QLabel("Status: Transcription is OFF", self)
        self.status_label.setGeometry(50, 150, 300, 30)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)


        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        # Set custom styles to change colors
        self.setStyleSheet("background-color: #000000;")  # Set window background color

        self.start_button.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;  /* Green background */
                        color: white;                /* White text */
                        font-size: 16px;
                        border-radius: 10px;
                        padding: 10px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;  /* Darker green on hover */
                    }
                """)

        self.stop_button.setStyleSheet("""
                    QPushButton {
                        background-color: #f44336;  /* Red background */
                        color: white;                /* White text */
                        font-size: 16px;
                        border-radius: 10px;
                        padding: 10px;
                    }
                    QPushButton:hover {
                        background-color: #d32f2f;  /* Darker red on hover */
                    }
                """)

        self.status_label.setStyleSheet("""
                    QLabel {
                        color: #FFFFFF;  /* white transcript text */
                        font-size: 14px;
                    }
                """)

        # # Set window to be adaptive to all screen sizes
        # self.resize(QtWidgets.QDesktopWidget().availableGeometry(self).size() * 0.4)

    def start_transcription(self):
        global transcription_active, transcript_collector

        if not transcription_active:
            transcription_active = True
            transcript_collector = TranscriptCollector()
            transcription_thread = threading.Thread(target=asyncio.run, args=(get_transcript(),))
            transcription_thread.start()
            self.status_label.setText("Status: Transcription is ON")

    def stop_transcription(self):
        global transcription_active

        if transcription_active:
            transcription_active = False
            self.status_label.setText("Status: Transcription is OFF")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_window = VoiceTypingApp()
    main_window.show()

    with loop:
        loop.run_forever()
