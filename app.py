from QuadTree import QuadTree
import csv, argparse
from datetime import datetime

def main(file, number_of_layer):
    first  = QuadTree([[90.0,-180.0],[-90.0,180.0]], number_of_layer, 0)
    second = QuadTree([[90.0,-180.0],[-90.0,180.0]], number_of_layer, 1)
    third  = QuadTree([[90.0,-180.0],[-90.0,180.0]], number_of_layer, 2)
    fourth = QuadTree([[90.0,-180.0],[-90.0,180.0]], number_of_layer, 3)

    with open(file) as positions_file:
        for position in csv.DictReader(positions_file):
            process([first, second, third, fourth], position)

    print('8h/12h: \n{}'.format(first))
    print('12h/14h: \n{}'.format(second))
    print('14h/19h: \n{}'.format(third))
    print('19h/8h: \n{}'.format(fourth))

def process(quadtrees, position):
    if float(position['accuracy']) < 100.0:
        index = select_by_hour(datetime.fromtimestamp(int(position['timestamp'])/1000))
        qt = quadtrees[index]
        qt.add_position([float(position['lat']), float(position['lng'])])

def select_by_hour(date):
    hour = date.hour

    if hour >= 8 and hour < 12:
        return 0 # first
    if hour >= 12 and hour < 14:
        return 1 # second
    if hour >= 14 and hour < 19:
        return 2 # third

    return 3 # fourth

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file containing POIs to extract")
    parser.add_argument("--layer", help="number of layer", type=int, default=1)
    args = parser.parse_args()
    main(args.file, args.layer)