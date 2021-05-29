#from ../simplicial import Dim0SimplexKey

def spatial_ordering(st,layer:list):
    """
    """
    origin = layer[0]
    boundry = origin
    not_indexed = set(layer)-{origin}
    index = {origin:0}
    for i in range(len(layer)):
        for f in not_indexed:
            if (f|boundry) in st.simplices[1]:
                
                not_indexed-={f}
                index[f] = index[boundry]+1
                boundry = f
                break
    return(index)
