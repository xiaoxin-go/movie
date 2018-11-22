import os
import shutil

# 删除文件
if os.path.exists(r'app\templates\home\index.html'):
    os.remove(r'app\templates\home\index.html')

csses = r'app\static\css'
if os.path.exists(csses):
    shutil.rmtree(csses)

jses = r'app\static\js'
if os.path.exists(jses):
    shutil.rmtree(jses)


# 复制文件
base_path = r'F:\movie\home-movie\dist'
index = r'%s\index.html' % base_path
shutil.copy(index, 'app/templates/home/index.html')

# 复制目录
src_css = r'%s\static\css' % base_path
shutil.copytree(src_css, csses)

src_js = r'%s\static\js' % base_path
shutil.copytree(src_js,jses)




