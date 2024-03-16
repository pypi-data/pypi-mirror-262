# coding:utf8
from paddlenlp import Taskflow

def information_extact_tool(schema, text_list):
    ie = Taskflow('information_extraction',
                  schema=schema,
                  model='uie-base',
                  use_fast=True,
                  device_id=1,
                  position_prob=0.2,
                  )
    return ie(text_list)