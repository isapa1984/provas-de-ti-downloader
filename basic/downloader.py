from basic.models import *
from bs4 import BeautifulSoup
from zipfile import ZipFile
from tqdm.auto import tqdm
import re, requests, os, shutil

class Downloader:
    
    def __init__(self):        
        self.__disciplinas: list[Disciplina] = []
        
    def __extrair(self):
        """
            Extração dos dados do site e criação de estrutura para download
        """
    
        base_url = 'https://www.provasdeti.com.br'

        with open(self.html_file, 'r') as f:
            bs = BeautifulSoup(f, 'html.parser')
            divs_em = bs.find_all('div', class_='edital-materia')
            for div_em in divs_em:
                divs_trilha = div_em.find_all('div', class_='plano plano-align')
                nome_disciplina = div_em.find_all('h4', class_='materia-txt')[0].string

                disciplina = Disciplina()
                disciplina.nome = nome_disciplina

                if (disciplina in self.__disciplinas):
                    i_disc = self.__disciplinas.index(disciplina)
                    disciplina = self.__disciplinas[i_disc]
                else:
                    self.__disciplinas.append(disciplina)

                for div_trilha in divs_trilha:
                    trilha = Trilha()
                    ind_trilha = len(disciplina.trilhas) + 1
                    trilha.nome = f'Trilha {ind_trilha:02d}'

                    divs_pw = div_trilha.find_all('div', class_='plano-wrapper')

                    for div_pw in divs_pw:
                        div_info = div_pw.find_all('p', class_='more-info-txt')
                        a_slide = div_pw.find_all('a', href=re.compile('slides'))

                        modulo = Modulo()
                        ind_modulo = len(trilha.modulos) + 1
                        modulo.nome = f'{ind_modulo:02d} - {div_info[1].string}'.replace(':', ' -').strip()
                        modulo.url = f"{base_url}{a_slide[0]['href']}"
                        modulo.arquivo = modulo.url.split('/')[-1]
                        modulo.diretorio = f'{self.download_dir}/{disciplina.nome}/{trilha.nome}/{modulo.nome}'

                        trilha.modulos.append(modulo)

                    disciplina.trilhas.append(trilha)


    def __download(self):
        """
            Download, extração e organização do conteúdo das disciplinas
        """
        for disciplina in self.__disciplinas:
            for trilha in disciplina.trilhas:
                for modulo in trilha.modulos:
                    print(f'Baixando {disciplina.nome}, {trilha.nome}, {modulo.nome}')
                    
                    if (os.path.exists(modulo.diretorio) and os.listdir(modulo.diretorio)):
                        print('==> Módulo já baixado')
                        continue

                    try:
                        # cria a estrutura de diretório
                        os.makedirs(modulo.diretorio, exist_ok=True)
                        
                        nome_arquivo = f'{modulo.diretorio}/{modulo.arquivo}'
                        
                        # make an HTTP request within a context manager
                        with requests.get(modulo.url, stream=True) as r:
                            
                            header_content_length = r.headers.get("Content-Length")
                            
                            if (header_content_length is None):
                                raise FileNotFoundError('O arquivo não existe no endereço')
                            
                            
                            # check header to get content length, in bytes
                            total_length = int(r.headers.get("Content-Length"))
                            
                            # implement progress bar via tqdm
                            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="") as raw:
                            
                                # save the output to a file
                                with open(nome_arquivo, 'wb') as output:
                                    shutil.copyfileobj(raw, output)
                            
                            # extrai o arquivo baixado
                            with ZipFile(nome_arquivo) as zip:
                                for zip_info in zip.infolist():
                                    if zip_info.is_dir():
                                        continue
                                    zip_info.filename = os.path.basename(zip_info.filename)
                                    zip.extract(zip_info, modulo.diretorio)
                            
                            # exclui o arquivo
                            os.unlink(nome_arquivo)
                    
                    except Exception as ex:
                        print(f'ERRO: {ex}')

    def __print_disciplinas(self):
        """
            Impressão da estrutura dos dados
        """
        for disciplina in self.__disciplinas:
            print(f'{disciplina.nome}')
            for trilha in disciplina.trilhas:
                print(f'\t{trilha.nome}')
                for modulo in trilha.modulos:
                    print(f'\t\t"{modulo.nome}"')
                    print(f'\t\t"{modulo.url}"')
                    print(f'\t\t"{modulo.arquivo}"')
                    print(f'\t\t"{modulo.diretorio}"')
                    print(f'\t\t')


    def baixar(self, html_file: str, download_dir: str, debug_est: bool = False):
        self.html_file = html_file
        self.download_dir = download_dir
        self.__extrair()
        if (debug_est):
            self.__print_disciplinas()
        else:
            self.__download()


