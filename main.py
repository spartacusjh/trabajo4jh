from acitoolkit.acitoolkit import Credentials, Session
import sys
from acitoolkit.aciphysobject import Pod
import six


def print_inventory(item):
    """
    Display routine

    :param item: Object to print
    :return: None
    """
    for child in item.get_children():
        print_inventory(child)
    print(item.info())


def main():
    """
    Main execution routine

    :return: None
    """
    # Take login credentials from the command line if provided
    # Otherwise, take them from your environment variables
    description = ('Simple application that logs on to the APIC and displays'
                   ' the physical inventory.')
    creds = Credentials('apic', description)
    args = creds.get()

    # Login to APIC
    session = Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
        sys.exit(0)

    # Print the inventory of each Pod
    pods = Pod.get(session)
    for pod in pods:
        pod.populate_children(deep=True)
        pod_name = 'Pod: %s' % pod.name
        print(pod_name)
        print('=' * len(pod_name))
        print_inventory(pod)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
