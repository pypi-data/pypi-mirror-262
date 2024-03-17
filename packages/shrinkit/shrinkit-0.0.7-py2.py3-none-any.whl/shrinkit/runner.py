import sys
import os
import streamlit.web.cli as stcli

class ShrinkitRunner:
    def __init__(self):
        pass

    def run(self):
        # sys.argv = ["streamlit", "run", "./shrinkit/main.py"]
        # sys.exit(stcli.main())

        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(current_dir)
        main_file_path = os.path.join(current_dir, 'main.py')
        sys.argv = ["streamlit", "run", main_file_path]
        sys.exit(stcli.main())