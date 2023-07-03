import requests
import json
import unittest
import threading
import multiprocessing
from qbank import app
import pdb

headers = {'content-type': 'application/json'
          }

class TestViewer(unittest.TestCase):
     def setUp(self):
         print('setUp')
         t1 = threading.Thread(target=app.run, daemon=True)
         t1.start()


     def tearDown(self):
         print('tearDown\n')

# test home page
     def test_index(self):
        payload = {'category':'category',
                    'skills':'skills',
                    'levels':'levels' }

        r = requests.get("http://127.0.0.1:5000", data=json.dumps(payload),headers=headers)
        if r.status_code == 200: print("PASS: viewer test")
        else: print("FAIL: viewer test")


# test Get_API
     def test_questions(self):
        payload = {'sid': 'sid',
                    'lid':'lid',
                    'cid':'cid',
                    'questions':'questions'
                  }

        r = requests.get("http://127.0.0.1:5000/question",data=json.dumps(payload), headers=headers)
        if r.status_code == 200: print("PASS: get test")
        else: print("FAIL: get test")

# test Post_API
     def test_add_questions(self):
        payload = {"sid":"1",
                    "tag":"python10",
                    "summary":"nothing10",
                    "description":"something10",
                    "weightage":"2",
                    "user_id":"12345",
                    "qtype_id":"1",
                    "level_id":"2"
                  }

        r = requests.post("http://127.0.0.1:5000/addquestion",data=json.dumps(payload),headers=headers)
        print(r)
        if r.status_code == 200: print("PASS: add test")
        else: print("FAIL: add test")

#test Delete_API
     def test_delete(self):
        r = requests.delete("http://127.0.0.1:5000/delete/3",headers=headers)
        if r.status_code == 200: print("PASS: delete test")
        else: print("FAIL: delete test")

#test Update_API
     def test_update(self):
        payload = {"sid":"1",
                    "tag":"python1011231",
                    "summary":"nothing1012910221",
                    "description":"something101923028193",
                    "weightage":"2",
                    "user_id":"12321345",
                    "qtype_id":"1",
                    "level_id":"2"
                  }
        r = requests.put("http://127.0.0.1:5000/update/1",data=json.dumps(payload),headers=headers)
        if r.status_code == 200: print("PASS: update test")
        else: print("FAIL: update test")


if name == '__main__':
    unittest.main()

