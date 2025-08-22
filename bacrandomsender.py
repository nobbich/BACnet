import asyncio
import random
import BAC0

LAN_IP = "192.168.110.107"   # oder "localhost"
SUBNET = "24"

DEVICE_ID = 1234
DEVICE_NAME = "TestDevice"

NUM_ANALOG = 3
NUM_BINARY = 2
NUM_STATUS = 2
UPDATE_INTERVAL = 5  # Sekunden

async def main():
    # BACnet-Lite starten
    bacnet = BAC0.lite(ip=f"{LAN_IP}/{SUBNET}")

    # Device erstellen → network angeben
    device = await BAC0.device(
        device_id=DEVICE_ID,
        address=LAN_IP,
        network=bacnet  # Netzwerk muss hier übergeben werden
    )
    device.name = DEVICE_NAME

    # Objekte erzeugen
    analog_objects = [
        await device.add_object(
            object_type="analogInput",
            instance=i+1,
            properties={"presentValue": 0.0, "description": f"Analog Input {i+1}", "units": "percent"}
        )
        for i in range(NUM_ANALOG)
    ]

    binary_objects = [
        await device.add_object(
            object_type="binaryInput",
            instance=i+1,
            properties={"presentValue": "inactive", "description": f"Binary Input {i+1}"}
        )
        for i in range(NUM_BINARY)
    ]

    status_objects = [
        await device.add_object(
            object_type="multiStateInput",
            instance=i+1,
            properties={"presentValue": 1, "description": f"Status Input {i+1}"}
        )
        for i in range(NUM_STATUS)
    ]

    print(f"{DEVICE_NAME} läuft auf {LAN_IP} und liefert zufällige Werte:")

    try:
        while True:
            for obj in analog_objects:
                obj.properties["presentValue"] = round(random.uniform(0, 100), 2)
            for obj in binary_objects:
                obj.properties["presentValue"] = random.choice(["active", "inactive"])
            for obj in status_objects:
                obj.properties["presentValue"] = random.randint(1, 5)

            analog_vals = ", ".join(str(obj.properties["presentValue"]) for obj in analog_objects)
            binary_vals = ", ".join(obj.properties["presentValue"] for obj in binary_objects)
            status_vals = ", ".join(str(obj.properties["presentValue"]) for obj in status_objects)

            print(f"Analog=[{analog_vals}]  Binary=[{binary_vals}]  Status=[{status_vals}]")
            await asyncio.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        print("Beende Testdevice...")
        bacnet.close()

asyncio.run(main())
