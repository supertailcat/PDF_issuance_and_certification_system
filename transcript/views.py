from django.http import JsonResponse
import json
from django.http import FileResponse
import os
import random
import datetime

# from django.views.generic.base import View

in_file_path = 'file\\'
out_file_path = 'file\\'
sign_name = 'ypy'
style_name = 'bjtu'
p12_file = 'p.p12'
p12_password_file = 'password'
p12_password = open(p12_password_file).readline()
temp_save_path = 'file\\'
serial = '0382e2fa47f0eb5461d5d46648c152b6839cf0b59b52a22b65a7e38e889af94f'

# class SignView(View):
#     def get(self, request):
#         print(1111)
#         a = {"a":123, "b":234}
#         return JsonResponse({"msg": "wrong request method"})
#
#     def post(self, request):
#         print(request)
#         return JsonResponse({"msg": "wrong request method"})


def sign(request):
    if request.method == 'GET':
        data = json.loads(request.body.decode())
        id = data.get("id")
        cmd = "pyhanko sign addsig --field -1/0,0,100,100/"
        cmd += sign_name
        cmd += " --style-name "
        cmd += style_name
        cmd += " pkcs12 "
        cmd += "\""
        cmd += in_file_path + id
        cmd += ".pdf"
        cmd += "\" \""
        cmd += out_file_path + id
        cmd += "-signed.pdf"
        cmd += "\" \""
        cmd += p12_file
        cmd += "\""
        cmd += " --passfile "
        cmd += "\""
        cmd += p12_password_file
        cmd += "\""
        # cmd = f"pyhanko sign addsig --field -1/0,0,100,100/{sign_name} --style-name {style_name} pkcs12 \"{in_file_path + id}.pdf\" \"{out_file_path + id}-signed.pdf\" \"{p12_file}\" --passfile \"{p12_password_file}\""
        print(cmd)
        os.system(cmd)

        file = open(out_file_path + id + "-signed.pdf", 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'APPLICATION/OCTET-STREAM'
        filename = id + "-signed.pdf"
        response['content-disposition'] = f'attachment;filename={filename}'
        file.close()
        return response
    return JsonResponse({"msg": "wrong request method"})


def validate(request):
    if request.method == "POST":
        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_num = random.randint(0, 100)
        if random_num <= 10:
            random_num = str(0) + str(random_num)
        temp_file_name = str(time) + str(random_num) + ".pdf"

        file = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not file:
            return JsonResponse({"msg": "请上传文件"})
        else:
            destination = open(os.path.join(temp_save_path, temp_file_name), 'wb+')  # 进行二进制的写操作
            for chunk in file.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

            cmd = "pyhanko sign validate "
            cmd += "\""
            cmd += temp_save_path
            cmd += temp_file_name
            cmd += "\""
            # cmd = f"pyhanko sign validate \"{temp_save_path + temp_file_name}\""
            print(cmd)

            results = os.popen(cmd).readlines()
            if len(results) != 0:
                result = os.popen(cmd).readlines()[0]
                print(result)
                os.remove(temp_save_path + temp_file_name)
                if serial in result and 'UNTOUCHED' in result:
                    return JsonResponse({"msg": "true"})
                else:
                    return JsonResponse({"msg": "false"})
            else:
                os.remove(temp_save_path + temp_file_name)
                return JsonResponse({"msg": "false"})

    return JsonResponse({"msg": "wrong request method"})
