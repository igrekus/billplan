import datetime


class OrderItem:
    # TODO make properties
    def __init__(self, id_=None, name=None, descript=None, qty=None, date_receive=None, priority=None, user=None,
                 approved=None, approved_by=None, cost=None, document=None, date=None):
        self.item_id = id_
        self.item_name = name
        self.item_descript = descript
        self.item_quantity = qty
        self.item_date_receive = date_receive
        self.item_priority = priority
        self.item_user = user
        self.item_approved = approved
        self.item_approved_by = approved_by
        self.item_cost = cost
        self.item_document = document
        self.item_date = date

    def __str__(self):
        return '{}(id={} name={} desc={} qty={} receive={} prior={} user={} appr={} by={} cost={} doc={} date={})'. \
            format(self.__class__
                   , self.item_id
                   , self.item_name
                   , self.item_descript
                   , self.item_quantity
                   , self.item_date_receive
                   , self.item_priority
                   , self.item_user
                   , self.item_approved
                   , self.item_approved_by
                   , self.item_cost
                   , self.item_document
                   , self.item_date)

    @classmethod
    def fromSqlTuple(cls, sql_tuple):
        return cls(id_=sql_tuple[0],
                   name=sql_tuple[1],
                   descript=sql_tuple[2],
                   qty=sql_tuple[3],
                   date_receive=sql_tuple[4],
                   priority=sql_tuple[5],
                   user=sql_tuple[6],
                   approved=sql_tuple[7],
                   approved_by=sql_tuple[8],
                   cost=sql_tuple[9],
                   document=sql_tuple[10],
                   date=sql_tuple[11])

    def toTuple(self):
        def formatDate(indate):
            if isinstance(indate, datetime.date):
                return indate.isoformat()
            return "2000-01-01"

        return tuple([self.item_name
                         , self.item_descript
                         , self.item_quantity
                         , formatDate(self.item_date_receive)
                         , self.item_priority
                         , self.item_user
                         , self.item_approved
                         , self.item_approved_by
                         , self.item_cost
                         , self.item_document
                         , self.item_id])

