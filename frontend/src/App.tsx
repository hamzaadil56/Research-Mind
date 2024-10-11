import { useState } from "react";

import "./App.css";
import ResearchAIDashboard from "./components/ResearchDashboard";

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="App">
      <ResearchAIDashboard />
    </div>
  );
}

export default App;
