from lasso.dyna import D3plot, ArrayType, FilterType
import numpy as np

# d3plot = D3plot('d3plot', state_array_filter=["node_displacement"])
d3plot = D3plot('d3plot')
part_ids = [10101]
mask = d3plot.get_part_filter(FilterType.SHELL, part_ids)
shell_stress = d3plot.arrays[ArrayType.element_shell_stress]
print(shell_stress)
np.save('shell_stress.txt', shell_stress)
shell_id = d3plot.arrays[ArrayType.element_shell_ids]
print(d3plot)