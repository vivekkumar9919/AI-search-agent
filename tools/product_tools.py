import random
from collections import Counter
from typing import List, Dict, Any, Optional, Union

# Tool 1: Profit Margin Analyzer
def profit_margin_analyzer(products: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate profit margin percentage for each product and the average margin.
    Since cost_price is not available, margin is based on discount vs. final_price.
    """
    if not products:
        return {"average_margin": 0, "margins": []}

    margins = []
    for p in products:
        try:
            # Profit = price - final_price
            profit = p["price"] - p["final_price"]
            margin_pct = (profit / p["price"]) * 100 if p["price"] > 0 else 0
            margins.append({"product_id": p.get("_id"), "margin_pct": round(margin_pct, 2)})
        except Exception:
            continue

    avg_margin = round(sum([m["margin_pct"] for m in margins]) / len(margins), 2) if margins else 0
    return {"average_margin": avg_margin, "margins": margins}


# Tool 2: Low Stock Alert with Velocity (velocity mocked for now)
def low_stock_with_velocity(
    products: List[Dict[str, Any]],
    stock_threshold: int = 10,
    days_window: int = 7,
    velocity_map: Optional[Dict[Any, float]] = None,
    random_seed: Optional[int] = None,
    **kwargs
) -> List[Dict[str, Any]]:
    """
    Identify products that may run out soon using 'days of cover' logic.
    - quantity field is used (schema)
    - velocity is mocked (1..10 units/day) unless provided via velocity_map
    - at-risk if (quantity <= stock_threshold) OR (days_of_cover <= days_window)

    Params:
      stock_threshold: consider low if quantity <= threshold
      days_window: consider at-risk if days_of_cover <= days_window
      velocity_map: optional {product_id|_id: velocity_per_day}
      random_seed: optional for repeatable mocked velocities
    """
    if random_seed is not None:
        random.seed(random_seed)

    alerts: List[Dict[str, Any]] = []

    for p in products:
        qty = p.get("quantity", 0)  # <-- schema uses 'quantity'
        # pick an identifier for velocity map lookup
        pid = p.get("product_id") or p.get("_id") or p.get("sku") or p.get("name")

        # determine velocity per day
        if velocity_map and pid in velocity_map:
            velocity = float(velocity_map[pid]) if velocity_map[pid] else 0.0
        else:
            velocity = float(random.randint(1, 10))  # mocked for now

        days_of_cover = (qty / velocity) if velocity > 0 else float("inf")
        at_risk = (qty <= stock_threshold) or (days_of_cover <= float(days_window))

        if at_risk:
            alerts.append({
                "product_id": pid,
                "name": p.get("name"),
                "quantity": qty,
                "velocity_per_day": round(velocity, 2),
                "days_of_cover": (round(days_of_cover, 2) if velocity > 0 else None)
            })

    # sort by least days_of_cover first (most urgent)
    alerts.sort(key=lambda x: (x["days_of_cover"] if x["days_of_cover"] is not None else float("inf")))
    return alerts


# Tool 3: Price Band Distribution
def price_band_distribution(products: List[Dict[str, Any]], bands: List[Union[int, List[int]]] = None) -> Dict[str, int]:
    """
    Count how many products fall into different price bands.

    Supports both formats:
    - Flat list: [0, 500, 1000, 2000, 5000]
    - Explicit ranges: [[0, 500], [500, 1000], [1000, 2000]]
    """
    distribution = Counter()

    if bands is None:
        # default flat list
        bands = [0, 500, 1000, 2000, 5000, 10000]

    # detect if it's explicit ranges
    if isinstance(bands[0], list):
        for p in products:
            price = p.get("final_price", 0)
            matched = False
            for band in bands:
                low, high = band
                if low <= price < high:
                    distribution[f"{low}-{high-1}"] += 1
                    matched = True
                    break
            if not matched:
                distribution[f"{bands[-1][1]}+"] += 1
    else:
        # flat list mode
        for p in products:
            price = p.get("final_price", 0)
            for i in range(len(bands) - 1):
                if bands[i] <= price < bands[i + 1]:
                    distribution[f"{bands[i]}-{bands[i+1]-1}"] += 1
                    break
            else:
                distribution[f"{bands[-1]}+"] += 1

    return dict(distribution)


# Tool 4: Calculate average price 
def calculate_average_price(products: list, **kwargs) -> float:
    """
    Calculate the average price of products.
    
    :param products: List of product dictionaries, each containing a 'price' field.
    :return: Average price (float). Returns 0.0 if no products or no valid prices.
    """
    if not products:
        return 0.0
    
    prices = [p.get("price", 0) for p in products if isinstance(p.get("price", 0), (int, float))]
    
    if not prices:
        return 0.0
    
    avg_price = sum(prices) / len(prices)
    return round(avg_price, 2)

