import const
import codecs
import datetime


class BillItem:
    # TODO make properties
    def __init__(self, id_=None, date=None, name=None, category=None, vendor=None, cost=None, project=None,
                 descript=None, shipment_time=None, status=None, priority=None, shipment_date=None,
                 shipment_status=None, payment_week=None, note=None, doc=None, order=None):
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
        self.item_doc = doc
        self.item_order = order

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
               + "note:" + str(self.item_note) + " " \
               + "doc:" + str(self.item_doc) + " " \
               + "order:" + str(self.item_order) + ")"

    @classmethod
    def fromSqlTuple(cls, sql_tuple):
        return cls(id_=sql_tuple[0]
                   , date=sql_tuple[1]
                   , name=sql_tuple[2]
                   , category=sql_tuple[3]
                   , vendor=sql_tuple[4]
                   , cost=sql_tuple[5]
                   , project=sql_tuple[6]
                   , descript=sql_tuple[7]
                   , shipment_time=sql_tuple[8]
                   , status=sql_tuple[9]
                   , priority=sql_tuple[10]
                   , shipment_date=sql_tuple[11]
                   , shipment_status=sql_tuple[12]
                   # sqlite_tuple[13] - not used
                   , note=sql_tuple[14]
                   , payment_week=sql_tuple[15]
                   , doc=sql_tuple[17]
                   , order=sql_tuple[18])


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

    def toTuple(self):
        def formatDate(indate):
            if isinstance(indate, datetime.date):
                return indate.isoformat()
            return "01.01.2000"

        return tuple([self.item_date,
                      self.item_name,
                      self.item_category,
                      self.item_vendor,
                      self.item_cost,
                      self.item_project,
                      self.item_descript,
                      self.item_shipment_time,
                      self.item_status,
                      self.item_priority,
                      self.item_shipment_date,
                      self.item_shipment_status,
                      self.item_payment_week,
                      self.item_note,
                      self.item_doc,
                      self.item_order,
                      self.item_id])

    @classmethod
    def itemListRequestString(self):
        return str("CALL getBillList()")
