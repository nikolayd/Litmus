import os
import shutil
import requests
from requests.adapters import HTTPAdapter
from Pack1.Litmus.auth import get_items
from Pack1.Litmus.utils import folder_name
from Pack1.Litmus.utils import img_name


def write_results():
    file_path = 'Litmus_Results'
    results_folder = os.path.join(os.getcwd(), file_path)
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    else:
        print('Directory already exists')
    for item in get_items():
        name, img_list = item
        subfolder = os.path.join(results_folder, folder_name(name))
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
        for img in img_list:
            s = requests.Session()
            adapter = requests.adapters.HTTPAdapter(max_retries=3)
            s.mount('https://', adapter)
            response = s.get(img, stream=True)
            image = os.path.join(subfolder, img_name(img))
            with open(image, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

if __name__ == "__main__":
    write_results()


