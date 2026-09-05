import qrcode

meals = ["breakfast", "lunch", "dinner"]

for meal in meals:
    qr = qrcode.make(meal)   # ✅ FIXED
    qr.save(f"{meal}.png")

    print(f"{meal} QR generated")