import os
import shutil


class DiskUtils:

    @staticmethod
    def safe_move(src, dest):
        if os.path.exists(src):
            shutil.move(src, dest)
        else:
            print('src file does not exist! %s' % src)
