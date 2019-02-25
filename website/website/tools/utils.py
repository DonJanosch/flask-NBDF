import requests

def load_script_from_filename(filename,subdir='js/',static_path='static'):
    return f'<script type="text/javascript" src="'+'{{'+f' url_for({static_path}, filename="{subdir}{filename}") '+'}}'+'"></script>'
