from Context import Point
def get_tile_neighborhood(location : Point, radius, max_width, max_height):
    pts =  lambda x, y : [Point(x2, y2) for x2 in range(x-radius, x+radius+1)
                            for y2 in range(y-radius, y+radius+1)
                            if (-1 < x <= max_width and
                                -1 < y <= max_height and
                                (x != x2 or y != y2) and
                                (0 <= x2 <= max_width) and
                                (0 <= y2 <= max_height))]
    return pts(location.x, location.y)

def get_tile_radius_outer_ring(location : Point, radius, max_width, max_height):
    horizontal =  lambda x, y : [Point(x2, y2) for x2 in (x-radius, x+radius)
                            for y2 in range(y-radius, y+radius+1)
                            if (0 <= x < max_width and
                                0 <= y < max_height and
                                (x != x2 or y != y2) and
                                (0 <= x2 < max_width) and
                                (0 <= y2 < max_height))]
                            
    vertical =  lambda x, y : [Point(x2, y2) for x2 in range(x-radius, x+radius+1)
                        for y2 in (y-radius, y+radius)
                        if (0 <= x < max_width and
                            0 <= y < max_height and
                            (x != x2 or y != y2) and
                            (0 <= x2 < max_width) and
                            (0 <= y2 < max_height))]
    
    return set(horizontal(location.x, location.y) + vertical(location.x, location.y))
