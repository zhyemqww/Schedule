#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2024/6/19 20:36
# @File     : path_utils
# @Project  : PELSA_Decipher_1.0
# @Desc     :

import os
import sys


class PathUtils:
    """
    This class is used to get the path to the resource
    """
    @staticmethod
    def get_resource_path(relative_path):
        """
        This function is used to get the path to the resource. First, it checks whether the frozen path of the program
        (the executable file path) can be retrieved, and if so, returns a combination of the frozen path and the relative
        path.
        If the frozen path cannot be obtained, it returns a combination of the absolute and relative paths of the current
        working directory.
        :param relative_path:
        :return:
        """
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath(""), relative_path)