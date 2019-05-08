import os
import sqlite3
import datetime

USERNAME = os.popen('whoami').read().strip()


class DataGrabber(object):
    """docstring for ClassName"""
    def __init__(self):
        print('/Users/'+USERNAME+'/Library/Messages/chat.db')
        self.conn = sqlite3.connect('/Users/'+USERNAME+'/Library/Messages/chat.db',
                                    check_same_thread=False)
        self.OSX_EPOCH = 978307200

    def get_table_names(self):
        c = self.conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(c.fetchall())

    def get_messages(self, handle_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM `message` WHERE handle_id=" + str(handle_id) + " ORDER BY date DESC LIMIT 20" )
        all_messages = c.fetchall()[::-1]
        payload = []
        for message in all_messages:
            fro = "ME" if message[21] == 1 else "THEM"
            payload += [ { "message":message[2], "time":str(datetime.datetime.fromtimestamp(message[15] + self.OSX_EPOCH)), "from":fro } ]
        c.close()
        return payload

    def get_handles_like(self, search):
        c = self.conn.cursor()
        c.execute("SELECT * FROM `handle` WHERE id LIKE '%"+search+"%'")
        all_handles = c.fetchall()
        c.close()
        return all_handles

    def get_all_conversations(self, handle_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM `chat_handle_join` WHERE handle_id=" + str(handle_id))
        all_convs = c.fetchall()
        c.close()
        return all_convs

    def find_get_messages(self, search):
        payload = []
        for hand in self.get_handles_like(search):
            # print hand
            payload += [self.get_messages(hand[0])]
        return payload
