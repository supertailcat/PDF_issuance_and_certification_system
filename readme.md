# 签发认证系统文档

## 环境配置

1. 配置MySQL环境；

2. 为Django项目配置虚拟环境，安装依赖包：django，mysqlclient，pyopenssl。配置setting.py数据库信息（DATABASE），之后执行迁库操作；

3. 安装MyPDFSigner https://www.kryptokoder.com/MyPDFSigner-3.1.5-1-x86_64.exe，将环境变量添加到Python变量之前；

4. 编辑MyPDFSigner配置文件pypdfsigner.conf：

   ```
   certstore=PKCS12 KEYSTORE FILE
   certfile=/Applications/MyPDFSigner.app/Contents/Home/tests/mypdfsigner-test.p12
   certpasswd=47cabdb7b2b2dcc416a21cd0c4b6903e
   subfilter=ETSI.CAdES.detached
   sigrect=[-170 -80 -40 -40]
   sigimage=/Applications/MyPDFSigner.app/Contents/Home/tests/signature.png
   tsaurl=http://adobe-timestamp.geotrust.com/tsa
   ```

   准备好你的PKCS#12证书（第三方提供或者本机生成，方法略）、证书密码、签名图像（仅png格式）。将他们的路径赋值给certfile、certpasswd、sigimage。sigrect用于标记签名位置。详见https://www.kryptokoder.com/manual.html。
   
5. 配置Django项目中views.py的文件路径。更改：
   
   in_file_path：保存待加签文件的路径
   
   in_file_name：待加签文件名
   
   out_file_path：加签文件的路径
   
   out_file_name：加签文件名
   
   config_file_path：配置文件路径
   
   config_file_name：配置文件名
   
   p12_path：pkcs#12证书路径
   
   p12_name：pkcs#12证书名
   
   p12_password：pkcs#12证书密码
   
   temp_save_path：待验证文件临时存放位置（验证后文件自动删除）
   
   path格式如'C:\\\xxx\\\xxx\\\...\\\files\\\\'。name格式如'xxx.pdf'。

## URL

### 创建学生

http://ip:port/one_app/create/

以sid为主键，创建一个学生。

输入（POST）Content-Type:application/json：

```json
{
	"name" : "小明",
	"sid" : "18301000",
	"iid" : "200200200001010011"
}
```

返回值：

```json
{
    "msg": "test"
}
```

### 签发文件

http://ip:port/one_app/download/

请求指定学号的成绩单，生成签发后的文件。

输入（GET）Content-Type:application/json：

```json
{
    "id": "18301000"
}
```

返回值：

文件（APPLICATION/OCTET-STREAM）

### 验证文件

http://ip:port/one_app/verify/

检查文件是否被篡改，姓名与服务器证书上是否一致。

输入（POST）Content-Type:multipart/form-data：

file:[发送的文件]

返回值：

```json
{
    "msg": "succeed"(or fail)
}
```

