#!/usr/bin/env python2.7

from requests import Session
import json

class Publisher:
  def __init__(self):
    self.s = Session()

  def publish(self, payload):
    self.s.post("http://ec2-54-93-71-88.eu-central-1.compute.amazonaws.com/", data=json.dumps(payload))

if __name__ == "__main__":
  p = Publisher()
  for i in range(10):
    p.publish({"bla": 1})
