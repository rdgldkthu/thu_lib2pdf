import os
import re
import tkinter as tk
import ttkbootstrap as ttk
from urllib.request import urlretrieve
from PIL import Image


# convert site url to file directory url
def convert_url(site_url):
    pattern = r'http.*?mobile'
    res = re.findall(pattern, site_url)
    file_url = res[0][:-6:] + 'files/mobile/'
    return file_url


def lib2pdf():
    site_url = url_entry.get()
    pdf_name = pdf_entry.get()
    no_of_pages = page_entry_int.get() + 1

    # download images
    os.makedirs('TEMP')
    base_url = convert_url(site_url)
    for i in range(1, no_of_pages):
        url = base_url + str(i) + '.jpg'
        urlretrieve(url, f'./TEMP/{i}.jpg')

    # create pdf from images saved
    images = [Image.open(f'./TEMP/' + str(p) + '.jpg') for p in range(1, no_of_pages)]
    pdf_path = f'./{pdf_name}.pdf'
    images[0].save(pdf_path, 'PDF', resolution=100.0, save_all=True, append_images=images[1:])

    # remove TEMP directory
    for root, dirs, files in os.walk('./TEMP/', topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
    os.rmdir('TEMP')
    output_string.set('conversion complete!')
    # Clear the input boxes after executing the function
    url_entry.delete(0, tk.END)
    pdf_entry.delete(0, tk.END)
    page_entry.delete(0, tk.END)


def clear_inputs():
    # Clear all input boxes
    url_entry.delete(0, tk.END)
    pdf_entry.delete(0, tk.END)
    page_entry.delete(0, tk.END)

    output_string.set('boxes cleared!')


# main window
window = ttk.Window(themename='journal')
window.title('THU LIB2PDF')
window.geometry('500x300')
window.place_window_center()
window.position_center()

# title
title_label = ttk.Label(master=window, text='Convert THU Library Books to pdf files', font='Calibri 12 bold')
title_label.pack(pady=10)

# input field
input_frame = ttk.Frame(master=window)

url_frame = ttk.Frame(master=input_frame)
url_label = ttk.Label(master=url_frame, text='SITE URL:')
url_label.pack(side='left')
url_entry = ttk.Entry(master=url_frame)
url_entry.pack(side='left')
url_frame.pack(pady=5)

pdf_frame = ttk.Frame(master=input_frame)
pdf_label = ttk.Label(master=pdf_frame, text='PDF NAME: ')
pdf_label.pack(side='left')
pdf_entry = ttk.Entry(master=pdf_frame)
pdf_entry.pack(side='left')
pdf_frame.pack(pady=5)

page_frame = ttk.Frame(master=input_frame)
page_label = ttk.Label(master=page_frame, text='NUMBER OF PAGES:')
page_label.pack(side='left')
page_entry_int = tk.IntVar()
page_entry = ttk.Entry(master=page_frame, textvariable=page_entry_int)
page_entry.pack(side='left')
page_frame.pack(pady=5)

button_frame = ttk.Frame(master=input_frame)
convert_button = ttk.Button(master=button_frame, text='Convert', command=lib2pdf)
convert_button.pack(side='left', padx=5)
clear_button = ttk.Button(master=button_frame, text='Clear', command=clear_inputs)
clear_button.pack(side='left', padx=5)
button_frame.pack(pady=20)

input_frame.pack(pady=10)

# output
output_string = tk.StringVar()
output_label = ttk.Label(master=window, textvariable=output_string)
output_label.pack()

# run
window.mainloop()
