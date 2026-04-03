session_video_map = {}

def set_session_video(session_id, video_name):
    session_video_map[session_id] = video_name

def get_session_video(session_id):
    return session_video_map.get(session_id)