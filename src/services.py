# Методы для работы с файлами

import os

class files_srv:
    
# Проверка, если файл существует
    def check_if_exists(full_fpath):        
        try:
            with open(full_fpath) as f:
                pass
        except FileNotFoundError:
            print('The file does not exist.')
            return(False)
        else:
            print('The file exists.')
            return(True)
        
## Управление директориями для загрузки файлов:
## файл сохраняется в директорию, соответствующую его расширению
    def manage_directories(root,exts):
        if exts=='.png' or exts=='.PNG':
            os.makedirs(os.path.join(root+'\\Изображения', 'png'),exist_ok=True)
            return(os.path.join(root+'\\Изображения', 'png'))
        elif exts=='.jpg' or exts=='.jpeg' or exts=='.JPG' or exts=='.JPEG':
            os.makedirs(os.path.join(root+'\\Изображения', 'jpg'),exist_ok=True)
            return(os.path.join(root+'\\Изображения', 'jpg'))
        elif exts=='.doc' or exts=='.DOCX':
            os.makedirs(os.path.join(root+'\\Документы', 'doc'),exist_ok=True)
            return(os.path.join(root+'\\Документы', 'doc'))        
        elif exts=='.pdf' or exts=='.PDF':
            os.makedirs(os.path.join(root+'\\Документы', 'pdf'),exist_ok=True)
            return(os.path.join(root+'\\Документы', 'pdf'))
        elif exts=='.mp3' or exts=='.MP3':
            os.makedirs(os.path.join(root+'\\Аудио', 'mp3'),exist_ok=True)
            return(os.path.join(root+'\\Документы', 'pdf'))        
        else:
            os.makedirs(os.path.join(root+'\\Разное', exts[0:]),exist_ok=True)
            return(os.path.join(root+'\\Разное', exts[0:]))

## Вывод всех директорий в файловом хранилище        
class paths_srv:
    
    def __init__(self):
        self.path=[]
    def get_paths(self,root):        
        tree=os.walk(root)
        for i in tree:
            self.path.append(i[0])
        return(self.path)
    
            
    
        
