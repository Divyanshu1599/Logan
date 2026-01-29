from commands.email_cmd import handle_email_command
from commands.system_cmd import handle_system_command
from commands.battery_cmd import handle_battery_command

TOOLS = {
    "send_email": {
        "description": "Send an email to a recipient",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Recipient email address"
                },
                "subject": {
                    "type": "string",
                    "description": "Subject of the email"
                },
                "message": {
                    "type": "string",
                    "description": "Email body"
                }
            },
            "required": ["to", "subject", "message"]
        },
        "handler": handle_email_command
    },

    "get_system_info": {
        "description": "Get CPU and RAM usage",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "handler": handle_system_command
    },

    "get_battery_status": {
        "description": "Get battery percentage and charging status",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "handler": handle_battery_command
    }
}
