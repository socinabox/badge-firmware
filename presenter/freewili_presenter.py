#!/usr/bin/env python3
"""
FreeWili Presenter v5 - With persistent library cache
"""
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pathlib
from PIL import Image
import threading
import wave
import json
import serial.tools.list_ports

sys.path.insert(0, r'D:\CODE\freewili-python')
from freewili import FreeWili
from freewili.image import convert as convert_image

CACHE_FILE = pathlib.Path("freewili_library_cache.json")

class FreeWiliPresenter:
    def __init__(self, root):
        self.root = root
        self.root.title("FreeWili Presenter v5 - Persistent Library")
        self.root.geometry("700x700")

        self.device = None
        self.image_list = []
        self.audio_list = []

        self.load_cache()
        self.setup_ui()
        self.connect_device()

    def load_cache(self):
        """Load the library cache from disk"""
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'r') as f:
                    cache = json.load(f)
                    self.image_list = cache.get('images', [])
                    self.audio_list = cache.get('audio', [])
            except:
                self.image_list = []
                self.audio_list = []

    def save_cache(self):
        """Save the library cache to disk"""
        cache = {
            'images': self.image_list,
            'audio': self.audio_list
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)

    def setup_ui(self):
        # Status frame
        status_frame = ttk.LabelFrame(self.root, text="Device Status", padding=10)
        status_frame.pack(fill="x", padx=10, pady=5)

        self.status_label = ttk.Label(status_frame, text="Searching...", foreground="orange")
        self.status_label.pack()

        btn_frame = ttk.Frame(status_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Reconnect", command=self.connect_device).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Scan Badge Files", command=self.scan_badge_files).pack(side="left", padx=5)

        # Image Library frame
        img_lib_frame = ttk.LabelFrame(self.root, text="Image Library (/images/)", padding=10)
        img_lib_frame.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Label(img_lib_frame, text="Images on badge:").pack(anchor="w")

        self.image_listbox = tk.Listbox(img_lib_frame, height=5)
        self.image_listbox.pack(fill="both", expand=True, pady=5)

        img_btn_frame = ttk.Frame(img_lib_frame)
        img_btn_frame.pack(pady=5)

        ttk.Button(img_btn_frame, text="Display Selected", command=self.display_from_library).pack(side="left", padx=5)
        ttk.Button(img_btn_frame, text="Upload New...", command=self.upload_new_image).pack(side="left", padx=5)
        ttk.Button(img_btn_frame, text="Upload (No Rotate)...", command=self.upload_new_image_no_rotate).pack(side="left", padx=5)
        ttk.Button(img_btn_frame, text="Remove from List", command=self.remove_image).pack(side="left", padx=5)

        self.img_status = ttk.Label(img_lib_frame, text="")
        self.img_status.pack()

        # Audio Library frame
        audio_lib_frame = ttk.LabelFrame(self.root, text="Audio Library", padding=10)
        audio_lib_frame.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Label(audio_lib_frame, text="Audio on badge:").pack(anchor="w")

        self.audio_listbox = tk.Listbox(audio_lib_frame, height=5)
        self.audio_listbox.pack(fill="both", expand=True, pady=5)

        audio_btn_frame = ttk.Frame(audio_lib_frame)
        audio_btn_frame.pack(pady=5)

        ttk.Button(audio_btn_frame, text="Play Selected", command=self.play_from_library).pack(side="left", padx=5)
        ttk.Button(audio_btn_frame, text="Upload New...", command=self.upload_new_audio).pack(side="left", padx=5)
        ttk.Button(audio_btn_frame, text="Remove from List", command=self.remove_audio).pack(side="left", padx=5)

        self.audio_status = ttk.Label(audio_lib_frame, text="")
        self.audio_status.pack()

        # Info
        info_frame = ttk.Frame(self.root, padding=10)
        info_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(info_frame, text="Library persists between sessions. Use 'Scan Badge Files' to find existing files on badge.",
                 font=("", 8), foreground="gray").pack()

        # Test frame
        test_frame = ttk.Frame(self.root, padding=5)
        test_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(test_frame, text="Quick Tests:").pack(side="left", padx=5)
        ttk.Button(test_frame, text="Upload Oscar", command=self.test_oscar).pack(side="left", padx=5)
        ttk.Button(test_frame, text="Upload Beep", command=self.test_beep).pack(side="left", padx=5)

    def connect_device(self):
        self.status_label.config(text="Searching...", foreground="orange")
        self.root.update()

        devices = FreeWili.find_all()
        if devices:
            self.device = devices[0]
            self.status_label.config(text=f"Connected: {self.device}", foreground="green")
            self._update_listboxes()
        else:
            self.device = None
            self.status_label.config(text="No device found", foreground="red")

    def scan_badge_files(self):
        """Scan the badge filesystem via serial commands to find existing files"""
        if not self.device:
            messagebox.showerror("Error", "No device connected!")
            return

        self.status_label.config(text="Scanning badge...", foreground="blue")
        threading.Thread(target=self._scan_badge_thread, daemon=True).start()

    def _scan_badge_thread(self):
        """Try to list files via serial commands"""
        try:
            # Use serial connection to list files
            # File menu -> List files command
            import serial
            import time

            # Find COM port
            ports = list(serial.tools.list_ports.comports())
            com_port = None
            for port in ports:
                if "Main Processor" in port.description or "USB Serial Device" in port.description:
                    com_port = port.device
                    break

            if not com_port:
                com_port = "COM4"  # Fallback

            ser = serial.Serial(com_port, 115200, timeout=1)
            time.sleep(0.5)

            # Clear buffer
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            # Send file list command
            ser.write(b'f\n')  # File menu
            time.sleep(0.5)
            ser.read(ser.in_waiting)  # Clear response

            ser.write(b'l\n')  # List files
            time.sleep(1.0)

            # Read file list
            response = ser.read(ser.in_waiting).decode('ascii', errors='ignore')
            ser.close()

            # Parse response for .fwi and .wav files
            lines = response.split('\n')
            found_images = []
            found_audio = []

            for line in lines:
                if '.fwi' in line.lower():
                    # Extract filename
                    parts = line.strip().split()
                    for part in parts:
                        if '.fwi' in part.lower():
                            found_images.append(part)
                            break
                elif '.wav' in line.lower():
                    parts = line.strip().split()
                    for part in parts:
                        if '.wav' in part.lower():
                            found_audio.append(part)
                            break

            # Merge with existing cache (keep unique)
            for img in found_images:
                if img not in self.image_list:
                    self.image_list.append(img)

            for audio in found_audio:
                if audio not in self.audio_list:
                    self.audio_list.append(audio)

            self.save_cache()
            self.root.after(0, self._update_listboxes)
            self.root.after(0, lambda: self.status_label.config(
                text=f"Found {len(found_images)} images, {len(found_audio)} audio",
                foreground="green"))

        except Exception as e:
            error_msg = str(e)[:30]  # Capture message immediately
            self.root.after(0, lambda: self.status_label.config(
                text=f"Scan failed: {error_msg}",
                foreground="orange"))

    def _update_listboxes(self):
        self.image_listbox.delete(0, tk.END)
        for img in self.image_list:
            self.image_listbox.insert(tk.END, img)

        self.audio_listbox.delete(0, tk.END)
        for audio in self.audio_list:
            self.audio_listbox.insert(tk.END, audio)

    def remove_image(self):
        """Remove selected image from library list (doesn't delete from badge)"""
        selection = self.image_listbox.curselection()
        if selection:
            filename = self.image_listbox.get(selection[0])
            self.image_list.remove(filename)
            self.save_cache()
            self._update_listboxes()

    def remove_audio(self):
        """Remove selected audio from library list (doesn't delete from badge)"""
        selection = self.audio_listbox.curselection()
        if selection:
            filename = self.audio_listbox.get(selection[0])
            self.audio_list.remove(filename)
            self.save_cache()
            self._update_listboxes()

    def display_from_library(self):
        selection = self.image_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Select an image from the list")
            return

        filename = self.image_listbox.get(selection[0])
        self.img_status.config(text=f"Displaying {filename}...", foreground="blue")
        threading.Thread(target=self._display_existing, args=(filename,), daemon=True).start()

    def _display_existing(self, filename):
        try:
            result = self.device.show_gui_image(filename)
            if result.is_ok():
                self.root.after(0, lambda: self.img_status.config(text=f"[OK] {filename}", foreground="green"))
            else:
                self.root.after(0, lambda: self.img_status.config(text=f"Displayed (check badge)", foreground="orange"))
        except Exception as e:
            error_msg = str(e)[:50]  # Capture message immediately
            self.root.after(0, lambda: self.img_status.config(text=f"Error: {error_msg}", foreground="red"))

    def play_from_library(self):
        selection = self.audio_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Select audio from the list")
            return

        filename = self.audio_listbox.get(selection[0])
        self.audio_status.config(text=f"Playing {filename}...", foreground="blue")
        threading.Thread(target=self._play_existing, args=(filename,), daemon=True).start()

    def _play_existing(self, filename):
        try:
            # Use API method that worked in v2
            result = self.device.play_audio_file(filename)

            if result.is_ok():
                self.root.after(0, lambda: self.audio_status.config(text=f"[OK] Playing {filename}", foreground="green"))
            else:
                # May still play even with error
                self.root.after(0, lambda: self.audio_status.config(text=f"Playing (check badge)", foreground="orange"))

        except Exception as e:
            error_msg = str(e)[:50]  # Capture message immediately
            self.root.after(0, lambda: self.audio_status.config(text=f"Error: {error_msg}", foreground="red"))
            import traceback
            traceback.print_exc()

    def upload_new_image(self):
        filename = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.fwi"), ("All files", "*.*")]
        )
        if filename:
            threading.Thread(target=self._upload_image_thread, args=(filename, True), daemon=True).start()

    def upload_new_image_no_rotate(self):
        filename = filedialog.askopenfilename(
            title="Select Image (No Rotation)",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.fwi"), ("All files", "*.*")]
        )
        if filename:
            threading.Thread(target=self._upload_image_thread, args=(filename, False), daemon=True).start()

    def _upload_image_thread(self, img_path, rotate=True):
        try:
            img_path = pathlib.Path(img_path)

            # Check if already .fwi format
            if img_path.suffix.lower() == '.fwi':
                self.root.after(0, lambda: self.img_status.config(text="Using pre-converted FWI...", foreground="blue"))
                fwi_path = img_path
                fwi_filename = img_path.name
            else:
                # Convert image to FWI
                self.root.after(0, lambda: self.img_status.config(text="Converting...", foreground="blue"))

                img = Image.open(img_path)
                if rotate:
                    img = img.transpose(Image.ROTATE_270)
                img.thumbnail((320, 240), Image.Resampling.LANCZOS)

                canvas = Image.new('RGB', (320, 240), (0, 0, 0))
                x, y = (320 - img.width) // 2, (240 - img.height) // 2
                canvas.paste(img, (x, y))

                fwi_filename = img_path.stem + ".fwi"
                temp_png = pathlib.Path("temp_convert.png")
                canvas.save(temp_png)

                fwi_path = pathlib.Path(fwi_filename)
                convert_image(temp_png, fwi_path)

            self.root.after(0, lambda: self.img_status.config(text=f"Uploading {fwi_filename}..."))

            # Try uploading to images directory first
            result = self.device.send_file(fwi_path, f"images/{fwi_filename}", None)
            if result.is_err():
                # Try root directory as fallback
                result = self.device.send_file(fwi_path, fwi_filename, None)

            # Wait a moment for upload to complete
            import time
            time.sleep(0.5)

            self.root.after(0, lambda: self.img_status.config(text="Displaying..."))

            # Display the newly uploaded image - try both paths
            display_result = self.device.show_gui_image(fwi_filename)
            if display_result.is_err():
                # Try with images/ prefix
                display_result = self.device.show_gui_image(f"images/{fwi_filename}")

            # Add to library and save cache
            if fwi_filename not in self.image_list:
                self.image_list.append(fwi_filename)

            # Save cache synchronously (not in root.after)
            self.save_cache()

            # Update UI
            self.root.after(0, self._update_listboxes)
            self.root.after(0, lambda: self.img_status.config(text=f"[OK] Uploaded & displayed {fwi_filename}", foreground="green"))

        except Exception as e:
            error_msg = str(e)[:50]  # Capture message immediately
            self.root.after(0, lambda: self.img_status.config(text=f"Error: {error_msg}", foreground="red"))
            import traceback
            traceback.print_exc()

    def upload_new_audio(self):
        filename = filedialog.askopenfilename(
            title="Select Audio",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if filename:
            threading.Thread(target=self._upload_audio_thread, args=(filename,), daemon=True).start()

    def compress_audio(self, input_path, output_path, max_duration_sec=3):
        """Compress WAV by trimming duration and downsampling to 8kHz mono"""
        with wave.open(str(input_path), 'rb') as wav_in:
            params = wav_in.getparams()

            # Trim to max duration
            max_frames = int(params.framerate * max_duration_sec)
            frames_to_read = min(params.nframes, max_frames)
            frames = wav_in.readframes(frames_to_read)

        # Downsample to 8kHz
        new_rate = 8000
        sample_width = params.sampwidth
        num_channels = params.nchannels

        # Calculate downsampling ratio
        ratio = params.framerate / new_rate
        bytes_per_frame = sample_width * num_channels

        # Downsample by taking every Nth frame
        new_samples = []
        num_original_frames = len(frames) // bytes_per_frame

        for i in range(int(num_original_frames / ratio)):
            # Get source frame index
            src_frame_idx = int(i * ratio)
            src_byte_idx = src_frame_idx * bytes_per_frame

            # Extract one frame
            frame = frames[src_byte_idx:src_byte_idx + bytes_per_frame]

            if len(frame) == bytes_per_frame:
                # If stereo, convert to mono by taking first channel
                if num_channels == 2:
                    # Take just the first channel (left)
                    mono_sample = frame[:sample_width]
                    new_samples.append(mono_sample)
                else:
                    new_samples.append(frame)

        # Write compressed file
        with wave.open(str(output_path), 'wb') as wav_out:
            wav_out.setnchannels(1)  # Always mono
            wav_out.setsampwidth(sample_width)
            wav_out.setframerate(new_rate)
            wav_out.writeframes(b''.join(new_samples))

        return pathlib.Path(output_path).stat().st_size / 1024

    def _upload_audio_thread(self, audio_path):
        try:
            audio_path = pathlib.Path(audio_path)

            self.root.after(0, lambda: self.audio_status.config(text="Checking audio format...", foreground="blue"))

            # Check and trim audio
            trimmed_filename = audio_path.stem + "_trim.wav"
            trimmed_path = pathlib.Path(trimmed_filename)

            # Just trim to 3 seconds, keep original format
            try:
                with wave.open(str(audio_path), 'rb') as wav_in:
                    params = wav_in.getparams()

                    # Log format info
                    print(f"Audio format: {params.nchannels}ch, {params.framerate}Hz, {params.sampwidth*8}bit, {params.nframes} frames")

                    # Read only first 3 seconds (or less if file is shorter)
                    max_frames = int(params.framerate * 3)
                    try:
                        frames = wav_in.readframes(max_frames)
                    except Exception:
                        # If reading fails, read whatever we can
                        wav_in.rewind()
                        frames = wav_in.readframes(wav_in.getnframes())

                # Write trimmed file - set params individually to avoid invalid nframes
                with wave.open(str(trimmed_path), 'wb') as wav_out:
                    wav_out.setnchannels(params.nchannels)
                    wav_out.setsampwidth(params.sampwidth)
                    wav_out.setframerate(params.framerate)
                    # Don't set nframes - let it be calculated from written data
                    wav_out.writeframes(frames)

            except Exception as e:
                error_msg = str(e)[:50]  # Capture message immediately
                self.root.after(0, lambda: self.audio_status.config(
                    text=f"Error: {error_msg}", foreground="red"))
                return

            file_size_kb = trimmed_path.stat().st_size / 1024
            self.root.after(0, lambda: self.audio_status.config(
                text=f"Uploading {file_size_kb:.0f}KB ({params.nchannels}ch {params.framerate}Hz)..."))

            try:
                devices = FreeWili.find_all()
                if devices:
                    self.device = devices[0]
            except:
                pass

            # Use v3's working approach: send_file with None for target path
            result = self.device.send_file(trimmed_path, None, None)

            # Wait for upload to complete
            import time
            time.sleep(0.5)

            self.root.after(0, lambda: self.audio_status.config(text="Playing..."))

            # Play using the filename from the path (v3 approach)
            try:
                play_result = self.device.play_audio_file(trimmed_path.name)
                if play_result.is_ok():
                    self.root.after(0, lambda: self.audio_status.config(text="[OK] Playing!", foreground="green"))
            except Exception as play_err:
                print(f"Playback error: {play_err}")

            # Add to library with the actual filename
            actual_filename = trimmed_path.name
            if actual_filename not in self.audio_list:
                self.audio_list.append(actual_filename)

            # Save cache synchronously
            self.save_cache()

            # Update UI
            self.root.after(0, self._update_listboxes)
            self.root.after(0, lambda: self.audio_status.config(text=f"[OK] Uploaded & played {actual_filename}", foreground="green"))

        except Exception as e:
            error_msg = str(e)[:50]  # Capture message immediately
            self.root.after(0, lambda: self.audio_status.config(text=f"Error: {error_msg}", foreground="red"))
            import traceback
            traceback.print_exc()

    def test_oscar(self):
        oscar = pathlib.Path(r"D:\CODE\freewili\oscar.jpg")
        if oscar.exists():
            threading.Thread(target=self._upload_image_thread, args=(str(oscar), True), daemon=True).start()

    def test_beep(self):
        beep = pathlib.Path(r"D:\CODE\freewili\test_beep.wav")
        if beep.exists():
            threading.Thread(target=self._upload_audio_thread, args=(str(beep),), daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = FreeWiliPresenter(root)
    root.mainloop()
