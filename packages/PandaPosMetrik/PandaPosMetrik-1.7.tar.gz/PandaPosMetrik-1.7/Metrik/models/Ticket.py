import datetime

from Metrik.models.ORMModel import Model


class Orders(Model):
    Id: int
    TicketId: int
    WarehouseId: int
    DepartmentId: int
    TerminalId: int
    MenuItemId: int
    MenuItemName: str
    PortionName: str
    Price: float
    Quantity: float
    PortionCount: int
    Locked: bool
    CalculatePrice: bool
    DecreaseInventory: bool
    IncreaseInventory: bool
    OrderNumber: int
    CreatingUserName: str
    CreatedDateTime: datetime
    LastUpdateTime: datetime
    AccountTransactionTypeId: int
    ProductTimerValueId: int
    GroupTagName: str
    GroupTagFormat: str
    Separator: str
    PriceTag: str
    Tag: str
    DisablePortionSelection: bool
    OrderUid: str
    Taxes: str
    OrderTags: str
    OrderStates: str
    

class Tickets(Model):
    Id: int
    LastUpdateTime: datetime.datetime
    TicketVersion: datetime.datetime
    TicketUid: str
    TicketNumber: str
    Date: datetime.datetime
    LastOrderDate: datetime.datetime
    LastPaymentDate: datetime.datetime
    PreOrder: bool
    IsClosed: bool
    IsLocked: bool
    RemainingAmount: float
    TotalAmount: float
    DepartmentId: int
    TerminalId: int
    TicketTypeId: int
    Note: str
    LastModifiedUserName: str
    TicketTags: str
    TicketStates: str
    TicketLogs: str
    LineSeparators: str
    ExchangeRate: float
    TaxIncluded: bool
    Name: str
    TransactionDocument_Id: int
    IsOpened: bool
    TotalAmountPreTax: float
    orders: list[Orders]
    
