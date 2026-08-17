{
    "transaction": {
        "id": "${transactionId}",
        "country_code": "MEX",
        "type": "PAYMENT",
        "point_type": "MOTO",
        "entry_mode": "MANUAL",
        "origin": "DOMESTIC",
        "local_date_time": "2022-09-26T12:00:12.000Z",
        "original_transaction_id": "",
        "source": "CLEARING"
    },
    "merchant": {
        "id": "07979112",
        "mcc": "4816",
        "address": "UNKNOWN",
        "name": "AMAZONMX"
    },
    "card": {
        "id": "${pomeloCardId}",
        "product_type": "CREDIT",
        "provider": "MASTERCARD",
        "last_four": "3375"
    },
    "user": {
        "id": "${pomeloUserId}"
    },
    "amount": {
        "local": {
            "total": 10.0,
            "currency": "MXN"
        },
        "transaction": {
            "total": 10.0,
            "currency": "MXN"
        },
        "settlement": {
            "total": 10.0,
            "currency": "MXN"
        },
        "details": [
            {
                "type": "BASE",
                "currency": "MXN",
                "amount": 10.0,
                "name": "BASE"
            }
        ]
    }
}