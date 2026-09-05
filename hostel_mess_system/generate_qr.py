import qrcode
import json

meals = ["breakfast", "lunch", "dinner"]

for meal in meals:
    data = json.dumps({"meal": meal})

    qr = qrcode.make(data)
    qr.save(f"{meal}.png")

    print(f"{meal} QR generated")