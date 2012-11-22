import unittest
import sys
from datetime import datetime

sys.path.append('controller/')

from DatabaseParser import *

class TestDatabaseParser(unittest.TestCase):

  def setUp(self):
    """
    Called before *each* testcase. We want to operate on a fresh database
    """
    clear()

  def testVerifyLoginOnEmptyDb(self):
    self.assertFalse(verifyLogin("test@0xabc.de", "asfelkj"))

  def testRegister(self):
    self.assertTrue(registerUser("benjamin@flowerpower.org"))
    self.assertFalse(registerUser("benJamin@flowerpower.org"))
    self.assertTrue(registerUser("karlaColumna@bild.de"))
    self.assertTrue(userExists("benjamin@flowerpower.org", includeGhosts = True))
    self.assertTrue(userExists("karlaColumna@bild.de", includeGhosts = True))
    self.assertFalse(userExists("benjamin@flowerpower.org"))
    self.assertFalse(userExists("karlaColumna@bild.de"))

  def testActivate(self):
    activateUser("test@0xabc.de", "test", "123456", True) #force = register if not present and activate
    self.assertTrue(userExists("test@0xabc.de"))

    self.assertFalse(activateUser("test@0xabc.de", "test2", "765432")) #an activated user can't be activated a second time
    
    registerUser("ghost@test.de")
    self.assertTrue(activateUser("ghost@test.de", "ghosty", "123456")) #activate a ghost user
    self.assertTrue(userExists("ghost@test.de")) #User should be found in "normal" users

  def testListEvents(self):
    activateUser("a", "alpha", "1", True)
    activateUser("b", "beta", "2", True)
    activateUser("c", "charlie", "3", True)
    date_a = datetime.now
    id_a = insertEvent("a", "1.4.2013", 10, ["b"], "Event1")
    print listEvents()
    self.assertEqual(listEvents(), [(id_a, u'a', '1.4.2013', 10, u'["b"]', u'Event1')])

  def testListEvents_emptyDB(self):
    listEvents()

  def testGetPassword_NonexistentUser(self):
    getPassword("martin@0xabc.de")

  def testGetPassword(self):
    activateUser("awesome@0xabc.de", "Bluemchen", "blume", True)
    getPassword("awesome@0xabc.de")

  def testInsertEvent(self):
    activateUser("awesome@0xabc.de", "Bluemchen", "blume", True)
    insertEvent("awesome@0xabc.de", "4.1.2010", 12.1, ["tobstu@0xabc.de"], "An Event")

  def testSetEventStatus(self):
    setEventStatus("tobstu@gmail.com", 2, "paid")

  def testResetUrl(self):
    activateUser("dummy@0xabc.de", "dummy", "thisIsMyPwd", True)
    reset = getResetUrlKey("dummy@0xabc.de")
    self.assertTrue(str(reset).__len__() == 8)
    self.assertTrue(isValidResetUrlKey("dummy@0xabc.de", reset))

  def testResetLogin(self):
    activateUser("userA@0xabc.de", "A", "123456", True)
    activateUser("userB@0xabc.de", "B", "654321", True)
    self.assertFalse(updateLogin("userC@0xabc.de", "ffffff"))
    self.assertTrue(updateLogin("userb@0xabc.de", "abcdef"))
    self.assertFalse(verifyLogin("userB@0xabc.de", "654321"))
    self.assertTrue(verifyLogin("userB@0xabc.de", "abcdef"))
    self.assertTrue(verifyLogin("userA@0xabc.de", "123456"))

  def testGetEvent(self):
    activateUser("userA@0xabc.de", "A", "123456", True)
    id = insertEvent("userA@0xabc.de", "10.4.2013", 101.12, ["tobstu@gmail.com"], "comment")
    self.assertEqual(getEvent(id + 1), None)
    print str(getEvent(id))
    self.assertEqual(str(getEvent(id)), str(Event(id=id, owner="userA@0xabc.de", date="10.4.2013", amount=101.12, participants=['tobstu@gmail.com'], comment="comment")))

  def testBuildTransactionTree(self):
    registerUser("userA@0xabc.de")
    registerUser("userB@0xabc.de")
    registerUser("userC@0xabc.de")
    insertEvent("userA@0xabc.de", "1.1.2010", 12, ["userB@0xabc.de", "userC@0xabc.de"], "event1")
    insertEvent("userA@0xabc.de", "1.1.2010", 2, ["userC@0xabc.de"], "event2")
    insertEvent("userB@0xabc.de", "1.1.2010", 3.3, ["userA@0xabc.de", "userC@0xabc.de"], "event3")
    buildTransactionTree()
    self.assertIn("userA@0xabc.de", graphNodes)#node for every user?
    self.assertIn("userB@0xabc.de", graphNodes)
    self.assertIn("userC@0xabc.de", graphNodes)

    #entries from B to A and C (event3)
    self.assertIn("userA@0xabc.de", graphNodes["userB@0xabc.de"].incoming.keys())
    self.assertIn("userC@0xabc.de", graphNodes["userB@0xabc.de"].incoming.keys())
    self.assertEqual(graphNodes["userB@0xabc.de"].incoming["userA@0xabc.de"], TransactionEdge("userA@0xabc.de", "userB@0xabc.de", 1.1))
    self.assertEqual(graphNodes["userB@0xabc.de"].incoming["userC@0xabc.de"], TransactionEdge("userC@0xabc.de", "userB@0xabc.de", 1.1))
    self.assertIn("userB@0xabc.de", graphNodes["userA@0xabc.de"].outgoing.keys())
    self.assertIn("userB@0xabc.de", graphNodes["userC@0xabc.de"].outgoing.keys())

    #entries hosted by A for C
    self.assertIn("userC@0xabc.de", graphNodes["userA@0xabc.de"].incoming.keys())
    self.assertEqual(graphNodes["userA@0xabc.de"].incoming["userC@0xabc.de"], TransactionEdge("userC@0xabc.de", "userA@0xabc.de", 5)) #(12/4 + 2/2)
    self.assertEqual(graphNodes["userC@0xabc.de"].outgoing["userA@0xabc.de"], TransactionEdge("userC@0xabc.de", "userA@0xabc.de", 5))

    #entries hosted by A for B
    self.assertIn("userB@0xabc.de", graphNodes["userA@0xabc.de"].incoming.keys())
    self.assertEqual(graphNodes["userA@0xabc.de"].incoming["userB@0xabc.de"], TransactionEdge("userB@0xabc.de", "userA@0xabc.de", 4))
    self.assertEqual(graphNodes["userB@0xabc.de"].outgoing["userA@0xabc.de"], TransactionEdge("userB@0xabc.de", "userA@0xabc.de", 4))


if __name__ == '__main__':
  unittest.main()
