from datetime import datetime

from core.storage import (
    load_attacks,
    save_attacks
)

def create_attack(
    source_ip,
    country,
    device,
    attack_type,
    risk="Medium",
    status="Open"
):

    attacks = load_attacks()

    attack = {
        "id": f"ATT-{len(attacks)+1}",
        "time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "ip": source_ip,         
        "country": country,
        "target": device,        
        "attack_type": attack_type,
        "risk": risk,
        "status": status
    }

    attacks.append(
        attack
    )

    save_attacks(
        attacks
    )

    return attack