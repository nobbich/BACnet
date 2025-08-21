import random
import time
import BAC0

# ====== Konfiguration ======
# LAN-IP des Rechners, über die N3uron erreichbar ist
LAN_IP = "192.168.1.100"  # anpassen
SUBNET = "24"

DEVICE_NAME = "TestDevice"
DEVICE_ID = 1234

# ====== BACnet starten ======
bacnet = BAC0.lite(ip=f"{LAN_IP}/{SUBNET}")

# Device erstellen
device = BAC0.device(name=DEVICE_NAME, device_id=DEVICE_ID, address=LAN_IP)

# Objekte hinzufügen
analog = device.add_object("analogInput", instance=1, properties={"presentValue": 0.0})
binary = device.add_object("binaryInput", instance=1, properties={"presentValue": "inactive"})
status = device.add_object("multiStateInput", instance=1, properties={"presentValue": 1})

print(f"{DEVICE_NAME} läuft auf {LAN_IP} und liefert zufällige Werte:")

try:
    while True:
        # Zufallswerte generieren
        analog.properties["presentValue"] = round(random.uniform(0, 100), 2)
        binary.properties["presentValue"] = random.choice(["active", "inactive"])
        status.properties["presentValue"] = random.randint(1, 5)

        print(f"Analog={analog.properties['presentValue']}  "
              f"Digital={binary.properties['presentValue']}  "
              f"Status={status.properties['presentValue']}")

        time.sleep(5)

except KeyboardInterrupt:
    print("Beende Testdevice...")
    bacnet.close()
