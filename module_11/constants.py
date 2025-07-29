"""
    Title: constants.py
    Author: Brittaney Perry-Morgan
    Date: July 20th, 2025
    Description: Contains constants for the willson_financial database.
"""

NEW_CLIENT_REPORT = """
SELECT
    MONTH(date_added) AS 'Month',
    YEAR(date_added) AS 'Year',
    COUNT(client_id) AS 'New Clients'
FROM
    clients
WHERE
    date_added >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY
    YEAR(date_added),
    MONTH(date_added)
ORDER BY
    Year,
    MONTH(date_added);
"""

AVG_ASSETS_REPORT = """
SELECT
    CONCAT('$', FORMAT(AVG(total_assets_per_client), 2, 'en_US')) AS 'Avg Client Assets'
FROM (
    SELECT
        client_id,
        SUM(asset_value) AS total_assets_per_client
    FROM
        assets
    GROUP BY
        client_id
    ) AS client_asset_totals;
"""

HIGH_TRANSACTION_CLIENTS_REPORT = """
SELECT
    c.name AS 'Client',
    COUNT(t.transaction_id) AS 'Transaction Count'
FROM
    transactions t
JOIN
    clients AS c ON t.client_id = c.client_id
WHERE
    YEAR(t.txn_date) = %s AND MONTH(t.txn_date) = %s
GROUP BY
    c.name
HAVING
    COUNT(t.transaction_id) > 10 
ORDER BY
    'Transaction Count' DESC;
"""
