def process_video_frames(video_path):
    import cv2, os, sqlite3
    from ultralytics import YOLO

    frames_folder = "frames"
    db_path = "video_data.db"

    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)

    model = YOLO("yolov8n.pt")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS frame_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        frame_name TEXT,
        objects TEXT
    )
    """)

    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % 60 == 0:
            frame_name = f"frame_{frame_count}.jpg"
            frame_path = os.path.join(frames_folder, frame_name)

            cv2.imwrite(frame_path, frame)

            results = model(frame_path)

            object_counts = {}
            for r in results:
                for cls in r.boxes.cls:
                    name = r.names[int(cls)]
                    object_counts[name] = object_counts.get(name, 0) + 1

            cursor.execute(
                "INSERT INTO frame_data (frame_name, objects) VALUES (?, ?)",
                (frame_name, str(object_counts))
            )
            conn.commit()

        frame_count += 1

    cap.release()
    conn.close()
