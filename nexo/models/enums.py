from enum import Enum


class BoardType(str, Enum):
    OPEN = "O"
    PRIVATE = "P"


class BlockType(str, Enum):
    BOARD = "board"
    CARD = "card"
    VIEW = "view"
    COMMENT = "comment"
    ATTACHMENT = "attachment"
    TEXT = "text"
    IMAGE = "image"
    DIVIDER = "divider"
    CHECKBOX = "checkbox"
    HEADING1 = "heading1"
    HEADING2 = "heading2"
    HEADING3 = "heading3"
    VIDEO = "video"
    QUOTE = "quote"
    LIST_ITEM = "listItem"
    UNKNOWN = "unknown"


class ContentBlockType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    DIVIDER = "divider"
    CHECKBOX = "checkbox"
    HEADING1 = "heading1"
    HEADING2 = "heading2"
    HEADING3 = "heading3"
    LIST_ITEM = "listItem"
    ATTACHMENT = "attachment"
    QUOTE = "quote"
    VIDEO = "video"


class MemberRole(str, Enum):
    NONE = ""
    VIEWER = "viewer"
    COMMENTEUR = "commenter"
    EDITOR = "editor"
    ADMIN = "admin"


class CategoryType(str, Enum):
    SYSTEM = "system"
    CUSTOM = "custom"


class SubscriberType(str, Enum):
    USER = "user"
    CHANNEL = "channel"


class PropertyType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multiSelect"
    DATE = "date"
    PERSON = "person"
    CHECKBOX = "checkbox"
    URL = "url"
    EMAIL = "email"
    PHONE = "phone"
    CREATED_TIME = "createdTime"
    CREATED_BY = "createdBy"
    UPDATED_TIME = "updatedTime"
    UPDATED_BY = "updatedBy"
    FILE = "file"
    VIDEO = "video"
    IMAGE = "image"
    BOOL = "bool"


class FilterCondition(str, Enum):
    INCLUDES = "includes"
    NOT_INCLUDES = "notIncludes"
    IS_EMPTY = "isEmpty"
    IS_NOT_EMPTY = "isNotEmpty"
    IS_SET = "isSet"
    IS_NOT_SET = "isNotSet"
    IS = "is"
    CONTAINS = "contains"
    NOT_CONTAINS = "notContains"
    STARTS_WITH = "startsWith"
    NOT_STARTS_WITH = "notStartsWith"
    ENDS_WITH = "endsWith"
    NOT_ENDS_WITH = "notEndsWith"
    IS_BEFORE = "isBefore"
    IS_AFTER = "isAfter"


class IViewType(str, Enum):
    BOARD = "board"
    TABLE = "table"
    GALLERY = "gallery"
    CALENDAR = "calendar"
