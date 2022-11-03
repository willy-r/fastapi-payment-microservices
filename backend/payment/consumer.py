from time import sleep

from main import redis, Order, OrderStatus

key = "refund_order"
group = "payment_group"


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

                    order = Order.get(order_dict["pk"])
                    order.status = OrderStatus.REFUNDED
                    order.reason = order_dict["reason"]
                    order.save()
                    print(f"Order {order_dict['pk']} was refunded successfully")
        except Exception as err:
            print(str(err))
        sleep(interval_sec)


def main() -> None:
    create_stream_group(key, group)
    consume(group, key)


if __name__ == "__main__":
    main()
