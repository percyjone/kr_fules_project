import json
import streamlit as st
import paho.mqtt.client as mqtt

st.set_page_config(
    page_title="IoT MQTT Publisher",
    page_icon="📡",
    layout="centered"
)

st.title("📡 IoT MQTT Publisher")
st.write("Upload a JSON file and publish its contents to your Mosquitto MQTT broker.")

st.divider()

st.subheader("MQTT Connection")

broker = st.text_input(
    "Broker address",
    value="localhost",
    help="Use localhost if Mosquitto is running on this computer. For another computer, enter its IP address."
)

port = st.number_input(
    "Broker port",
    min_value=1,
    max_value=65535,
    value=1883
)

topic = st.text_input(
    "MQTT Topic",
    value="water/tank"
)

st.divider()

st.subheader("Upload JSON")

uploaded_file = st.file_uploader(
    "Choose a JSON file",
    type=["json"]
)

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.getvalue()
        json_text = file_bytes.decode("utf-8")
        data = json.loads(json_text)

        st.success("Valid JSON file")
        st.write("JSON data:")
        st.json(data)

        if st.button("🚀 Publish to MQTT", type="primary"):
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

            try:
                client.connect(broker, int(port), 60)
                client.loop_start()

                result = client.publish(
                    topic,
                    json_text,
                    qos=0
                )

                result.wait_for_publish()

                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    st.success(
                        f"Published successfully to `{topic}` "
                        f"at `{broker}:{port}`"
                    )
                else:
                    st.error(f"MQTT publish failed. Error code: {result.rc}")

            except Exception as e:
                st.error(f"Could not connect/publish: {e}")

            finally:
                try:
                    client.loop_stop()
                    client.disconnect()
                except Exception:
                    pass

    except UnicodeDecodeError:
        st.error("The file is not a valid UTF-8 text file.")

    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON: {e}")

else:
    st.info("Upload a .json file to continue.")

st.divider()

st.caption("Example JSON:")
st.code(
    """{
    "outlet_code": "OUT001",
    "tank_id": 1,
    "temperature": 28.5,
    "volume": 75.0,
    "height": 32.5
}""",
    language="json"
)
