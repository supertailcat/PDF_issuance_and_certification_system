from OpenSSL import crypto
from django.http import JsonResponse
from .models import Student
import json
from django.http import FileResponse
import os
import random
import datetime


in_file_path = r'D:\\Study\\fieldwork\\digitalsign\\file\\'
out_file_path = r'D:\\Study\\fieldwork\\digitalsign\\file\\'
config_file_path = r'D:\\MyPDFSigner\\tests\\'
config_file_name = 'mypdfsigner.conf'
p12_path = r'D:\\MyPDFSigner\\tests\\'
p12_name = r'mypdfsigner-test.p12'
p12_password = '47cabdb7b2b2dcc416a21cd0c4b6903e'
temp_save_path = r'D:\\Study\\fieldwork\\digitalsign\\file\\'

def student_create(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        name = data.get("name")
        sid = data.get("sid")

        new_s = Student()
        new_s.name = name
        new_s.sid = sid
        new_s.save()

        return JsonResponse({"msg": str(new_s)})
    return JsonResponse({"msg": "请求方法不对"})


def file_download(request):
    if request.method == "GET":
        data = json.loads(request.body.decode())
        sid = data.get("id")

        in_file_name = sid + '.pdf'
        out_file_name = sid + '-signed.pdf'

        cmd = r'mypdfsigner'

        cmd += r' -i '
        cmd += '"'
        cmd += in_file_path
        cmd += in_file_name
        cmd += '"'

        cmd += r' -o '
        cmd += out_file_path
        cmd += out_file_name

        cmd += r' -z '
        cmd += '"'
        cmd += config_file_path
        cmd += config_file_name
        cmd += '"'

        cmd += r' -v -c -q'
        print(cmd)
        os.system(cmd)

        file = open(out_file_path + out_file_name, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'APPLICATION/OCTET-STREAM'
        filename = out_file_name
        response['content-disposition'] = f'attachment;filename={filename}'
        return response
    return JsonResponse({"msg": "请求方法不对"})

def verify(request):
    if request.method == "POST":
        #获取公钥和签名者姓名CN
        # p12 = crypto.load_pkcs12(open(p12_path + p12_name, 'rb').read(), p12_password)
        # pubkey = p12.get_certificate().get_pubkey()
        # name = p12.get_certificate().get_issuer()
        # print(pubkey)

        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_num = random.randint(0, 100)
        if random_num <= 10:
            random_num = str(0) + str(random_num)
        temp_file_name = str(time) + str(random_num) + ".pdf"

        file = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not file:
            return JsonResponse({"msg": "请上传文件"})
        else:
            destination = open(
                os.path.join(temp_save_path, temp_file_name),
                'wb+')  # 进行二进制的写操作
            for chunk in file.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

            cmd = r'mypdfsigner verify -i '
            cmd += temp_save_path
            cmd += temp_file_name
            cmd += r' -z '
            cmd += config_file_path
            cmd += config_file_name

            print(cmd)
            result = os.popen(cmd).readlines()[0]
            os.remove(temp_save_path + temp_file_name)
            true_result = r'0#Document signature verified [Signer: '
            # true_result += p12.get_certificate().get_issuer()
            true_result += 'MyPDFSigner Test'
            true_result += ']\n' #no 'r' here
            print(result)
            print(true_result)
            if result == true_result:
                return JsonResponse({"msg": "succeed"})
            else:
                return JsonResponse({"msg": "fail"})
    return JsonResponse({"msg": "请求方法不对"})