import json
import boto3
import datetime

licenses_pcodes = {'NetScaler VPX AWS MP Express': 'dd3t06r4cf8m5dxnjq7341ms6',
                   'NetScaler VPX AWS MP Standard Edition - 10 Mbps': '7x0sc2rlacl3ue0mc6sx4gpxa',
                   'NetScaler VPX AWS MP Enterprise Edition - 10 Mbps': '9gwd6wx07zoi4fa1hrw9r2j03',
                   'NetScaler VPX AWS MP Platinum Edition - 10 Mbps': 'x02avncoh3bqgjorf138yozz',
                   'NetScaler VPX AWS MP Standard Edition - 200 Mbps': 'd44dqi95o5e1eo9wnisjgoszr',
                   'NetScaler VPX AWS MP Enterprise Edition - 200 Mbps': 'f5jhck0pp9gfyuouof8enr4fw',
                   'NetScaler VPX AWS MP Platinum Edition - 200 Mbps': '9m9iz4peseekf061pr78846be',
                   'NetScaler VPX AWS MP Standard Edition - 1000 Mbps': '7rj9rmm05kihjjlsqkj6gni1x',
                   'NetScaler VPX AWS MP Enterprise Edition - 1000 Mbps': '4me4c3bsqvtl9mb82btr9ymzp',
                   'NetScaler VPX AWS MP Platinum Edition - 1000 Mbps': '1igr8r6hftwfcvfn7rveuz7xw',
                   'NetScaler VPX AWS MP Standard Edition - 3000 Mbps': '8egnp5pvfn0jbt6dnu0209akl',
                   'NetScaler VPX AWS MP Enterprise Edition - 3000 Mbps': '9umuukc118llnmofd3gkbwko1',
                   'NetScaler VPX AWS MP Platinum Edition - 3000 Mbps': 'bhmfw8b5z51g48gcb6jpvtrmg'}

regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
           'eu-west-1', 'eu-west-2', 'eu-central-1', 'ca-central-1',
           'ap-south-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2',
           'ap-northeast-1', 'sa-east-1']


def license_to_latest_ami(ec2_client, license):
    # ec2_client = boto3.client('ec2', region_name=region)
    product_code = licenses_pcodes[license]

    images = ec2_client.describe_images(Filters=[{'Name': 'product-code', 'Values': [product_code]}])
    sorted_images = sorted(images['Images'],
                           key=lambda i: datetime.datetime.strptime(i['CreationDate'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                           reverse=True)

    if len(sorted_images) > 0:
        return sorted_images[0]['ImageId']
    else:
        return None


def mappings():
    mapping = {}
    for region in regions:
        mapping[region] = {}
        ec2_client = boto3.client('ec2', region_name=region)
        for license in licenses_pcodes.keys():
            image_id = license_to_latest_ami(ec2_client, license)
            if image_id:
                mapping[region][license] = image_id
    print json.dumps(mapping)


def main():
    mappings()


if __name__ == '__main__':
    main()
