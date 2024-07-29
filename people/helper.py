import os
import pandas as pd
from .models import MS, BTech, MTech, Faculty, Staff, Alumni, Phd
from django.core.files import File
from django.core.files.images import ImageFile
from .manager import im_to_base64

def postDataForBulkPeople(img_dir_path, csv_path, people):
    image_dir = os.listdir(img_dir_path)
    df = pd.read_csv(csv_path)
    roll_list = df.roll_no.tolist()
    if (len(image_dir)!= len(roll_list)):
        print("Number of images and number of rows in csv file do not match")
        return Exception("Number of images and number of rows in csv file do not match")
    for i in range(len(roll_list)):
        if (roll_list[i]+'.jpg' not in image_dir):
            print(f"Image {roll_list[i]} not found in image directory")
            return Exception(f"Image {roll_list[i]} not found in image directory")
        image_path = os.path.join(img_dir_path, f'{roll_list[i]}.jpg')
        im = open(image_path, 'rb')
        django_file = File(im)
        django_image_file = ImageFile(im)
        if (people=='btech') :
            btech = BTech.objects.create(name=df.name[i], roll_no=df.roll_no[i], year=df.year[i], image=django_image_file)
            btech.image.save(f'{roll_list[i]}.jpg', django_file, save=True)
            btech.save()
        elif (people=='mtech'):
            mtech = MTech.objects.create(name=df.name[i], roll_no=df.roll_no[i], year=df.year[i], image=django_image_file)
            mtech.image.save(f'{roll_list[i]}.jpg', django_file, save=True)
            mtech.save()
        elif (people=='faculty'):
            faculty = Faculty.objects.create(name=df.name[i], place=df.place[i], title=df.title[i], subtitle=df.subtitle[i], email=df.email[i], phone=df.phone[i], details=df.details[i], address=df.address[i], link=df.link[i], image=django_image_file)
            faculty.image.save(f'{roll_list[i]}.jpg', django_file, save=True)
            faculty.save()
        elif (people=='staff'):
            staff = Staff.objects.create(name=df.name[i], title=df.title[i], email=df.email[i], phone=df.phone[i], image=django_image_file)
            staff.image.save(f'{roll_list[i]}.jpg', django_file, save=True)
            staff.save()
        elif (people=='alumni'):
            alumni = Alumni.objects.create(name=df.name[i], roll_no=df.roll_no[i], program=df.program[i], date=df.date[i], year=df.year[i], image=django_image_file)
            alumni.image.save(f'{roll_list[i]}.jpg', django_file, save=True)
            alumni.save()
        elif (people=='phd'):
            phd = Phd.objects.create(name=df.name[i], roll_no=df.roll_no[i], year=df.year[i], details=df.details[i], image=django_image_file)
            phd.image.save(f'{roll_list[i]}.jpg', django_file, save=True)
            phd.save()
        elif (people=='ms'):
            ms = MS.objects.create(name=df.name[i], roll_no=df.roll_no[i], year=df.year[i], image=django_image_file)
            ms.image.save(f'{roll_list[i]}.jpg', django_file, save=True)
            ms.save()
        im.close()
    return "Data posted successfully"


def convertToAlumni(year):
    # btech and mtech
    btech = BTech.objects.filter(year=year)
    mtech = MTech.objects.filter(year=year)

    if (len(btech)!=0):
        for i in btech:
            Alumni.objects.create(name=i.name, roll_no=i.roll_no, program='BTech', year=year, image=i.image)
            BTech.objects.get(roll_no=i.roll_no).delete()
    if (len(mtech)!=0):
        for i in mtech:
            Alumni.objects.create(name=i.name, roll_no=i.roll_no, program='MTech', year=year, image=i.image)
            MTech.objects.get(roll_no=i.roll_no).delete()
    
    return "Data converted to Alumni successfully"