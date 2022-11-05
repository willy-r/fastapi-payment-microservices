import { BrowserRouter, Routes, Route } from "react-router-dom";
import Checkout from "./components/Checkout";
import Products from "./components/Products";
import ProductsCreate from "./components/ProductsCreate";

export default function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Products />} />
          <Route path="/create-product" element={<ProductsCreate />} />
          <Route path="/checkout-product" element={<Checkout />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}
