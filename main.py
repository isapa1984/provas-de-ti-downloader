from basic.downloader import Downloader 
import sys, os

debug_est = False

if ('-d' in sys.argv):
    debug_est = True        

base_dir = os.getcwd()
input_file = f'{base_dir}/input.html'
download_dir = f'{base_dir}/downloads'

downloader = Downloader()
downloader.baixar(input_file, download_dir, debug_est)