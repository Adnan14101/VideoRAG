import os
from moviepy import VideoFileClip
import whisper


def extract_audio_from_video(video_path, audio_path=None):
    """
    Extract audio from a video file and save it as an audio file.
    """
    try:

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")

        if audio_path is None:
            audio_path = os.path.splitext(video_path)[0] + "_audio.mp3"

        print("Loading video file...")
        video = VideoFileClip(video_path)

        if video.audio is None:
            print("Video has no audio track.")
            return None

        print("Extracting audio...")
        video.audio.write_audiofile(audio_path)

        # print(f"Audio saved to: {audio_path}")
        return audio_path
        

    except Exception as e:
        print("Error extracting audio:", e)


def transcribe_audio(audio_path):
    """
    Convert audio to text using Whisper model and save transcript.
    """
    try:
        print("Loading Whisper model...")
        model = whisper.load_model("base")

        print("Transcribing audio...")
        result = model.transcribe(audio_path)

        transcript = result["text"]

        # print("Saving transcript to file...")
        # with open(output_text_file, "w", encoding="utf-8") as f:
        #     f.write(transcript)

        # print(f"Transcript saved to: {output_text_file}")
        return transcript

    except Exception as e:
        print("Error during transcription:", e)


def main():
    """
    Main function to run the pipeline.
    """
    video_path = "/home/prateeksingh/Downloads/videorag/videorag/videoconverter/videoplayback.mp4"
    # audio_path = "/home/prateeksingh/Downloads/videorag/videorag/videoconverter/extracted_audio.mp3"
    # transcript_file = "transcript.txt"

    if not os.path.exists(video_path):
        print("Video file not found!")
        return

    # Step 1: Extract Audio
    audio_path = extract_audio_from_video(video_path)

    # Step 2: Convert Audio to Text
    text = transcribe_audio(audio_path)
    print(text)
    print("\nProcess completed successfully!")


if __name__ == "__main__":
    main()