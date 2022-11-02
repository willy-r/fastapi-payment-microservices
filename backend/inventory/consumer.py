from time import sleep

from main import redis, Product

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
                    product = Product.get(order_dict["product_id"])
                    print(product)
                    product.quantity_available = product.quantity_available - int(order_dict["quantity"])
                    product.save()
        except Exception as err:
            print(str(err))
        sleep(interval_sec)


def main() -> None:
    create_stream_group(key, group)
    consume(group, key)


if __name__ == "__main__":
    main()
