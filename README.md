# Open Photogrammetry Toolkit (OPT)

OPT is a flexible, extensible, open-source toolkit designed for photogrammetry and Structure from Motion (SFM) applications. Built on Qt6 with PySide6 bindings, it offers a powerful graphical user interface that can be customized and extended through plugins.

## Key Features

- **Qt 6 Based (PySide6)**: Utilizes PySide6 for a robust, user-friendly GUI experience.
- **Flexibility and Extensibility**: Supports plugins to enhance or modify functionality, catering to specific user needs and easing licensing constraints.
- **FOSS Philosophy**: Adheres to the principles of free and open-source software, promoting a collaborative community.
- **Apache 2.0 License**: Ensures legal security and transparency, with flexible plugin licensing options.
- **Designed for Photogrammetry & SFM**: Tailored specifically to meet the needs of photogrammetry and SFM processes.

## Installation Instructions

### Python Version

Use **Python 3.9** or higher. Older versions are not officially supported.

### Upgrade pip

Upgrade pip to the latest version:

#### Windows

```batch
python -m pip install --upgrade pip
```

#### macOS and Linux

```bash
python3 -m pip install --upgrade pip
```

### Toolkit Installation

#### Mandatory Components

Install PySide6:

##### Windows

```batch
pip install PySide6
```

##### macOS and Linux

```bash
pip3 install PySide6
```

#### Non-Mandatory Components

Optional but recommended for full functionality:

##### Windows

```**batch**
pip install opencv-python
pip install numpy
```

##### macOS and Linux

```bash
pip3 install opencv-python
pip3 install numpy
```

### Testing Framework

Install pytest and related libraries if you plan to run tests:

##### Windows

```batch
pip install pytest
pip install pytest-qt
```

##### macOS and Linux

```bash
pip3 install pytest
pip3 install pytest-qt
```

## More Information

Visit [openphotogrammetrytoolkit.com](http://openphotogrammetrytoolkit.com) to customize your installation with selected modules.

## License

This project is licensed under the Apache 2.0 License. See the LICENSE file for more details.
