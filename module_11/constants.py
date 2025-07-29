"""
    Title: constants.py
    Author: Brittaney Perry-Morgan
    Date: July 20th, 2025
    Description: Contains constants for the willson_financial database.
"""

# SQL Logic: This query counts clients, grouping them by the year and the month they were added.
# It then filters the results to show only the last six months.
# The query uses the client_id and date_added columns from the clients table.
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

# SQL Logic: This query calculates the average total asset value per client.
# It does this by first grouping the assets table by client_id and summing the asset_value for each.
# Then it calculates the average of these totals.
# The query uses the client_id and asset_value columns from the assets table.
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

# SQL Logic: This query generates a report of clients with more than 10 transactions in a
# specific month and year.
# It joins the transactions and clients tables on the client_id column.
# It filters the results to show only the transactions from the specified year and month.
# It groups the results by client name and counts the number of transactions for each client.
# The query uses the client_id, name, transaction_id, txn_date columns from the transactions
# and clients tables.
# It orders the results by the transaction count in descending order.
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
