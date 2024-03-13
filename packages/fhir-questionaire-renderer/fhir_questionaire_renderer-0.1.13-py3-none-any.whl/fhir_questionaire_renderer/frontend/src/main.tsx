import { createRoot } from "react-dom/client";
import FHIRQuestionaireRenderer from "./FHIRQuestionaireRenderer";

const container = document.getElementById("root");
const root = createRoot(container!);
root.render(<FHIRQuestionaireRenderer />);
