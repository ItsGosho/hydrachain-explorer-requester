import enum


class AddressBalanceCategory(enum.Enum):
    NO_CATEGORY = ''
    TOTAL_RECEIVED = 'total-received'
    TOTAL_SENT = 'total-sent'
    UNCONFIRMED = 'unconfirmed'
    STAKING = 'staking'
    MATURE = 'mature'
