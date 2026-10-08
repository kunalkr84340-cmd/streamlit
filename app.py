import streamlit as st
import subprocess
import os
import re
import zipfile

st.set_page_config(page_title="Lossless Video Cutter", page_icon="🎬")

st.title("⚡ Lossless Instant Video Cutter")
st.write("Video upload karein aur exact durations enter karke original quality clips ZIP me download karein!")

# Large file upload stability setting
uploaded_file = st.file_uploader(
    "📹 Original Video Upload Karein", 
    type=["mp4", "mov", "avi", "mkv"],
    accept_multiple_files=False
)

durations_text = st.text_area(
    "⏱️ Durations Enter Karein (Seconds me)", 
    value="1.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.8, 1.0, 0.9, 0.9, 1.0, 0.8, 1.9"
)

if st.button("✂️ Video Cut Karein", type="primary"):
    if not uploaded_file or not durations_text:
        st.error("Kripya video upload karein aur durations text enter karein!")
    else:
        with st.spinner("Video clips cut ho rahe hain..."):
            temp_video_path = "temp_input_video.mp4"
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            raw_durations = re.findall(r"[-+]?\d*\.\d+|\d+", durations_text)
            durations = [float(d) for d in raw_durations]

            output_dir = "lossless_clips"
            os.makedirs(output_dir, exist_ok=True)
            
            for f in os.listdir(output_dir):
                try:
                    os.remove(os.path.join(output_dir, f))
                except:
                    pass

            current_time = 0.0
            clip_files = []

            for i, dur in enumerate(durations, start=1):
                start_str = f"{current_time:.3f}"
                duration_str = f"{dur:.3f}"
                out_file = os.path.join(output_dir, f"clip_{i:02d}.mp4")

                ffmpeg_cmd = [
                    "ffmpeg", "-y",
                    "-ss", start_str,
                    "-i", temp_video_path,
                    "-t", duration_str,
                    "-c", "copy",
                    out_file
                ]

                subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                if os.path.exists(out_file) and os.path.getsize(out_file) > 0:
                    clip_files.append(out_file)

                current_time += dur

            if clip_files:
                zip_path = "exact_quality_clips.zip"
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for f in clip_files:
                        zipf.write(f, os.path.basename(f))

                st.success(f"🔥 Done! Total {len(clip_files)} clips cut ho gaye!")
                
                with open(zip_path, "rb") as fp:
                    st.download_button(
                        label="📦 All Clips ZIP Download Karein",
                        data=fp,
                        file_name="exact_quality_clips.zip",
                        mime="application/zip"
                    )
            else:
                st.error("Clips cut nahi ho paye!")
