# Data-decoding
Application for decoding/encoding, reading and downloading/uploading binary files which contains test results 
with providing structure
 Example:
- MIR: Header = "MIR", Temperature = `25.0`, Operator Name = "Operator_1".
- PRR: Header = "PRR", Part Number = `1`, Pass/Fail Status = `1` (Pass).
- PTR: Header = "PTR", Test Name = "Voltage Test", Test Value = `3.3`, Low Limit = `3.0`, High
Limit = `3.6`, Pass/Fail Status = `1` (Pass).
- PRR: Header = "PRR", Part Number = `2`, Pass/Fail Status = `0` (Pass).
- PTR: Header = "PTR", Test Name = "Voltage Test", Test Value = `4.3`, Low Limit = `3.0`, High
Limit = `3.6`, Pass/Fail Status = `0` (Pass).

# Application running
For running application you need to - git clone git@github.com:VolodymyrSemchysyn/Data-decoding.git
Setup requirements - poetry install
Run server - uvicorn src.main:app --reload
Interact with functionality - http://localhost:8000/static/index.html
Another way to interact you can check endpoints with using swagger http://127.0.0.1:8000/docs/

Or use docker "docker-compose up --build"

Here are 4 endpoints 
- "api/data/upload_file" for uploading binary files and saving it in project directory
- "api/data/edit" for editing and encoding specific file
- "api/data/download" for downloading binary files
- "api/data/read" for reading data from file

Run test with command "pytest src/test.py"


