from time import sleep

from main import redis, Product
from exceptions import ProductNotAvailableException

key = "order_completed"
group = "inventory_group"


def create_stream_group(key: str, group: str) -> None:
    try:
        redis.xgroup_create(key, group)
    except Exception:
        print(f"Group {group} already exists")


def consume(group: str, key: str, interval_sec: int = 1) -> None:
    while True:
        try:
            results = redis.xreadgroup(group, key, {key: ">"}, None)  # All events.
            
            if results:
                for result in results:
                    order_dict = result[1][0][1]

                    try:
                        product = Product.get(order_dict["product_id"])

                        if product.quantity_available <= 0 or product.quantity_available < int(order_dict["quantity"]):
                            raise ProductNotAvailableException()

                        product.quantity_available = product.quantity_available - int(order_dict["quantity"])
                        product.save()
                        print(f"Payment approved, updating product to: {product}")
                    except ProductNotAvailableException:
                        order_dict["reason"] = "Product is not available"
                        redis.xadd("refund_order", order_dict, "*")
                        print(f"Refunding client payment because product is not available...")
                    except Exception:
                        order_dict["reason"] = "Product was not found"
                        redis.xadd("refund_order", order_dict, "*")
                        print(f"Refunding client payment because product was not found...")
        except Exception as err:
            print(str(err))
        sleep(interval_sec)


def main() -> None:
    create_stream_group(key, group)
    consume(group, key)


if __name__ == "__main__":
    main()
