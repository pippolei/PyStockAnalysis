file_folder1= "C:/"
file_folder= file_folder1+"python/"
file_name='资产负债表.csv'

#资产负债表
url_zc='http://quotes.money.163.com/service/zcfzb_600001.html '
#利润表
url_lr='http://quotes.money.163.com/service/lrb_600001.html'
#现金流量表
url_xj='http://quotes.money.163.com/service/xjllb_600001.html '

import urllib
import urllib.request
path=file_folder+file_name
urllib.request.urlretrieve(url_zc,path,None)

# File.open(file_folder+file_name, 'wb') {|f| f.write(open('http://quotes.money.163.com/service/lrb_' + "#{scode}"+'.html') {|f1| f1.read})}
# 不好使
# 链接：https://www.zhihu.com/question/23148894/answer/286589221

# File=open(file_folder+file_name,'wb')
# File.write(url_zc)
# File.close()
# 也不好使