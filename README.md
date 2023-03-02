# Automation-for-EC-Shop-Product-Display-Page

# 代码功能描述
这段代码的功能是读取一个Excel文件中的产品信息，并基于产品信息生成对应的产品信息网页，然后将网页转换为对应的图片并保存在本地。

# 代码实现步骤
1. 导入所需的模块，包括os、pandas、jinja2、imgkit等模块。
2. 设置工作路径和相关路径，其中path是主文件夹路径，app_path是wkhtmltox的二进制文件夹路径，output_path是输出图片的文件夹路径，pic_path是存放产品图片的文件夹路径。
3. 使用pandas模块读取Excel文件中的产品信息，存入cloth_info_raw变量中。
4. 读取有赞模版_3.0.html模版，并使用jinja2模块生成模版对象template。
5. 对于cloth_info_raw中每个不同的商品编码，执行以下步骤：
* 通过os.walk函数遍历pic_path路径下的所有文件，获取包含当前商品编码的图片名称列表pic_ls。
* 将pic_ls中的图片名称逐个赋值给pic1、pic2、pic3、pic4变量，这里使用exec函数动态生成变量名，这样可以避免手动定义变量。
* 获取当前商品编码对应的系列介绍，存入story_text变量中。
* 获取当前商品编码对应的尺码表信息和商品属性信息，分别存入spu_size_info和attri_values变量中。
* 将尺码表信息和商品属性信息分别转换为二维列表和字典，并存入table_vals和attri_values变量中。
* 使用template对象生成html_content字符串，同时将table_vals、attri_values、story_text、pic1、pic2、pic3、pic4作为参数传入模版中。
* 使用imgkit模块将html_content字符串转换为对应的图片，并保存在output_path路径下，文件名为当前商品编码加上后缀名（jpg或png）。
# 重点内容
通过jinja2模块将变量嵌入到HTML模版中，方便地生成产品信息网页。
使用imgkit模块将HTML转换为图片，实现对产品信息的可视化展示。
通过os.walk函数遍历文件夹内的所有文件，并使用动态生成变量名的方式避免手动定义变量。
