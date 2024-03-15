#!/usr/bin/env python
# coding=utf-8

'''
Author       : Kofi
Date         : 2024-03-08 10:54:54
LastEditors  : Kofi
LastEditTime : 2024-03-08 11:10:56
Description  : 工具函数
'''
import time

class Tools:
  def timing_decorator(func):
      def wrapper(*args, **kwargs):
          start = time.time()
          result = func(*args, **kwargs)
          end = time.time()
          print(f"{func.__name__} 耗时 {end - start} 秒")
          return result

      return wrapper