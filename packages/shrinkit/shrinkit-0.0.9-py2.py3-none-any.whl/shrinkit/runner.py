import sys
import os

class ShrinkitRunner:
    def __init__(self):
        pass

    def get_path(self):
        # sys.argv = ["streamlit", "run", "./shrinkit/main.py"]
        # sys.exit(stcli.main())
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(current_dir)
        main_file_path = os.path.join(current_dir, 'main.py')
        return main_file_path