import ffmpeg


def analyse_file(path: str) -> dict:
    try:
        return ffmpeg.probe(path)
    except ffmpeg.Error as e:
        print(e.stderr)
        raise e


def extract_audio_tracks(path: str) -> dict:
    analysis = analyse_file(path)
    audio_tracks = [s for s in analysis["streams"] if s["codec_type"] == "audio"]
    mappings = dict()

    for i, track in enumerate(audio_tracks):
        if "tags" in track:
            mappings[track["tags"]["language"]] = i
        else:
            mappings["unk"] = i
    return mappings
