SARIMAX_CONFIG = {

    "seasonal_period": 12,

    "order_grid": [
        (1, 0, 1),
        (1, 1, 1),
        (2, 1, 2)
    ],

    "seasonal_order_grid": [
        (1, 0, 1, 12),
        (1, 1, 1, 12)
    ]
}