import zipfile, os, requests


with requests.get('https://www.provasdeti.com.br/assets/slides/md372.zip', stream=True) as r:
    header_content_length = r.headers.get("Content-Length")
                        
    if (header_content_length is None):
        raise FileNotFoundError('O arquivo não existe no endereço')
    
