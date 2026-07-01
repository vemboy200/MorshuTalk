# MorshuTalk (macOS fork)

A [Morshu](https://knowyourmeme.com/memes/morshu) text-to-speech program.

This is a fork of [n0spaces/MorshuTalk](https://github.com/n0spaces/MorshuTalk) that adds a native macOS `.app`
release, built with a lightweight tkinter GUI instead of PySide6. All TTS/audio logic is unchanged from upstream.

<img width="554" height="241" alt="image" src="https://github.com/user-attachments/assets/6ee7751d-ae1e-4c2d-a6a7-b60f1120bce2" />

Its quite basic, but you can make it speak or save the shown text as .wav or .mp3 file

This program works by converting the given text into phonemes with [g2p_en](https://pypi.org/project/g2p-en/), then
concatenates the segments of Morshu's audio where he speaks those phonemes.

## Requirements
Python 3.7+ (tested on macos 27 developer beta 2)

Python is not required if you're just using a prebuilt MorshuTalk executable/app.

## Installation
### macOS App
Download `MorshuTalk-macos.zip` from the [latest release](https://github.com/vemboy200/MorshuTalk/releases/latest)
and unzip it.

This app is signed with an ad-hoc signature only (I'm not an Apple-registered developer, so it isn't notarized).
macOS Gatekeeper will refuse to open it with a warning like *"MorshuTalk.app is damaged and can't be opened"* or
*"cannot verify the developer"*. To open it anyway:

1. Right-click (or Control-click) `MorshuTalk.app` and choose **Open**, then confirm **Open** in the dialog that
   appears — this only needs to be done once.
2. If that still refuses to open, go to **System Settings → Privacy & Security**, scroll down to the Security
   section, and click **Open Anyway** next to the MorshuTalk message, then confirm.
3. If it's still blocked, clear the quarantine flag from Terminal:
   ```
   xattr -cr /path/to/MorshuTalk.app
   ```

### Windows Executable
If you're on Windows and you don't want to install Python, you can download an executable from the
[the upstream of this fork](https://github.com/n0spaces/MorshuTalk/releases/latest). Simply download the 7z or ZIP
archive (they're both identical) and extract it.

### Python Package
If you have Python installed, you can install this with `pip`:

    pip install morshutalk

Or you can clone this repo and run the setup script:

    python setup.py install

This installs all the packages necessary for running MorshuTalk from the command-line. If you want to use the GUI, you
will also need to install PySide6. (It's not included by default because it's a slightly larger download.)

    pip install PySide6

## Running
### macOS App
Open `MorshuTalk.app` (see the Gatekeeper note above if it won't open). Type text into the box and click **Speak**
to hear it, or **Save Audio** to export a `.wav`/`.mp3`.


### Python Package
Installing the package will add the commands `morshutalk` and `morshutalkgui` to your command-line. If those commands
don't work, you can run the modules with `python -m morshutalk` or `python -m morshutalkgui`.

#### Command-Line
Run `morshutalk` to load the interactive command-line app. Simply type whatever lines you want Morshu to speak, then he
will talk. To exit, leave the line blank and hit enter.

#### GUI
Run `morshutalkgui` to load the GUI app. Remember that PySide6 is required.

Type text into the textbox, then click Load to load the audio. Click Play to hear the audio. The Morshu sprite will
animate as he speaks. You can toggle the sprite visibility from the View menu.

## Building
1. Clone this repo.
2. Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) and activate it.
3. Install the required packages with `pip install -r requirements.txt`
4. If you make changes to `mainwindow.ui`, update `ui_mainwindow.py` with:
```commandline
pyside6-uic morshutalkgui/ui/mainwindow.ui -o morshutalkgui/ui_mainwindow.py --from-imports
```
5. If you make changes to `res.qrc`, update `res_rc.py` with:
```commandline
pyside6-rcc morshutalkgui/res/res.qrc -o morshutalkgui/res_rc.py
```
6. Use `build` to create a distributable package:
    1. Install it with `pip install build`
    2. Run `python -m build`. A tar.gz and wheel package should be located in the `dist` folder.
7. Use cx_freeze to build an executable for Windows:
    1. Install it with `pip install cx_freeze`
    2. Run `python freeze_setup.py build`. The executable and many other files should be located in the `build` folder.
    3. Run `python clean_cx_freeze_build.py` to remove unnecessary files. (cx_freeze does a bad job at choosing what
       packages are necessary. This script removes 150+ MB of unused files.)
8. Build the macOS `.app` with PyInstaller (this is what [`.github/workflows/build-macos.yml`](.github/workflows/build-macos.yml)
   runs automatically on every tag push):
    ```
    pip install pyinstaller "inflect<6"
    python3 -m PyInstaller --windowed --onedir --name MorshuTalk --clean \
        --collect-all morshutalk --collect-all g2p_en macos_gui.py
    codesign --force --deep -s - dist/MorshuTalk.app
    xattr -cr dist/MorshuTalk.app
    ```
    `inflect<6` avoids a `typeguard`/PyInstaller incompatibility in newer `inflect` releases, and `--collect-all g2p_en`
    ensures its data files are bundled into the app.

## License
[MIT License](LICENSE.txt)

This uses the following libraries:
* [g2p_en](https://pypi.org/project/g2p-en/)
* [NumPy](https://numpy.org/)
* [Pydub](http://pydub.com/)
* [sounddevice](https://pypi.org/project/sounddevice/)
* [PySide 6 (Qt for Python)](https://wiki.qt.io/Qt_for_Python)
