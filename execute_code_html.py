# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 16:28:00 2023

@author: jiahachen
"""

import os
import pandas as pd

path = r"C:\Users\jiahachen\Desktop\Others\zzqsb" # setting working path
app_path = os.path.join(path, r"wkhtmltox\bin")
output_path = os.path.join(path, 'output')
pic_path = os.path.join(path, '第二批衣服')

cloth_info_raw = pd.read_excel(os.path.join(path, '上线产品第二批.xlsx'), sheet_name = '有赞商品Only')

from jinja2 import Template
import imgkit

css = os.path.join(path, 'eCommerceStyle.css')
zoom_n = 9
img_format = 'jpg' # alternative: 'png'
options = {'format':img_format, 'enable-local-file-access': None, 'width': str(round(420*zoom_n)), 'disable-smart-width': None, 'zoom':str(zoom_n)}

for spu_code in list(cloth_info_raw['商品编码'].unique()):

    http_template = open(os.path.join(path, '有赞模版_3.0.html'), encoding='utf-8').read()
    template = Template(http_template)
    
    # url_picture
    pic_ls = []
    pic1, pic2, pic3, pic4 = '', '', '', ''
    for root, dirs, files in os.walk(pic_path):
        for filename in files:
            if str(spu_code) in filename:
                pic_ls.append(filename)
                
    for pic_element, n in zip(pic_ls, range(len(pic_ls))):
        exec("pic{} = r'{}'".format(n+1, os.path.join(pic_path, pic_ls[n])))
    
    story_text = list(cloth_info_raw[cloth_info_raw['商品编码'] == spu_code]['系列介绍'].drop_duplicates())[0]
    
    slct_range_atrri1 = ['尺码', '衣长', '肩宽', '胸围', '腰围', '袖长', '裤长', '臀围']
    spu_size_info = cloth_info_raw[cloth_info_raw['商品编码'] == spu_code][slct_range_atrri1]
    if list(spu_size_info['衣长'].isna().drop_duplicates())[0]:
        spu_size_info = spu_size_info[['裤长', '腰围', '臀围']].dropna(axis=1, how='all')
    spu_size_info = spu_size_info.dropna(axis=1, how='all')
    
    table_vals = [list(spu_size_info.columns)]
    for index, row in spu_size_info.iterrows():
        table_vals.append(list(row))
    
    slct_range_atrri2 = ['颜色', '材质', '工艺', '版型', '护理']
    spu_size_info = cloth_info_raw[slct_range_atrri2][cloth_info_raw['商品编码'] == spu_code].dropna(axis=1, how='all').drop_duplicates()
    spu_size_info.rename(columns={'成分':'材质'}, inplace=True)
    attri_values = spu_size_info.to_dict('records')[0]
    
    html_content = template.render(table_vals=table_vals, attri_values=attri_values, story_text=story_text,\
                                   pic1=pic1, pic2=pic2, pic3=pic3, pic4=pic4)
    
    # with open(os.path.join(path, 'html', str(spu_code)+".txt"), 'w+', encoding='utf-8') as font:
    #     font.write(html_content)

    # output picture 
    imgkit.from_string(html_content, config=imgkit.config(wkhtmltoimage=os.path.join(app_path, 'wkhtmltoimage.exe')), \
                        output_path = os.path.join(output_path, str(spu_code)+'.'+img_format), css=css, options=options)
