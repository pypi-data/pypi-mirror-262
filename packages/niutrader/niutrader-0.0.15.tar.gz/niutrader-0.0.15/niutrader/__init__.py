# -*- coding: utf-8 -*-
import urllib3

from niutrader import exceptions
from niutrader.api import use  # , follower
from niutrader.log import logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__version__ = "0.0.15"
__author__ = "NiuGe"
