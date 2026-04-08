def process_video_frames(video_path):
    import cv2, os, sqlite3
    from ultralytics import YOLO

    frames_folder = "data/frames"
    db_path = "data/video_data.db"

    # Create folders
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)

    print("🔍 Loading YOLO model...")
    model = YOLO("yolov8n.pt")

    print("🗄️ Setting up database...")
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

    print("🎞️ Processing frames...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % 60 == 0:
            frame_name = f"frame_{frame_count}.jpg"
            frame_path = os.path.join(frames_folder, frame_name)

            # Save frame
            cv2.imwrite(frame_path, frame)

            # Object detection
            results = model(frame_path)

            object_counts = {}
            for r in results:
                for cls in r.boxes.cls:
                    name = r.names[int(cls)]
                    object_counts[name] = object_counts.get(name, 0) + 1

            # Store in DB
            cursor.execute(
                "INSERT INTO frame_data (frame_name, objects) VALUES (?, ?)",
                (frame_name, str(object_counts))
            )
            conn.commit()

            print(f"✅ {frame_name}: {object_counts}")

        frame_count += 1

    cap.release()
    conn.close()

    print("🎉 Frame processing completed!")
