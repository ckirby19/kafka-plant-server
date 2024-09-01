import { useEffect, useState } from 'react';
import mqtt from 'mqtt'// const mqtt = require("mqtt");
import { DataDisplay } from './components/DataDisplay';
import { Data } from './model';

export const App = () => {
  const [subData, setSubData] = useState<Record<string, Data[]>>({})

  const updateSubData = (topic: string, data: number) => {
    const update = { SensorId: topic, Value: data, Timestamp: Date.now()} as Data
    setSubData((prev) => ({ ...prev, [update.SensorId]: [...(prev[update.SensorId] ?? []), update] }))
  }

  useEffect(() => {
      const client = mqtt.connect("ws://192.168.0.101:9001");

      client.on("connect", () => {
          console.log("Connected to MQTT broker");
          client.subscribe("moistureData", (err) => {
              if (err) {
                  console.error("Subscription error:", err);
              }
          });
      });

      client.on("message", (topic, message) => {
          if (topic === "moistureData") {
              const moistureValue = parseFloat(
                  message.toString().replace("%", "")
              );
              updateSubData(topic, moistureValue);
          }
      });

      // Clean up on unmount
      return () => {
          client.end();
      };
  }, []);

  return (
    <DataDisplay Data={subData} />
  );
}

export default App;
