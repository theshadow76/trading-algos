import mitmproxy.http
from mitmproxy import ctx
import json
from ExpertOptionAPI2.expert import EoApi as Expert

expert = Expert(token="76782ad35d33d99cb0ed7bc948919dd8", server_region="wss://fr24g1eu.expertoption.com/ws/v34?app_os=win&app_source=web&app_type=web&app_version=15.4.3&app_build_number=7043&app_brand=expertoption&app_device_info=")

expert.connect()

def find_matching_trades(data_list, trade_data):
    target_user_id = trade_data["message"]["options"][0]["user_id"] 
    matching_trades = []

    for sublist in data_list:
        for trade_id in sublist:
            if trade_id == target_user_id:
                matching_trades.append(trade_id)
                break  # Stop checking this sublist if a match is found

    return matching_trades

with open("uids.json", "r") as f:
    user_id_list = json.load(f)

def process_data(data):
    user_ids_with_profit = []

    open_options = data.get("message", {}).get("openOptions", [])
    for option in open_options:
        traders = option.get("traders", [])
        for trader in traders:
            user_ids_with_profit.append(trader["userId"])

    return user_ids_with_profit

def websocket_message(flow: mitmproxy.http.HTTPFlow):
    # Access the WebSocket message (only the last one is easily accessible)
    message = flow.websocket.messages[-1]

    if b'"action":"expertOption"' in message.content:
        # Find matching trades
        matching_trades = find_matching_trades(user_id_list, message.content)

        if matching_trades:
            print(f"Matching user IDs found: {matching_trades}")
            expert.Buy(amount=10, type="put", assetid="245")
        else:
            print("No matching user IDs found")
    
    
