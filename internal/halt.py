from jajucha.communication import Client
import jajucha.config as config

"""
CarDS - internal.halt.py
Copyright 2023. jtaeyeon05 all rights reserved 
"""


def halt():
    try:
        client = Client('tcp://%s:%d' % config.address)
        client.connect()
        if client.id is None:
            if not client.override():
                print('연결 실패')
                return
        if client.exit():
            print('자주차가 정상적으로 종료되었습니다.')
        else:
            print('종료 실패')
    except:
        print('종료 실패')
