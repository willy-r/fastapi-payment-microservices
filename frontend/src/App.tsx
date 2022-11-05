import { BrowserRouter, Routes, Route } from "react-router-dom";

import Products from "./components/Products";
import ProductsCreate from "./components/ProductsCreate";

export default function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Products />} />
          <Route path="/create-product" element={<ProductsCreate />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}
