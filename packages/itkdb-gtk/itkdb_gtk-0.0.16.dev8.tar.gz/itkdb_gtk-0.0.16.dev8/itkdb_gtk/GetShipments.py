#!/usr/bin/env python3
"""GEt shipments to a particular site (default is IFIC)."""
import pathlib
import sys

try:
    import itkdb_gtk
    
except ImportError:
    from pathlib import Path
    cwd = Path(sys.argv[0]).parent.parent
    sys.path.append(cwd.as_posix())

from itkdb_gtk import dbGtkUtils, ITkDBlogin, ITkDButils
import gi
import serial

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib

# Check if Gtk can be open
gtk_runs, gtk_args = Gtk.init_check()


class ReceiveShipments(dbGtkUtils.ITkDBWindow):
    """Find shipments related to given recipient."""

    def __init__(self, session, recipient="IFIC"):
        """Initialization.

        Args:
        ----
            session: ITkDB session.
            recipient: default recipient

        """
        self.recipient = recipient
        self.state = "inTransit"
        self.institute = None
        self.model = None
        self.store = None
        self.shipments = {}

        global gtk_runs
        if gtk_runs:
            super().__init__(session=session, title="Upload AVS Data",
                             show_search="Cliick to search shipments",
                             gtk_runs=gtk_runs)

            self.init_window()

    def init_window(self):
        """Initialize window."""
        #
        self.set_border_width(10)

        # intercept keyboard
        self.setup_scanner()

        # Prepare HeaderBar
        self.hb.props.title = "{} shipments".format(self.recipient)

        # action button in header
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="insert-object-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        button.set_tooltip_text("Click to receive shipment items.")
        button.connect("clicked", self.receive_items)
        self.hb.pack_end(button)

        # Data panel
        grid = Gtk.Grid(column_spacing=5, row_spacing=1)
        self.mainBox.pack_start(grid, False, True, 0)

        # The shipment receiver
        receiver = self.create_institute_combo()
        receiver.connect("changed", self.on_receiver)
        receiver.set_tooltip_text("Select the Institute receiving the items.")
        dbGtkUtils.set_combo_iter(receiver, self.recipient)
        grid.attach(Gtk.Label(label="To:"), 0, 0, 1, 1)
        grid.attach(receiver, 1, 0, 1, 1)

        # The senders combo
        senders = self.create_institute_combo()
        senders.connect("changed", self.on_institute)
        senders.set_tooltip_text("Select the Institute sending the items.")
        grid.attach(Gtk.Label(label="From: "), 0, 1, 1, 1)
        grid.attach(senders, 1, 1, 1, 1)

        # The shipment status
        status = Gtk.ListStore(str)
        for st in ["prepared", "inTransit", "delivered", "deliveredIncomplete", "deliveredWithDamage", "undelivered"]:
            status.append([st])
        cmb_status = Gtk.ComboBox.new_with_model_and_entry(status)
        cmb_status.set_entry_text_column(0)
        cmb_status.set_active(1)
        cmb_status.connect("changed", self.on_status_changed)
        grid.attach(Gtk.Label(label="State"), 0, 2, 1, 1)
        grid.attach(cmb_status, 1, 2, 1, 1)

        # The list of shipments from sender to receiver
        shipment_list = Gtk.ListStore(str, str)
        cmb_shipment = Gtk.ComboBox.new_with_model_and_entry(shipment_list)
        cmb_shipment.set_entry_text_column(0)
        cmb_shipment.set_active(1)
        cmb_shipment.connect("changed", self.on_new_shipment)
        self.cmb_shipment = cmb_shipment
        grid.attach(Gtk.Label(label="Shipment"), 0, 3, 1, 1)
        grid.attach(cmb_shipment, 1, 3, 1, 1)

        btn = Gtk.Button(label="Receive Items")
        btn.set_tooltip_text("Click to receive shipment items.")
        btn.connect("clicked", self.receive_items)
        grid.attach(btn, 2, 3, 1, 1)

        # Add a Separator
        self.mainBox.pack_start(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL), False, True, 0)

        # Paned object
        paned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        paned.set_size_request(-1, 200)
        self.mainBox.pack_start(paned, True, True, 0)

        # The main TreeView
        tree_view = self.create_tree_view()
        paned.add1(tree_view)

        # The text view
        paned.add2(self.message_panel.frame)

        self.show_all()

    def create_tree_view(self, size=150):
        """Create a tree view with the shipment items."""
        store = Gtk.ListStore(str, str, str, bool)
        self.tree = Gtk.TreeView(model=store)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.tree)
        scrolled.set_size_request(-1, size)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Serial No.", renderer, text=0)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Object", renderer, text=1)
        self.tree.append_column(column)

        renderer = Gtk.CellRendererToggle()
        column = Gtk.TreeViewColumn("UnCheck to receive", renderer, active=3)
        renderer.connect("toggled", self.on_cell_toggled)
        self.tree.append_column(column)

        return scrolled

    def setup_scanner(self):
        """Setup scanner."""
        for fnam in ["/dev/ttyACM0", "/dev/cu.usbmodemS_N_G19F204881"]:
            P = pathlib.Path(fnam)
            if P.exists():
                rdr = serial.Serial(fnam, 9600)
                GLib.unix_fd_add_full(GLib.PRIORITY_DEFAULT, rdr.fileno(), GLib.IOCondition.IN, self.get_qrcode, rdr)
                break

    def get_qrcode(self, fd, state, reader):
        """Gets data from QR scanner."""
        available = reader.in_waiting
        while True:
            delta = reader.in_waiting - available
            if not delta:
                break

        # Get data from serial device passed in via
        data = reader.read_until(expected='\r', size=reader.in_waiting).strip()
        txt = data.decode('utf-8')
        self.write_message("{}\n".format(txt))

        # search code in the list
        if self.store:
            iter = self.store.get_iter_first()
            while iter:
                if (self.store.get_value(iter, 0) == txt):
                    self.write_message("...found\n")
                    self.store[iter][3] = False

                iter = self.store.iter_next(iter)

        return True

    def get_institute_list(self):
        """Get the institute list."""
        sites = self.session.get("listInstitutions", json={})
        liststore = Gtk.ListStore(str, str)
        for site in sites:
            self.code2inst[site['code']] = site['name']
            self.inst2code[site['name']] = site['code']
            liststore.append([site["code"], site["code"]])
            liststore.append([site["name"], site["code"]])

        completion = Gtk.EntryCompletion()
        completion.set_model(liststore)
        completion.set_text_column(0)
        return completion

    def on_cell_toggled(self, widget, path):
        """A cell has been toggled."""
        model = self.tree.get_model()
        model[path][3] = not model[path][3]

    def on_new_shipment(self, combo):
        """New shipment selected from combo."""
        if len(combo.get_model()) == 0:
            return

        tree_iter = combo.get_active_iter()
        if tree_iter is None:
            self.write_message("Cannot select current shipment.\n")
            return

        model = combo.get_model()
        shpmnt = model[tree_iter][1]

        # Store the model associated to this shipment.
        self.store = self.shipments[shpmnt]
        filter = self.store.filter_new()
        filter.set_visible_column(3)
        self.tree.set_model(filter)

    def on_status_changed(self, combo):
        """Status changed."""
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            name = model[tree_iter][0]
        else:
            entry = combo.get_child()
            name = entry.get_text()

        self.state = name

    def get_institute_from_combo(self, combo):
        """Get Institute from combo."""
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            name = model[tree_iter][1]

        else:
            name = combo.get_child().get_text()
            if name in self.inst2code:
                name = self.inst2code[name]

            elif name not in self.code2inst:
                name = None

        return name

    def on_receiver(self, combo):
        """Sets the recipient."""
        name = self.get_institute_from_combo(combo)
        if name:
            self.recipient = name
            hb = self.get_titlebar()
            hb.props.title = "{} shipments".format(self.recipient)

    def on_institute(self, combo):
        """New institute chosen."""
        name = self.get_institute_from_combo(combo)
        if name:
            self.institute = name

    def get_tree_view_model(self):
        """Return an empty model for the tree view."""
        return Gtk.ListStore(str, str, str, bool, str, str)

    def query_db(self, *args):
        """Query for shipments in DB."""
        if self.institute is None or self.state == "":
            return

        payload = {
            "code": self.recipient,
            "status": self.state
        }
        shpmts = self.session.get("listShipmentsByInstitution", json=payload)

        # We store SN, component type, shipment ID, visibility
        # We populate the combo of shipments and prepare the models for
        # the tree view.
        cmb_store = Gtk.ListStore(str, str)
        for s in shpmts:
            if s["recipient"]["code"] == self.recipient and s['sender']['code'] == self.institute:
                store = self.get_tree_view_model()
                cmb_store.append([s['name'], s['id']])
                items = self.session.get("listShipmentItems", json={"shipment": s["id"]})
                for i in items:
                    store.append([i['component']['serialNumber'],
                                  i["component"]["componentType"]['name'],
                                  s['id'],
                                  True,
                                  s['name'],
                                  i['component']['code']])
                self.shipments[s['id']] = store

        # Load the model in the shipment combo
        if len(cmb_store) == 0:
            self.write_message("Could not find any shipment in DB.\n")

        self.cmb_shipment.set_model(cmb_store)
        self.cmb_shipment.set_entry_text_column(0)
        self.cmb_shipment.set_active(0)

    def receive_items(self, *args):
        """Receive shipment items."""
        data = {}
        names = {}

        # self.store is the model of the tree view
        if self.store:
            iter = self.store.get_iter_first()
            while iter:
                shpmnt = self.store.get_value(iter, 2)
                if shpmnt not in data:
                    data[shpmnt] = create_shipment_status(shpmnt)
                    names[shpmnt] = self.store.get_value(iter, 4)

                item = {
                    "code": self.store[iter][5],
                    "delivered": not self.store[iter][3]
                }
                data[shpmnt]["shipmentItems"].append(item)

                iter = self.store.iter_next(iter)

        else:
            self.write_message("Empty list of items.\n")

        for id, S in data.items():
            # Check that all items are there
            nlost = 0
            for item in S["shipmentItems"]:
                if not item["delivered"]:
                    nlost += 1

            for Q in S["checklist"]["questionList"]:
                if Q["code"] == "Q14":
                    Q["value"] = (nlost == 0)

            if nlost:
                rc = dbGtkUtils.ask_for_confirmation("{} items are missing.".format(nlost),
                                                     "Proceed with shipment reception ?")
                if not rc:
                    self.write_message("Shipment reception cancelled by user.\n")
                    return

            # Open dialog to fill-in questions
            create_check_list(S["checklist"]["questionList"], names[id])

            # send the update to the DB
            S['status'] = "delivered"
            resp = ITkDButils.set_shipment_status(self.session, S)
            if resp is None:
                rc = ITkDButils.get_db_response()
                ipos = rc.find("The following details may help:")
                msg = ""
                if ipos >= 0:
                    msg = rc[ipos:]

                dbGtkUtils.complain("Could not update the shipment status.", msg)
                self.write_message("Could not update the shipment status.\n{}\n".foramt(rc))

            else:
                self.write_message("Shipment {} received\n".format(names[id]))
                # Now remove the current shipment
                iter = self.cmb_shipment.get_active_iter()
                self.cmb_shipment.get_model().remove(iter)
                self.cmb_shipment.set_active(0)


def create_check_list(check_list, name):
    """Create a checklist."""
    dlg = Gtk.Dialog(title="Question List: {}".format(name))
    dlg.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OK, Gtk.ResponseType.OK)
    grid = Gtk.Grid(column_spacing=5, row_spacing=1)
    box = dlg.get_content_area()
    box.add(grid)

    irow = 0
    S = {}
    T = {}
    for question in check_list:
        label = Gtk.Label(label=question["text"])
        label.set_xalign(0.0)
        if isinstance(question["value"], bool):
            sw = Gtk.Switch()
            sw.set_active(question["value"])
            S[question["code"]] = sw
            wdgt = Gtk.Box()
            wdgt.pack_start(sw, False, False, 0)
        else:
            wdgt = Gtk.Entry()
            wdgt.set_text(question["value"])
            T[question["code"]] = wdgt

        grid.attach(label, 0, irow, 1, 1)
        grid.attach(wdgt, 1, irow, 1, 1)
        irow += 1

    dlg.show_all()
    rc = dlg.run()
    if rc == Gtk.ResponseType.OK:
        for question in check_list:
            if isinstance(question["value"], bool):
                question["value"] = S[question["code"]].get_active()

            else:
                question["value"] = T[question["code"]].get_text()

    dlg.hide()
    dlg.destroy()
    return check_list


def create_shipment_status(shpmnt):
    """Create the json data for a shipment status update."""
    out = {
        "shipment": shpmnt,
        "status": "delivered",
        "shipmentItems": [],
        "checklist": {"type": "DEFAULT",
                      "questionList": [
                          {
                              "code": "Q01",
                              "text": "Shipment was properly packaged",
                              "value": False
                          },
                          {
                              "code": "Q02",
                              "text": "Outer box intact",
                              "value": False
                          },
                          {
                              "code": "Q03",
                              "text": "Inner box intact",
                              "value": False
                          },
                          {
                              "code": "Q04",
                              "text": "ESD state bag used",
                              "value": False
                          },
                          {
                              "code": "Q05",
                              "text": "Humidity barrier bag used",
                              "value": False
                          },
                          {
                              "code": "Q06",
                              "text": "Vacuum sealed bag used",
                              "value": False
                          },
                          {
                              "code": "Q07",
                              "text": "50g shock watch present",
                              "value": False
                          },
                          {
                              "code": "Q08",
                              "text": "50g shock watch was not triggered",
                              "value": False
                          },
                          {
                              "code": "Q09",
                              "text": "25g shock watch present",
                              "value": False
                          },
                          {
                              "code": "Q10",
                              "text": "25g shock watch was not triggered",
                              "value": False
                          },
                          {
                              "code": "Q11",
                              "text": "Desiccant present",
                              "value": False
                          },
                          {
                              "code": "Q12",
                              "text": "Humidity indicator present",
                              "value": False
                          },
                          {
                              "code": "Q13",
                              "text": "Humidity indicator triggered up to percentage",
                              "value": ""
                          },
                          {
                              "code": "Q14",
                              "text": "All items present",
                              "value": False
                          },
                          {
                              "code": "Q15",
                              "text": "Comments",
                              "value": ""
                          }
                      ]
                      }
    }
    return out


def main():
    """Main entry."""
    dlg = ITkDBlogin.ITkDBlogin()
    client = dlg.get_client()
    if client is None:
        print("Could not connect to DB with provided credentials.")
        dlg.die()
        sys.exit()

    client.user_gui = dlg
    IS = ReceiveShipments(client)
    IS.set_accept_focus(True)
    IS.present()
    IS.connect("destroy", Gtk.main_quit)

    try:
        Gtk.main()

    except KeyboardInterrupt:
        print("Arrrgggg!!!")

    dlg.die()


if __name__ == "__main__":
    main()
