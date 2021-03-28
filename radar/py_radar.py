import matplotlib.pyplot as plt

import pydarn

# read a non-compressed file
fitacf_file = r'D:\20210323.1800.00.cly.a.fitacf\20210323.1800.00.cly.a.fitacf'

# pyDARN functions to read a fitacf file
fitacf_data = pydarn.SuperDARNRead(fitacf_file).read_fitacf()

pydarn.RTP.plot_summary(fitacf_data, beam_num=2)
plt.show()
