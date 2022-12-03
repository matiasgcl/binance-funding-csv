# binance-funding-csv

Simple as it gets. For a given Perpetual contract, get all the funding rates between given dates.

Output is a csv file with the following structure:
contract,fundingDate(YYYY-MM-DD HH:MM:SS),fundingRate

Note: fundingRate is saved as number, not percentage (i.e. 0.1% is saved as 0.001)
