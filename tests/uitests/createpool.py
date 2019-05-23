# This work is licensed under the GNU GPLv2 or later.
# See the COPYING file in the top-level directory.

from tests.uitests import utils as uiutils


class CreatePool(uiutils.UITestCase):
    """
    UI tests for the createpool wizard
    """

    def _open_create_win(self, hostwin):
        hostwin.find("pool-add", "push button").click()
        win = self.app.root.find(
                "Add a New Storage Pool", "frame")
        uiutils.check_in_loop(lambda: win.active)
        return win


    ##############
    # Test cases #
    ##############

    def testCreatePool(self):
        hostwin = self._open_host_window("Storage")
        win = self._open_create_win(hostwin)

        # Create a simple default dir pool
        finish = win.find("Finish", "push button")
        name = win.find("Name:", "text")
        self.assertEqual(name.text, "pool")
        newname = "a-test-new-pool"
        name.text = newname
        finish.click()

        # Select the new object in the host window, then do
        # stop->start->stop->delete, for lifecycle testing
        uiutils.check_in_loop(lambda: hostwin.active)
        cell = hostwin.find(newname, "table cell")
        delete = hostwin.find("pool-delete", "push button")
        start = hostwin.find("pool-start", "push button")
        stop = hostwin.find("pool-stop", "push button")

        cell.click()
        stop.click()
        uiutils.check_in_loop(lambda: start.sensitive)
        start.click()
        uiutils.check_in_loop(lambda: stop.sensitive)
        stop.click()
        uiutils.check_in_loop(lambda: delete.sensitive)

        # Delete it
        delete.click()
        alert = self.app.root.find("vmm dialog", "alert")
        alert.find_fuzzy("permanently delete the pool", "label")
        alert.find("Yes", "push button").click()

        # Ensure it's gone
        uiutils.check_in_loop(lambda: cell.dead)

        # Test a scsi pool
        win = self._open_create_win(hostwin)
        typ = win.find("Type:", "combo box")
        newname = "a-scsi-pool"
        name.text = "a-scsi-pool"
        typ.click()
        win.find_fuzzy("SCSI Host Adapter", "menu item").click()
        win.find_fuzzy("Source Path:", "combo").click_combo_entry()
        win.find_fuzzy("host2", "menu item").click()
        finish.click()
        hostwin.find(newname, "table cell")

        # Test a ceph pool
        win = self._open_create_win(hostwin)
        newname = "a-ceph-pool"
        name.text = "a-ceph-pool"
        typ.click()
        win.find_fuzzy("RADOS Block", "menu item").click()
        win.find_fuzzy("Host Name:", "text").text = "example.com:1234"
        win.find_fuzzy("Source Name:", "text").typeText("frob")
        finish.click()
        hostwin.find(newname, "table cell")

        # Ensure host window closes fine
        hostwin.click()
        hostwin.keyCombo("<ctrl>w")
        uiutils.check_in_loop(lambda: not hostwin.showing and
                not hostwin.active)


    def testCreatePoolXMLEditor(self):
        hostwin = self._open_host_window("Storage")
        win = self._open_create_win(hostwin)
        finish = win.find("Finish", "push button")
        name = win.find("Name:", "text")

        # Create a new obj with XML edited name, verify it worked
        tmpname = "objtmpname"
        newname = "froofroo"
        name.text = tmpname
        win.find("XML", "page tab").click()
        xmleditor = win.find("XML editor")
        xmleditor.text = xmleditor.text.replace(
                ">%s<" % tmpname, ">%s<" % newname)
        finish.click()
        uiutils.check_in_loop(lambda: hostwin.active)
        cell = hostwin.find(newname, "table cell")
        cell.click()

        # Do standard xmleditor tests
        win = self._open_create_win(hostwin)
        self._test_xmleditor_interactions(win, finish)
        win.find("Cancel", "push button").click()
        uiutils.check_in_loop(lambda: not win.visible)
