import os
import shutil
import time
import logging

logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG, format='%(levelname)s / %(message)s')


class Sincronize:

    def __init__(self, path1, path2, seconds):
        self.path1 = path1
        self.path2 = path2
        self.seconds = seconds
        self.yellow = '\033[33m'
        self.blue = '\033[34m'
        self.red = '\033[31m'
        self.end = '\033[m'
    

    def monitoring(self):
        """Will check at all times if any changes occur in the folders"""

        folder1 = os.listdir(self.path1)
        folder2 = os.listdir(self.path2)
        
        if folder1 == folder2:
            self.check_status(self.path1, self.path2)
            self.create_files_directories(self.path1)                     
                               
        else:
            self.delete(f'{self.path2}')    
            self.create_full_directory(f'{self.path1}')
           

    def check_status(self, path1, path2):
        """Check if any files have been edited"""

        folder1 = os.listdir(path1)
        folder2 = os.listdir(path2)
        
        for files1 in folder1:
            for files2 in folder2:
                if files1 == files2:
                    
                    path1_completo = os.path.join(self.path1, files1)
                    path2_completo = os.path.join(self.path2, files2)

                    status_path1 = os.stat(path1_completo)
                    status_path2 = os.stat(path2_completo)

                    if status_path1.st_mtime > status_path2.st_mtime:
                        
                        if not (os.path.isdir(f'{self.path1}/{files1}') and os.path.isdir(f'{self.path2}/{files2}')):

                            # Edited files 
                            shutil.copyfile(f'{self.path1}/{files1}', f'{self.path2}/{files1}')
                            logging.info(f'Edited file: {files1}')
                            print(f'Edited file: {self.yellow}{files1}{self.end}')
                            
                        else:
                            self.check_status(path1_completo, path2_completo)
                            

    def create_files_directories(self, path1):
        """It will create several files and directories, but it will not have log and print messages.
        why is it being monitored all the time, and whenever this function is called,
        will create an infinite loop of messages. I still couldn't solve this problem."""
        
        files = os.listdir(path1)
        for file in files:
            path1_completo = os.path.join(path1, file)
            if os.path.isdir(path1_completo):
                
                path_1 = path1_completo.replace(f'{self.path1}', '')
                shutil.copytree(path1_completo, f'{self.path2}{path_1}', dirs_exist_ok=True,)
                # logging.info(f'Directory created: {file}')
                # print(f'Directory created: {self.yellow}{file}{self.end}')
                self.create_files_directories(path1_completo)
            else:
                path_ = path1_completo.replace(f'{self.path1}', '')
                shutil.copyfile(path1_completo, f'{self.path2}{path_}')
                

    def create_full_directory (self, path1):
        """If the 'replica_folder' folder is not the same as the 'origin_folder' folder,
        a complete copy will be created in the 'replica_folder' folder"""

        files = os.listdir(path1)

        for file in files:
            path1_completo = os.path.join(path1, file)

            if os.path.isdir(path1_completo):
                if not os.path.exists(f'{self.path2}/{file}'):
                    shutil.copytree(path1_completo, f'{self.path2}/{file}', dirs_exist_ok=True)
                    logging.info(f'Directory created: {file}')
                    print(f'Directory created: {self.yellow}{file}{self.end}')
                    self.create_full_directory(path1)
            else:
                if not os.path.exists(f'{self.path2}/{file}'):
                    shutil.copyfile(path1_completo, f'{self.path2}/{file}')
                    logging.info(f'File created: {file}')
                    print(f'File created: {self.yellow}{file}{self.end}')



    def delete(self, path):
        """Will delete file or directory, that is in the same tree as the 'replica_folder' directory """

        folder1 = os.listdir(self.path1)
        folder2 = os.listdir(self.path2)

        list_diference = [x for x in folder2 if x not in folder1]

        for a in list_diference:
            path_2 = f'{path}/{a}'

            if os.path.isdir(path_2):
                shutil.rmtree(path_2)
                logging.info(f'Directory removed: {a}')
                print(f'Directory removed: {self.red}{a}{self.end}')
            else:
                os.remove(path_2)
                logging.info(f'File removed: {a}')
                print(f'File removed: {self.red}{a}{self.end}')


    # Extra
    def format_size(self, size):
        """Just to format the size of each file"""

        base = 1024
        kilo = base
        mega = base ** 2
        giga = base ** 3
        tera = base ** 4
        peta = base ** 5

        if size < kilo:
            text = 'B'
        elif size < mega:
            size /= kilo
            text = 'K'
        elif size < giga:
            size /= mega
            text = 'M'
        elif size < tera:
            size /= giga
            text = 'G'
        elif size < peta:
            size /= tera
            text = 'T'
        else:
            size /= peta
            text = 'P'
        
        size = round(size, 2)
        return f'{size}{text}'


    # Extra
    def find_file(self):
        """Extra function I made, the purpose is to fetch any file inside the 'origin_folder' folder,
        if you want to look for a specific file just do a search in search_term, if you
        pass nothing, it will bring all the files"""

        search_term = ''
        counter = 0
        
        for root, directory, files in os.walk(self.path1):

            for file in files:
                if search_term in file:
                    try:
                        counter += 1
                        full_path = os.path.join(root, file)
                        file_name, file_extension = os.path.splitext(file)
                        size = os.path.getsize(full_path)

                        print()
                        print(f'I found the file: {self.yellow}{file}{self.end}')
                        print(f'Complete Path: {self.yellow}{full_path}{self.end}')
                        print(f'File name: {self.yellow}{file_name}{self.end}')
                        print(f'File Extension: {self.yellow}{file_extension}{self.end}')
                        print(f'size: {self.yellow}{size}{self.end}')
                        print(f'size formatted: {self.yellow}{self.format_size(size)}{self.end}')

                    except PermissionError as e:
                        print('No permission')
                    except FileNotFoundError as e:
                        print('File not found')
                    except Exception as e:
                        print(f'Unknown error: {e}')

        print()                
        print(f'{self.blue}{counter} Files(s) found{self.end}')


    def main(self):
        print(f'{self.blue}Monitoring...{self.end}')
        print()
        # self.find_file()
        while True:
            self.monitoring()
            time.sleep(self.seconds)


if __name__ == '__main__':

    sincronize = Sincronize('/home/renan/codigos/task_veeam/origin_folder', '/home/renan/codigos/task_veeam/replica_folder', 2)
    sincronize.main()