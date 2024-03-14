import pandas as pd
from areport import Report
from tests.deterministic_data import geometric_daily


series = geometric_daily(1, 2, 31, start_time=1704067200)
series_2 = geometric_daily(2, 1, 29, start_time=series.index[-1].timestamp() + 86400)
series_3 = geometric_daily(1, 4, 31, start_time=series_2.index[-1].timestamp() + 86400)
series_4 = geometric_daily(4, 4, 2, start_time=series_2.index[-1].timestamp() + 86400)

# combine
series = pd.concat([series, series_2, series_3, series_4])
# drop duplicates

report = Report(series)

_report, performance_fees = report.less_performance_fees(0.1, "M")
breakpoint()