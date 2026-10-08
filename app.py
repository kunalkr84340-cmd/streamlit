            for i, dur in enumerate(durations, start=1):
                start_str = f"{current_time:.3f}"
                duration_str = f"{dur:.3f}"
                out_file = os.path.join(output_dir, f"clip_{i:02d}.mp4")

                # High Quality Re-encoding Command
                ffmpeg_cmd = [
                    "ffmpeg", "-y",
                    "-ss", start_str,
                    "-i", temp_video_path,
                    "-t", duration_str,
                    "-c:v", "libx264",
                    "-crf", "18",
                    "-preset", "ultrafast",
                    "-c:a", "aac",
                    out_file
                ]

                subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                if os.path.exists(out_file) and os.path.getsize(out_file) > 0:
                    clip_files.append(out_file)

                current_time += dur
                
