## Screenshot Organizer

This Python script enhances the management of MacOS screenshots by leveraging AI vision and text models. It automatically describes, renames, and adds metadata to screenshots for easier searching and organization.

### Features

- **Automatic Description**: Utilizes AI models to generate concise descriptions of screenshot content.
- **File Renaming**: Renames screenshot files based on the AI-generated descriptions.
- **Metadata Addition**: Embeds the description into the image's metadata for better searchability.

### Prerequisites

- Ollama (https://ollama.com/)
- Python 3.x
- `ollama` python package for AI models
- `yaspin` python package for terminal spinner
- `PIL` (Python Imaging Library) for image processing

### Installation

1. Clone the repository or download the script.
2. Install required Python packages:
   ```bash
   pip install ollama yaspin Pillow
   ```

### Usage

1. Ensure your screenshots are in the default MacOS format (`Screenshot YYYY-MM-DD at HH.MM.SS.png`).
2. Run the script:
   ```bash
   # go to the directory where your screenshots are (make a test copy first!)
   cd ~/Pictures
   python /path/to/repo/renamer.py
   ```

The script will process each screenshot, renaming it and updating its metadata based on the content description.

### Example

Before running the script:

- `Screenshot 2024-02-15 at 10.20.30.png`

After running the script:

- `Screenshot 2024-02-15 at 10.20.30_website_about_raspberry_pi.png`
- Description in metadata: "screenshot of a website about a raspberry pi.  It shows the layout of the board with an ethernet and hdmi cable plugged in."

---

There is also a helper bash script `ssc` which uses ImageMagick to extract information from screenshot files to make them searchable (Spotlight doesn't index .png metadata).  To use it just put it somewhere in your path then :
```bash
ssc 'search-term'
```

### Contributing

Feel free to fork this project and submit pull requests for any enhancements.

### License

This project is licensed under the MIT License - see the LICENSE.md file for details.
