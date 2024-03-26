from barbarika.citrixadc import CitrixADC

NSIP = "10.10.10.10"
DEFAULT_PASSWORD = "instance-id"
NEW_PASSWORD = "newpassword"

adc = CitrixADC(nsip=NSIP, nsuser="nsroot", default_password=DEFAULT_PASSWORD, new_password=NEW_PASSWORD,)

print(adc.get_nsip())
