# FreeWili Presenter

A Python GUI application for managing and presenting images and audio on FreeWili badges.

## Features

- **Image Library Management**: Upload, display, and manage images on your badge
  - Supports JPG, PNG, and pre-converted FWI formats
  - Auto-rotation option for portrait images
  - Persistent library between sessions
- **Audio Library Management**: Upload and play audio files
  - Auto-trims to 3 seconds for quick upload
  - Supports WAV files
- **Library Persistence**: Uploaded files are cached and persist between sessions
- **Badge File Scanner**: Discover existing files on your badge

## Requirements

- Python 3.13+
- FreeWili badge connected via USB
- Required packages:
  ```bash
  pip install pillow
  ```
- FreeWili Python library (from parent directory)

## Usage

1. Connect your FreeWili badge via USB
2. Run the presenter:
   ```bash
   python freewili_presenter.py
   ```
3. The app will automatically detect your badge on COM4 and COM15

### Uploading Images

- **Upload New...**: Uploads and rotates image 90° clockwise (for portrait photos)
- **Upload (No Rotate)...**: Uploads without rotation
- **Pre-converted FWI files**: Select .fwi files to skip conversion

### Uploading Audio

- Audio files are automatically trimmed to 3 seconds
- Supports various sample rates and formats
- Files are stored in the badge's audio directory

### Test Files

- `oscar.jpg`: Sample test image
- `test_beep.wav`: Pleasant two-tone beep sound
- `create_pleasant_beep.py`: Script to regenerate test beep

## File Structure

```
presenter/
├── freewili_presenter.py    # Main application
├── oscar.jpg                 # Test image
├── test_beep.wav            # Test audio
├── create_pleasant_beep.py  # Beep generator
└── README.md                # This file
```

## Cache File

The app creates `freewili_library_cache.json` to store your library between sessions.

## Tips

- Images are automatically resized to 320x240
- Large audio files may take 20-30 seconds to upload
- Use "Scan Badge Files" to refresh the library from the badge
- Pre-converted .fwi files upload faster than JPG/PNG

## Troubleshooting

- **No device found**: Make sure your badge is connected and drivers are installed
- **Audio not playing**: Ensure file is valid WAV format
- **Image not displaying**: Try using both upload buttons (with/without rotation)

## Version History

- v5: Added no-rotation upload, improved audio handling, pre-converted FWI support
- v4: Added library management with persistence
- v3: Improved error handling and audio compression
- v2: Added audio support
- v1: Initial release with image display
