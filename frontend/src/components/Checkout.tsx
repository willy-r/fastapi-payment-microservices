import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import Wrapper from "./Wrapper"

export default function Checkout() {
  const [id, setId] = useState("");
  const [quantity, setQuantity] = useState(0);
  const [message, setMessage] = useState("Buy your favorite product");

  useEffect(() => {
    (async () => {
      try {
        if (id) {
          const r = await fetch(`${import.meta.env.VITE_INVENTORY_API_URL}/api/products/${id}`);
          const data = await r.json();
          const realPrice = (parseFloat(data.price) * 1.2).toFixed(2)
          setMessage(`Your product price is $${realPrice}`);
        }
      } catch (_) {
        setMessage("Buy your favorite product");
      }
    })();
  }, [id]);

  const submitForm = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await toast.promise(
      fetch(`${import.meta.env.VITE_PAYMENT_API_URL}/api/orders`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          product_id: id,
          quantity,
        }),
      }),
      {
        pending: "Ordering payment...",
        success: "Your payment was received! You will receive an email with more informations about it",
        error: "Unexpected error occurred, please try again..."
      }
    );
  }

  return (
    <Wrapper>
      <div className="container">
        <main>
          <div className="py-5 text-center">
            <h2>Checkout form</h2>
            <p className="lead">{message}</p>
          </div>

          <form onSubmit={submitForm}>
            <div className="row g-3">
              <div className="col-sm-6">
                <label className="form-label" htmlFor="id">Product</label>
                <input id="id" className="form-control" type="text" required
                  onChange={(event) => setId(event.target.value)}
                />
              </div>

              <div className="col-sm-6">
                <label className="form-label" htmlFor="quantity">Quantity</label>
                <input id="quantity" className="form-control" type="text" required
                  onChange={(event) => setQuantity(parseInt(event.target.value))}
                />
              </div>
            </div>
            <hr className="my-4" />
            <button className="w-100 btn btn-secondary btn-lg" type="submit">Buy</button>
          </form>
        </main>
      </div>
    </Wrapper>
  );
}
