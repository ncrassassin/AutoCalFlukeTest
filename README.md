# AutoCalTest

## Project Overview
AutoCalTest is a Python-based automation tool with a graphical user interface (GUI) designed to perform automated functional voltage tests using a Fluke 5522A calibrator and a digital multimeter (DMM). The application leverages PyVISA for instrument control, PyQt5 for the GUI, and SQLite for result logging. It follows the MVC (Model-View-Controller) architecture, ensuring clarity, maintainability, and scalability.

## Features
- Automated DC and AC voltage testing
- Real-time measurement and logging
- SQLite database integration for historical result tracking
- User-friendly GUI built with PyQt5

## Directory Structure

```
AutoCalTest/
│
├── controllers/
│   └── test_controller.py
│
├── models/
│   ├── instruments.py
│   └── database.py
│
├── views/
│   └── main_window.py
│
├── resources/
│   └── test_results.db
│
├── .gitignore
├── main.py
└── requirements.txt
```

## Installation

### Prerequisites
- Python 3.7 or later
- PyVISA
- PyQt5
- pyvisa-py

### Setup
1. Clone the repository:
```bash
git clone https://github.com/ncrassassin/AutoCalFlukeTest.git
```

2. Navigate to the project directory:
```bash
cd AutoCalTest
```

3. Set up a virtual environment:
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
.\env\Scripts\activate  # Windows
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application by executing:
```bash
python main.py
```

## GUI Overview
- **Start DC Voltage Tests**: Performs automated DC voltage tests (1V, 5V, 10V).
- **Start AC Voltage Tests**: Performs automated tests at specified AC voltage and frequency points.
- **Results**: Displayed after each test execution, indicating pass/fail status and measured values.

## Instruments Configuration
Adjust the instrument addresses in `views/main_window.py` to match your hardware setup:
```python
self.calibrator = Fluke5522A('GPIB0::1::INSTR')
self.dmm = DMM('GPIB0::2::INSTR')
```

## Database
Test results are logged in SQLite database located at:
```
resources/test_results.db
```

## Contributing
Feel free to fork the repository and submit pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License.

## Author
ncrassassin - [ncrassassin](https://github.com/ncrassassin)
