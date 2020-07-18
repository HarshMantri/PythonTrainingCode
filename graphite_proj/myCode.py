import requests
import argparse
import sys

server = "https://play.grafana.org/api/datasources/proxy/1/"

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help = "graphite server port no", default="80")
parser.add_argument("-t", "--target", help = "metric target", default="aliasByNode(movingAverage(scaleToSeconds(apps.fakesite.*.counters.requests.count,%201),%202),%202)")
parser.add_argument("-wt", help = "warning threshold")
parser.add_argument("-ct", help = "critical threshold")
parser.add_argument("--format", help = "format expected from server", default="json")
parser.add_argument("--time", help = "amount of time for which data to be fetched", default="5min")
args = parser.parse_args()


class ErrorCode():
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

def main():
    try:
        serv_ret = requests.get(server+f"render?target={args.target}&format={args.format}&from=-{args.time}")
    except Exception as e:
        print("Error connecting to server!")
        print(e)
        sys.exit(ErrorCode.UNKNOWN)

    data = serv_ret.json()

    if not data:
        print("No data returned!")
        sys.exit(ErrorCode.UNKNOWN)

    try:
        assert(args.ct >= args.wt)
    except:
        print("Critical threshold can't be lesser than warning threshold!")
        sys.exit(ErrorCode.UNKNOWN)

    for sub_data in data:
        for point in sub_data['datapoints']:
            print(point)
        
            if point[0] >= float(args.ct):
                print("CRITICAL!")
                sys.exit(ErrorCode.CRITICAL)
            elif point[0] >= float(args.wt):
                print("WARNING!")
                sys.exit(ErrorCode.WARNING)
    sys.exit(ErrorCode.OK)


if __name__ == '__main__':
    main()
