import enum

class JenisReminder(enum.Enum):
    SMS = 'SMS'
    EMAIL = 'EMAIL'
    PUSH = 'PUSH'

class TipeFaskes(enum.Enum):
    RSU = 'RSU'
    RSIA = 'RSIA'
    PUSKESMAS = 'PUSKESMAS'
    KLINIK = 'KLINIK'

class StatusAntrian(enum.Enum):
    MENUNGGU = 'MENUNGGU'
    DILAYANI = 'DILAYANI'
    BATAL = 'BATAL'