import os
from urllib.request import urlretrieve
from PIL import Image

# set url to download images from
# example: 'https://reserves.lib.tsinghua.edu.cn/book6//00006705/00006705002/files/mobile/'
base_url = input('BASE URL: ')
tail_url = '.jpg'

# set last page
no_of_pages = int(input('NUMBER OF PAGES: ')) + 1

# set pdf name
pdf_name = input('PDF NAME: ')

# download images
os.makedirs('TEMP')
for i in range(1, no_of_pages):
    url = base_url + str(i) + tail_url
    urlretrieve(url, f'./TEMP/{i}.jpg')
    print(f'page {i} complete.')
print('download images complete.\ncreating pdf...')

# create pdf from images saved
images = [Image.open(f'./TEMP/' + str(p) + '.jpg') for p in range(1, no_of_pages)]
pdf_path = f'./{pdf_name}.pdf'
images[0].save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
print('create pdf complete.')

# remove TEMP directory
print('removing saved images...')
for root, dirs, files in os.walk('./TEMP/', topdown=False):
    for file in files:
        file_path = os.path.join(root, file)
        os.remove(file_path)
os.rmdir('TEMP')
print('remove images complete.')