from pwp_core.pwp_data_resources import *

print('Power Word Prism - Corpora Extractor')
print('************************************')

print('Testing HTML request\n')

response = request.urlopen('http://www.google.com')
html = response.read()
print(html[:100])

print('\nTesting HTML request - SUCCESSFUL')

