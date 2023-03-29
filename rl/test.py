from getlimit import get_limits
from cpumemory import metricsCpu
print(get_limits(),metricsCpu())
cpu= get_limits()[0]
memory=get_limits()[1]
cpuact=metricsCpu()[0]
memact=metricsCpu()[1]
print('Percent ut ', cpuact/cpu *100, memact/memory*100)
