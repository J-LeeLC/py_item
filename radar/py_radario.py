import pydarnio

# read a non-compressed file
fitacf_file = r'D:\20210323.1800.00.cly.a.fitacf\20210323.1800.00.cly.a.fitacf'

# pyDARNio functions to read a fitacf file
reader = pydarnio.SDarnRead(fitacf_file)
records = reader.read_fitacf()