
# Marinas Data Extraction and Processing

This repository contains scripts to fetch marina data from the Marinas.com API and process it into an Excel file. This guide will help you replicate the process.

## Overview

We use the Marinas.com API to retrieve data about marinas across the United States. The data is fetched in chunks, processed on the fly, and saved into a tabular format suitable for ingestion into Excel.

## Data Flow

```ascii
+------------------------+
|   Grid Points (Lat/Lon)|
|      Generation        |
+-----------+------------+
            |
            v
+-----------+------------+
| Fetch Data Using curl  |
|     (Marinas.com API)  |
+-----------+------------+
            |
            v
+-----------+------------+
|  Flatten JSON Structure|
+-----------+------------+
            |
            v
+-----------+------------+
|  Append Data to List   |
+-----------+------------+
            |
            v
+-----------+------------+
| Convert List to DataFrame |
+-----------+------------+
            |
            v
+-----------+------------+
|  Save DataFrame to Excel  |
+------------------------+
```

## Files

- `fetch_and_process_marinas_us.py`: Main script to fetch and process marina data for the entire US.
- `us_marinas_data_small_area.xlsx`: Example output file for a smaller test area.

## Setup

1. **Clone the repository**

   ```sh
   git clone https://github.com/yourusername/marinas.git
   cd marinas
   ```

2. **Install dependencies**

   ```sh
   pip install pandas
   ```

3. **Get an API Key**

   Register on [Marinas.com](https://marinas.com) and get an API key.

4. **Set the API Key**

   Open the `fetch_and_process_marinas_us.py` script and replace the `api_key` variable with your API key.

## Running the Script

1. **Run the script**

   ```sh
   python fetch_and_process_marinas_us.py
   ```

   This will fetch marina data for the entire US, process it, and save the results to an Excel file (`us_marinas_data.xlsx`).

## Script Explanation

### `fetch_and_process_marinas_us.py`

This script performs the following steps:

1. **Grid Points Generation**: Generates grid points for the entire US using 1-degree steps for latitude and longitude.
2. **Fetch and Process Data**: For each grid point, it fetches data using `curl`, processes the JSON response, flattens the data, and appends it to a list.
3. **Rate Limiting**: Introduces a delay between requests to ensure no more than 300 requests per minute.
4. **Save to Excel**: At the end, the list is converted to a DataFrame and saved to an Excel file (`us_marinas_data.xlsx`).

## Example Output

You can find an example output file for a smaller test area (`us_marinas_data_small_area.xlsx`) in the repository.

## Notes

- Ensure that you adhere to the rate limits specified by the Marinas.com API to avoid being blocked.
- The script covers the entire US; you can adjust the bounding box and grid steps for smaller regions if needed.

## Contributing

Feel free to fork this repository and submit pull requests if you have any improvements or additional features.

## License

This project is licensed under the GPLv3+ License - see the LICENSE file for details.

