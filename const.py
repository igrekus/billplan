from PyQt5.QtCore import Qt

COLOR_PAYMENT_FINISHED = 0xff92D050
COLOR_PAYMENT_PENDING = 0xffFF6767

COLOR_PRIORITY_LOW = 0xffAABF00
COLOR_PRIORITY_MEDIUM = 0xffFFFF00
COLOR_PRIORITY_HIGH = 0xffFFA7A7

COLOR_ARRIVAL_PENDING = 0xffFF6767
COLOR_ARRIVAL_PARTIAL = 0xffFF9462
COLOR_ARRIVAL_RECLAIM = 0xffFF6767

RoleNodeId = Qt.UserRole + 1
RoleProject = Qt.UserRole + 2
RoleStatus = Qt.UserRole + 3
RolePriority = Qt.UserRole + 4
RoleShipment = Qt.UserRole + 5
RoleDate = Qt.UserRole + 6
RoleOrderId = Qt.UserRole + 7

LEVEL_USER = 1
LEVEL_JANITOR = 2
LEVEL_APPROVER = 3
