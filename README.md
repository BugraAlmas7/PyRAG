This project is python version of MultiCoreRAG. This project gives me how to use any API to create basic LLM. 
Python code and .env must be same location in computer and show their location when use this code.
app.py is http interface to use main.py part.
In terminal part is 
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
python main.py
flet run main.py
