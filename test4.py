from ExpertOptionAPI2.expert import EoApi as Expert
import time

uids = [
    499535683,
    585373418,
    585373418,
    900499604,
    900499604,
    158932095,
    548481935
]

expert = Expert(token="76782ad35d33d99cb0ed7bc948919dd8", server_region="wss://fr24g1eu.expertoption.com/ws/v34?app_os=win&app_source=web&app_type=web&app_version=15.4.3&app_build_number=7043&app_brand=expertoption&app_device_info=")

expert.connect()

data = expert.GetSocialTradingInfo()
data2 = expert.GetTopTraders()

print(data)
print(data2)