# 说明文档

### 环境

django, pyhanko

### 配置

##### 根目录

pyhanko.yml中可新建样式，可以更改签名印章，字体，文字信息；
p.p12为你的pkcs12证书；
password保存您pkcs12证书的私钥密码；
xxx.png为要使用的签名印章。

##### view.py(路径表达方式取决于系统)

```python
in_file_path = 'file\\' # 待加签文件保存目录，文件名为[id].pdf
out_file_path = 'file\\' # 已加签文件保存目录，文件名为[id]-signed.pdf
sign_name = 'ypy' #为签名创建一个名字
style_name = 'bjtu' #为签名格式创建一个名字
p12_file = 'p.p12' #pkcs12证书存放位置
p12_password_file = 'password' #pkcs12证书保存私钥密码文件及路径
temp_save_path = 'file\\' #用于验证文件时临时保存文件，验证后文件删除
serial = '0382e2fa47f0eb5461d5d46648c152b6839cf0b59b52a22b65a7e38e889af94f' #运行一次pyhanko sign validate xxx.pdf以查看序列号，暂时不清楚怎么获得这个序列号，应该可以根据pyopenssl.crypto获取，未知
```

##### pyhanko.yml

```
stamp-styles:
    default:
        type: text
        background: __stamp__
        stamp-text: "Signed by %(signer)s\nTimestamp: %(ts)s"
    noto-qr:
        type: qr
        background: background.png
        stamp-text: "Signed by %(signer)s\nTimestamp: %(ts)s\n%(url)s"
        text-box-style:
            font: NotoSerif-Regular.otf
            leading: 13
    bjtu:
        type: text
        background: bjtu.png
        stamp-text: ""
```

default和noto-qr为默认样式。新建样式格式如“bjtu”，type需为text，background为印章图片的相对路径，stamp-text为根据需要添加到印章上的文本。

##### 其他

###### PKCS#12证书的生成：

Linux系统下：
1）生成私钥 $ openssl genrsa -out private.pem 1024
2）创建证书请求 $ openssl req -new -key private.pem -out rsacert.csr
3）生成证书并签名，有效期10年 $ openssl x509 -req -days 3650 -in rsacert.csr -signkey private.pem -out rsacert.crt
4）将 PEM 格式文件转换成 DER 格式 $ openssl x509 -outform der -in rsacert.crt -out rsacert.der
5）导出P12文件 $ openssl pkcs12 -export -out p.p12 -inkey private.pem -in rsacert.crt
（来源：简书；转自https://www.jianshu.com/p/d7df3de72669；作者：Mario_ZJ）

### 运行

python manage.py migrations
python manage.py makemigrate
python manage.py runserver

#### url

###### /transcript/sign/

输入（Content-Type:application/json）：

```json
{
    "id": "18301030"
}
```

输出（文件）：

```
<Headers>
Date →Wed, 12 May 2021 06:47:45 GMT
Server →WSGIServer/0.2 CPython/3.6.13
Content-Type →APPLICATION/OCTET-STREAM
content-disposition →attachment;filename=18301030-signed.pdf
X-Frame-Options →DENY
X-Content-Type-Options →nosniff
Referrer-Policy →same-origin
Connection →close
```

###### /transcript/validate/

输入（Content-Type:multipart/form-data）：

```
KEY:file
VALUE:18301030-signed.pdf
```

输出（Content-Type:application/json）：

```json
{
    "msg": "true(or false)"
}
```

