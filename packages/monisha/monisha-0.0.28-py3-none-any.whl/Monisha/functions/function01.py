from ..scripts.en import Scripted
#======================================================================

def timend(elapsedti, timetocom):
    estimated = elapsedti + timetocom
    estimeing = Timemod(milles=estimated)
    finaltime = estimeing if estimeing != '' else "0 s"
    return finaltime

#======================================================================

def uptime(timetaken):
    hours, hourz = divmod(timetaken, 3600)
    minutes, seconds = divmod(hourz, 60)
    return round(hours), round(minutes), round(seconds)
  
#======================================================================

def Timemod(milles: int) -> str:
    second, milles = divmod(int(milles), 1000)
    minute, second = divmod(second, 60)
    hours, minute = divmod(minute, 60)
    days, hours = divmod(hours, 24)
    year, days = divmod(days, 365)
    mos  = ((str(year) + "𝚢𝚎𝚛, ") if year else Scripted.DATA01)
    mos += ((str(days) + "𝚍𝚊𝚢, ") if days else Scripted.DATA01)
    mos += ((str(hours) + "𝚑𝚛𝚜, ") if hours else Scripted.DATA01)
    mos += ((str(minute) + "𝚖𝚒𝚗, ") if minute else Scripted.DATA01)
    mos += ((str(second) + "𝚜𝚎𝚌  ") if second else Scripted.DATA04)
    return mos
  
#======================================================================
