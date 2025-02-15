# Pull Request Description

## Overview
This pull request introduces new functionality to the PHP project by adding a transaction details page. The following changes have been made:

## New Files
- **transaction_details.php**: A new PHP file that displays detailed information about a specific transaction, including:
  - Block header
  - Transaction ID
  - Sender details
  - Amount
  - Validation status

- **css/transaction_details.css**: A new CSS file that provides styling for the transaction details page, ensuring it matches the overall design of the application.

## Changes Made
- **index.php**: Updated to include a link to the new transaction details page. The link passes a sample transaction ID as a query parameter.

## Testing
- The transaction details page can be accessed via the link in the login container of the index page.
- The page displays the relevant transaction information and is styled according to the new CSS file.

## Additional Notes
- Ensure that the database and transaction data are properly set up to test the transaction details functionality.
- The sample transaction ID in the link should be replaced with actual transaction IDs as needed.

Please review the changes and let me know if any modifications are required.
