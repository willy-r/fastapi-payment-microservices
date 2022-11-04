import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Products from "./components/Products";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Products />} />
      </Routes>
    </BrowserRouter>
  );
}
