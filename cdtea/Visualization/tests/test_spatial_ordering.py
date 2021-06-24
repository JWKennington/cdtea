"""Tests for spatial ordering"""

from cdtea.Visualization import SpatialOrdering 
from cdtea.generate_flat import generate_flat_2d_space_time
class TestSpatialOrdering:
    """Tests for EquivDict class"""

    def test_one_layer_order(self):
        st = generate_flat_2d_space_time(space_size = 4, time_size = 4)
        
    def test_layer(self):
    	st = generate_flat_2d_space_time(space_size = 4, time_size = 4)
    	layer = SpatialOrdering.get_layer(st,t=1)
    	for v in layer:
    		time_index_of_v = st.simplex_meta[v]["t"]
    		assert time_index_of_v==1,f"{v} in layer had t={time_index_of_v}"
