# appalpy


### appalpy - a python module to download information about public tenders in Italy.

The package aims to help researchers in the field of Public Policy and Public Economics gather insightful information about 
public tenders in Italy, based on data published by the *National Anti-Corruption Authority* (*ANAC*).

The Tenders class and its methods may be used to easily download a dataset according to parameters and filters specified by
the user (e.g., date range, keywords, contracting entity).

Since ANAC provides information on contractors in separate files, `appalpy` is also able to extrapolate information on the awardees,
matching the data according to the unique tender key (the "CIG" code) and procurement ID.

The results are returned as **Pandas DataFrames**, allowing the user to further manipulate the data using the well-known capabilities
of the `pandas` library.

*Note: compatibility issues have been observed with Python 3.10.1*