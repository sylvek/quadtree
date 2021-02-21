from QuadTree import QuadTree
import csv, argparse, time

def main(file, number_of_layer):
    print("initializing...")
    t1 = time.time()
    qt = QuadTree([[90.0,-180.0],[-90.0,180.0]], number_of_layer, '00')
    print("QuadTree initialized in {} s".format(time.time() - t1))

    with open(file) as positions_file:
        for position in csv.DictReader(positions_file):
            process(qt, position)

def process(qt, position):
    if float(position['accuracy']) < 100.0:
        qt.add_position([float(position['lat']), float(position['lng'])])
        print('{}\n{}'.format(position, qt))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file containing POIs to extract")
    parser.add_argument("--layer", help="number of layer", type=int, default=1)
    args = parser.parse_args()
    main(args.file, args.layer)