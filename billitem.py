import codecs
import const


class BillItem:
    # TODO make properties
    def __init__(self, id_=None, date=None, name=None, category=None, vendor=None, cost=None, project=None,
                 descript=None, shipment_time=None, status=None, priority=None, shipment_date=None,
                 shipment_status=None, payment_week=None, note=None):
        self.item_id = id_
        self.item_date = date
        self.item_name = name
        self.item_category = category
        self.item_vendor = vendor
        self.item_cost = cost
        self.item_project = project
        self.item_descript = descript
        self.item_shipment_time = shipment_time
        self.item_status = status
        self.item_priority = priority
        self.item_shipment_date = shipment_date
        self.item_shipment_status = shipment_status
        self.item_payment_week = payment_week
        self.item_note = note

    def __str__(self):
        return "BillItem(" + "id:" + str(self.item_id) + " " \
               + "date:" + str(self.item_date) + " " \
               + "name:" + str(self.item_name) + " " \
               + "cat:" + str(self.item_category) + " " \
               + "vend:" + str(self.item_vendor) + " " \
               + "cost:" + str(self.item_cost) + " " \
               + "proj:" + str(self.item_project) + " " \
               + "desc:" + str(self.item_descript) + " " \
               + "due:" + str(self.item_shipment_time) + " " \
               + "stat:" + str(self.item_status) + " " \
               + "prior:" + str(self.item_priority) + " " \
               + "ship date:" + str(self.item_shipment_date) + " " \
               + "ship stat:" + str(self.item_shipment_status) + " " \
               + "week:" + str(self.item_payment_week) + " " \
               + "note:" + str(self.item_note) + ")"

    @classmethod
    def fromRawList(cls, raw_list):
        if not raw_list:
            raise ValueError("Wrong war list.")

        return cls(id_=raw_list[0]
                   , date=raw_list[1]
                   , name=raw_list[2]
                   , category=raw_list[3]
                   , vendor=raw_list[4]
                   , cost=raw_list[5]
                   , project=raw_list[6]
                   , descript=raw_list[7]
                   , shipment_time=raw_list[8]
                   , status=raw_list[9]
                   , priority=raw_list[10]
                   , shipment_date="no date set"
                   , shipment_status=raw_list[11]
                   , payment_week=raw_list[12]
                   , note="empty note")

    @classmethod
    def fromSqliteTuple(cls, sqlite_tuple):
        return cls(id_=sqlite_tuple[0]
                   , date=sqlite_tuple[1]
                   , name=sqlite_tuple[2]
                   , category=sqlite_tuple[3]
                   , vendor=sqlite_tuple[4]
                   , cost=sqlite_tuple[5]
                   , project=sqlite_tuple[6]
                   , descript=sqlite_tuple[7]
                   , shipment_time=sqlite_tuple[8]
                   , status=sqlite_tuple[9]
                   , priority=sqlite_tuple[10]
                   , shipment_date=sqlite_tuple[11]
                   , shipment_status=sqlite_tuple[12]
                   , payment_week=sqlite_tuple[13]
                   , note=sqlite_tuple[14])


    @classmethod
    def fromQSqlRecord(cls, record):
        # if not record:
        #     raise ValueError("Wrong SQL record.")
        # return cls(id_=record.value(0)
        #            , date=record.value(1)
        #            , text=codecs.decode(record.value(2).replace("Р", "РЄ").encode("cp1251")).replace("Ъ", "И")
        #            , author=record.value(3)
        #            , approver=record.value(4)
        #            , is_active=record.value(5)
        #            , status=record.value(6)
        #            , is_dirty=False)
        pass
