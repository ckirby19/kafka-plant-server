import { useState } from 'react';
// import WebSocket from 'ws';
import { Data } from './model';
import { DataDisplay } from './components/DataDisplay';

export const App = () => {
  const [subData, setSubData] = useState<Record<string, Data[]>>({})

  const updateSubData = (data: number) => {
    const update = { SensorId: "Sensor1", Value: data, Timestamp: Date.now()} as Data
    setSubData((prev) => ({ ...prev, [update.SensorId]: [...(prev[update.SensorId] ?? []), update] }))
  }
  const WEBSOCKET_URL = "ws://localhost:8765";

  // Create a WebSocket connection
  const socket = new WebSocket(WEBSOCKET_URL);

  // Connection opened
  socket.addEventListener("open", () => {
    console.log('Connected to WebSocket server');
  });

  socket.addEventListener("message", (data) => {
    console.log('Message from server:', data.toString());
    updateSubData(parseFloat(data.toString().replace("%","")))
  })

  socket.addEventListener("error", (error) => {
    console.error(`WebSocket error: ${error}`);
  })

  socket.addEventListener("close", (reason) => {
    console.log(`WebSocket connection closed: ${reason}`);
  })

  return (
    <DataDisplay Data={subData} />
  );
}

export default App;
