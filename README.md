This script gives the time at which the cron job will be triggered. Follow the below Steps to execute this project:
1) Download the cron_parser.py file
2) Install python v3 or greater
3) Open terminal and move to the path where cron_parser.py file is located.
4) Execute the below command to run the script: `python cron_parser.py <cron_string>`. Enter the cron string value in the place of `<cron_string>` .
    Example: python cron_parser.py "0 12 * * ? /usr/bin/find"
5) On executing the above command all the minutes,hours,days of month, month and day of week will be listed on which cron job will be triggered.

    ![cron_parser_output](https://github.com/VineethPeddi/cron_parser/assets/53893023/812a5fc1-3264-4f14-ae0a-086d4e92bc57)

6) To run all the unit tests execute the following command:
    `python cron_parser_test.py`

Limitations:
1) In the input, characters W and C are not allowed as these require the year to be known to predict the nearest weekday or calendar day.
2) All the months were treated as 30 day long.
