class Cell:
    def __init__(self, latlng_bounding_box, *name):
        self.__check_bounding_box(latlng_bounding_box)
        self.__latlng_bounding_box = latlng_bounding_box
        self.__name = name
        self.count = 0

    def __check_latlng(_, *element):
        for e in element:
            if not isinstance(e, float):
                raise ValueError("position have to be a float boxed on a [lat,lng]")

    def __check_bounding_box(self, element):
        if isinstance(element, list) and len(element) == 2:
            for e in element:
                self.__check_bounding_box(e)
        else:
            self.__check_latlng(element)

    def _increment(self):
        self.count += 1

    def name(self):
        name = 0
        for element in list(self.__flatten(self.__name)):
            name = (name << 2) | int(element)
        return '{}'.format(bin(name))

    def __flatten(self, object):
        for item in object:
            if isinstance(item, (list, tuple, set)):
                yield from self.__flatten(item)
            else:
                yield item

    def __str__(self):
        name = self.name()
        return "{}|{}-{} -> {}".format(name, int(name, 2), self.__latlng_bounding_box, self.count)

class QuadTree:
    
    def __init__(self, latlng_bounding_box, layer_level, *name):
        if layer_level < 1:
            raise ValueError("number_if_layer must be greater than 0")
    
        self.__latlng_bounding_box = latlng_bounding_box
        self.__layer_level = layer_level
        self.__name = name

        if layer_level == 1:
            self.element = Cell(latlng_bounding_box, name)
        else:
            self.element = None

    def __split_in_four_bounding_box(self):
        lat_nw = self.__latlng_bounding_box[0][0]
        lng_nw = self.__latlng_bounding_box[0][1]
        lat_se = self.__latlng_bounding_box[1][0]
        lng_se = self.__latlng_bounding_box[1][1]

        return [
                QuadTree([ [lat_nw, lng_nw], [(lat_nw + lat_se) / 2, (lng_nw + lng_se) / 2] ], self.__layer_level - 1, self.__name, 0),
                QuadTree([ [lat_nw, (lng_nw + lng_se) / 2], [(lat_nw + lat_se) / 2, lng_se] ], self.__layer_level - 1, self.__name, 1),
                QuadTree([ [(lat_nw + lat_se) / 2, lng_nw], [lat_se, (lng_nw + lng_se) / 2] ], self.__layer_level - 1, self.__name, 2),
                QuadTree([ [(lat_nw + lat_se) / 2, (lng_nw + lng_se) / 2], [lat_se, lng_se] ], self.__layer_level - 1, self.__name, 3)
            ]
    
    def __iscontain(self, latlng):
        box = self.__latlng_bounding_box
        return box[0][0] >= latlng[0] >= box[1][0] and box[0][1] <= latlng[1] <= box[1][1]

    def add_position(self, latlng):
        if self.__iscontain(latlng):
            if isinstance(self.element, Cell):
                self.element._increment()
            else:
                if not self.element:
                    self.element = self.__split_in_four_bounding_box()
                for e in self.element:
                    e.add_position(latlng)

    def __str__(self):
        if isinstance(self.element, Cell):
            if self.element.count > 0:
                return '{}\n'.format(str(self.element))
            else:
                return ''
        elif isinstance(self.element, list):
            string = ''
            for e in self.element:
                string += str(e)
            return string
        else:
            return ''
