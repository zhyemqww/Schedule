#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2025/1/16 20:16
# @File     : style
# @Project  : Schedule
# @Desc     :


class StyleMixIn:

    COLOR_MAP = {
        "Reset": "rgba(255, 255, 255, 0.7)",
        "This Week": "rgba(237, 125, 49, 0.7)",
        "Next Week": "rgba(255, 217, 102, 0.7)",
        "Week After Next": "rgba(197, 224, 180, 0.7)",
        "Incomplete": "rgba(207, 213, 234, 0.7)",
        "Skipped": "rgba(68, 114, 196, 0.7)",
        "Finished": "rgba(65, 200, 40, 0.7)",

        "Reset_highlight": "rgba(255, 255, 255, 1)",
        "This Week_highlight": "rgba(237, 125, 49, 1)",
        "Next Week_highlight": "rgba(255, 217, 102, 1)",
        "Week After Next_highlight": "rgba(197, 224, 180, 1)",
        "Incomplete_highlight": "rgba(207, 213, 234, 1)",
        "Skipped_highlight": "rgba(68, 114, 196, 1)",
        "Finished_highlight": "rgba(65, 200, 40, 1)",

        "Reset_downplay": "rgba(255, 255, 255, 0.2)",
        "This Week_downplay": "rgba(237, 125, 49, 0.2)",
        "Next Week_downplay": "rgba(255, 217, 102, 0.2)",
        "Week After Next_downplay": "rgba(197, 224, 180, 0.2)",
        "Incomplete_downplay": "rgba(207, 213, 234, 0.2)",
        "Skipped_downplay": "rgba(68, 114, 196, 0.5)",
        "Finished_downplay": "rgba(65, 200, 40, 0.5)",
    }