import mitmproxy.http
from mitmproxy import ctx
import json

def websocket_message(flow: mitmproxy.http.HTTPFlow):
    # Access the WebSocket message (only the last one is easily accessible)
    message = flow.websocket.messages[-1]
    
    if b'"action":"optionFinished"' in message.content:
        data = message.content
        try:
            data = json.loads(message.content)

            for option in data["message"]["options"]:
                option["result_amount"] = 99  # Change to your desired value
                option["result_usd"] = 99  # Change to your desired value
                option['is_demo'] = 0

            modified_json_data = json.dumps(data, indent=4)
            message.content = modified_json_data.encode("utf-8")

            data1 = {"action":"buyOption","message":{"type":"call","amount":0,"assetid":245,"strike_time":1709521421,"expiration_time":1709521430,"is_demo":0,"rateIndex":1},"token":"76782ad35d33d99cb0ed7bc948919dd8","ns":20}
             # Encode as JSON
            json_data = json.dumps(data1).encode("utf-8")

            # Send the new message to the client 
            ctx.master.commands.call("inject.websocket", flow, False, json_data, False)  

        except ValueError:
            # Handle cases where the message content is not valid JSON
            ctx.log.info("Message content is not valid JSON")


        ctx.log.info(f"Modified client message: {modified_json_data}")
    if b'"action":"profile"' in message.content:

        try:
            data = json.loads(message.content)

            if data["action"] == "profile":
                profile = data["message"]["profile"]
                amount_to_add = 100
                profile["real_balance"] += amount_to_add
                profile["bonus_balance"] += amount_to_add
                ctx.log.info(f"Increased real_balance by {amount_to_add}. New value: {profile['real_balance']}")

            modified_json_data = json.dumps(data, indent=4)
            message.content = modified_json_data.encode("utf-8")

        except ValueError:
            # Handle cases where the message content is not valid JSON
            ctx.log.info("Message content is not valid JSON")
    if b'ERROR_BALANCE_TOO_SMALL' in message.content:
        try:
            data = json.loads(message.content)

            if data["action"] == "error" and data["message"] == "ERROR_BALANCE_TOO_SMALL":
                original_ns = data["ns"]

                # Modify the original data
                data["action"] = "buyOption"
                data["message"] = {}
                data["ns"] = original_ns  # Assign the extracted ns

                modified_json_data = json.dumps(data, indent=4).encode("utf-8")
                
                # Construct the message to send
                message_to_send = {
                    "action": "buySuccessful",
                    "message": {
                        "option": {
                            "ts": "2024-03-04 02:45:45",
                            "user_id": 798789067,
                            "is_demo": 0,
                            "asset_id": 245,
                            "type": 0,
                            "amount": 1,
                            "currency_id": 0,
                            "strike_time": 1709520344.5,
                            "strike_rate": 1.08739,
                            "exp_time": 1709520350,
                            "exp_rate": 0,
                            "profit": 83,
                            "refund": 1,
                            "status": 0,
                            "bonus_amount_percent": 90,
                            "res_shown": 1,
                            "result_amount": 2,
                            "ip": "",
                            "country": "CL",
                            "id": 3124500592
                        }
                    }
                }

                # Encode as JSON
                json_data = json.dumps(message_to_send).encode("utf-8")

                message.content = json_data

                ctx.log.info("Modified original 'error' message")

        except ValueError:
            ctx.log.info("Message content is not valid JSON")
        
    if b'{"action":"buyOption","message":{"type":"call"' in message.content:
        try:
            data = json.loads(message.content)

            if data["action"] == "buyOption":
                data["message"]["is_demo"] = 1
                data["message"]["amount"] = 1

                ctx.log.info("Modified 'buyOption' message: set 'is_demo' to 0 and 'amount' to 0")

                modified_json_data = json.dumps(data, indent=4)
                message.content = modified_json_data.encode("utf-8")

        except ValueError:
            ctx.log.info("Message content is not valid JSON")
    if b'{"action":"buyOption","message":{"type":"put"' in message.content:
        try:
            data = json.loads(message.content)

            if data["action"] == "buyOption":
                data["message"]["is_demo"] = 0
                data["message"]["amount"] = 1

                ctx.log.info("Modified 'buyOption' message: set 'is_demo' to 0 and 'amount' to 0")

                modified_json_data = json.dumps(data, indent=4)
                message.content = modified_json_data.encode("utf-8")

        except ValueError:
            ctx.log.info("Message content is not valid JSON")





# You can add other mitmproxy addon functions as needed,  
# e.g., request, response, etc.  
